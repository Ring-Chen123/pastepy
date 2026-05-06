"""
Name: LRU Cache (no deps)

Why:
- Small caches are useful in restricted environments
- Helps avoid repeated work without extra dependencies

Features:
- Fixed capacity
- Least recently used eviction
- Simple get / put API

Limitations:
- No thread safety
- No TTL or persistence
- Uses OrderedDict from the standard library

Usage:
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)

    print(cache.get("a"))  # 1

    cache.put("c", 3)      # evicts "b"
    print(cache.get("b"))  # None
"""

from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError("capacity must be a positive integer")

        self.capacity = capacity
        self._items = OrderedDict()

    def __len__(self):
        return len(self._items)

    def get(self, key):
        if key not in self._items:
            return None

        self._items.move_to_end(key)
        return self._items[key]

    def put(self, key, value):
        if key in self._items:
            self._items.move_to_end(key)

        self._items[key] = value

        if len(self._items) > self.capacity:
            self._items.popitem(last=False)


if __name__ == "__main__":
    print("[TEST] lru")

    try:
        cache = LRUCache(2)

        cache.put("a", 1)
        cache.put("b", 2)
        assert cache.get("a") == 1
        assert cache.get("missing") is None
        assert len(cache) == 2
        print("[OK] basic put/get")

        cache.put("c", 3)
        assert cache.get("b") is None
        assert cache.get("a") == 1
        assert cache.get("c") == 3
        print("[OK] eviction")

        cache.put("a", 10)
        cache.put("d", 4)
        assert cache.get("a") == 10
        assert cache.get("c") is None
        assert cache.get("d") == 4
        print("[OK] update")

        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)