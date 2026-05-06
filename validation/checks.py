"""
Name: Validation Checks (no deps)

Why:
- Scripts need small input checks without a schema library
- Keep validation explicit and readable

Features:
- required mapping keys
- integer / float checks
- email-like check
- URL-like check
- clamp numeric values
- choice validation

Limitations:
- Email and URL checks are intentionally basic
- No nested schema validation

Usage:
    require_keys({"name": "ada"}, ["name"])
"""

import re
from urllib.parse import urlparse


def require_keys(mapping, keys):
    missing = [key for key in keys if key not in mapping]
    if missing:
        raise ValueError("missing keys: " + ", ".join(missing))
    return True


def is_int(value):
    try:
        int(value)
        return True
    except (TypeError, ValueError):
        return False


def is_float(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def is_email(value):
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", str(value)))


def is_url(value):
    parts = urlparse(str(value))
    return parts.scheme in ("http", "https") and bool(parts.netloc)


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def require_choice(value, choices):
    if value not in choices:
        raise ValueError("expected one of: " + ", ".join(map(str, choices)))
    return value


if __name__ == "__main__":
    print("[TEST] checks")

    try:
        assert require_keys({"a": 1}, ["a"]) is True
        assert is_int("1") is True
        assert is_float("1.5") is True
        assert is_email("a@example.com") is True
        assert is_url("https://example.com") is True
        assert clamp(10, 1, 5) == 5
        assert require_choice("a", ["a", "b"]) == "a"
        print("[OK] validation helpers")
        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
