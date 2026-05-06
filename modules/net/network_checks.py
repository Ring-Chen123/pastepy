"""
Name: Network Checks (no deps)

Why:
- Edge devices need lightweight connectivity diagnostics
- These helpers use only socket and urllib

Features:
- DNS, TCP, and HTTP checks
- local IP lookup
- TLS URL checks
- reconnect delay
"""

import socket
import time
import urllib.request
from urllib.parse import urlparse


def resolve_host(host):
    return socket.gethostbyname(host)


def can_resolve(host):
    try:
        resolve_host(host)
        return True
    except OSError:
        return False


def tcp_check(host, port, timeout=3):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def http_check(url, timeout=3):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return 200 <= resp.getcode() < 500
    except Exception:
        return False


def local_ip(remote=("8.8.8.8", 80)):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(remote)
        return s.getsockname()[0]
    finally:
        s.close()


def is_tls_url(url):
    return urlparse(url).scheme.lower() == "https"


def allowlist_url(url, hosts):
    return urlparse(url).hostname in hosts


def denylist_url(url, hosts):
    return urlparse(url).hostname not in hosts


def reconnect_delay(attempt, base=0.5, max_delay=60):
    return min(max_delay, base * (2 ** attempt))


def wait_for_tcp(host, port, timeout=10, interval=0.2):
    end = time.time() + timeout
    while time.time() < end:
        if tcp_check(host, port, timeout=interval):
            return True
        time.sleep(interval)
    return False


if __name__ == "__main__":
    print("[TEST] network_checks")
    try:
        assert is_tls_url("https://example.com")
        assert allowlist_url("https://example.com", ["example.com"])
        assert denylist_url("https://example.com", ["bad.test"])
        assert reconnect_delay(2, base=1) == 4
        assert isinstance(can_resolve("localhost"), bool)
        assert isinstance(tcp_check("localhost", 1, timeout=0.01), bool)
        print("[OK] network helpers")
        print("[DONE]")
    except Exception as e:
        print("[FAIL]", e)
