"""
Name: System Probe (no deps)

Why:
- Edge AI apps need quick checks for memory, disk, CPU, and platform
- Standard library probes are enough for many deployment diagnostics

Features:
- platform info
- CPU count
- disk usage
- memory info when available
- Python version
- environment snapshot

Limitations:
- Memory probing is platform-dependent
- No privileged hardware telemetry

Usage:
    print(system_summary())
"""

import os
import platform
import shutil
import sys


def platform_info():
    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }


def cpu_count():
    return os.cpu_count() or 1


def disk_usage(path="."):
    usage = shutil.disk_usage(path)
    return {"total": usage.total, "used": usage.used, "free": usage.free}


def python_version():
    return sys.version.split()[0]


def env_snapshot(names):
    return {name: os.environ.get(name) for name in names}


def memory_info():
    if hasattr(os, "sysconf"):
        try:
            pages = os.sysconf("SC_PHYS_PAGES")
            page_size = os.sysconf("SC_PAGE_SIZE")
            return {"total": pages * page_size}
        except (ValueError, OSError, AttributeError):
            pass
    return {"total": None}


def system_summary(path="."):
    return {
        "platform": platform_info(),
        "cpu_count": cpu_count(),
        "disk": disk_usage(path),
        "memory": memory_info(),
        "python": python_version(),
    }


if __name__ == "__main__":
    print("[TEST] system_probe")

    try:
        assert platform_info()["system"]
        assert cpu_count() >= 1
        assert disk_usage(".")["total"] > 0
        assert python_version().count(".") >= 1
        assert isinstance(env_snapshot(["PATH"]), dict)
        assert "total" in memory_info()
        assert "disk" in system_summary(".")
        print("[OK] system helpers")
        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
