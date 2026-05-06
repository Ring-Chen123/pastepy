"""
Name: Simple File Lock (no deps)

Why:
- Small scripts sometimes need a basic cross-process lock
- Lock files work in restricted environments without extra services

Features:
- Exclusive lock using atomic file creation
- Timeout support
- Context manager API

Limitations:
- Stale lock files must be cleaned up by the caller
- Not intended for high-contention workloads
- Works only when all processes agree to use the same lock file

Usage:
    with FileLock("job.lock", timeout=5):
        print("only one process runs this block")
"""

import os
import time


class FileLock:
    def __init__(self, path, timeout=10, poll_interval=0.05):
        if timeout is not None and timeout < 0:
            raise ValueError("timeout must be None or non-negative")
        if poll_interval <= 0:
            raise ValueError("poll_interval must be greater than 0")

        self.path = path
        self.timeout = timeout
        self.poll_interval = poll_interval
        self._fd = None

    def acquire(self):
        start = time.monotonic()

        while True:
            try:
                self._fd = os.open(
                    self.path,
                    os.O_CREAT | os.O_EXCL | os.O_RDWR,
                )
                os.write(self._fd, str(os.getpid()).encode("ascii"))
                return True

            except FileExistsError:
                if self.timeout is not None:
                    elapsed = time.monotonic() - start
                    if elapsed >= self.timeout:
                        raise TimeoutError("could not acquire lock: " + self.path)

                time.sleep(self.poll_interval)

    def release(self):
        if self._fd is None:
            return

        os.close(self._fd)
        self._fd = None

        try:
            os.remove(self.path)
        except FileNotFoundError:
            pass

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.release()


if __name__ == "__main__":
    print("[TEST] file_lock")

    try:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "job.lock")

            with FileLock(path, timeout=0.1):
                assert os.path.exists(path)

                try:
                    FileLock(path, timeout=0.05).acquire()
                    raise AssertionError("second lock should fail")
                except TimeoutError:
                    pass

            assert not os.path.exists(path)
            print("[OK] acquire/release")

        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
