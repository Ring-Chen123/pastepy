"""
Name: Simple HTTP Client (no deps)

Why:
- Cannot use external libraries like requests
- Designed for edge / restricted environments

Features:
- GET / POST
- Timeout support
- Retry (simple backoff)
- JSON support

Limitations:
- No HTTP/2
- No streaming
- Basic error handling only

Usage:
    res = get("https://example.com")
    print(res.status, res.text)

    res = post("https://example.com", json={"a": 1})
    print(res.json())
"""

import json as _json
import time as _time
import urllib.request as _request
import urllib.error as _error


# -----------------------------
# Response
# -----------------------------

class Response:
    def __init__(self, status, text):
        self.status = status
        self.text = text

    def json(self):
        return _json.loads(self.text)


# -----------------------------
# internal
# -----------------------------

def _sleep(attempt):
    _time.sleep(0.3 * (2 ** attempt))


def _request_once(url, method, data, headers, timeout):
    if headers is None:
        headers = {}

    if data is not None and not isinstance(data, bytes):
        data = data.encode("utf-8")

    req = _request.Request(url, data=data, headers=headers, method=method)

    try:
        with _request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return Response(resp.getcode(), body)

    except _error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return Response(e.code, body)


# -----------------------------
# public
# -----------------------------

def get(url, headers=None, timeout=5, retries=0):
    for i in range(retries + 1):
        try:
            return _request_once(url, "GET", None, headers, timeout)
        except Exception:
            if i == retries:
                raise
            _sleep(i)


def post(url, data=None, json=None, headers=None, timeout=5, retries=0):
    if headers is None:
        headers = {}

    if json is not None:
        data = _json.dumps(json)
        headers["Content-Type"] = "application/json"

    for i in range(retries + 1):
        try:
            return _request_once(url, "POST", data, headers, timeout)
        except Exception:
            if i == retries:
                raise
            _sleep(i)


# -----------------------------
# self test
# -----------------------------

if __name__ == "__main__":
    import sys
    DEBUG = "--debug" in sys.argv
    if DEBUG:
        print("[DEBUG] Running self test with debug output")
    print("[TEST] simple_http")

    try:
        r = get("https://httpbin.org/get", timeout=3, retries=1)
        assert r.status == 200
        print(r.text[:100], "...") if DEBUG else None
        print("[OK] GET")

        r = post("https://httpbin.org/post", json={"a": 1}, timeout=3, retries=1)
        assert r.status == 200
        print(r.text[:100], "...") if DEBUG else None
        print("[OK] POST")

        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
