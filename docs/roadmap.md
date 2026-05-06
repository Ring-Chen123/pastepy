# pastepy Roadmap

This roadmap lists useful modules that fit pastepy's constraints. It is not a
promise to build everything. Small, readable modules are preferred over broad
coverage.

## Current Modules

### Core MVP

- `modules/http/simple_http.py`: minimal GET/POST client.
- `modules/retry/backoff.py`: simple exponential retry.
- `modules/cache/lru.py`: fixed-size LRU cache.
- `modules/config/env_loader.py`: `.env` file loader.
- `modules/rate_limit/token_bucket.py`: token bucket rate limiter.

### Practical Utilities

- `modules/archive/zip_tools.py`: ZIP archive helpers.
- `modules/cache/ttl_cache.py`: cache with time-based expiry.
- `modules/cli/args.py`: tiny command-line flag parser.
- `modules/crypto/hash_tools.py`: checksums, HMAC, secure tokens, and constant-time comparison.
- `modules/csv_tools/csv_rows.py`: CSV row and dict helpers.
- `modules/data/iter_tools.py`: iterable cleanup and grouping helpers.
- `modules/dataset/jsonl_tools.py`: newline-delimited JSON data capture helpers.
- `modules/fs/atomic_file.py`: atomic text and bytes writes.
- `modules/fs/file_lock.py`: lock-file based coordination.
- `modules/fs/path_tools.py`: small path and text file helpers.
- `modules/log/simple_logger.py`: small timestamped logger.
- `modules/net/url_tools.py`: small URL query helpers.
- `modules/process/run_cmd.py`: subprocess wrapper with timeout and captured output.
- `modules/storage/json_store.py`: JSON load/save helpers.
- `modules/text/text_tools.py`: text cleanup and case conversion helpers.
- `modules/time_tools/time_tools.py`: stopwatch, timestamp, and duration helpers.
- `modules/validation/checks.py`: small validation helpers.

### Experimental Edge Expansion

- `modules/asr/diarization_tools.py`: speaker-tag text turns, counts, durations, overlaps, and relabeling.
- `modules/asr/endpointing_tools.py`: speech/silence endpointing and flush helpers.
- `modules/asr/streaming_text.py`: partial/final streaming ASR text stabilization and display helpers.
- `modules/ai/output_tools.py`: classifier and detector output post-processing.
- `modules/ai/transcript_tools.py`: ASR transcript cleanup and segment helpers.
- `modules/ai/vector_tools.py`: small vector and embedding comparison helpers.
- `modules/audio/pcm_tools.py`: raw PCM16 preprocessing, simple VAD, and retention helpers.
- `modules/audio/wav_tools.py`: PCM WAV inspection, writing, chunking, and metrics.
- `modules/device/system_probe.py`: platform, CPU, disk, memory, Python, and env probes.
- `modules/edge/resource_policy.py`: resource-aware model, chunk, retry, and degradation policy helpers.
- `modules/model/manifest_tools.py`: model metadata, checksum, version, rollout, and rollback helpers.
- `modules/model/metrics_tools.py`: small classification metrics and drift helpers.
- `modules/net/network_checks.py`: DNS, TCP, HTTP, TLS URL, allowlist, and reconnect helpers.
- `modules/ops/device_ops.py`: PID, heartbeat, config, feature flag, crash marker, and diagnostics helpers.
- `modules/stream/chunk_tools.py`: stream chunk sizing, sequencing, latency, jitter, RTF, and queue helpers.
- `modules/subtitles/subtitle_tools.py`: SRT/VTT parsing, writing, conversion, and cue helpers.
- `modules/sensor/sensor_tools.py`: sensor CSV, timestamp, gap, window, calibration, and downsample helpers.
- `modules/update/ota_tools.py`: OTA manifest, staged install, rollback, lock, and readiness helpers.
- `modules/vision/image_tools.py`: tiny PPM/PGM image IO, transforms, frame schedule, and box helpers.

## Good Future Candidates

- `modules/config/ini_loader.py`: small configparser wrapper.
- `modules/dataset/label_studio.py`: tiny import/export helpers for annotation workflows.
- `modules/http/static_server.py`: tiny local static file server.
- `modules/model/manifest.py`: local model metadata and checksum manifest helpers.
- `modules/net/socket_check.py`: TCP connectivity checks.
- `modules/process/pid_file.py`: pid-file helper for scripts.
- `modules/text/redact.py`: redact secrets from logs and text.
- `modules/vision/box_tools.py`: bounding-box format conversion helpers.

## Non-Goals

- package publishing
- framework-style APIs
- shared internal utility modules
- optional third-party integrations
- replacing mature libraries when dependencies are available

## Acceptance Bar

Each new module should answer:

- Can a user copy this one file and run it?
- Does it solve a common real problem?
- Is the public API small?
- Are limitations explicit?
- Does the direct self-test pass without external services?
