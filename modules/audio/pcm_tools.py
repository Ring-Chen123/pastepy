"""
Name: PCM Tools (no deps)

Why:
- Edge ASR often works with raw PCM16 chunks before writing WAV files
- Small audio preprocessing should not require numpy, scipy, or ffmpeg

Features:
- PCM16 sample helpers
- silence trim
- gain normalization
- simple energy VAD
- speech segment detection
- chunk manifests and retention cleanup

Limitations:
- PCM16 little-endian only
- VAD is energy-based, not model-based
"""

import json
import os
import struct
import time


def pcm16_samples(frames):
    return [struct.unpack_from("<h", frames, i)[0] for i in range(0, len(frames) - 1, 2)]


def pcm16_bytes(samples):
    out = bytearray()
    for sample in samples:
        sample = max(-32768, min(32767, int(sample)))
        out.extend(struct.pack("<h", sample))
    return bytes(out)


def sample_count(frames):
    return len(frames) // 2


def frame_windows(frames, sample_rate, window_ms):
    size = max(1, int(sample_rate * window_ms / 1000)) * 2
    for i in range(0, len(frames), size):
        yield frames[i:i + size]


def pcm16_rms(frames):
    samples = pcm16_samples(frames)
    if not samples:
        return 0
    return int((sum(s * s for s in samples) / len(samples)) ** 0.5)


def trim_silence(frames, threshold=500):
    samples = pcm16_samples(frames)
    start = 0
    end = len(samples)
    while start < end and abs(samples[start]) < threshold:
        start += 1
    while end > start and abs(samples[end - 1]) < threshold:
        end -= 1
    return pcm16_bytes(samples[start:end])


def normalize_gain(frames, target_peak=30000):
    samples = pcm16_samples(frames)
    peak = max([abs(s) for s in samples] or [0])
    if peak == 0:
        return frames
    factor = float(target_peak) / peak
    return pcm16_bytes(int(s * factor) for s in samples)


def energy_vad(frames, sample_rate, window_ms=30, threshold=500):
    return [pcm16_rms(w) >= threshold for w in frame_windows(frames, sample_rate, window_ms)]


def speech_segments(frames, sample_rate, window_ms=30, threshold=500):
    flags = energy_vad(frames, sample_rate, window_ms, threshold)
    segments = []
    start = None
    step = window_ms / 1000.0
    for i, active in enumerate(flags):
        if active and start is None:
            start = i * step
        elif not active and start is not None:
            segments.append({"start": start, "end": i * step})
            start = None
    if start is not None:
        segments.append({"start": start, "end": len(flags) * step})
    return segments


def pad_audio(frames, sample_rate, pre_ms=0, post_ms=0):
    pre = b"\x00\x00" * int(sample_rate * pre_ms / 1000)
    post = b"\x00\x00" * int(sample_rate * post_ms / 1000)
    return pre + frames + post


def validate_sample_rate(rate, allowed=(8000, 16000, 22050, 44100, 48000)):
    if rate not in allowed:
        raise ValueError("unsupported sample rate: %s" % rate)
    return True


def validate_channels(channels, allowed=(1, 2)):
    if channels not in allowed:
        raise ValueError("unsupported channels: %s" % channels)
    return True


def clipping_ratio(frames, limit=32700):
    samples = pcm16_samples(frames)
    if not samples:
        return 0
    clipped = sum(1 for sample in samples if abs(sample) >= limit)
    return clipped / float(len(samples))


def noise_floor(frames, sample_rate, window_ms=30):
    values = sorted(pcm16_rms(w) for w in frame_windows(frames, sample_rate, window_ms))
    if not values:
        return 0
    return values[len(values) // 10]


def level_histogram(frames, buckets=10):
    samples = [abs(s) for s in pcm16_samples(frames)]
    if not samples:
        return [0] * buckets
    hist = [0] * buckets
    for sample in samples:
        index = min(buckets - 1, int(sample / 32768.0 * buckets))
        hist[index] += 1
    return hist


def write_chunk_manifest(path, chunks):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, sort_keys=True)
        f.write("\n")


def media_filename(prefix, timestamp=None, ext="wav"):
    timestamp = int(timestamp if timestamp is not None else time.time())
    return "%s_%d.%s" % (prefix, timestamp, ext.lstrip("."))


def cleanup_retention(directory, max_age_seconds):
    now = time.time()
    removed = []
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isfile(path) and now - os.path.getmtime(path) > max_age_seconds:
            os.remove(path)
            removed.append(path)
    return removed


if __name__ == "__main__":
    print("[TEST] pcm_tools")
    try:
        frames = pcm16_bytes([0, 1000, -1000, 0])
        assert pcm16_samples(frames) == [0, 1000, -1000, 0]
        assert sample_count(frames) == 4
        assert trim_silence(frames, 500) == pcm16_bytes([1000, -1000])
        assert sample_count(normalize_gain(frames)) == 4
        assert energy_vad(frames, 1000, window_ms=2, threshold=500) == [True, True]
        assert speech_segments(frames, 1000, window_ms=2, threshold=500)[0]["start"] == 0
        assert sample_count(pad_audio(frames, 1000, 1, 1)) == 6
        assert validate_sample_rate(16000) is True
        assert validate_channels(1) is True
        assert clipping_ratio(pcm16_bytes([32767])) == 1
        assert noise_floor(frames, 1000) >= 0
        assert sum(level_histogram(frames)) == 4
        assert media_filename("mic", timestamp=1) == "mic_1.wav"
        print("[OK] pcm helpers")
        print("[DONE]")
    except Exception as e:
        print("[FAIL]", e)
