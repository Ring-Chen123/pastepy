"""
Name: Text Tools (no deps)

Why:
- Small scripts often need predictable string cleanup
- Avoid pulling in larger helper libraries for simple text tasks

Features:
- whitespace normalization
- prefix / suffix helpers
- slug, snake_case, and kebab-case conversion
- safe truncation

Limitations:
- ASCII-focused slugs
- Not a natural-language processing library

Usage:
    print(slugify("Hello, World!"))  # hello-world
"""

import re
import unicodedata


def normalize_space(text):
    return " ".join(str(text).split())


def strip_prefix(text, prefix):
    text = str(text)
    return text[len(prefix):] if text.startswith(prefix) else text


def strip_suffix(text, suffix):
    text = str(text)
    return text[:-len(suffix)] if suffix and text.endswith(suffix) else text


def slugify(text, separator="-"):
    text = unicodedata.normalize("NFKD", str(text))
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^A-Za-z0-9]+", separator, text).strip(separator)
    return text.lower()


def snake_case(text):
    return slugify(text, "_")


def kebab_case(text):
    return slugify(text, "-")


def truncate(text, max_length, suffix="..."):
    text = str(text)
    if max_length < 0:
        raise ValueError("max_length must be non-negative")
    if len(text) <= max_length:
        return text
    if max_length <= len(suffix):
        return suffix[:max_length]
    return text[:max_length - len(suffix)] + suffix


if __name__ == "__main__":
    print("[TEST] text_tools")

    try:
        assert normalize_space(" a \n b\t c ") == "a b c"
        assert strip_prefix("prefix-value", "prefix-") == "value"
        assert strip_suffix("value.txt", ".txt") == "value"
        assert slugify("Hello, World!") == "hello-world"
        assert snake_case("Hello, World!") == "hello_world"
        assert kebab_case("Hello, World!") == "hello-world"
        assert truncate("abcdef", 5) == "ab..."
        print("[OK] text helpers")
        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
