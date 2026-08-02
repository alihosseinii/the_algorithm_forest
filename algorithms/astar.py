import math

def _heuristic(node, goal, coordinates):
    if not coordinates or node not in coordinates or goal not in coordinates:
        return 0
    x1, y1 = coordinates[node]
    x2, y2 = coordinates[goal]
    return math.hypot(x1 - x2, y1 - y2)

def astar(graph, start, goal, coordinates=None):
    coordinates = coordinates or {}

    open_set = {start}
    g_score = {node: math.inf for node in graph.nodes()}
    g_score[start] = 0
    f_score = {node: math.inf for node in graph.nodes()}
    f_score[start] = _heuristic(start, goal, coordinates)
    prev = {start: None}

    while open_set:
        current = min(open_set, key=lambda n: f_score[n])
        if current == goal:
            path = [current]
            while prev[current] is not None:
                current = prev[current]
                path.append(current)
            path.reverse()
            return path, g_score[goal]

        open_set.remove(current)
        for neighbor, weight in graph.neighbors(current):
            tentative_g = g_score[current] + weight
            if tentative_g < g_score[neighbor]:
                prev[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + _heuristic(neighbor, goal, coordinates)
                open_set.add(neighbor)

    return [], math.inf