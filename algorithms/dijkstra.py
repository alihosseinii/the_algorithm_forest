import math

def dijkstra(graph, source):
    nodes = graph.nodes()
    dist = {node: math.inf for node in nodes}
    prev = {node: None for node in nodes}
    dist[source] = 0

    visited = set()
    unvisited = set(nodes)

    while unvisited:
        current = min(unvisited, key=lambda n: dist[n])
        unvisited.remove(current)

        if dist[current] == math.inf:
            break

        for neighbor, weight in graph.neighbors(current):
            if neighbor in visited:
                continue
            candidate = dist[current] + weight
            if candidate < dist[neighbor]:
                dist[neighbor] = candidate
                prev[neighbor] = current

        visited.add(current)

    return dist, prev

def reconstruct_path(prev, source, target):
    if source == target:
        return [source]

    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev.get(node)
    path.reverse()

    if path and path[0] == source:
        return path
    return []

def shortest_path(graph, source, target):
    dist, prev = dijkstra(graph, source)
    path = reconstruct_path(prev, source, target)
    total = dist.get(target, math.inf)
    return path, total