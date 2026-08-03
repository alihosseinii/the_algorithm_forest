class _Node:
    __slots__ = ("data", "next")

    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class Stack:
    def __init__(self):
        self._top = None
        self._size = 0

    def push(self, item):
        self._top = _Node(item, self._top)
        self._size += 1

    def pop(self):
        if self._top is None:
            raise IndexError("pop from an empty stack")
        node = self._top
        self._top = node.next
        self._size -= 1
        return node.data

    def peek(self):
        if self._top is None:
            raise IndexError("peek from an empty stack")
        return self._top.data

    def is_empty(self):
        return self._top is None

    def clear(self):
        self._top = None
        self._size = 0

    def __len__(self):
        return self._size

    def __repr__(self):
        items = []
        node = self._top
        while node:
            items.append(node.data)
            node = node.next