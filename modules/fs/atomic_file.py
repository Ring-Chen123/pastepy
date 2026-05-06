"""
Name: Atomic File Write (no deps)

Why:
- Interrupted writes can leave config or state files corrupted
- Writing to a temporary file first is safer for small files

Features:
- Atomic text writes with os.replace
- Atomic bytes writes
- Creates the target directory when needed

Limitations:
- Best suited for small files
- Atomicity depends on source and target being on the same filesystem
- Does not lock against concurrent writers

Usage:
    atomic_write_text("state.txt", "ready\\n")
    atomic_write_bytes("state.bin", b"ready")
"""

import os
import tempfile


def _target_dir(path):
    directory = os.path.dirname(os.path.abspath(path))
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def _atomic_write(path, data, mode, encoding=None):
    directory = _target_dir(path)
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode, encoding=encoding, dir=directory, delete=False
        ) as f:
            temp_path = f.name
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_path, path)

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def atomic_write_text(path, text, encoding="utf-8"):
    _atomic_write(path, text, "w", encoding=encoding)


def atomic_write_bytes(path, data):
    _atomic_write(path, data, "wb")


if __name__ == "__main__":
    print("[TEST] atomic_file")

    try:
        with tempfile.TemporaryDirectory() as tmp:
            text_path = os.path.join(tmp, "nested", "state.txt")
            atomic_write_text(text_path, "hello")
            with open(text_path, "r", encoding="utf-8") as f:
                assert f.read() == "hello"
            print("[OK] text")

            bytes_path = os.path.join(tmp, "state.bin")
            atomic_write_bytes(bytes_path, b"abc")
            with open(bytes_path, "rb") as f:
                assert f.read() == b"abc"
            print("[OK] bytes")

        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
