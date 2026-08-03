class MaxHeap:
    def __init__(self):
        self._heap = []
    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._heap[i][0] > self._heap[parent][0]:
                self._heap[i], self._heap[parent] = self._heap[parent], self._heap[i]
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self._heap)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            largest = i
            if left < n and self._heap[left][0] > self._heap[largest][0]:
                largest = left
            if right < n and self._heap[right][0] > self._heap[largest][0]:
                largest = right
            if largest == i:
                break
            self._heap[i], self._heap[largest] = self._heap[largest], self._heap[i]
            i = largest

    def push(self, score, username):
        self._heap.append((score, username))
        self._sift_up(len(self._heap) - 1)

    def pop_max(self):
        if not self._heap:
            return None
        top = self._heap[0]
        last = self._heap.pop()
        if self._heap:
            self._heap[0] = last
            self._sift_down(0)
        return top

    def peek_max(self):
        return self._heap[0] if self._heap else None

    def top_k(self, k):
        temp = MaxHeap()
        temp._heap = list(self._heap)
        result = []
        for _ in range(min(k, len(temp._heap))):
            top = temp.pop_max()
            if top is None:
                break
            result.append(top)
        return result

    def rebuild(self, score_username_pairs):
        self._heap = []
        for score, username in score_username_pairs:
            self.push(score, username)

    def __len__(self):
        return len(self._heap)