"""
Name: Sensor Tools (no deps)

Why:
- Edge AI often combines model output with device sensor streams
- CSV-based sensor logs should be easy to inspect and downsample

Features:
- CSV read/write
- timestamp normalization
- gap detection
- rolling windows
- unit conversion
- outlier detection
"""

import csv
import datetime


def parse_time(value):
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.datetime.fromisoformat(text).timestamp()
    except ValueError:
        return float(text)


def read_sensor_csv(path):
    with open(path, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_sensor_csv(path, rows, fieldnames):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def normalize_timestamps(rows, field="time", output="timestamp"):
    result = []
    for row in rows:
        item = dict(row)
        item[output] = parse_time(row[field])
        result.append(item)
    return result


def detect_gaps(rows, timestamp="timestamp", max_gap=1.0):
    gaps = []
    ordered = sorted(rows, key=lambda r: r[timestamp])
    for prev, current in zip(ordered, ordered[1:]):
        gap = current[timestamp] - prev[timestamp]
        if gap > max_gap:
            gaps.append({"start": prev[timestamp], "end": current[timestamp], "gap": gap})
    return gaps


def rolling_windows(rows, size):
    if size < 1:
        raise ValueError("size must be at least 1")
    for i in range(0, max(0, len(rows) - size + 1)):
        yield rows[i:i + size]


def convert_units(value, factor=1.0, offset=0.0):
    return float(value) * factor + offset


def apply_calibration(rows, field, factor=1.0, offset=0.0, output=None):
    output = output or field
    result = []
    for row in rows:
        item = dict(row)
        item[output] = convert_units(row[field], factor, offset)
        result.append(item)
    return result


def detect_outliers(values, z=3.0):
    values = [float(v) for v in values]
    if not values:
        return []
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    std = variance ** 0.5
    if std == 0:
        return []
    return [i for i, value in enumerate(values) if abs((value - mean) / std) > z]


def downsample(rows, step):
    if step < 1:
        raise ValueError("step must be at least 1")
    return rows[::step]


def moving_average(values, size):
    return [sum(window) / size for window in rolling_windows([float(v) for v in values], size)]


def minmax(values):
    values = [float(v) for v in values]
    return {"min": min(values), "max": max(values)} if values else {"min": None, "max": None}


def summary(values):
    values = [float(v) for v in values]
    if not values:
        return {"count": 0, "min": None, "max": None, "mean": None}
    return {"count": len(values), "min": min(values), "max": max(values), "mean": sum(values) / len(values)}


def resample_nearest(rows, timestamps, timestamp="timestamp"):
    ordered = sorted(rows, key=lambda r: r[timestamp])
    result = []
    for target in timestamps:
        result.append(min(ordered, key=lambda row: abs(row[timestamp] - target)))
    return result


def latest_value(rows, field, timestamp="timestamp"):
    if not rows:
        return None
    return max(rows, key=lambda row: row[timestamp]).get(field)


if __name__ == "__main__":
    print("[TEST] sensor_tools")
    try:
        rows = normalize_timestamps([{"time": "0", "v": "1"}, {"time": "2", "v": "5"}])
        assert detect_gaps(rows, max_gap=1)
        assert len(list(rolling_windows(rows, 2))) == 1
        assert convert_units(1, 2, 3) == 5
        assert apply_calibration(rows, "v", 2)[0]["v"] == 2
        assert detect_outliers([1, 1, 1, 10], z=1)
        assert downsample([1, 2, 3], 2) == [1, 3]
        assert moving_average([1, 3, 5], 2) == [2, 4]
        assert minmax([2, 3]) == {"min": 2, "max": 3}
        assert summary([2, 4])["mean"] == 3
        assert resample_nearest(rows, [1])[0]["v"] in ("1", "5")
        assert latest_value(rows, "v") == "5"
        print("[OK] sensor helpers")
        print("[DONE]")
    except Exception as e:
        print("[FAIL]", e)
