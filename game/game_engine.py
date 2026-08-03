import random

from data_structures.stack import Stack
from algorithms.dijkstra import dijkstra, reconstruct_path
from algorithms.bfs import bfs_shortest_path
from algorithms.astar import astar
from game.game_state import GameState

UNDO_PENALTY = 2
SUGGESTED_MOVE_BONUS = 3
ALTERNATIVE_MOVE_BONUS = 1
GOAL_BONUS = 5


class GameEngine:
    def __init__(self, graph, goal="V", coordinates=None):
        self.graph = graph
        self.goal = goal
        self.coordinates = coordinates or {}
        self.history = Stack()
        self.state = None
        self._first_move_done = False

    def setup_new_game(self):
        candidates = [n for n in self.graph.nodes() if n != self.goal]
        player_pos = random.choice(candidates)
        remaining = [n for n in candidates if n != player_pos]
        wolf_pos = random.choice(remaining)

        self.state = GameState(player_pos, wolf_pos, self.goal)
        self.history = Stack()
        self._first_move_done = False
        return self.state

    def suggested_path(self):
        dist, prev = dijkstra(self.graph, self.state.player_pos)
        return reconstruct_path(prev, self.state.player_pos, self.goal)

    def suggested_path_astar(self):
        path, _cost = astar(self.graph, self.state.player_pos, self.goal, self.coordinates)
        return path

    def valid_moves(self):
        return self.graph.neighbor_names(self.state.player_pos)

    def is_valid_move(self, target):
        return self.graph.has_edge(self.state.player_pos, target)

    def can_undo(self):
        return self._first_move_done and len(self.history) > 0

    def undo(self):
        if not self.can_undo():
            return False
        snap = self.history.pop()
        self.state.restore(snap)
        self.state.score -= UNDO_PENALTY
        if len(self.history) == 0:
            self._first_move_done = False
        return True

    def player_move(self, target):
        result = {"valid": True, "events": []}

        if self.state.game_over:
            result["valid"] = False
            result["events"].append("game_already_over")
            return result

        if not self.is_valid_move(target):
            result["valid"] = False
            result["events"].append("invalid_move")
            return result

        suggested = self.suggested_path()
        next_suggested = suggested[1] if len(suggested) > 1 else None

        self.history.push(self.state.snapshot())
        self._first_move_done = True

        if next_suggested is not None and target == next_suggested:
            self.state.score += SUGGESTED_MOVE_BONUS
            result["events"].append(f"move_matches_dijkstra (+{SUGGESTED_MOVE_BONUS})")
        else:
            self.state.score += ALTERNATIVE_MOVE_BONUS
            result["events"].append(f"move_alternative_valid (+{ALTERNATIVE_MOVE_BONUS})")

        self.state.player_pos = target

        if self.state.player_pos == self.goal:
            self.state.score += GOAL_BONUS
            self.state.game_over = True
            self.state.won = True
            result["events"].append(f"reached_grandmas_house (+{GOAL_BONUS})")
            return result

        if self.state.player_pos == self.state.wolf_pos:
            self.state.game_over = True
            self.state.won = False
            result["events"].append("caught_by_wolf_on_player_move")
            return result

        dice = random.randint(1, 6)
        result["dice"] = dice

        if dice % 2 == 0:
            wolf_path = bfs_shortest_path(self.graph, self.state.wolf_pos, self.state.player_pos)
            if len(wolf_path) > 1:
                self.state.wolf_pos = wolf_path[1]
                result["events"].append("wolf_moved")
            else:
                result["events"].append("wolf_has_no_path")
        else:
            result["events"].append("wolf_stayed_put")

        if self.state.wolf_pos == self.state.player_pos:
            self.state.game_over = True
            self.state.won = False
            result["events"].append("caught_by_wolf_after_wolf_move")
            return result

        self.state.turn_number += 1
        return result