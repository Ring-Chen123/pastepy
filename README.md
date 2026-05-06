<p align="center">
  <img src="assets/icon.png" alt="pastepy icon" width="160">
</p>

# pastepy

> Copy. Paste. Done.
>
> No pip. No install. Standard library only.

pastepy is a collection of **zero-dependency, copy-pasteable Python modules**
for edge devices, restricted environments, and practical scripts.

pastepy 是一組 **零依賴、可直接複製貼上使用的 Python 單檔工具**，
適合 edge devices、embedded systems、離線環境、無法安裝套件的設備，
以及 edge AI / streaming ASR 周邊應用。

## Quick Start

Copy one file from `modules/` into your project and use it directly.

```python
from simple_http import get

res = get("https://example.com", timeout=3)
print(res.status, res.text)
```

## Core MVP

Start here if you want the smallest stable set:

| Need | File |
| --- | --- |
| HTTP requests | [modules/http/simple_http.py](modules/http/simple_http.py) |
| Retry logic | [modules/retry/backoff.py](modules/retry/backoff.py) |
| Small cache | [modules/cache/lru.py](modules/cache/lru.py) |
| Config | [modules/config/env_loader.py](modules/config/env_loader.py) |
| Rate limiting | [modules/rate_limit/token_bucket.py](modules/rate_limit/token_bucket.py) |

這五個模組是 pastepy 的核心門面，會優先保持簡潔、穩定、容易理解。

## Repository Layout

```text
pastepy/
  assets/       icon and public assets
  docs/         public documentation
  modules/      copy-pasteable Python modules
    http/
    retry/
    cache/
    config/
    rate_limit/
    ...
```

## Module Groups

pastepy currently includes **41 single-file modules** and **311 public entry
points**.

| Group | Purpose |
| --- | --- |
| Core MVP | HTTP, retry, LRU cache, env loader, token bucket |
| Practical utilities | files, JSON, CSV, ZIP, CLI, logging, text, validation |
| Experimental edge expansion | ASR, streaming text, audio, subtitles, model ops, device ops |

Full module index: [docs/feature_index.md](docs/feature_index.md)

Maturity policy: [docs/maturity.md](docs/maturity.md)

Design principles: [docs/design.md](docs/design.md)

Roadmap: [docs/roadmap.md](docs/roadmap.md)

## Design Principles

- Standard library only
- Single-file modules
- No cross-module imports
- Copy-paste first
- Clear limitations
- Direct self-test in every module

## Run Self-Tests

Each module can be run directly:

```bash
python modules/cache/lru.py
python modules/rate_limit/token_bucket.py
python modules/asr/streaming_text.py
```

## When To Use

Use pastepy when:

- you cannot install dependencies
- you work on edge or embedded systems
- you need small, inspectable utilities
- you want code that can be copied into restricted environments

Avoid it when a mature package is available and dependencies are acceptable.

## Philosophy

> Ship less. Run everywhere.

## License

MIT
