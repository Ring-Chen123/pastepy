"""
Name: Simple Logger (no deps)

Why:
- Small scripts need readable logs without configuration ceremony
- Standard logging is powerful, but sometimes too much for copy-paste scripts

Features:
- timestamped log lines
- level filtering
- stderr by default
- JSON-line helper

Limitations:
- No log rotation
- No handlers or format configuration

Usage:
    logger = Logger(level="INFO")
    logger.info("started")
"""

import json
import sys
import time


LEVELS = {"DEBUG": 10, "INFO": 20, "WARN": 30, "ERROR": 40}


class Logger:
    def __init__(self, level="INFO", stream=None):
        self.level = LEVELS.get(level.upper(), 20)
        self.stream = stream if stream is not None else sys.stderr

    def _enabled(self, level):
        return LEVELS[level] >= self.level

    def log(self, level, message):
        level = level.upper()
        if not self._enabled(level):
            return
        stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print("%s [%s] %s" % (stamp, level, message), file=self.stream)

    def debug(self, message):
        self.log("DEBUG", message)

    def info(self, message):
        self.log("INFO", message)

    def warn(self, message):
        self.log("WARN", message)

    def error(self, message):
        self.log("ERROR", message)

    def json(self, level, **fields):
        level = level.upper()
        if not self._enabled(level):
            return
        fields["level"] = level
        fields["time"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        print(json.dumps(fields, sort_keys=True), file=self.stream)


def make_logger(level="INFO", stream=None):
    return Logger(level=level, stream=stream)


if __name__ == "__main__":
    print("[TEST] simple_logger")

    try:
        import io

        stream = io.StringIO()
        logger = Logger(level="INFO", stream=stream)
        logger.debug("hidden")
        logger.info("shown")
        logger.json("ERROR", event="failed")
        output = stream.getvalue()
        assert "hidden" not in output
        assert "[INFO] shown" in output
        assert '"event": "failed"' in output
        assert isinstance(make_logger(), Logger)
        print("[OK] logging")
        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
