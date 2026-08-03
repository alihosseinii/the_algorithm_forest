class Graph:
    def __init__(self):
        # node -> list[(neighbor, weight)]
        self._adjacency = {}

    def add_node(self, node):
        if node not in self._adjacency:
            self._adjacency[node] = []

    def add_edge(self, u, v, weight):
        self.add_node(u)
        self.add_node(v)
        if not self.has_edge(u, v):
            self._adjacency[u].append((v, weight))
            self._adjacency[v].append((u, weight))

    def neighbors(self, node):
        return self._adjacency.get(node, [])

    def neighbor_names(self, node):
        return [n for n, _w in self.neighbors(node)]

    def nodes(self):
        return list(self._adjacency.keys())

    def has_node(self, node):
        return node in self._adjacency

    def has_edge(self, u, v):
        return any(n == v for n, _w in self._adjacency.get(u, []))

    def edge_weight(self, u, v):
        for n, w in self._adjacency.get(u, []):
            if n == v:
                return w
        return None

    def __len__(self):
        return len(self._adjacency)

    def __repr__(self):
        return f"Graph(nodes={len(self)})"