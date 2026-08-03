class HashTable:
    def __init__(self, capacity=53):
        self._capacity = capacity
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _hash(self, key):
        h = 0
        for ch in str(key):
            h = (h * 31 + ord(ch)) % self._capacity
        return h

    def _resize(self):
        old_items = self.items()
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        for k, v in old_items:
            self.set(k, v)

    def set(self, key, value):
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, _v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self._size > self._capacity * 0.75:
            self._resize()

    def get(self, key, default=None):
        idx = self._hash(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        return default

    def contains(self, key):
        idx = self._hash(key)
        return any(k == key for k, _v in self._buckets[idx])

    def delete(self, key):
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, _v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def items(self):
        result = []
        for bucket in self._buckets:
            result.extend(bucket)
        return result

    def keys(self):
        return [k for k, _v in self.items()]

    def values(self):
        return [v for _k, v in self.items()]

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"HashTable(size={self._size}, capacity={self._capacity})"