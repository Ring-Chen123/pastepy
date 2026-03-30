# pastepy Design Principles

pastepy is not a library.

It is a collection of **copy-pasteable, zero-dependency Python modules**.

---

## Core Philosophy

> Copy. Paste. Run.

No installation.
No setup.
No hidden dependencies.

---

## 1. Single File Only

- Each module must be a single file
- No cross-file imports
- Must work independently

---

## 2. Zero Dependencies

- Only Python standard library
- No external packages
- No optional dependencies

---

## 3. Keep It Small

- Prefer < 200 lines
- Hard limit: ~300 lines
- If it grows too big → split it

---

## 4. Readability First

- Code should be understandable in 1-2 minutes
- Avoid over-abstraction
- Avoid unnecessary flexibility

Bad:
    request(method, ...)

Good:
    get(...)
    post(...)

---

## 5. Minimal API

- Only expose what is commonly needed
- No feature bloat
- No "just in case" design

---

## 6. Safe Defaults

- Timeout must exist
- Retry should be optional
- Fail loudly when necessary

---

## 7. Self-Test Required

Every module must include:

```python
if __name__ == "__main__":