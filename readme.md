# HoodQuest: The Algorithm Forest

Implementation of the final project for the Data Structures and Algorithms course — in Python (without using built-in data structures where custom implementations are required).

## Run
```bash
python3 main.py
```
No external packages need to be installed (only Python standard library is used).


Project Structure

hoodquest/
├── main.py                     # Program entry point
├── data_structures/            # Custom data structures (no built-in list/dict/heapq)
│   ├── graph.py                # Weighted undirected graph (adjacency list)
│   ├── stack.py                # Stack (linked list) → for Undo
│   ├── queue_.py               # Queue (linked list) → for BFS
│   ├── hash_table.py           # Hash table with separate chaining → for Users
│   ├── max_heap.py             # Max heap (array-based) → for Leaderboard
│   └── bst.py                  # Binary Search Tree → for fast score lookup (bonus)
├── algorithms/
│   ├── dijkstra.py             # Shortest path from player to grandmother's house
│   ├── bfs.py                  # Unweighted shortest path from wolf to player
│   └── astar.py                # A* algorithm (bonus section)
├── game/
│   ├── map_builder.py          # Build game map according to page 8 diagram
│   ├── game_state.py           # Single round state (positions, score, turn)
│   └── game_engine.py          # Complete turn logic, rules, scoring, Undo
├── users/
│   ├── security.py             # Password hashing (salt + SHA-256)
│   └── user_manager.py         # Register/login/score with HashTable + BST + MaxHeap
├── ui/
│   └── cli.py                  # Command-line interface: menus, game flow, leaderboard
└── data/
    └── users.json              # User account storage location (created at runtime)
‍‍‍


Implemented Rules:
    The map graph exactly matches the diagram on page 8 of the project document, with node V as the grandmother's house (safe point).
    Initial positions of the player and wolf are randomly selected, distinct from each other and from node V.
    Each turn executes exactly according to the 10-step order described in the document (Dijkstra → display path → choose move/Undo → move and score → check win → check collision → wolf dice → BFS and wolf move → check collision → next turn).
    Scoring according to the document table: +3, +1, -2, +5.
    If the player moves directly onto the wolf's house, the game ends immediately (without waiting for wolf movement).
    Passwords are never stored in plain text (Salt + SHA-256).
    Usernames are case-sensitive (Ali ≠ ali).
    After every score change, the max heap and BST are rebuilt to keep the leaderboard and score lookup always up-to-date.

