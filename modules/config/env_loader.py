"""
Name: Env Loader (no deps)

Why:
- Small scripts often need configuration from a .env file
- Useful when external dotenv packages are not available

Features:
- Reads simple KEY=VALUE lines
- Ignores blank lines and comments
- Loads values into os.environ

Limitations:
- No variable interpolation
- No export support
- No multiline values or advanced parsing

Usage:
    values = load_env()
    print(values.get("API_KEY"))
"""

import os
import tempfile


def _parse_line(line):
    if "=" not in line:
        return None

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    if not key:
        return None

    return key, value


def load_env(path=".env", override=False):
    loaded = {}

    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            parsed = _parse_line(line)
            if parsed is None:
                continue

            key, value = parsed
            loaded[key] = value

            if override or key not in os.environ:
                os.environ[key] = value

    return loaded


if __name__ == "__main__":
    print("[TEST] env_loader")

    previous = {}
    touched = ["PASTEPY_A", "PASTEPY_B", "PASTEPY_C"]

    for key in touched:
        previous[key] = os.environ.get(key)

    try:
        content = "\n".join(
            [
                "# comment",
                "",
                "PASTEPY_A = one",
                "PASTEPY_B=two",
                "INVALID_LINE",
            ]
        )

        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", delete=False, suffix=".env"
        ) as f:
            f.write(content)
            path = f.name

        loaded = load_env(path)
        assert loaded == {"PASTEPY_A": "one", "PASTEPY_B": "two"}
        assert os.environ["PASTEPY_A"] == "one"
        assert os.environ["PASTEPY_B"] == "two"
        print("[OK] basic load")

        os.environ["PASTEPY_A"] = "keep"
        with open(path, "w", encoding="utf-8") as f:
            f.write("PASTEPY_A=replace\nPASTEPY_C=three\n")

        loaded = load_env(path, override=False)
        assert loaded == {"PASTEPY_A": "replace", "PASTEPY_C": "three"}
        assert os.environ["PASTEPY_A"] == "keep"
        assert os.environ["PASTEPY_C"] == "three"
        print("[OK] override false")

        loaded = load_env(path, override=True)
        assert loaded == {"PASTEPY_A": "replace", "PASTEPY_C": "three"}
        assert os.environ["PASTEPY_A"] == "replace"
        print("[OK] override true")

        os.remove(path)
        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)

    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
