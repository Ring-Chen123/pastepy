"""
Name: Transcript Tools (no deps)

Why:
- ASR output usually needs cleanup before display or indexing
- These helpers work on plain segments from common ASR systems

Features:
- normalize segment dictionaries
- join transcript text
- timestamp words
- segment by character budget
- remove filler words
- compute words per minute

Limitations:
- Text cleanup is language-agnostic and simple
- No punctuation restoration model

Usage:
    text = transcript_text([{"text": " hello "}])
"""

import re


def normalize_segment(segment):
    return {
        "start": float(segment.get("start", 0)),
        "end": float(segment.get("end", segment.get("start", 0))),
        "text": str(segment.get("text", "")).strip(),
    }


def normalize_segments(segments):
    return [normalize_segment(segment) for segment in segments]


def transcript_text(segments, separator=" "):
    return separator.join(segment.get("text", "").strip() for segment in segments if segment.get("text", "").strip())


def clean_asr_text(text):
    text = re.sub(r"\s+", " ", str(text)).strip()
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    return text


def remove_fillers(text, fillers=None):
    fillers = fillers or ["um", "uh", "erm", "ah"]
    pattern = r"\b(" + "|".join(re.escape(word) for word in fillers) + r")\b"
    return clean_asr_text(re.sub(pattern, "", str(text), flags=re.IGNORECASE))


def words_per_minute(segments):
    segments = normalize_segments(segments)
    if not segments:
        return 0
    duration = max(segment["end"] for segment in segments) - min(segment["start"] for segment in segments)
    if duration <= 0:
        return 0
    words = len(transcript_text(segments).split())
    return words / duration * 60


def segments_to_words(segments):
    words = []
    for segment in normalize_segments(segments):
        parts = segment["text"].split()
        if not parts:
            continue
        step = (segment["end"] - segment["start"]) / len(parts) if segment["end"] > segment["start"] else 0
        for i, word in enumerate(parts):
            words.append({"word": word, "start": segment["start"] + i * step, "end": segment["start"] + (i + 1) * step})
    return words


def chunk_text(text, max_chars=500):
    chunks = []
    current = ""
    for word in str(text).split():
        candidate = (current + " " + word).strip()
        if current and len(candidate) > max_chars:
            chunks.append(current)
            current = word
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def find_keyword_segments(segments, keyword):
    keyword = keyword.lower()
    return [segment for segment in segments if keyword in segment.get("text", "").lower()]


def redact_terms(text, terms, replacement="[REDACTED]"):
    output = str(text)
    for term in terms:
        output = re.sub(re.escape(term), replacement, output, flags=re.IGNORECASE)
    return output


if __name__ == "__main__":
    print("[TEST] transcript_tools")

    try:
        segments = normalize_segments([{"start": 0, "end": 2, "text": " um hello world "}])
        assert transcript_text(segments) == "um hello world"
        assert remove_fillers("um hello") == "hello"
        assert round(words_per_minute(segments)) == 90
        assert len(segments_to_words(segments)) == 3
        assert chunk_text("a b c", max_chars=3) == ["a b", "c"]
        assert find_keyword_segments(segments, "world")
        assert redact_terms("api key", ["key"]) == "api [REDACTED]"
        assert clean_asr_text("hello , world") == "hello, world"
        print("[OK] transcript helpers")
        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
