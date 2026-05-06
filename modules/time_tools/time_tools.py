"""
Name: Time Tools (no deps)

Why:
- Operational scripts often need small timing helpers
- Keep timestamps, durations, and sleeps consistent

Features:
- stopwatch
- ISO timestamp
- Unix milliseconds
- duration formatting
- simple duration parsing
- sleep until timestamp

Limitations:
- Duration parser supports s, m, h, and d suffixes only
- Uses local time for ISO output by default

Usage:
    sw = Stopwatch()
    print(sw.elapsed())
"""

import datetime
import time


class Stopwatch:
    def __init__(self):
        self.start = time.monotonic()

    def elapsed(self):
        return time.monotonic() - self.start

    def reset(self):
        value = self.elapsed()
        self.start = time.monotonic()
        return value


def now_iso(utc=False):
    if utc:
        return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    return datetime.datetime.now().replace(microsecond=0).isoformat()


def unix_ms():
    return int(time.time() * 1000)


def format_duration(seconds):
    seconds = int(seconds)
    minutes, sec = divmod(seconds, 60)
    hours, minute = divmod(minutes, 60)
    if hours:
        return "%dh%02dm%02ds" % (hours, minute, sec)
    if minute:
        return "%dm%02ds" % (minute, sec)
    return "%ds" % sec


def parse_duration(value):
    text = str(value).strip().lower()
    units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    if text[-1:] in units:
        return float(text[:-1]) * units[text[-1]]
    return float(text)


def sleep_until(timestamp):
    delay = timestamp - time.time()
    if delay > 0:
        time.sleep(delay)


if __name__ == "__main__":
    print("[TEST] time_tools")

    try:
        sw = Stopwatch()
        assert sw.elapsed() >= 0
        assert sw.reset() >= 0
        assert "T" in now_iso()
        assert isinstance(unix_ms(), int)
        assert format_duration(3661) == "1h01m01s"
        assert parse_duration("2m") == 120
        sleep_until(time.time() - 1)
        print("[OK] time helpers")
        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
