# pastepy Roadmap

This roadmap lists useful modules that fit pastepy's constraints. It is not a
promise to build everything. Small, readable modules are preferred over broad
coverage.

For a larger edge/embedded AI feature backlog, see `docs/edge_feature_ideas.md`.

## Current Modules

- `asr/diarization_tools.py`: speaker-tag text turns, counts, durations, overlaps, and relabeling.
- `asr/endpointing_tools.py`: speech/silence endpointing and flush helpers.
- `asr/streaming_text.py`: partial/final streaming ASR text stabilization and display helpers.
- `archive/zip_tools.py`: ZIP archive helpers.
- `ai/output_tools.py`: classifier and detector output post-processing.
- `ai/transcript_tools.py`: ASR transcript cleanup and segment helpers.
- `ai/vector_tools.py`: small vector and embedding comparison helpers.
- `audio/wav_tools.py`: PCM WAV inspection, writing, chunking, and metrics.
- `audio/pcm_tools.py`: raw PCM16 preprocessing, simple VAD, and retention helpers.
- `cli/args.py`: tiny command-line flag parser.
- `config/env_loader.py`: `.env` file loader.
- `crypto/hash_tools.py`: checksums, HMAC, secure tokens, and constant-time comparison.
- `csv_tools/csv_rows.py`: CSV row and dict helpers.
- `data/iter_tools.py`: iterable cleanup and grouping helpers.
- `dataset/jsonl_tools.py`: newline-delimited JSON data capture helpers.
- `device/system_probe.py`: platform, CPU, disk, memory, Python, and env probes.
- `edge/resource_policy.py`: resource-aware model, chunk, retry, and degradation policy helpers.
- `fs/atomic_file.py`: atomic text and bytes writes.
- `fs/file_lock.py`: lock-file based coordination.
- `fs/path_tools.py`: small path and text file helpers.
- `http/simple_http.py`: minimal GET/POST client.
- `log/simple_logger.py`: small timestamped logger.
- `model/manifest_tools.py`: model metadata, checksum, version, rollout, and rollback helpers.
- `model/metrics_tools.py`: small classification metrics and drift helpers.
- `net/network_checks.py`: DNS, TCP, HTTP, TLS URL, allowlist, and reconnect helpers.
- `net/url_tools.py`: small URL query helpers.
- `ops/device_ops.py`: PID, heartbeat, config, feature flag, crash marker, and diagnostics helpers.
- `process/run_cmd.py`: subprocess wrapper with timeout and captured output.
- `rate_limit/token_bucket.py`: token bucket rate limiter.
- `storage/json_store.py`: JSON load/save helpers.
- `stream/chunk_tools.py`: stream chunk sizing, sequencing, latency, jitter, RTF, and queue helpers.
- `subtitles/subtitle_tools.py`: SRT/VTT parsing, writing, conversion, and cue helpers.
- `sensor/sensor_tools.py`: sensor CSV, timestamp, gap, window, calibration, and downsample helpers.
- `text/text_tools.py`: text cleanup and case conversion helpers.
- `time_tools/time_tools.py`: stopwatch, timestamp, and duration helpers.
- `update/ota_tools.py`: OTA manifest, staged install, rollback, lock, and readiness helpers.
- `validation/checks.py`: small validation helpers.
- `vision/image_tools.py`: tiny PPM/PGM image IO, transforms, frame schedule, and box helpers.
- `retry/backoff.py`: simple exponential retry.
- `cache/lru.py`: fixed-size LRU cache.
- `cache/ttl_cache.py`: cache with time-based expiry.

## Good Future Candidates

- `config/ini_loader.py`: small configparser wrapper.
- `dataset/label_studio.py`: tiny import/export helpers for annotation workflows.
- `http/static_server.py`: tiny local static file server.
- `model/manifest.py`: local model metadata and checksum manifest helpers.
- `net/socket_check.py`: TCP connectivity checks.
- `process/pid_file.py`: pid-file helper for scripts.
- `text/redact.py`: redact secrets from logs and text.
- `vision/box_tools.py`: bounding-box format conversion helpers.

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
