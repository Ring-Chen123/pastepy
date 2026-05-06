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
適合 edge devices、embedded systems、離線環境，以及無法安裝套件的受限設備。

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
