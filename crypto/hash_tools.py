"""
Name: Hash Tools (no deps)

Why:
- Scripts often need checksums, tokens, and safe comparisons
- hashlib, hmac, and secrets cover these needs in the standard library

Features:
- SHA-256 for text, bytes, and files
- HMAC-SHA256
- secure random tokens
- constant-time equality

Limitations:
- Small API only
- No password hashing helper

Usage:
    print(sha256_text("hello"))
"""

import hashlib
import hmac
import secrets


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_text(text, encoding="utf-8"):
    return sha256_bytes(str(text).encode(encoding))


def sha256_file(path, chunk_size=1024 * 1024):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def hmac_sha256(secret, message, encoding="utf-8"):
    if isinstance(secret, str):
        secret = secret.encode(encoding)
    if isinstance(message, str):
        message = message.encode(encoding)
    return hmac.new(secret, message, hashlib.sha256).hexdigest()


def random_token(bytes_count=32):
    return secrets.token_hex(bytes_count)


def constant_time_equal(a, b):
    return hmac.compare_digest(str(a), str(b))


if __name__ == "__main__":
    print("[TEST] hash_tools")

    try:
        import os
        import tempfile

        expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        assert sha256_text("hello") == expected
        assert sha256_bytes(b"hello") == expected
        assert hmac_sha256("k", "m")
        assert len(random_token(4)) == 8
        assert constant_time_equal("a", "a") is True

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "x.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write("hello")
            assert sha256_file(path) == expected
        print("[OK] hash helpers")
        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
