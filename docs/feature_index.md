# pastepy Feature Index

This index groups pastepy modules by the problem they solve. Every file is
copy-pasteable, standard-library only, and has a direct self-test.

## Edge AI / ASR

| Category | File | Public API | Use When |
| --- | --- | --- | --- |
| Subtitles | `subtitles/subtitle_tools.py` | `parse_timestamp`, `format_srt_timestamp`, `format_vtt_timestamp`, `make_cue`, `parse_srt`, `to_srt`, `parse_vtt`, `to_vtt`, `shift_cues`, `merge_close_cues`, `cues_to_text`, `split_text_to_cues` | Reading, writing, converting, or adjusting SRT/VTT captions from ASR output. |
| WAV Audio | `audio/wav_tools.py` | `wav_info`, `read_wav_frames`, `write_wav`, `wav_duration`, `split_wav`, `pcm16_silence`, `pcm16_peak`, `pcm16_rms`, `pcm16_to_mono`, `dbfs_from_rms` | Inspecting and chunking PCM WAV files before local ASR. |
| Raw PCM | `audio/pcm_tools.py` | `pcm16_samples`, `pcm16_bytes`, `sample_count`, `frame_windows`, `pcm16_rms`, `trim_silence`, `normalize_gain`, `energy_vad`, `speech_segments`, `pad_audio`, `validate_sample_rate`, `validate_channels`, `clipping_ratio`, `noise_floor`, `level_histogram`, `write_chunk_manifest`, `media_filename`, `cleanup_retention` | Preprocessing raw PCM16 audio for ASR capture and segmentation. |
| Transcripts | `ai/transcript_tools.py` | `normalize_segment`, `normalize_segments`, `transcript_text`, `clean_asr_text`, `remove_fillers`, `words_per_minute`, `segments_to_words`, `chunk_text`, `find_keyword_segments`, `redact_terms` | Cleaning, searching, chunking, and exporting ASR transcript segments. |
| Vectors | `ai/vector_tools.py` | `dot`, `norm`, `cosine_similarity`, `l2_distance`, `normalize_vector`, `mean_vector`, `top_k_similar`, `minmax_scale` | Small embedding comparisons without NumPy. |
| Model Output | `ai/output_tools.py` | `softmax`, `argmax`, `top_k`, `threshold_predictions`, `box_area`, `iou`, `non_max_suppression`, `confusion_matrix` | Post-processing classifier or detector outputs on-device. |
| Model Manifest | `model/manifest_tools.py` | `sha256_file`, `read_manifest`, `write_manifest`, `build_manifest`, `validate_model_checksum`, `parse_version`, `compare_versions`, `is_newer_version`, `compatibility_check`, `rollback_candidate`, `rollout_bucket`, `ab_variant`, `model_record` | Managing local model metadata, checksums, compatibility, rollout, and rollback. |
| Model Metrics | `model/metrics_tools.py` | `accuracy`, `confusion_counts`, `precision`, `recall`, `f1_score`, `per_class_counts`, `label_distribution`, `moving_average`, `confidence_average`, `majority_vote`, `debounce_predictions`, `drift_score` | Evaluating small classification runs and tracking drift on-device. |
| Sensors | `sensor/sensor_tools.py` | `parse_time`, `read_sensor_csv`, `write_sensor_csv`, `normalize_timestamps`, `detect_gaps`, `rolling_windows`, `convert_units`, `apply_calibration`, `detect_outliers`, `downsample`, `moving_average`, `minmax`, `summary`, `resample_nearest`, `latest_value` | Processing sensor CSV logs alongside local AI output. |
| Tiny Images | `vision/image_tools.py` | `image_dimensions`, `read_ppm`, `write_ppm`, `read_pgm`, `write_pgm`, `rgb_to_grayscale`, `crop`, `resize_nearest`, `tile_image`, `frame_schedule`, `write_frame_manifest`, `clamp_box`, `box_center`, `xywh_to_xyxy`, `xyxy_to_xywh` | Handling tiny debug image pipelines without Pillow or OpenCV. |
| JSONL Data | `dataset/jsonl_tools.py` | `read_jsonl`, `iter_jsonl`, `write_jsonl`, `append_jsonl`, `count_jsonl`, `filter_jsonl`, `split_jsonl` | Capturing ASR events, labels, prompts, and telemetry records locally. |
| Device Probe | `device/system_probe.py` | `platform_info`, `cpu_count`, `disk_usage`, `python_version`, `env_snapshot`, `memory_info`, `system_summary` | Checking deployment environment before running edge AI workloads. |

## Data And Text

| Category | File | Public API | Use When |
| --- | --- | --- | --- |
| Text | `text/text_tools.py` | `normalize_space`, `strip_prefix`, `strip_suffix`, `slugify`, `snake_case`, `kebab_case`, `truncate` | Cleaning filenames, labels, logs, and small text fields. |
| Iterables | `data/iter_tools.py` | `chunked`, `flatten`, `unique`, `first`, `compact`, `group_by`, `windowed` | Processing small in-memory streams or records. |
| CSV | `csv_tools/csv_rows.py` | `read_rows`, `write_rows`, `append_row`, `read_dicts`, `write_dicts`, `has_header` | Reading and writing simple CSV exports. |
| Validation | `validation/checks.py` | `require_keys`, `is_int`, `is_float`, `is_email`, `is_url`, `clamp`, `require_choice` | Guarding script inputs without a schema library. |

## Files, Storage, And Archives

| Category | File | Public API | Use When |
| --- | --- | --- | --- |
| Atomic Files | `fs/atomic_file.py` | `atomic_write_text`, `atomic_write_bytes` | Avoiding partial writes for state and config files. |
| File Lock | `fs/file_lock.py` | `FileLock` | Coordinating simple cross-process jobs. |
| Paths | `fs/path_tools.py` | `ensure_dir`, `read_text`, `write_text`, `touch`, `list_files`, `file_size`, `remove_empty_dirs` | Common small filesystem tasks. |
| JSON Store | `storage/json_store.py` | `load_json`, `save_json` | Small durable state without a database. |
| ZIP | `archive/zip_tools.py` | `zip_dir`, `unzip`, `list_zip`, `add_file`, `is_zip` | Moving logs, model outputs, or small datasets. |

## Networking, CLI, Process, And Ops

| Category | File | Public API | Use When |
| --- | --- | --- | --- |
| HTTP | `http/simple_http.py` | `Response`, `get`, `post` | Small GET/POST calls without requests. |
| URLs | `net/url_tools.py` | `encode_params`, `add_query`, `get_query`, `remove_query`, `join_url`, `is_http_url` | Editing query strings and joining URLs. |
| Network Checks | `net/network_checks.py` | `resolve_host`, `can_resolve`, `tcp_check`, `http_check`, `local_ip`, `is_tls_url`, `allowlist_url`, `denylist_url`, `reconnect_delay`, `wait_for_tcp` | Diagnosing edge connectivity and validating outbound targets. |
| CLI | `cli/args.py` | `parse_args`, `get_flag`, `has_flag`, `env_or_flag`, `require_flag` | Tiny scripts with a few command-line flags. |
| Process | `process/run_cmd.py` | `CommandResult`, `run`, `run_lines`, `which`, `shell_quote` | Running subprocesses with captured output. |
| Device Ops | `ops/device_ops.py` | `write_pid`, `read_pid`, `is_process_alive`, `write_heartbeat`, `read_heartbeat`, `heartbeat_stale`, `uptime_since`, `write_json_marker`, `read_json_marker`, `device_id`, `local_hostname`, `config_diff`, `merge_config`, `feature_enabled`, `rollout_enabled`, `low_disk`, `write_crash_marker`, `write_last_good`, `make_diagnostic_bundle` | Writing local reliability markers and diagnostic bundles for field devices. |
| OTA | `update/ota_tools.py` | `read_ota_manifest`, `write_ota_manifest`, `parse_version`, `ota_is_newer`, `mark_staged`, `mark_rollback`, `update_locked`, `create_update_lock`, `clear_update_lock`, `update_ready` | Managing simple local OTA state and rollback markers. |
| Logging | `log/simple_logger.py` | `Logger`, `make_logger` | Timestamped logs without logging setup. |
| Retry | `retry/backoff.py` | `retry` | Retrying unstable operations. |
| Rate Limit | `rate_limit/token_bucket.py` | `TokenBucket` | Limiting API calls or device actions. |
| Time | `time_tools/time_tools.py` | `Stopwatch`, `now_iso`, `unix_ms`, `format_duration`, `parse_duration`, `sleep_until` | Timing, timestamps, and simple delays. |
| Config | `config/env_loader.py` | `load_env` | Loading small `.env` files. |
| Hashing | `crypto/hash_tools.py` | `sha256_bytes`, `sha256_text`, `sha256_file`, `hmac_sha256`, `random_token`, `constant_time_equal` | Checksums, signatures, and secure tokens. |

## Choosing Quickly

- Need captions from ASR: start with `subtitles/subtitle_tools.py`.
- Need to cut audio before ASR: start with `audio/wav_tools.py`.
- Need raw PCM preprocessing or simple VAD: start with `audio/pcm_tools.py`.
- Need to clean transcript text: start with `ai/transcript_tools.py`.
- Need tiny embedding search: start with `ai/vector_tools.py`.
- Need model post-processing: start with `ai/output_tools.py`.
- Need model rollout metadata: start with `model/manifest_tools.py`.
- Need device heartbeat or diagnostics: start with `ops/device_ops.py`.
- Need local data capture: start with `dataset/jsonl_tools.py`.
- Need deployment diagnostics: start with `device/system_probe.py`.
