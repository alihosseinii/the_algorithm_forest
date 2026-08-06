import os
import re
import time
import getpass

from users.user_manager import UserManager
from game.map_builder import build_map, GOAL_NODE, COORDINATES
from game.game_engine import GameEngine
from algorithms.bfs import bfs_shortest_path


WIDTH = 58 


class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


_ANSI_RE = re.compile(r"\033\[[0-9;]*m")


def _visible_len(s):
    return len(_ANSI_RE.sub("", s))


def _pad(s, width):
    extra = width - _visible_len(s)
    return s + (" " * extra if extra > 0 else "")


def _enable_ansi_on_windows():
    if os.name == "nt":
        os.system("")


_enable_ansi_on_windows()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def hr(width=WIDTH, ch="─"):
    return ch * width


def box(title, lines, color=C.CYAN):
    print(f"{color}+{hr()}+{C.RESET}".replace("+", "┌", 1).replace("+", "┐", 1) if False else
          f"{color}┌{hr()}┐{C.RESET}")
    print(f"{color}│{C.RESET}{title.center(WIDTH)}{color}│{C.RESET}")
    print(f"{color}├{hr()}┤{C.RESET}")
    for line in lines:
        content = _pad(line, WIDTH - 2)
        print(f"{color}│ {C.RESET}{content}{color} │{C.RESET}")
    print(f"{color}└{hr()}┘{C.RESET}")


def ok(text):
    return f"{C.GREEN}[OK] {text}{C.RESET}"


def fail(text):
    return f"{C.RED}[FAIL] {text}{C.RESET}"


def info(text):
    return f"{C.YELLOW}[INFO] {text}{C.RESET}"


def loading(text, delay=0.25):
    print(text)
    time.sleep(delay)


def pause():
    input(f"\n{C.DIM}Press ENTER to continue...{C.RESET}")


def prompt(label):
    return input(f"{label}: > ").strip()


def hp_bar(percent, width=20):
    percent = max(0, min(100, percent))
    filled = int(width * percent / 100)
    return "[" + ("#" * filled) + ("-" * (width - filled)) + f"] {percent}%"


def title_screen():
    clear_screen()
    box("RED RIDING HOOD ADVENTURE", ["", "GRAPH PATH FINDING GAME", ""], color=C.MAGENTA)
    print()
    print("  [1] Login")
    print("  [2] Register")
    print("  [3] Leaderboard")
    print("  [4] Exit")
    print()
    return input(f"{C.BOLD}Select Option:{C.RESET}\n> ").strip()


def login_flow(user_manager):
    clear_screen()
    box("USER LOGIN", [], color=C.BLUE)
    print()
    username = prompt("Username")
    try:
        password = getpass.getpass("Password: > ")
    except Exception:
        password = prompt("Password")

    print()
    loading("Checking User Database...")
    ok_flag, msg, user = user_manager.login(username, password)

    if not ok_flag:
        print(fail(msg))
        pause()
        return False, None

    print(ok("Account Found"))
    loading("Loading Saved Data...", 0.2)
    print()
    print(f"Player          : {user.username}")
    print(f"Previous Score  : {user.score}")
    print()
    print("Encryption:")
    print(f"{C.GREEN}SHA-256 Verification Successful{C.RESET}")
    pause()
    return True, username


def register_flow(user_manager):
    clear_screen()
    box("USER REGISTRATION", [], color=C.BLUE)
    print()
    username = prompt("Username")
    try:
        password = getpass.getpass("Password: > ")
    except Exception:
        password = prompt("Password")

    print()
    loading("Checking Hash Table For Duplicates...")
    ok_flag, msg = user_manager.register(username, password)

    if not ok_flag:
        print(fail(msg))
        pause()
        return False, None

    print(ok("Username Available"))
    loading("Creating Account...", 0.2)
    print(ok("Password Hashed (SHA-256 + Salt)"))
    print(ok("Account Created"))
    print(ok("Hash Table Updated"))
    pause()
    return True, username


def leaderboard_screen(user_manager):
    clear_screen()
    top = user_manager.top_players(10)

    lines = ["", "(MAX HEAP DATA)", "", f"{'Rank':<8}{'Username':<24}{'Score':<10}", hr(WIDTH - 2, "-")]
    if not top:
        lines.append("No players yet.")
    else:
        for rank, (score, username) in enumerate(top, start=1):
            lines.append(f"#{rank:<7}{username:<24}{score:<10}")

    box("TOP PLAYERS", lines, color=C.YELLOW)
    print()
    query = prompt("Search Player Score (username, blank to skip)")
    if query:
        score = user_manager.get_score(query)
        if score is None:
            print(fail("No such user."))
        else:
            print(f"{C.GREEN} {query} -> Score: {score}{C.RESET}")
    pause()


def how_to_play_screen():
    clear_screen()
    lines = [
        "",
        f"Goal: Guide Red Riding Hood to Grandma's House ({GOAL_NODE})",
        "before the Wolf catches her.",
        "",
        "TURN SEQUENCE",
        hr(WIDTH - 2, "-"),
        "1. Dijkstra suggests the shortest path to the goal.",
        "2. You follow the path, choose another node, or Undo.",
        "3. Your score is updated based on the move you made.",
        "4. A die is rolled for the Wolf; on an even roll the Wolf",
        "   advances one node toward you using BFS.",
        "",
        "SCORING",
        hr(WIDTH - 2, "-"),
        "+3   move matches the Dijkstra-suggested node",
        "+1   valid move, different from the suggestion",
        "-2   using Undo",
        "+5   reaching Grandma's House",
        "",
        "GAME OVER",
        hr(WIDTH - 2, "-"),
        f"WIN   - you reach node {GOAL_NODE}",
        "LOSE  - you and the Wolf occupy the same node",
    ]
    box("HOW TO PLAY", lines, color=C.CYAN)
    pause()


def _danger_hp(engine, state):
    path = bfs_shortest_path(engine.graph, state.player_pos, state.wolf_pos)
    dist = len(path) - 1 if path else 5
    return max(10, min(100, dist * 25))


def show_map_screen(engine, state, username, previous_total):
    clear_screen()

    path = engine.suggested_path()
    neighbors = engine.valid_moves()
    hp = _danger_hp(engine, state)

    lines = [
        "",
        "PLAYER INFO",
        hr(WIDTH - 2, "-"),
        f"Name           : {username}",
        f"Score          : {state.score}",
        f"Total Score    : {previous_total + state.score}",
        f"HP             : {hp_bar(hp)}",
        "",
        "MAP INFO",
        hr(WIDTH - 2, "-"),
        f"Current Position : {state.player_pos}",
        f"Wolf Position    : {state.wolf_pos}",
        f"Goal             : {GOAL_NODE}",
        "",
        "Path Algorithm   : Dijkstra",
        f"Recommended Path : {' -> '.join(path) if len(path) > 1 else 'N/A'}",
        f"Available Moves  : {', '.join(neighbors)}",
        "",
        "ACTIONS",
        hr(WIDTH - 2, "-"),
        "[1] Follow Recommended Path",
        "[2] Choose Different Route",
    ]

    if engine.can_undo():
        lines.append("[3] Undo Last Move")

    box(
        f"RED RIDING HOOD - GAME MAP (Turn {state.turn_number})",
        lines,
        color=C.CYAN,
    )

    print()
    graph = [
        "                    GAME MAP",
        "------------------------------------------------------",
        "",
        "       B---2---C---5---D",
        "      /               /",
        "    3/               /1",
        "    A-6-F--4--G--3--E",
        "       /6     |5\\4",
        "      J-3-K-2-W-3-M",
        "       \\5  \\3      \\1",
        "         P-1-R--2--S",
        "        /    \\4     \\6",
        "    O--3      T---2---U",
        "     \\2      /        \\3",
        "       Q----5          V",
        "        \\------5-------/",
    ]

    box(
        "GAME MAP",
        graph,
        color=C.CYAN,
    )


def show_movement_result(prev_pos, target, matched, current_score):
    lines = [
        "",
        f"Previous Position : {prev_pos}",
        f"Selected Position : {target}",
        "",
        "PATH EVALUATION",
        hr(WIDTH - 2, "-"),
        f"Result   : {ok('Correct Decision') if matched else info('Alternative Route')}",
        f"Score    : {'+3' if matched else '+1'}",
        "",
        f"Current Score : {current_score}",
    ]
    box("PLAYER MOVEMENT", lines, color=C.GREEN if matched else C.YELLOW)
    pause()


def show_undo_result(current_score):
    clear_screen()
    lines = [
        "",
        "Last full turn has been reverted.",
        "",
        f"Penalty  : -2",
        f"Current Score : {current_score}",
    ]
    box("UNDO MOVE", lines, color=C.YELLOW)
    pause()


def show_wolf_turn(wolf_before, wolf_after, dice, moved, had_path):
    clear_screen()
    lines = [
        "",
        "Enemy               : Wolf",
        "Movement Algorithm  : BFS",
        "Movement Rule       : One Node Per Turn",
        "",
        f"Dice Result         : {dice}",
        f"Movement Allowed    : {'YES (Even Roll)' if dice % 2 == 0 else 'NO (Odd Roll)'}",
    ]
    if moved:
        lines.append(f"Wolf Movement       : {wolf_before} -> {wolf_after}")
    elif dice % 2 == 0 and not had_path:
        lines.append("Wolf Movement       : No path available")
    else:
        lines.append("Wolf Movement       : Wolf stays in place")

    box("WOLF TURN", lines, color=C.RED)
    pause()


def show_result_screen(state, user_manager, username, previous_total):
    clear_screen()
    if state.won:
        status = "SUCCESS!"
        message = "Red Riding Hood reached Grandma's House"
        color = C.GREEN
    else:
        status = "GAME OVER"
        message = "The Wolf caught Red Riding Hood"
        color = C.RED

    new_total = user_manager.add_score(username, state.score)

    lines = [
        "",
        f"STATUS: {status}",
        "",
        message,
        "",
        "FINAL SCORE REPORT",
        hr(WIDTH - 2, "-"),
        f"Previous Score : {previous_total}",
        f"Game Reward    : {state.score}",
        f"Final Score    : {new_total}",
        "",
        "Saving Data...",
        ok("Database Updated"),
        ok("BST Updated"),
        ok("MAX HEAP Updated"),
        "",
        "Thank You For Playing!",
    ]
    box("GAME RESULT", lines, color=color)
    pause()


def play_game(user_manager, username):
    graph = build_map()
    engine = GameEngine(graph, goal=GOAL_NODE, coordinates=COORDINATES)
    state = engine.setup_new_game()
    previous_total = user_manager.get_score(username) or 0

    while not state.game_over:
        show_map_screen(engine, state, username, previous_total)
        path = engine.suggested_path()
        next_suggested = path[1] if len(path) > 1 else None
        neighbors = engine.valid_moves()
        can_undo = engine.can_undo()

        choice = input("\n> ").strip()

        target = None
        if choice == "1":
            if next_suggested is None:
                print(fail("No suggested path available."))
                pause()
                continue
            target = next_suggested
        elif choice == "2":
            target = input(f"Enter destination node {tuple(neighbors)}: > ").strip().upper()
            if target not in neighbors:
                print(fail("Invalid move."))
                pause()
                continue
        elif choice == "3" and can_undo:
            engine.undo()
            show_undo_result(state.score)
            continue
        else:
            print(fail("Invalid option."))
            pause()
            continue

        prev_pos = state.player_pos
        wolf_before = state.wolf_pos
        matched = (target == next_suggested)

        result = engine.player_move(target)
        if not result["valid"]:
            print(fail("Invalid move."))
            pause()
            continue

        clear_screen()
        show_movement_result(prev_pos, target, matched, state.score)

        if state.game_over:
            break

        dice = result.get("dice")
        if dice is not None:
            moved = "wolf_moved" in result["events"]
            had_path = not any(e == "wolf_has_no_path" for e in result["events"])
            show_wolf_turn(wolf_before, state.wolf_pos, dice, moved, had_path)

    show_result_screen(state, user_manager, username, previous_total)

def account_menu(user_manager):
    while True:
        choice = title_screen()
        if choice == "1":
            ok_flag, username = login_flow(user_manager)
            if ok_flag:
                return username
        elif choice == "2":
            ok_flag, username = register_flow(user_manager)
            if ok_flag:
                return username
        elif choice == "3":
            leaderboard_screen(user_manager)
        elif choice == "4":
            clear_screen()
            print("Goodbye!")
            return None
        else:
            print(fail("Invalid option."))
            pause()


def game_menu(user_manager, username):
    while True:
        clear_screen()
        box(f"WELCOME, {username}", [], color=C.MAGENTA)
        print()
        print("  [1] Play")
        print("  [2] Leaderboard")
        print("  [3] How To Play")
        print("  [4] My Score (BST Lookup)")
        print("  [5] Logout / Exit")
        print()
        choice = input(f"{C.BOLD}Select Option:{C.RESET}\n> ").strip()

        if choice == "1":
            play_game(user_manager, username)
        elif choice == "2":
            leaderboard_screen(user_manager)
        elif choice == "3":
            how_to_play_screen()
        elif choice == "4":
            clear_screen()
            score = user_manager.get_score(username)
            box("MY SCORE", ["", f"Username : {username}", f"Score    : {score}",], color=C.YELLOW)
            pause()
        elif choice == "5":
            clear_screen()
            print("Goodbye!")
            break
        else:
            print(fail("Invalid option."))
            pause()


def main_menu():
    user_manager = UserManager()
    username = account_menu(user_manager)
    if username is not None:
        game_menu(user_manager, username)