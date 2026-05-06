"""
Name: CSV Rows (no deps)

Why:
- CSV remains common for logs, exports, and device data
- Small wrappers make common read/write tasks less repetitive

Features:
- list rows
- dict rows
- append one row
- header detection

Limitations:
- Loads rows into memory
- No schema validation

Usage:
    write_dicts("out.csv", [{"name": "ada"}], ["name"])
    print(read_dicts("out.csv"))
"""

import csv


def read_rows(path, encoding="utf-8"):
    with open(path, "r", newline="", encoding=encoding) as f:
        return list(csv.reader(f))


def write_rows(path, rows, encoding="utf-8"):
    with open(path, "w", newline="", encoding=encoding) as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def append_row(path, row, encoding="utf-8"):
    with open(path, "a", newline="", encoding=encoding) as f:
        csv.writer(f).writerow(row)


def read_dicts(path, encoding="utf-8"):
    with open(path, "r", newline="", encoding=encoding) as f:
        return list(csv.DictReader(f))


def write_dicts(path, rows, fieldnames, encoding="utf-8"):
    with open(path, "w", newline="", encoding=encoding) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def has_header(path, sample_size=2048, encoding="utf-8"):
    with open(path, "r", newline="", encoding=encoding) as f:
        sample = f.read(sample_size)
    return csv.Sniffer().has_header(sample) if sample else False


if __name__ == "__main__":
    print("[TEST] csv_rows")

    try:
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "data.csv")
            write_rows(path, [["name", "age"], ["ada", "36"]])
            append_row(path, ["grace", "85"])
            assert read_rows(path) == [["name", "age"], ["ada", "36"], ["grace", "85"]]
            assert has_header(path) is True

            dict_path = os.path.join(tmp, "dict.csv")
            write_dicts(dict_path, [{"name": "ada"}], ["name"])
            assert read_dicts(dict_path) == [{"name": "ada"}]
            print("[OK] csv helpers")

        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
