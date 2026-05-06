"""
Name: Edge Resource Policy (no deps)

Why:
- Edge AI apps need simple decisions under CPU, memory, disk, and latency limits
- These helpers keep resource policies explicit and testable

Features:
- memory/disk budget checks
- adaptive chunk size
- model selection by constraints
- battery and thermal policy helpers

Limitations:
- Policy helpers only; no hardware telemetry collection
- Inputs are plain dictionaries or numbers
"""


def within_budget(value, limit):
    return value <= limit


def memory_headroom(total, used):
    return max(0, total - used)


def disk_headroom(total, used):
    return max(0, total - used)


def choose_chunk_ms(latency_budget_ms, min_chunk_ms=20, max_chunk_ms=200):
    return max(min_chunk_ms, min(max_chunk_ms, int(latency_budget_ms / 4)))


def choose_model(models, max_size=None, max_latency=None, min_accuracy=None):
    candidates = []
    for model in models:
        if max_size is not None and model.get("size", 0) > max_size:
            continue
        if max_latency is not None and model.get("latency", 0) > max_latency:
            continue
        if min_accuracy is not None and model.get("accuracy", 0) < min_accuracy:
            continue
        candidates.append(model)
    candidates.sort(key=lambda m: (m.get("accuracy", 0), -m.get("latency", 0)), reverse=True)
    return candidates[0] if candidates else None


def should_use_low_power(battery_percent, threshold=20):
    return battery_percent <= threshold


def should_throttle(temperature_c, threshold_c=80):
    return temperature_c >= threshold_c


def sample_rate_for_power(low_power, normal_rate=16000, low_rate=8000):
    return low_rate if low_power else normal_rate


def max_queue_for_memory(free_bytes, bytes_per_item):
    return free_bytes // bytes_per_item if bytes_per_item else 0


def retry_allowed(attempt, max_attempts):
    return attempt < max_attempts


def degrade_mode(memory_ok=True, disk_ok=True, thermal_ok=True):
    if not memory_ok:
        return "memory_saver"
    if not disk_ok:
        return "no_spool"
    if not thermal_ok:
        return "low_power"
    return "normal"


def feature_allowed(policy, feature):
    return feature not in policy.get("disabled_features", [])


if __name__ == "__main__":
    print("[TEST] resource_policy")
    try:
        assert within_budget(1, 2)
        assert memory_headroom(10, 3) == 7
        assert disk_headroom(10, 4) == 6
        assert choose_chunk_ms(400) == 100
        assert choose_model([{"name": "a", "accuracy": 0.9, "latency": 10}], max_latency=20)["name"] == "a"
        assert should_use_low_power(10)
        assert should_throttle(90)
        assert sample_rate_for_power(True) == 8000
        assert max_queue_for_memory(100, 20) == 5
        assert retry_allowed(1, 2)
        assert degrade_mode(memory_ok=False) == "memory_saver"
        assert feature_allowed({"disabled_features": ["x"]}, "y")
        print("[OK] resource policy helpers")
        print("[DONE]")
    except Exception as e:
        print("[FAIL]", e)
