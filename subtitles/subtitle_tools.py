"""
Name: Subtitle Tools (no deps)

Why:
- Edge ASR pipelines often need SRT or WebVTT output
- Subtitle conversion should not require media libraries

Features:
- parse SRT
- write SRT
- parse VTT
- write VTT
- shift and merge cues
- plain-text export

Limitations:
- Handles common SRT/VTT files, not every authoring extension
- Does not validate media duration

Usage:
    cues = parse_srt("1\\n00:00:00,000 --> 00:00:01,000\\nhello\\n")
    print(to_vtt(cues))
"""

import re


def parse_timestamp(value):
    text = value.strip().replace(",", ".")
    parts = text.split(":")
    if len(parts) != 3:
        raise ValueError("expected HH:MM:SS.mmm timestamp")
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds


def format_srt_timestamp(seconds):
    milliseconds = int(round(seconds * 1000))
    hours, rest = divmod(milliseconds, 3600000)
    minutes, rest = divmod(rest, 60000)
    secs, millis = divmod(rest, 1000)
    return "%02d:%02d:%02d,%03d" % (hours, minutes, secs, millis)


def format_vtt_timestamp(seconds):
    return format_srt_timestamp(seconds).replace(",", ".")


def make_cue(start, end, text, index=None):
    return {"index": index, "start": float(start), "end": float(end), "text": str(text)}


def parse_srt(text):
    cues = []
    blocks = re.split(r"\n\s*\n", text.strip().replace("\r\n", "\n"))
    for block in blocks:
        lines = [line for line in block.split("\n") if line.strip()]
        if not lines:
            continue

        index = None
        if "-->" not in lines[0]:
            try:
                index = int(lines[0].strip())
            except ValueError:
                index = None
            lines = lines[1:]

        if not lines or "-->" not in lines[0]:
            continue

        start_text, end_text = [part.strip() for part in lines[0].split("-->", 1)]
        cues.append(make_cue(parse_timestamp(start_text), parse_timestamp(end_text), "\n".join(lines[1:]), index))
    return cues


def to_srt(cues):
    blocks = []
    for i, cue in enumerate(cues, 1):
        blocks.append(
            "%d\n%s --> %s\n%s"
            % (
                cue.get("index") or i,
                format_srt_timestamp(cue["start"]),
                format_srt_timestamp(cue["end"]),
                cue["text"],
            )
        )
    return "\n\n".join(blocks) + ("\n" if blocks else "")


def parse_vtt(text):
    text = text.replace("\r\n", "\n").strip()
    if text.startswith("WEBVTT"):
        text = "\n".join(text.split("\n")[1:]).strip()

    cues = []
    for block in re.split(r"\n\s*\n", text):
        lines = [line for line in block.split("\n") if line.strip()]
        if not lines:
            continue
        if "-->" not in lines[0]:
            lines = lines[1:]
        if not lines or "-->" not in lines[0]:
            continue
        start_text, end_text = [part.strip().split()[0] for part in lines[0].split("-->", 1)]
        cues.append(make_cue(parse_timestamp(start_text), parse_timestamp(end_text), "\n".join(lines[1:])))
    return cues


def to_vtt(cues):
    lines = ["WEBVTT", ""]
    for cue in cues:
        lines.append("%s --> %s" % (format_vtt_timestamp(cue["start"]), format_vtt_timestamp(cue["end"])))
        lines.append(cue["text"])
        lines.append("")
    return "\n".join(lines)


def shift_cues(cues, offset):
    return [make_cue(max(0, c["start"] + offset), max(0, c["end"] + offset), c["text"], c.get("index")) for c in cues]


def merge_close_cues(cues, max_gap=0.3):
    merged = []
    for cue in cues:
        if merged and cue["start"] - merged[-1]["end"] <= max_gap:
            merged[-1]["end"] = max(merged[-1]["end"], cue["end"])
            merged[-1]["text"] = (merged[-1]["text"].rstrip() + " " + cue["text"].lstrip()).strip()
        else:
            merged.append(dict(cue))
    return merged


def cues_to_text(cues, separator=" "):
    return separator.join(cue["text"].replace("\n", " ").strip() for cue in cues if cue["text"].strip())


def split_text_to_cues(text, seconds_per_cue=3.0, words_per_cue=8):
    words = str(text).split()
    cues = []
    for i in range(0, len(words), words_per_cue):
        start = (i // words_per_cue) * seconds_per_cue
        cues.append(make_cue(start, start + seconds_per_cue, " ".join(words[i:i + words_per_cue])))
    return cues


if __name__ == "__main__":
    print("[TEST] subtitle_tools")

    try:
        cues = parse_srt("1\n00:00:00,000 --> 00:00:01,500\nhello\n\n")
        assert cues[0]["text"] == "hello"
        assert "00:00:01,500" in to_srt(cues)
        assert parse_vtt(to_vtt(cues))[0]["end"] == 1.5
        assert shift_cues(cues, 1)[0]["start"] == 1
        assert cues_to_text(cues) == "hello"
        assert len(split_text_to_cues("one two three", words_per_cue=2)) == 2
        assert merge_close_cues([make_cue(0, 1, "a"), make_cue(1.1, 2, "b")])[0]["text"] == "a b"
        print("[OK] subtitle helpers")
        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
