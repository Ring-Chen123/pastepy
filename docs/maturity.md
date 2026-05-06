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

- `modules/http/simple_http.py`
- `modules/retry/backoff.py`
- `modules/cache/lru.py`
- `modules/config/env_loader.py`
- `modules/rate_limit/token_bucket.py`

Expectations:

- very small public API
- safe defaults
- no surprising behavior
- short, readable implementation
- direct self-test

## Practical Utilities

These modules support common scripting work without becoming the main identity
of the project:

- `modules/archive/zip_tools.py`
- `modules/cache/ttl_cache.py`
- `modules/cli/args.py`
- `modules/crypto/hash_tools.py`
- `modules/csv_tools/csv_rows.py`
- `modules/data/iter_tools.py`
- `modules/dataset/jsonl_tools.py`
- `modules/fs/atomic_file.py`
- `modules/fs/file_lock.py`
- `modules/fs/path_tools.py`
- `modules/log/simple_logger.py`
- `modules/net/url_tools.py`
- `modules/process/run_cmd.py`
- `modules/storage/json_store.py`
- `modules/text/text_tools.py`
- `modules/time_tools/time_tools.py`
- `modules/validation/checks.py`

## Experimental Edge Expansion

These modules are useful for edge AI, ASR, streaming, model deployment, and
field operations. They should remain copy-pasteable, but their APIs may be
refined as real use cases become clearer.

- `modules/ai/output_tools.py`
- `modules/ai/transcript_tools.py`
- `modules/ai/vector_tools.py`
- `modules/asr/diarization_tools.py`
- `modules/asr/endpointing_tools.py`
- `modules/asr/streaming_text.py`
- `modules/audio/pcm_tools.py`
- `modules/audio/wav_tools.py`
- `modules/device/system_probe.py`
- `modules/edge/resource_policy.py`
- `modules/model/manifest_tools.py`
- `modules/model/metrics_tools.py`
- `modules/net/network_checks.py`
- `modules/ops/device_ops.py`
- `modules/sensor/sensor_tools.py`
- `modules/stream/chunk_tools.py`
- `modules/subtitles/subtitle_tools.py`
- `modules/update/ota_tools.py`
- `modules/vision/image_tools.py`

## Review Checklist

Before moving an experimental module closer to Core MVP:

- Is the use case common enough?
- Is the API still easy to remember?
- Can the module be understood quickly?
- Are limitations clear?
- Does the self-test cover the main behavior?
- Would a first-time user immediately understand why this belongs in pastepy?
