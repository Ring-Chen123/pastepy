"""
Name: Token Bucket Rate Limiter (no deps)

Why:
- Edge scripts often need to avoid flooding APIs or devices
- Token bucket limiting is simple, predictable, and cheap

Features:
- Fixed capacity token bucket
- Refill rate in tokens per second
- Non-blocking allow()
- Optional blocking wait()

Limitations:
- In-memory only
- No cross-process coordination
- Uses time.monotonic from the standard library

Usage:
    limiter = TokenBucket(rate=2, capacity=5)

    if limiter.allow():
        print("run now")

    limiter.wait()
    print("run after token is available")
"""

import time


class TokenBucket:
    def __init__(self, rate, capacity):
        if rate <= 0:
            raise ValueError("rate must be greater than 0")
        if capacity <= 0:
            raise ValueError("capacity must be greater than 0")

        self.rate = float(rate)
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.updated_at = time.monotonic()

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.updated_at
        self.updated_at = now
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)

    def allow(self, tokens=1):
        if tokens <= 0:
            raise ValueError("tokens must be greater than 0")

        tokens = float(tokens)
        self._refill()

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True

        return False

    def wait(self, tokens=1):
        if tokens <= 0:
            raise ValueError("tokens must be greater than 0")

        tokens = float(tokens)

        while True:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return

            missing = tokens - self.tokens
            time.sleep(missing / self.rate)


if __name__ == "__main__":
    print("[TEST] token_bucket")

    try:
        bucket = TokenBucket(rate=10, capacity=2)

        assert bucket.allow() is True
        assert bucket.allow() is True
        assert bucket.allow() is False
        print("[OK] capacity")

        bucket.wait()
        assert bucket.allow() is False
        print("[OK] wait")

        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
