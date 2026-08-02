from data_structures.queue import Queue


def bfs_shortest_path(graph, start, goal):
    if start == goal:
        return [start]

    visited = {start}
    prev = {start: None}
    q = Queue()
    q.enqueue(start)

    while not q.is_empty():
        current = q.dequeue()
        for neighbor, _weight in graph.neighbors(current):
            if neighbor in visited:
                continue
            visited.add(neighbor)
            prev[neighbor] = current
            if neighbor == goal:
                path = [neighbor]
                node = neighbor
                while prev[node] is not None:
                    node = prev[node]
                    path.append(node)
                path.reverse()
                return path
            q.enqueue(neighbor)

    return []  