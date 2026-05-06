# Module Maturity

pastepy started as a small, focused set of copy-pasteable utilities. The project
now also includes broader edge AI and ASR helpers. This document keeps that
growth explicit so the repo does not feel like an uncurated toolbox.

## Stability Levels

| Level | Meaning | Change Policy |
| --- | --- | --- |
| Core MVP | Stable front-door modules that define pastepy's promise. | Keep APIs small and conservative. Prefer bug fixes and simplification over expansion. |
| Practical Utility | General-purpose helpers that are useful in restricted environments. | Add features only when they stay small and copy-paste friendly. |
| Experimental Edge Expansion | Edge AI, ASR, model ops, streaming, and device operations helpers. | May evolve faster. Keep self-tests and clear limitations. |

## Core MVP

These files should be treated as the polished public face of the project:

- `http/simple_http.py`
- `retry/backoff.py`
- `cache/lru.py`
- `config/env_loader.py`
- `rate_limit/token_bucket.py`

Expectations:

- very small public API
- safe defaults
- no surprising behavior
- short, readable implementation
- direct self-test

## Practical Utilities

These modules support common scripting work without becoming the main identity
of the project:

- `archive/zip_tools.py`
- `cache/ttl_cache.py`
- `cli/args.py`
- `crypto/hash_tools.py`
- `csv_tools/csv_rows.py`
- `data/iter_tools.py`
- `dataset/jsonl_tools.py`
- `fs/atomic_file.py`
- `fs/file_lock.py`
- `fs/path_tools.py`
- `log/simple_logger.py`
- `net/url_tools.py`
- `process/run_cmd.py`
- `storage/json_store.py`
- `text/text_tools.py`
- `time_tools/time_tools.py`
- `validation/checks.py`

## Experimental Edge Expansion

These modules are useful for edge AI, ASR, streaming, model deployment, and
field operations. They should remain copy-pasteable, but their APIs may be
refined as real use cases become clearer.

- `ai/output_tools.py`
- `ai/transcript_tools.py`
- `ai/vector_tools.py`
- `asr/diarization_tools.py`
- `asr/endpointing_tools.py`
- `asr/streaming_text.py`
- `audio/pcm_tools.py`
- `audio/wav_tools.py`
- `device/system_probe.py`
- `edge/resource_policy.py`
- `model/manifest_tools.py`
- `model/metrics_tools.py`
- `net/network_checks.py`
- `ops/device_ops.py`
- `sensor/sensor_tools.py`
- `stream/chunk_tools.py`
- `subtitles/subtitle_tools.py`
- `update/ota_tools.py`
- `vision/image_tools.py`

## Review Checklist

Before moving an experimental module closer to Core MVP:

- Is the use case common enough?
- Is the API still easy to remember?
- Can the module be understood quickly?
- Are limitations clear?
- Does the self-test cover the main behavior?
- Would a first-time user immediately understand why this belongs in pastepy?
