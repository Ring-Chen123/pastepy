"""
Name: Tiny Args (no deps)

Why:
- Some scripts need lighter argument parsing than argparse
- Useful for copy-paste tools with a few flags

Features:
- --key=value flags
- --key value flags
- boolean flags
- positional arguments
- environment fallback helper

Limitations:
- Not a replacement for argparse
- No subcommands or advanced validation

Usage:
    args = parse_args(["--name", "ada", "--debug", "file.txt"])
    print(args["flags"]["name"])
"""

import os


def parse_args(argv):
    flags = {}
    positional = []
    i = 0

    while i < len(argv):
        arg = argv[i]

        if arg.startswith("--"):
            name = arg[2:]
            if "=" in name:
                key, value = name.split("=", 1)
                flags[key] = value
            elif i + 1 < len(argv) and not argv[i + 1].startswith("-"):
                flags[name] = argv[i + 1]
                i += 1
            else:
                flags[name] = True
        elif arg.startswith("-") and len(arg) > 1:
            flags[arg[1:]] = True
        else:
            positional.append(arg)

        i += 1

    return {"flags": flags, "positional": positional}


def get_flag(parsed, name, default=None):
    return parsed.get("flags", {}).get(name, default)


def has_flag(parsed, name):
    return bool(parsed.get("flags", {}).get(name))


def env_or_flag(parsed, flag_name, env_name, default=None):
    value = get_flag(parsed, flag_name)
    if value is not None:
        return value
    return os.environ.get(env_name, default)


def require_flag(parsed, name):
    value = get_flag(parsed, name)
    if value is None:
        raise ValueError("missing required flag: --" + name)
    return value


if __name__ == "__main__":
    print("[TEST] args")

    try:
        parsed = parse_args(["--name", "ada", "--count=3", "-v", "file.txt"])
        assert get_flag(parsed, "name") == "ada"
        assert get_flag(parsed, "count") == "3"
        assert has_flag(parsed, "v") is True
        assert parsed["positional"] == ["file.txt"]
        assert require_flag(parsed, "name") == "ada"
        print("[OK] parse")
        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
