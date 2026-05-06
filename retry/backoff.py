"""
Name: Simple Backoff (no deps)

Why:
- Retry logic is common in unstable environments
- Useful for network calls, file access, and edge devices

Features:
- Retry a function call
- Exponential backoff
- Optional max delay

Limitations:
- No jitter
- No exception filtering
- No decorator interface

Usage:
    def unstable():
        ...

    result = retry(unstable, retries=3)
"""

import time as _time


def _sleep(attempt, base_delay, max_delay):
    delay = base_delay * (2 ** attempt)
    if max_delay is not None:
        delay = min(delay, max_delay)
    _time.sleep(delay)


def retry(func, retries=3, base_delay=0.3, max_delay=5.0):
    last_error = None

    for attempt in range(retries + 1):
        try:
            return func()
        except Exception as e:
            last_error = e
            if attempt == retries:
                raise
            _sleep(attempt, base_delay, max_delay)

    raise last_error


if __name__ == "__main__":
    print("[TEST] backoff")

    state = {"count": 0}

    def unstable():
        state["count"] += 1
        if state["count"] < 3:
            raise RuntimeError("temporary failure")
        return "ok"

    try:
        result = retry(unstable, retries=3, base_delay=0.1)
        assert result == "ok"
        assert state["count"] == 3
        print("[OK] retry")
        print("[DONE]")
    except Exception as e:
        print("[FAIL]", e)
