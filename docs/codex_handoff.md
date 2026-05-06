# Codex Handoff for pastepy

This file explains how to work on this repository.

Read this file together with:
- `README.md`
- `docs/design.md`
- `docs/roadmap.md`

---

## What pastepy is

pastepy is a repository of **copy-pasteable, zero-dependency Python modules**.

The target environments include:
- edge devices
- embedded or restricted systems
- CPU architectures where wheels may not exist
- environments where `pip install` is unavailable or unreliable

This is not a normal Python package project.

---

## Hard Rules

These rules should be treated as mandatory unless the task explicitly says otherwise.

### 1. Standard library only
- Do not introduce third-party dependencies
- Do not suggest optional package fallbacks in the module itself

### 2. Single-file modules
- Each module must remain usable as one independent file
- Do not create cross-file imports between modules

### 3. Readability over abstraction
- Prefer explicit code over generic frameworks
- Prefer small APIs over flexible but complex APIs

### 4. Self-test required
- Every module must include a small `if __name__ == "__main__":` test block
- Self-test should be fast and easy to run

### 5. Keep modules small
- Prefer short files
- If complexity grows, reduce scope before adding abstraction

---

## Preferred Design Style

When implementing or revising a module:

- choose the smallest useful API
- avoid “future-proofing” that adds complexity now
- avoid decorators in v1 unless they remain very simple
- avoid feature combinations that make code much harder to read
- prefer “good enough and clear” over “complete and clever”

Examples of preferred style:
- `get(...)`, `post(...)`
- `retry(func, ...)`
- `load_env(path=".env")`

Examples of discouraged style:
- deeply generic request builders
- base classes for tiny utilities
- plugin systems
- multi-file helpers

---

## Current Style References

Use these modules as style references:
- `http/simple_http.py`
- `retry/backoff.py`

The direction is:
- short docstring at top
- small public API
- small private helpers
- self-test at bottom
- no unnecessary indirection

---

## What to optimize for

When making decisions, prioritize in this order:

1. copy-paste usability
2. readability
3. practical usefulness
4. small size
5. performance

Performance matters, but not at the cost of turning a module into hard-to-understand code.

---

## What not to optimize for

Do not optimize for:
- package architecture
- framework extensibility
- maximum feature coverage
- advanced abstraction layers
- “enterprise” style patterns

---

## Expected Output for New Modules

A new module should usually include:

1. top docstring with:
   - name
   - why
   - features
   - limitations
   - usage

2. implementation

3. self-test:
   - `[TEST]`
   - `[OK]`
   - `[FAIL]`

---

## Change Policy

When improving an existing file:
- prefer simplification over expansion
- do not add features unless they clearly fit the core goal
- do not refactor into multiple files
- preserve current API unless there is a strong reason to change it

If you must choose between:
- a shorter clearer module
- a more capable but more complex module

Choose the shorter clearer module.

---

## Typical Tasks

Examples of good tasks:
- implement `cache/lru.py`
- simplify `simple_http.py`
- unify self-test style
- add a small config loader using stdlib only

Examples of bad directions:
- convert repo into installable package
- add pytest dependency to core module design
- create shared internal utility modules for reuse
- redesign everything around a generic base class

---

## Instruction Template

When asked to work on this repo, assume this default instruction:

> Implement the requested module or revision in the style of pastepy:
> stdlib only, single-file, copy-pasteable, readable, self-tested, and minimal.

If unsure, remove complexity.