"""
Name: TTL Cache (no deps)

Why:
- Small scripts often need short-lived memoization
- Time-based expiry avoids serving stale data forever

Features:
- Fixed max size
- Per-cache TTL in seconds
- Simple get / put API
- Expired items are removed lazily

Limitations:
- No thread safety
- No per-key TTL
- In-memory only

Usage:
    cache = TTLCache(max_size=100, ttl=30)
    cache.put("answer", 42)
    print(cache.get("answer"))
"""

import time
from collections import OrderedDict


class TTLCache:
    def __init__(self, max_size=128, ttl=60):
        if not isinstance(max_size, int) or max_size < 1:
            raise ValueError("max_size must be a positive integer")
        if ttl <= 0:
            raise ValueError("ttl must be greater than 0")

        self.max_size = max_size
        self.ttl = float(ttl)
        self._items = OrderedDict()

    def __len__(self):
        self._remove_expired()
        return len(self._items)

    def _remove_expired(self):
        now = time.monotonic()
        expired = []

        for key, (_, expires_at) in self._items.items():
            if expires_at <= now:
                expired.append(key)

        for key in expired:
            self._items.pop(key, None)

    def get(self, key, default=None):
        item = self._items.get(key)
        if item is None:
            return default

        value, expires_at = item
        if expires_at <= time.monotonic():
            self._items.pop(key, None)
            return default

        self._items.move_to_end(key)
        return value

    def put(self, key, value):
        expires_at = time.monotonic() + self.ttl

        if key in self._items:
            self._items.move_to_end(key)

        self._items[key] = (value, expires_at)
        self._remove_expired()

        while len(self._items) > self.max_size:
            self._items.popitem(last=False)


if __name__ == "__main__":
    print("[TEST] ttl_cache")

    try:
        cache = TTLCache(max_size=2, ttl=0.05)

        cache.put("a", 1)
        assert cache.get("a") == 1
        assert cache.get("missing") is None
        print("[OK] basic put/get")

        cache.put("b", 2)
        cache.put("c", 3)
        assert cache.get("a") is None
        assert cache.get("b") == 2
        assert cache.get("c") == 3
        print("[OK] max size")

        time.sleep(0.06)
        assert cache.get("b") is None
        assert len(cache) == 0
        print("[OK] ttl expiry")

        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
