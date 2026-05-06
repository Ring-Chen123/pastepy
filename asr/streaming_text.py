"""
Name: Streaming ASR Text Tools (no deps)

Why:
- Streaming ASR returns partial hypotheses that can change before finalization
- Edge apps need lightweight text stabilization and display helpers

Features:
- partial/final result normalization
- stable prefix detection
- partial result merging
- repeated partial suppression
- live caption line wrapping

Limitations:
- Text-only helpers; no ASR engine included
- Stability is heuristic, not model-aware
"""


def normalize_result(result):
    return {
        "text": str(result.get("text", result.get("transcript", ""))).strip(),
        "is_final": bool(result.get("is_final", result.get("final", False))),
        "start": result.get("start"),
        "end": result.get("end"),
        "confidence": result.get("confidence"),
    }


def stable_prefix(previous, current):
    prev_words = str(previous).split()
    cur_words = str(current).split()
    out = []
    for a, b in zip(prev_words, cur_words):
        if a != b:
            break
        out.append(a)
    return " ".join(out)


def unstable_suffix(stable, current):
    stable_words = stable.split()
    current_words = str(current).split()
    return " ".join(current_words[len(stable_words):])


def merge_partial(final_text, partial_text):
    final_text = str(final_text).strip()
    partial_text = str(partial_text).strip()
    if not final_text:
        return partial_text
    if not partial_text:
        return final_text
    stable = stable_prefix(final_text, partial_text)
    if stable == final_text:
        return partial_text
    return (final_text + " " + unstable_suffix(stable, partial_text)).strip()


def apply_stream_result(state, result):
    result = normalize_result(result)
    state = dict(state or {"final": "", "partial": ""})
    if result["is_final"]:
        state["final"] = (state.get("final", "") + " " + result["text"]).strip()
        state["partial"] = ""
    else:
        state["partial"] = result["text"]
    return state


def display_text(state):
    final = state.get("final", "").strip()
    partial = state.get("partial", "").strip()
    return (final + " " + partial).strip()


def suppress_repeated_partial(previous, current):
    return "" if str(previous).strip() == str(current).strip() else str(current).strip()


def partial_changed_enough(previous, current, min_chars=3):
    previous = str(previous)
    current = str(current)
    return abs(len(current) - len(previous)) >= min_chars or stable_prefix(previous, current) != previous


def wrap_caption(text, max_chars=42):
    lines = []
    current = ""
    for word in str(text).split():
        candidate = (current + " " + word).strip()
        if current and len(candidate) > max_chars:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def trim_context(text, max_words=40):
    words = str(text).split()
    return " ".join(words[-max_words:])


def finalize_state(state):
    text = display_text(state)
    return {"final": text, "partial": ""}


if __name__ == "__main__":
    print("[TEST] streaming_text")
    try:
        assert normalize_result({"transcript": " hi ", "final": True})["is_final"]
        assert stable_prefix("hello world", "hello there") == "hello"
        assert unstable_suffix("hello", "hello there") == "there"
        assert merge_partial("hello", "hello world") == "hello world"
        state = apply_stream_result({}, {"text": "hello"})
        assert display_text(state) == "hello"
        state = apply_stream_result(state, {"text": "world", "is_final": True})
        assert state["final"] == "world"
        assert suppress_repeated_partial("a", "a") == ""
        assert partial_changed_enough("abc", "abcdef")
        assert wrap_caption("one two three", 7) == ["one two", "three"]
        assert trim_context("a b c", 2) == "b c"
        assert finalize_state({"final": "a", "partial": "b"}) == {"final": "a b", "partial": ""}
        print("[OK] streaming text helpers")
        print("[DONE]")
    except Exception as e:
        print("[FAIL]", e)
