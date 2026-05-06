# Edge AI Feature Ideas

This survey turns edge/embedded AI needs into a feature backlog for pastepy.
The ideas are based on common themes from edge AI and IoT materials: local
inference, sensor pipelines, model optimization, telemetry, OTA updates,
device management, security, and field diagnostics.

References used:

- Python Standard Library: https://docs.python.org/3/library/
- Edge AI survey, data/model/system optimization: https://arxiv.org/abs/2501.03265
- Edge Impulse TinyML/MLOps workflow paper: https://arxiv.org/abs/2212.03332
- EdgeMLOps visual inspection deployment paper: https://arxiv.org/abs/2501.17062
- NVIDIA Holoscan edge pipeline overview: https://www.nvidia.com/en-us/edge-computing/holoscan/
- Particle OTA and device management materials: https://www.particle.io/ota/
- Mender OTA device software updates: https://mender.io/
- LwM2M device management overview: https://en.wikipedia.org/wiki/OMA_LWM2M

## 1. Sensor, Audio, And Media IO

1. SRT parser
2. SRT writer
3. WebVTT parser
4. WebVTT writer
5. subtitle timestamp shifter
6. subtitle cue merger
7. subtitle cue splitter
8. transcript-to-subtitle formatter
9. subtitle-to-plain-text extractor
10. subtitle overlap detector
11. WAV metadata reader
12. WAV PCM16 writer
13. WAV duration calculator
14. WAV chunk splitter
15. WAV chunk manifest writer
16. PCM16 RMS calculator
17. PCM16 peak calculator
18. PCM16 dBFS converter
19. PCM16 silence generator
20. PCM16 mono converter
21. PCM16 trim silence
22. PCM16 normalize gain
23. PCM16 sample counter
24. PCM16 frame window iterator
25. simple energy VAD
26. speech segment detector
27. audio pre-roll/post-roll padding
28. audio sample-rate metadata validator
29. audio channel validator
30. audio clipping detector
31. audio noise floor estimator
32. audio level histogram
33. microphone capture manifest
34. image file dimension reader
35. PPM/PGM tiny image reader
36. PPM/PGM tiny image writer
37. RGB to grayscale converter
38. image crop box helper
39. image resize nearest-neighbor
40. image tile splitter
41. frame sampling schedule helper
42. camera frame manifest writer
43. sensor CSV reader
44. sensor timestamp normalizer
45. sensor gap detector
46. sensor rolling window iterator
47. sensor unit conversion table
48. sensor calibration offset helper
49. sensor outlier detector
50. sensor stream downsampler
51. media file naming helper
52. media retention cleanup helper

## 2. Edge Inference And Model Utilities

1. softmax
2. sigmoid
3. argmax
4. top-k labels
5. confidence threshold filter
6. class label mapper
7. prediction JSON formatter
8. prediction CSV formatter
9. prediction latency timer
10. model warmup runner
11. model input shape validator
12. model output shape validator
13. ONNX metadata reader
14. TFLite metadata sidecar reader
15. model manifest reader
16. model manifest writer
17. model checksum validator
18. model version comparator
19. model compatibility checker
20. model rollback selector
21. model A/B routing helper
22. model canary percentage helper
23. quantization scale/dezero helper
24. int8 tensor dequantizer
25. float tensor quantizer
26. vector dot product
27. vector norm
28. cosine similarity
29. L2 distance
30. vector normalization
31. mean embedding
32. top-k embedding search
33. min-max score scaling
34. box area
35. box IoU
36. non-max suppression
37. bounding box clamp
38. bounding box format converter
39. bounding box center calculator
40. detection label grouper
41. confusion matrix
42. precision/recall calculator
43. F1 score calculator
44. accuracy calculator
45. drift score tracker
46. moving average confidence
47. prediction debounce helper
48. prediction majority vote
49. temporal smoothing helper
50. inference benchmark summary
51. per-class threshold helper
52. model output redaction helper

## 3. Device Operations, Fleet, And Reliability

1. platform info probe
2. CPU count probe
3. disk usage probe
4. memory info probe
5. Python version probe
6. environment snapshot
7. system summary
8. process PID file
9. process liveness check
10. process restart counter
11. watchdog heartbeat file
12. watchdog stale heartbeat detector
13. service uptime tracker
14. boot ID recorder
15. device identity file
16. device serial reader
17. hostname normalizer
18. local IP detector
19. network reachability check
20. TCP port check
21. DNS resolution check
22. HTTP health check
23. exponential reconnect delay
24. offline queue status
25. disk low-watermark alert
26. log directory rotation
27. retention cleanup
28. crash marker writer
29. crash marker reader
30. last-good-state recorder
31. atomic config update
32. config schema-lite validator
33. config diff helper
34. remote config merge
35. feature flag reader
36. rollout bucket calculator
37. OTA manifest parser
38. OTA version comparator
39. OTA download verifier
40. OTA staged install marker
41. OTA rollback marker
42. update lock file
43. update readiness checker
44. battery level parser
45. thermal status parser
46. accelerator availability marker
47. storage mount checker
48. removable media detector
49. device time skew checker
50. NTP sync status parser
51. field diagnostic bundle creator
52. support snapshot exporter

## 4. Edge Data, Telemetry, And Sync

1. JSONL reader
2. JSONL iterator
3. JSONL writer
4. JSONL appender
5. JSONL counter
6. JSONL filter
7. JSONL splitter
8. CSV row reader
9. CSV row writer
10. CSV dict reader
11. CSV dict writer
12. CSV append row
13. event envelope builder
14. event timestamp normalizer
15. event ID generator
16. event deduplicator
17. event batcher
18. event size estimator
19. telemetry buffer
20. telemetry spool directory
21. telemetry retry queue
22. telemetry ACK tracker
23. telemetry compact summary
24. bandwidth budget estimator
25. upload chunk planner
26. resumable upload manifest
27. sync cursor reader
28. sync cursor writer
29. local sequence number generator
30. SQLite-lite wrapper
31. key-value JSON store
32. atomic JSON save
33. append-only audit log
34. data retention policy
35. data anonymization mapper
36. PII field remover
37. token counter approximation
38. transcript chunker
39. transcript keyword index
40. transcript summary record
41. ASR confidence histogram
42. label distribution report
43. dataset train/test splitter
44. dataset stratified splitter
45. dataset checksum manifest
46. dataset sample preview
47. dataset corrupt record detector
48. dataset schema-lite checker
49. dataset merge helper
50. dataset diff helper
51. compressed archive packer
52. compressed archive unpacker

## 5. Security, Privacy, And Safety Controls

1. SHA-256 text hash
2. SHA-256 file hash
3. HMAC-SHA256 signer
4. constant-time compare
5. secure random token
6. file integrity manifest
7. directory integrity manifest
8. signed manifest verifier
9. secret redactor
10. API key pattern redactor
11. email redactor
12. phone number redactor
13. local-only mode guard
14. network-disabled guard
15. allowlist URL checker
16. denylist URL checker
17. path traversal guard
18. safe filename sanitizer
19. extension allowlist checker
20. max file size checker
21. MIME guess validator
22. prompt injection marker detector
23. unsafe command detector
24. shell argument quote helper
25. subprocess timeout wrapper
26. audit event writer
27. audit event reader
28. audit event summarizer
29. privacy budget counter
30. data minimization checker
31. transcript PII scanner
32. location field remover
33. face crop metadata remover
34. EXIF strip planner
35. consent marker checker
36. retention expiry checker
37. secure delete best-effort helper
38. config permission checker
39. file owner checker
40. TLS URL checker
41. certificate expiry parser
42. update signature required checker
43. rollback safety checker
44. model provenance recorder
45. model license metadata checker
46. model source allowlist checker
47. safety threshold validator
48. human-review queue writer
49. anomaly alert formatter
50. incident bundle packer
51. offline incident journal
52. safe default config generator

## Suggested Build Order

1. Implement raw PCM and simple VAD helpers.
2. Implement model manifest and checksum helpers.
3. Implement telemetry spool and offline retry queue.
4. Implement device watchdog and diagnostic bundle helpers.
5. Implement redaction, allowlist, and audit-log helpers.
