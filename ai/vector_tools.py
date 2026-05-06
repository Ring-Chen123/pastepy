"""
Name: Vector Tools (no deps)

Why:
- Edge AI apps often need tiny embedding comparisons
- Simple vector math should not require numpy for small inputs

Features:
- dot product
- vector norm
- cosine similarity
- L2 distance
- top-k search
- min-max normalization

Limitations:
- Pure Python and intended for small vectors
- No ANN indexing

Usage:
    print(cosine_similarity([1, 0], [1, 1]))
"""

import math


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm(vector):
    return math.sqrt(sum(x * x for x in vector))


def cosine_similarity(a, b):
    denom = norm(a) * norm(b)
    return dot(a, b) / denom if denom else 0


def l2_distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def normalize_vector(vector):
    length = norm(vector)
    if not length:
        return [0 for _ in vector]
    return [x / length for x in vector]


def mean_vector(vectors):
    vectors = list(vectors)
    if not vectors:
        return []
    size = len(vectors[0])
    return [sum(vector[i] for vector in vectors) / len(vectors) for i in range(size)]


def top_k_similar(query, items, k=5):
    scored = [(cosine_similarity(query, item["vector"]), item) for item in items]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return scored[:k]


def minmax_scale(values):
    values = list(values)
    if not values:
        return []
    low = min(values)
    high = max(values)
    if high == low:
        return [0 for _ in values]
    return [(value - low) / float(high - low) for value in values]


if __name__ == "__main__":
    print("[TEST] vector_tools")

    try:
        assert dot([1, 2], [3, 4]) == 11
        assert norm([3, 4]) == 5
        assert round(cosine_similarity([1, 0], [1, 1]), 3) == 0.707
        assert l2_distance([0, 0], [3, 4]) == 5
        assert normalize_vector([0, 0]) == [0, 0]
        assert mean_vector([[1, 3], [3, 5]]) == [2, 4]
        assert top_k_similar([1, 0], [{"id": 1, "vector": [1, 0]}])[0][1]["id"] == 1
        assert minmax_scale([2, 4, 6]) == [0, 0.5, 1]
        print("[OK] vector helpers")
        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
