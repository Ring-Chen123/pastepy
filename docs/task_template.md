# Task Template for Codex

Use this template when asking Codex to implement or revise a module.

---

# Task

[Describe the exact file or change]

Example:
Implement `cache/lru.py`

---

# Goal

[Describe the practical goal]

Example:
A zero-dependency, copy-pasteable LRU cache for restricted environments.

---

# Constraints

- stdlib only
- single file
- no cross-file imports
- readable in 1-2 minutes
- include `if __name__ == "__main__":` self-test
- avoid over-abstraction
- keep the public API small

---

# Expected API

[List the expected public interface]

Example:
- `LRUCache(capacity)`
- `get(key)`
- `put(key, value)`

---

# Non-goals

[List what should NOT be included]

Example:
- thread safety
- TTL
- persistence
- serialization
- decorators

---

# Style Reference

Read first:
- `README.md`
- `docs/design.md`
- `docs/codex_handoff.md`
- existing modules such as `http/simple_http.py` and `retry/backoff.py`

---

# Acceptance Criteria

- file is self-contained
- self-test runs directly with Python
- no third-party imports
- API is minimal
- code is simpler rather than more abstract