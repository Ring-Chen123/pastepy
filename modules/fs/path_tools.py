"""
Name: Path Tools (no deps)

Why:
- File scripts need common safe path operations
- Keep tiny filesystem tasks easy to read

Features:
- ensure directory
- read and write text
- touch files
- list files
- size helper
- remove empty directories

Limitations:
- No glob DSL
- No atomic writes; use atomic_file.py for that

Usage:
    ensure_dir("out")
    write_text("out/readme.txt", "hello")
"""

import os


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


def read_text(path, encoding="utf-8"):
    with open(path, "r", encoding=encoding) as f:
        return f.read()


def write_text(path, text, encoding="utf-8"):
    directory = os.path.dirname(os.path.abspath(path))
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding=encoding) as f:
        f.write(text)


def touch(path):
    directory = os.path.dirname(os.path.abspath(path))
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "a", encoding="utf-8"):
        os.utime(path, None)


def list_files(root, suffix=None):
    found = []
    for current, _, files in os.walk(root):
        for name in files:
            if suffix is None or name.endswith(suffix):
                found.append(os.path.join(current, name))
    return found


def file_size(path):
    return os.path.getsize(path)


def remove_empty_dirs(root):
    removed = []
    for current, dirs, _ in os.walk(root, topdown=False):
        for name in dirs:
            path = os.path.join(current, name)
            try:
                os.rmdir(path)
                removed.append(path)
            except OSError:
                pass
    return removed


if __name__ == "__main__":
    print("[TEST] path_tools")

    try:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            nested = ensure_dir(os.path.join(tmp, "a", "b"))
            path = os.path.join(nested, "x.txt")
            write_text(path, "hello")
            assert read_text(path) == "hello"
            assert file_size(path) == 5
            assert list_files(tmp, ".txt") == [path]
            touch(os.path.join(tmp, "touch.txt"))
            empty = os.path.join(tmp, "empty")
            ensure_dir(empty)
            assert empty in remove_empty_dirs(tmp)
            print("[OK] path helpers")

        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
