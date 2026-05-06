"""
Name: JSON Store (no deps)

Why:
- Small tools often need durable state without a database
- JSON is easy to inspect, edit, copy, and back up

Features:
- Load JSON with a default value
- Save JSON atomically with os.replace
- UTF-8 text

Limitations:
- Best for small files
- No schema validation
- No locking or concurrent write protection

Usage:
    data = load_json("state.json", default={})
    data["runs"] = data.get("runs", 0) + 1
    save_json("state.json", data)
"""

import json
import os
import tempfile


def load_json(path, default=None):
    if not os.path.exists(path):
        return default

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data, indent=2):
    directory = os.path.dirname(os.path.abspath(path))
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=directory, delete=False
        ) as f:
            temp_path = f.name
            json.dump(data, f, indent=indent, ensure_ascii=False, sort_keys=True)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_path, path)

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    print("[TEST] json_store")

    try:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "state", "data.json")

            assert load_json(path, default={}) == {}
            print("[OK] missing default")

            save_json(path, {"runs": 1, "name": "pastepy"})
            loaded = load_json(path)
            assert loaded == {"name": "pastepy", "runs": 1}
            print("[OK] save/load")

        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
