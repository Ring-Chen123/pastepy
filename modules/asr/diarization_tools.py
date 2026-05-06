"""
Name: Diarization Text Tools (no deps)

Why:
- Streaming ASR may return speaker tags with words or segments
- Edge apps often need simple speaker turns and labels

Features:
- speaker turn grouping
- speaker label formatting
- overlap detection
- per-speaker word counts

Limitations:
- Does not perform speaker embedding or clustering
- Operates on existing speaker tags
"""


def normalize_word(word):
    return {
        "word": str(word.get("word", word.get("text", ""))),
        "start": float(word.get("start", 0)),
        "end": float(word.get("end", word.get("start", 0))),
        "speaker": word.get("speaker", word.get("speaker_tag", "SPEAKER_0")),
    }


def words_to_speaker_turns(words):
    turns = []
    current = None
    for raw in words:
        word = normalize_word(raw)
        if current is None or current["speaker"] != word["speaker"]:
            current = {"speaker": word["speaker"], "start": word["start"], "end": word["end"], "text": word["word"]}
            turns.append(current)
        else:
            current["end"] = word["end"]
            current["text"] = (current["text"] + " " + word["word"]).strip()
    return turns


def format_speaker_turn(turn):
    return "%s: %s" % (turn["speaker"], turn["text"])


def format_transcript_by_speaker(turns):
    return "\n".join(format_speaker_turn(turn) for turn in turns)


def speaker_word_counts(words):
    counts = {}
    for raw in words:
        word = normalize_word(raw)
        counts[word["speaker"]] = counts.get(word["speaker"], 0) + 1
    return counts


def speaker_durations(turns):
    durations = {}
    for turn in turns:
        durations[turn["speaker"]] = durations.get(turn["speaker"], 0) + max(0, turn["end"] - turn["start"])
    return durations


def relabel_speakers(items, mapping):
    output = []
    for item in items:
        item = dict(item)
        if "speaker" in item:
            item["speaker"] = mapping.get(item["speaker"], item["speaker"])
        elif "speaker_tag" in item:
            item["speaker_tag"] = mapping.get(item["speaker_tag"], item["speaker_tag"])
        output.append(item)
    return output


def detect_overlaps(turns):
    overlaps = []
    ordered = sorted(turns, key=lambda t: t["start"])
    for a, b in zip(ordered, ordered[1:]):
        if b["start"] < a["end"]:
            overlaps.append((a, b))
    return overlaps


def merge_short_turns(turns, min_duration=0.5):
    merged = []
    for turn in turns:
        if merged and turn["end"] - turn["start"] < min_duration:
            merged[-1]["end"] = max(merged[-1]["end"], turn["end"])
            merged[-1]["text"] = (merged[-1]["text"] + " " + turn["text"]).strip()
        else:
            merged.append(dict(turn))
    return merged


def active_speaker_at(turns, timestamp):
    for turn in turns:
        if turn["start"] <= timestamp <= turn["end"]:
            return turn["speaker"]
    return None


if __name__ == "__main__":
    print("[TEST] diarization_tools")
    try:
        words = [{"word": "hi", "start": 0, "end": 1, "speaker": "A"}, {"word": "yo", "start": 1, "end": 2, "speaker": "A"}]
        turns = words_to_speaker_turns(words)
        assert turns[0]["text"] == "hi yo"
        assert format_speaker_turn(turns[0]) == "A: hi yo"
        assert format_transcript_by_speaker(turns) == "A: hi yo"
        assert speaker_word_counts(words) == {"A": 2}
        assert speaker_durations(turns) == {"A": 2}
        assert relabel_speakers(words, {"A": "Agent"})[0]["speaker"] == "Agent"
        assert detect_overlaps([{"start": 0, "end": 2}, {"start": 1, "end": 3}])
        assert merge_short_turns([{"speaker": "A", "start": 0, "end": 1, "text": "a"}, {"speaker": "B", "start": 1, "end": 1.1, "text": "b"}])[0]["text"] == "a b"
        assert active_speaker_at(turns, 1) == "A"
        print("[OK] diarization helpers")
        print("[DONE]")
    except Exception as e:
        print("[FAIL]", e)
