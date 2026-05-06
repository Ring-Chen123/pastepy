"""
Name: WAV Tools (no deps)

Why:
- Edge ASR pipelines often exchange PCM WAV files
- Basic audio inspection and splitting should not need numpy or ffmpeg

Features:
- read WAV metadata
- duration calculation
- read and write frames
- split into chunks
- mono conversion for 16-bit PCM
- simple peak/RMS metrics

Limitations:
- Designed for PCM WAV
- Mono conversion only supports 16-bit samples

Usage:
    info = wav_info("audio.wav")
    print(info["duration"])
"""

import math
import os
import struct
import wave


def wav_info(path):
    with wave.open(path, "rb") as w:
        frames = w.getnframes()
        rate = w.getframerate()
        return {
            "channels": w.getnchannels(),
            "sample_width": w.getsampwidth(),
            "sample_rate": rate,
            "frames": frames,
            "duration": frames / float(rate) if rate else 0,
        }


def read_wav_frames(path):
    with wave.open(path, "rb") as w:
        params = w.getparams()
        frames = w.readframes(w.getnframes())
    return params, frames


def write_wav(path, frames, sample_rate=16000, channels=1, sample_width=2):
    with wave.open(path, "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(sample_width)
        w.setframerate(sample_rate)
        w.writeframes(frames)


def wav_duration(path):
    return wav_info(path)["duration"]


def split_wav(path, output_dir, chunk_seconds):
    if chunk_seconds <= 0:
        raise ValueError("chunk_seconds must be greater than 0")
    os.makedirs(output_dir, exist_ok=True)
    with wave.open(path, "rb") as w:
        rate = w.getframerate()
        chunk_frames = int(rate * chunk_seconds)
        outputs = []
        index = 0
        while True:
            frames = w.readframes(chunk_frames)
            if not frames:
                break
            out = os.path.join(output_dir, "chunk_%04d.wav" % index)
            with wave.open(out, "wb") as o:
                o.setparams(w.getparams())
                o.writeframes(frames)
            outputs.append(out)
            index += 1
    return outputs


def pcm16_silence(duration, sample_rate=16000, channels=1):
    samples = int(duration * sample_rate * channels)
    return b"\x00\x00" * samples


def pcm16_peak(frames):
    if not frames:
        return 0
    peak = 0
    for i in range(0, len(frames) - 1, 2):
        sample = struct.unpack_from("<h", frames, i)[0]
        peak = max(peak, abs(sample))
    return peak


def pcm16_rms(frames):
    if not frames:
        return 0
    total = 0
    count = 0
    for i in range(0, len(frames) - 1, 2):
        sample = struct.unpack_from("<h", frames, i)[0]
        total += sample * sample
        count += 1
    return int(math.sqrt(total / count)) if count else 0


def pcm16_to_mono(frames, channels):
    if channels == 1:
        return frames
    if channels != 2:
        raise ValueError("only mono or stereo PCM16 is supported")
    output = bytearray()
    for i in range(0, len(frames) - 3, 4):
        left = struct.unpack_from("<h", frames, i)[0]
        right = struct.unpack_from("<h", frames, i + 2)[0]
        mixed = int((left + right) / 2)
        output.extend(struct.pack("<h", mixed))
    return bytes(output)


def dbfs_from_rms(rms, max_value=32768):
    if rms <= 0:
        return float("-inf")
    return 20 * math.log10(float(rms) / max_value)


if __name__ == "__main__":
    print("[TEST] wav_tools")

    try:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "a.wav")
            frames = pcm16_silence(0.1, sample_rate=8000)
            write_wav(path, frames, sample_rate=8000)
            info = wav_info(path)
            assert info["sample_rate"] == 8000
            assert round(wav_duration(path), 1) == 0.1
            params, loaded = read_wav_frames(path)
            assert params.framerate == 8000
            assert loaded == frames
            assert pcm16_peak(frames) == 0
            assert pcm16_rms(frames) == 0
            assert dbfs_from_rms(0) == float("-inf")
            assert pcm16_to_mono(frames, 1) == frames
            assert len(split_wav(path, os.path.join(tmp, "chunks"), 0.05)) == 2
            print("[OK] wav helpers")
            print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
