"""
Name: Device Ops (no deps)

Why:
- Edge deployments need small reliability files and local diagnostics
- These helpers avoid requiring a service manager or agent SDK

Features:
- PID and heartbeat files
- uptime and boot markers
- crash and last-good-state markers
- feature flags and rollout buckets
- diagnostic bundle creation
"""

import hashlib
import ctypes
import json
import os
import socket
import time
import zipfile


def write_pid(path, pid=None):
    pid = pid or os.getpid()
    with open(path, "w", encoding="ascii") as f:
        f.write(str(pid))
    return pid


def read_pid(path):
    with open(path, "r", encoding="ascii") as f:
        return int(f.read().strip())


def is_process_alive(pid):
    if pid <= 0:
        return False
    if os.name == "nt":
        handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))
        if handle:
            ctypes.windll.kernel32.CloseHandle(handle)
            return True
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def write_heartbeat(path, timestamp=None):
    timestamp = timestamp if timestamp is not None else time.time()
    with open(path, "w", encoding="ascii") as f:
        f.write(str(timestamp))
    return timestamp


def read_heartbeat(path):
    with open(path, "r", encoding="ascii") as f:
        return float(f.read().strip())


def heartbeat_stale(path, max_age):
    return time.time() - read_heartbeat(path) > max_age


def uptime_since(start_timestamp):
    return time.time() - start_timestamp


def write_json_marker(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")


def read_json_marker(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def device_id(path, fallback=None):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    value = fallback or socket.gethostname()
    with open(path, "w", encoding="utf-8") as f:
        f.write(value)
    return value


def local_hostname():
    return socket.gethostname()


def config_diff(old, new):
    keys = set(old) | set(new)
    return {key: {"old": old.get(key), "new": new.get(key)} for key in keys if old.get(key) != new.get(key)}


def merge_config(base, override):
    result = dict(base)
    result.update({k: v for k, v in override.items() if v is not None})
    return result


def feature_enabled(flags, name, default=False):
    return bool(flags.get(name, default))


def rollout_enabled(device_id_value, percent):
    value = int(hashlib.sha256(str(device_id_value).encode("utf-8")).hexdigest()[:8], 16) % 100
    return value < percent


def low_disk(path, min_free_bytes):
    stat = os.statvfs(path) if hasattr(os, "statvfs") else None
    if stat:
        return stat.f_bavail * stat.f_frsize < min_free_bytes
    import shutil
    return shutil.disk_usage(path).free < min_free_bytes


def write_crash_marker(path, error):
    data = {"time": time.time(), "error": str(error)}
    write_json_marker(path, data)
    return data


def write_last_good(path, state):
    data = {"time": time.time(), "state": state}
    write_json_marker(path, data)
    return data


def make_diagnostic_bundle(output_zip, files):
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for path in files:
            if os.path.exists(path):
                z.write(path, os.path.basename(path))
    return output_zip


if __name__ == "__main__":
    print("[TEST] device_ops")
    try:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            pid_path = os.path.join(tmp, "app.pid")
            written_pid = write_pid(pid_path)
            assert read_pid(pid_path) == written_pid
            assert is_process_alive(os.getpid())
            hb = os.path.join(tmp, "hb")
            write_heartbeat(hb, time.time() - 10)
            assert heartbeat_stale(hb, 1)
            assert uptime_since(time.time()) <= 1
            marker = os.path.join(tmp, "m.json")
            write_json_marker(marker, {"a": 1})
            assert read_json_marker(marker)["a"] == 1
            assert device_id(os.path.join(tmp, "id"), fallback="dev") == "dev"
            assert local_hostname()
            assert config_diff({"a": 1}, {"a": 2})["a"]["new"] == 2
            assert merge_config({"a": 1}, {"b": 2})["b"] == 2
            assert feature_enabled({"x": True}, "x")
            assert isinstance(rollout_enabled("dev", 10), bool)
            assert isinstance(low_disk(tmp, 10**18), bool)
            assert write_crash_marker(os.path.join(tmp, "crash.json"), "x")["error"] == "x"
            assert write_last_good(os.path.join(tmp, "good.json"), "ok")["state"] == "ok"
            assert make_diagnostic_bundle(os.path.join(tmp, "d.zip"), [marker])
            print("[OK] device ops helpers")
            print("[DONE]")
    except Exception as e:
        print("[FAIL]", e)
