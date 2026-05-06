"""
Name: URL Tools (no deps)

Why:
- urllib.parse is reliable but verbose for common URL edits
- Scripts often need simple query and join helpers

Features:
- add query parameters
- remove query parameters
- read query values
- join URLs
- encode parameters
- HTTP URL check

Limitations:
- Does not validate every URL edge case
- Keeps query values as strings

Usage:
    print(add_query("https://x.test", page=2))
"""

from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse


def encode_params(params):
    return urlencode(params, doseq=True)


def add_query(url, **params):
    parts = urlparse(url)
    query = parse_qs(parts.query, keep_blank_values=True)
    for key, value in params.items():
        query[key] = value if isinstance(value, list) else [value]
    return urlunparse(parts._replace(query=urlencode(query, doseq=True)))


def get_query(url, name, default=None):
    values = parse_qs(urlparse(url).query, keep_blank_values=True).get(name)
    return values[0] if values else default


def remove_query(url, *names):
    parts = urlparse(url)
    query = parse_qs(parts.query, keep_blank_values=True)
    for name in names:
        query.pop(name, None)
    return urlunparse(parts._replace(query=urlencode(query, doseq=True)))


def join_url(base, path):
    return urljoin(base.rstrip("/") + "/", path)


def is_http_url(url):
    scheme = urlparse(url).scheme.lower()
    return scheme in ("http", "https")


if __name__ == "__main__":
    print("[TEST] url_tools")

    try:
        url = add_query("https://example.com?a=1", b=2)
        assert get_query(url, "a") == "1"
        assert get_query(url, "b") == "2"
        assert remove_query(url, "a") == "https://example.com?b=2"
        assert join_url("https://example.com/api", "v1") == "https://example.com/api/v1"
        assert encode_params({"a": [1, 2]}) == "a=1&a=2"
        assert is_http_url("https://example.com") is True
        print("[OK] url helpers")
        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
