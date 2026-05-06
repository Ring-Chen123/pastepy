"""
Name: JSONL Tools (no deps)

Why:
- Edge AI data capture often stores records as newline-delimited JSON
- JSONL is easy to append, stream, inspect, and upload later

Features:
- read JSONL
- write JSONL
- append record
- filter records
- count records
- split JSONL

Limitations:
- No schema validation
- split_jsonl writes full records only

Usage:
    append_jsonl("events.jsonl", {"text": "hello"})
"""

import json
import os


def read_jsonl(path):
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def iter_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def append_jsonl(path, record):
    directory = os.path.dirname(os.path.abspath(path))
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def count_jsonl(path):
    return sum(1 for _ in iter_jsonl(path))


def filter_jsonl(input_path, output_path, predicate):
    kept = []
    for record in iter_jsonl(input_path):
        if predicate(record):
            kept.append(record)
    write_jsonl(output_path, kept)
    return len(kept)


def split_jsonl(path, output_dir, records_per_file):
    if records_per_file < 1:
        raise ValueError("records_per_file must be at least 1")
    os.makedirs(output_dir, exist_ok=True)
    outputs = []
    batch = []
    index = 0
    for record in iter_jsonl(path):
        batch.append(record)
        if len(batch) == records_per_file:
            out = os.path.join(output_dir, "part_%04d.jsonl" % index)
            write_jsonl(out, batch)
            outputs.append(out)
            batch = []
            index += 1
    if batch:
        out = os.path.join(output_dir, "part_%04d.jsonl" % index)
        write_jsonl(out, batch)
        outputs.append(out)
    return outputs


if __name__ == "__main__":
    print("[TEST] jsonl_tools")

    try:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "data.jsonl")
            append_jsonl(path, {"id": 1})
            append_jsonl(path, {"id": 2})
            assert count_jsonl(path) == 2
            assert read_jsonl(path)[0]["id"] == 1
            out = os.path.join(tmp, "filtered.jsonl")
            assert filter_jsonl(path, out, lambda r: r["id"] == 2) == 1
            assert read_jsonl(out) == [{"id": 2}]
            parts = split_jsonl(path, os.path.join(tmp, "parts"), 1)
            assert len(parts) == 2
            write_jsonl(path, [{"id": 3}])
            assert list(iter_jsonl(path)) == [{"id": 3}]
            print("[OK] jsonl helpers")
            print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
