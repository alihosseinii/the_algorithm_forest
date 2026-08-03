class _BSTNode:
    __slots__ = ("username", "score", "left", "right")

    def __init__(self, username, score):
        self.username = username
        self.score = score
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self._root = None

    def insert(self, username, score):
        if self._root is None:
            self._root = _BSTNode(username, score)
            return
        node = self._root
        while True:
            if username == node.username:
                node.score = score
                return
            if username < node.username:
                if node.left is None:
                    node.left = _BSTNode(username, score)
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = _BSTNode(username, score)
                    return
                node = node.right

    def search(self, username):
        node = self._root
        while node is not None:
            if username == node.username:
                return node.score
            node = node.left if username < node.username else node.right
        return None

    def build_from(self, pairs):
        self._root = None
        for username, score in pairs:
            self.insert(username, score)

    def in_order(self):
        result = []

        def _walk(node):
            if node is None:
                return
            _walk(node.left)
            result.append((node.username, node.score))
            _walk(node.right)

        _walk(self._root)
        return result

    def __len__(self):
        return len(self.in_order())