# pastepy

> Copy. Paste. Done.
>
> No pip. No install. No bullshit.

A collection of **zero-dependency, copy-pasteable Python modules** built for **edge devices, restricted environments, and real-world constraints**.

---

## ⚡ The problem

I was building on an edge device where I **couldn't install Python packages**.

* No wheels for the CPU architecture
* No compiler for C extensions
* No internet access
* `pip install` simply not an option

But I still needed:

* HTTP requests
* Retry logic
* Caching
* Rate limiting

So I started rewriting things from scratch.

This repo is the result.

---

## 🚀 What this is

**pastepy = Python utilities you can copy and run instantly**

* Single-file modules
* Zero dependencies
* Standard library only
* Designed for real use (not demos)

```python
from simple_http import get

res = get("https://example.com", timeout=3)
print(res.status, res.text)
```

No install. No setup. Just works.

---

## 🎯 Design Principles

Every module in pastepy follows strict rules:

### 1. Zero Dependencies

* Only Python standard library
* No external packages

### 2. Copy-Paste First

* Single file
* No imports outside stdlib
* Works immediately

### 3. Edge-Ready

* Fast startup (no import chains)
* Low memory footprint
* Works on limited systems

### 4. Production-Aware

* Clear limitations
* Safe defaults
* Predictable behavior

### 5. Small & Focused

* One file = one job
* No feature bloat

---

## 📦 Modules

### 🌐 HTTP

* `simple_http.py` → Minimal HTTP client (GET/POST, timeout, retry)

### ♻️ Retry

* `backoff.py` → Exponential backoff with jitter

### 🧠 Cache

* `lru.py` → Lightweight LRU cache

### 🚦 Rate Limiting

* `token_bucket.py` → Token bucket limiter

### ⚙️ Config

* `env_loader.py` → `.env` loader (no deps)

---

## ⚔️ Why not just use requests?

| Feature      | requests | pastepy |
| ------------ | -------- | ------- |
| pip install  | ✅        | ❌       |
| dependencies | many     | 0       |
| copy-paste   | ❌        | ✅       |
| edge-ready   | ❌        | ✅       |
| startup cost | higher   | minimal |

---

## 📊 When to use pastepy

Use it when:

* You **cannot install dependencies**
* You're on **edge / embedded systems**
* You need a **quick, reliable solution**
* You want **full control over the code**

Avoid it when:

* You need high-performance numeric computing
* You need full-feature frameworks
* You can safely use mature libraries

---

## 🧪 Quality Standard

Each module includes:

* Purpose & use-case
* Limitations (explicit)
* Complexity (when relevant)
* Usage examples
* Self-contained implementation

---

## 🔍 Find what you need

* Need HTTP? → `http/simple_http.py`
* Need retry? → `retry/backoff.py`
* Need cache? → `cache/lru.py`
* Need rate limit? → `rate_limit/token_bucket.py`

---

## 🤝 Contributing

Contributions are welcome, but must follow strict rules:

* Single-file only
* No dependencies
* Clear documentation
* Production-safe behavior
* Keep it small

If you're unsure, make it simpler.

---

## 🧭 Philosophy

> Ship less. Run everywhere.

---

## 📜 License

MIT
