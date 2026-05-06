"""
Name: Model Manifest Tools (no deps)

Why:
- Edge devices need simple model version, checksum, and rollout metadata
- Manifest files make model deployment auditable without a database

Features:
- read/write manifests
- SHA-256 validation
- version comparison
- compatibility checks
- rollout and canary helpers
"""

import hashlib
import json
import os


def sha256_file(path, chunk_size=1024 * 1024):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def read_manifest(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_manifest(path, manifest):
    directory = os.path.dirname(os.path.abspath(path))
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")


def build_manifest(model_path, name, version, runtime=None, extra=None):
    manifest = {
        "name": name,
        "version": version,
        "sha256": sha256_file(model_path),
        "size": os.path.getsize(model_path),
    }
    if runtime:
        manifest["runtime"] = runtime
    if extra:
        manifest.update(extra)
    return manifest


def validate_model_checksum(model_path, manifest):
    return sha256_file(model_path) == manifest.get("sha256")


def parse_version(version):
    return tuple(int(part) for part in str(version).split(".") if part.isdigit())


def compare_versions(a, b):
    left = parse_version(a)
    right = parse_version(b)
    return (left > right) - (left < right)


def is_newer_version(candidate, current):
    return compare_versions(candidate, current) > 0


def compatibility_check(manifest, runtime=None, machine=None):
    if runtime and manifest.get("runtime") not in (None, runtime):
        return False
    machines = manifest.get("machines")
    if machine and machines and machine not in machines:
        return False
    return True


def rollback_candidate(manifests, current_version):
    older = [m for m in manifests if compare_versions(m.get("version", "0"), current_version) < 0]
    older.sort(key=lambda m: parse_version(m.get("version", "0")), reverse=True)
    return older[0] if older else None


def rollout_bucket(device_id, percent):
    value = int(hashlib.sha256(str(device_id).encode("utf-8")).hexdigest()[:8], 16) % 100
    return value < percent


def ab_variant(device_id, variants=("A", "B")):
    value = int(hashlib.sha256(str(device_id).encode("utf-8")).hexdigest()[:8], 16)
    return variants[value % len(variants)]


def model_record(name, version, path, runtime=None):
    return {"name": name, "version": version, "path": path, "runtime": runtime}


if __name__ == "__main__":
    print("[TEST] manifest_tools")
    try:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            model = os.path.join(tmp, "m.bin")
            with open(model, "wb") as f:
                f.write(b"model")
            manifest = build_manifest(model, "demo", "1.2.0", runtime="onnx")
            assert validate_model_checksum(model, manifest)
            assert compare_versions("1.2.0", "1.1.9") == 1
            assert is_newer_version("1.2.0", "1.1.0")
            assert compatibility_check(manifest, runtime="onnx")
            assert rollback_candidate([manifest, {"version": "1.0.0"}], "1.2.0")["version"] == "1.0.0"
            assert isinstance(rollout_bucket("dev", 50), bool)
            assert ab_variant("dev") in ("A", "B")
            path = os.path.join(tmp, "manifest.json")
            write_manifest(path, manifest)
            assert read_manifest(path)["name"] == "demo"
            assert model_record("n", "1", "p")["path"] == "p"
            print("[OK] manifest helpers")
            print("[DONE]")
    except Exception as e:
        print("[FAIL]", e)
