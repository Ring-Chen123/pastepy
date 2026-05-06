"""
Name: Iterator Tools (no deps)

Why:
- Data cleanup scripts often need small iterable helpers
- These functions keep common loops readable without dependencies

Features:
- chunking
- flattening
- unique item filtering
- grouping
- sliding windows

Limitations:
- Keeps ordering simple
- group_by stores grouped values in memory

Usage:
    print(list(chunked([1, 2, 3], 2)))  # [[1, 2], [3]]
"""


def chunked(items, size):
    if size < 1:
        raise ValueError("size must be at least 1")

    chunk = []
    for item in items:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []

    if chunk:
        yield chunk


def flatten(items):
    for group in items:
        for item in group:
            yield item


def unique(items, key=None):
    seen = set()
    for item in items:
        marker = key(item) if key else item
        if marker in seen:
            continue
        seen.add(marker)
        yield item


def first(items, default=None):
    for item in items:
        return item
    return default


def compact(items):
    for item in items:
        if item:
            yield item


def group_by(items, key):
    grouped = {}
    for item in items:
        grouped.setdefault(key(item), []).append(item)
    return grouped


def windowed(items, size):
    if size < 1:
        raise ValueError("size must be at least 1")

    window = []
    for item in items:
        window.append(item)
        if len(window) == size:
            yield tuple(window)
            window.pop(0)


if __name__ == "__main__":
    print("[TEST] iter_tools")

    try:
        assert list(chunked([1, 2, 3], 2)) == [[1, 2], [3]]
        assert list(flatten([[1], [2, 3]])) == [1, 2, 3]
        assert list(unique([1, 1, 2])) == [1, 2]
        assert first([], "x") == "x"
        assert list(compact([0, 1, "", "a"])) == [1, "a"]
        assert group_by(["a", "bb"], len) == {1: ["a"], 2: ["bb"]}
        assert list(windowed([1, 2, 3], 2)) == [(1, 2), (2, 3)]
        print("[OK] iterator helpers")
        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
