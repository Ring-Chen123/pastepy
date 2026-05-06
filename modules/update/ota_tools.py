"""
Name: OTA Tools (no deps)

Why:
- Edge devices need small update manifests and rollback markers
- OTA workflows benefit from explicit local state files

Features:
- OTA manifest read/write
- version checks
- staged install and rollback markers
- readiness checks
"""

import json
import os
import time


def read_ota_manifest(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_ota_manifest(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")


def parse_version(version):
    return tuple(int(part) for part in str(version).split(".") if part.isdigit())


def ota_is_newer(manifest, current_version):
    return parse_version(manifest.get("version", "0")) > parse_version(current_version)


def mark_staged(path, version):
    data = {"version": version, "staged_at": time.time()}
    write_ota_manifest(path, data)
    return data


def mark_rollback(path, version, reason):
    data = {"version": version, "reason": reason, "rollback_at": time.time()}
    write_ota_manifest(path, data)
    return data


def update_locked(path):
    return os.path.exists(path)


def create_update_lock(path):
    with open(path, "w", encoding="ascii") as f:
        f.write(str(os.getpid()))


def clear_update_lock(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def update_ready(manifest, current_version, lock_path=None):
    if lock_path and update_locked(lock_path):
        return False
    return ota_is_newer(manifest, current_version)


if __name__ == "__main__":
    print("[TEST] ota_tools")
    try:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            manifest = {"version": "1.1.0"}
            assert ota_is_newer(manifest, "1.0.0")
            path = os.path.join(tmp, "ota.json")
            write_ota_manifest(path, manifest)
            assert read_ota_manifest(path)["version"] == "1.1.0"
            assert mark_staged(os.path.join(tmp, "staged.json"), "1")["version"] == "1"
            assert mark_rollback(os.path.join(tmp, "rollback.json"), "1", "fail")["reason"] == "fail"
            lock = os.path.join(tmp, "lock")
            assert update_ready(manifest, "1.0.0", lock)
            create_update_lock(lock)
            assert update_locked(lock)
            assert not update_ready(manifest, "1.0.0", lock)
            clear_update_lock(lock)
            assert not update_locked(lock)
            print("[OK] ota helpers")
            print("[DONE]")
    except Exception as e:
        print("[FAIL]", e)
