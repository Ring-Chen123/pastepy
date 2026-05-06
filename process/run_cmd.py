"""
Name: Run Command (no deps)

Why:
- Scripts often need subprocess calls with captured output and timeouts
- subprocess.run is good but verbose for repeated use

Features:
- captured stdout/stderr
- timeout support
- optional check mode
- line output helper
- executable lookup

Limitations:
- No streaming output
- shell=False by default

Usage:
    result = run(["python", "--version"])
    print(result.code, result.stdout)
"""

import shlex
import shutil
import subprocess


class CommandResult:
    def __init__(self, code, stdout, stderr):
        self.code = code
        self.stdout = stdout
        self.stderr = stderr

    @property
    def ok(self):
        return self.code == 0


def run(command, timeout=None, check=False, cwd=None):
    completed = subprocess.run(
        command,
        cwd=cwd,
        timeout=timeout,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=isinstance(command, str),
    )
    result = CommandResult(completed.returncode, completed.stdout, completed.stderr)

    if check and not result.ok:
        raise RuntimeError(result.stderr.strip() or "command failed")

    return result


def run_lines(command, timeout=None, cwd=None):
    return run(command, timeout=timeout, cwd=cwd).stdout.splitlines()


def which(name):
    return shutil.which(name)


def shell_quote(value):
    return shlex.quote(str(value))


if __name__ == "__main__":
    print("[TEST] run_cmd")

    try:
        result = run(["cmd", "/c", "echo hello"] if which("cmd") else ["echo", "hello"])
        assert result.ok is True
        assert "hello" in result.stdout
        assert run_lines(["cmd", "/c", "echo hi"] if which("cmd") else ["echo", "hi"])[0].strip() == "hi"
        assert which("cmd") or which("echo")
        assert shell_quote("a b")
        print("[OK] command helpers")
        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
