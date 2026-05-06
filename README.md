<p align="center">
  <img src="assets/icon.png" alt="pastepy icon" width="160">
</p>

# pastepy

> Copy. Paste. Done.
>
> No pip. No install. Standard library only.

pastepy is a collection of zero-dependency, copy-pasteable Python modules
for edge devices, restricted environments, and local AI coding agents.

It is built for situations where:
- dependencies are hard to install
- CPU architecture is unusual
- network access is restricted
- cloud AI tools are not allowed
- local LLMs are helpful but not fully reliable at writing code from scratch

Instead of asking humans or small AI agents to reinvent common utilities,
pastepy provides known-good single-file modules that can be copied, reviewed,
and adapted.

pastepy 是一組 **零依賴、可直接複製貼上的 Python 模組**，
為 edge devices、受限環境，以及本地 AI coding agents 而設計。

## Core Modules

Start here:

- HTTP: [modules/http/simple_http.py](modules/http/simple_http.py)
- Retry: [modules/retry/backoff.py](modules/retry/backoff.py)
- Cache: [modules/cache/lru.py](modules/cache/lru.py)
- Config: [modules/config/env_loader.py](modules/config/env_loader.py)
- Rate Limit: [modules/rate_limit/token_bucket.py](modules/rate_limit/token_bucket.py)

這五個模組是 pastepy 的核心門面，會優先保持小、穩定、容易理解。

## How To Use

1. Open the module you need.
2. Copy the file into your project.
3. Import it locally.

Example:

```python
# copy modules/http/simple_http.py into your project first
from simple_http import get

res = get("https://example.com", timeout=3)
print(res.status, res.text)
```

No package install is required.

## Extended / Experimental Modules

pastepy also includes experimental utilities for edge AI, ASR, subtitles,
device probing, OTA markers, and resource policy.

More utilities are listed in [docs/feature_index.md](docs/feature_index.md).

## Why this exists 

**Built for constrained environments — and constrained AI**

In many companies, developers cannot freely use cloud-based AI coding tools.

Instead, they often rely on internal or local AI assistants running smaller models.
These models can understand intent, but they may not reliably generate correct
production code from scratch.

pastepy is designed to help with that.

The idea is simple:

- humans define the need
- small local LLMs search and understand the available modules
- the agent copies a known-good single-file implementation
- developers review and adapt the result

Small models do not need to invent reliable code.
They only need to find, copy, and connect existing reliable code.

This makes pastepy useful not only as a human toolbox, but also as a
code palette for local AI agents working in restricted environments.

## Docs

- [Feature index](docs/feature_index.md)
- [Module maturity](docs/maturity.md)
- [Design principles](docs/design.md)
- [Roadmap](docs/roadmap.md)

## Design Principles

- Standard library only
- Single-file modules
- No cross-module imports
- Copy-paste first
- Clear limitations
- Direct self-test in every module

## License

MIT
