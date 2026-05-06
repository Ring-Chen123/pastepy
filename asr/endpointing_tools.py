"""
Name: ASR Endpointing Tools (no deps)

Why:
- Streaming ASR depends on pause detection and turn boundaries
- Small edge apps need predictable endpoint heuristics

Features:
- speech state transitions
- silence counters
- end-of-utterance detection
- pre-roll and post-roll sample calculations

Limitations:
- Uses boolean speech frames or simple RMS values
- Not a neural endpointing model
"""


def frame_ms_to_samples(sample_rate, frame_ms):
    return int(sample_rate * frame_ms / 1000)


def samples_to_ms(samples, sample_rate):
    return samples / float(sample_rate) * 1000


def silence_frames_needed(silence_ms, frame_ms):
    return max(1, int(round(float(silence_ms) / frame_ms)))


def speech_frames_needed(speech_ms, frame_ms):
    return max(1, int(round(float(speech_ms) / frame_ms)))


def is_speech_rms(rms, threshold):
    return rms >= threshold


def speech_state(previous_state, is_speech):
    if is_speech and previous_state in ("idle", "pause"):
        return "speech_start"
    if is_speech:
        return "speech_resume" if previous_state == "speech_end" else "speech"
    if previous_state == "speech":
        return "speech_pause"
    return "idle"


def endpoint_detected(flags, min_silence_frames=5):
    count = 0
    seen_speech = False
    for flag in flags:
        if flag:
            seen_speech = True
            count = 0
        elif seen_speech:
            count += 1
            if count >= min_silence_frames:
                return True
    return False


def split_on_endpoints(flags, min_silence_frames=5):
    segments = []
    start = None
    silence = 0
    for i, flag in enumerate(flags):
        if flag:
            if start is None:
                start = i
            silence = 0
        elif start is not None:
            silence += 1
            if silence >= min_silence_frames:
                segments.append((start, i - silence + 1))
                start = None
                silence = 0
    if start is not None:
        segments.append((start, len(flags)))
    return segments


def preroll_frames(pre_ms, frame_ms):
    return max(0, int(round(float(pre_ms) / frame_ms)))


def postroll_frames(post_ms, frame_ms):
    return max(0, int(round(float(post_ms) / frame_ms)))


def should_flush_partial(last_update_time, now, max_age_seconds):
    return now - last_update_time >= max_age_seconds


if __name__ == "__main__":
    print("[TEST] endpointing_tools")
    try:
        assert frame_ms_to_samples(16000, 10) == 160
        assert samples_to_ms(160, 16000) == 10
        assert silence_frames_needed(100, 20) == 5
        assert speech_frames_needed(60, 20) == 3
        assert is_speech_rms(10, 5)
        assert speech_state("idle", True) == "speech_start"
        assert endpoint_detected([True, False, False], 2)
        assert split_on_endpoints([True, True, False, False, True], 2) == [(0, 2), (4, 5)]
        assert preroll_frames(100, 20) == 5
        assert postroll_frames(40, 20) == 2
        assert should_flush_partial(1, 3, 2)
        print("[OK] endpoint helpers")
        print("[DONE]")
    except Exception as e:
        print("[FAIL]", e)
