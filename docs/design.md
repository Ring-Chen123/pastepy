# pastepy Design Principles

pastepy is not a package-first library. It is a set of copy-pasteable,
zero-dependency Python modules for edge devices, restricted systems, and places
where `pip install` is unavailable or unreliable.

## Core Philosophy

Copy. Paste. Run.

No installation. No hidden dependencies. No unnecessary abstraction.

## 1. Single File Only

- Each module must be a single file.
- No cross-file imports between modules.
- A user should be able to copy one file and use it immediately.

Good:

- `http/simple_http.py`
- `retry/backoff.py`

Bad:

- `http/client.py` importing `core/utils.py`

## 2. Standard Library Only

- Only Python standard library imports are allowed.
- No external packages.
- No optional dependency fallbacks inside modules.
- No external test framework required for validation.

## 3. Readability First

Code should be understandable quickly.

Prefer:

- straightforward control flow
- explicit functions
- small helper functions
- simple names

Avoid:

- generic frameworks
- clever but hard-to-read code
- unnecessary indirection
- abstractions created for only one caller

## 4. Minimal API

Expose only what is commonly needed.

Good:

- `get(...)`
- `post(...)`
- `retry(func, ...)`
- `load_env(path=".env")`

Bad:

- deeply generic request builders
- base classes for tiny utilities
- plugin systems

Every public function should justify its existence.

## 5. Keep It Small

Target:

- ideally under 200 lines
- soft limit around 300 lines

If a file grows too much, remove features first. Split scope only when the new
scope can still stand alone as a copy-pasteable file.

## 6. Safe Defaults

Modules should prefer safe, practical defaults.

Examples:

- network functions should have timeouts
- retry should be explicit
- file writes should avoid partial output where practical
- errors should fail clearly

Do not silently hide important failures.

## 7. Self-Test Required

Every module must include a small self-test block:

```python
if __name__ == "__main__":
    ...
```

Rules:

- fast
- easy to run
- no external test runner
- human-readable output

Recommended labels:

- `[TEST]`
- `[OK]`
- `[FAIL]`
- `[DONE]`

## 8. Copy-Paste Friendly

A module should work immediately after copy-paste.

Avoid:

- package setup
- local package imports
- hidden environment assumptions
- extra configuration unless essential

The user experience should be:

1. open file
2. copy
3. paste
4. run

## 9. Production-Aware, Not Production-Maximalist

pastepy is not trying to replace mature ecosystems.

It does not aim to beat:

- full-feature libraries
- highly optimized C extensions
- large frameworks

It aims to provide:

- practical tools
- reliable behavior
- clear trade-offs
- good-enough performance under constraints

## 10. When In Doubt, Remove

If a feature:

- is rarely needed
- increases complexity
- makes the API harder to learn
- makes the file harder to adapt

remove it. A smaller, clearer module is better than a complete but tangled one.

## 11. File Structure

Recommended repository structure:

```text
pastepy/
  cache/
    lru.py
    ttl_cache.py
  config/
    env_loader.py
  docs/
    design.md
    feature_index.md
    maturity.md
    roadmap.md
  fs/
    atomic_file.py
    file_lock.py
  http/
    simple_http.py
  rate_limit/
    token_bucket.py
  retry/
    backoff.py
  storage/
    json_store.py
  README.md
```

## 12. Style Checklist

Before accepting a new module or change, verify:

- standard library only
- single file
- no cross-file imports
- simple public API
- self-test exists
- easy to read quickly
- easy to copy and paste
- complexity did not grow without a strong reason
