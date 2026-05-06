"""
Name: ZIP Tools (no deps)

Why:
- ZIP files are common for moving logs, configs, and small datasets
- zipfile is standard but common operations are repetitive

Features:
- zip a directory
- unzip an archive
- list archive names
- add one file
- ZIP detection

Limitations:
- ZIP only
- No encryption support

Usage:
    zip_dir("logs", "logs.zip")
"""

import os
import zipfile


def zip_dir(source_dir, zip_path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(source_dir):
            for name in files:
                path = os.path.join(root, name)
                arcname = os.path.relpath(path, source_dir)
                z.write(path, arcname)


def unzip(zip_path, target_dir):
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(target_dir)


def list_zip(zip_path):
    with zipfile.ZipFile(zip_path, "r") as z:
        return z.namelist()


def add_file(zip_path, file_path, arcname=None):
    with zipfile.ZipFile(zip_path, "a", zipfile.ZIP_DEFLATED) as z:
        z.write(file_path, arcname or os.path.basename(file_path))


def is_zip(path):
    return zipfile.is_zipfile(path)


if __name__ == "__main__":
    print("[TEST] zip_tools")

    try:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "src")
            out = os.path.join(tmp, "out")
            os.makedirs(src)
            with open(os.path.join(src, "a.txt"), "w", encoding="utf-8") as f:
                f.write("a")

            zip_path = os.path.join(tmp, "x.zip")
            zip_dir(src, zip_path)
            assert is_zip(zip_path) is True
            assert list_zip(zip_path) == ["a.txt"]
            unzip(zip_path, out)
            assert os.path.exists(os.path.join(out, "a.txt"))

            extra = os.path.join(tmp, "b.txt")
            with open(extra, "w", encoding="utf-8") as f:
                f.write("b")
            add_file(zip_path, extra)
            assert "b.txt" in list_zip(zip_path)
            print("[OK] zip helpers")

        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
