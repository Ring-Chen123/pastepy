"""
Name: AI Output Tools (no deps)

Why:
- Small edge AI apps need lightweight post-processing
- Common model outputs can be filtered without big frameworks

Features:
- softmax
- argmax
- top-k labels
- confidence thresholding
- non-max suppression for boxes
- confusion matrix

Limitations:
- Pure Python and intended for small outputs
- Boxes use [x1, y1, x2, y2]

Usage:
    print(top_k([0.1, 0.9], ["no", "yes"], 1))
"""

import math


def softmax(scores):
    if not scores:
        return []
    high = max(scores)
    exps = [math.exp(score - high) for score in scores]
    total = sum(exps)
    return [value / total for value in exps]


def argmax(values):
    if not values:
        raise ValueError("values must not be empty")
    return max(range(len(values)), key=lambda i: values[i])


def top_k(scores, labels=None, k=3):
    labels = labels or list(range(len(scores)))
    pairs = list(zip(labels, scores))
    pairs.sort(key=lambda pair: pair[1], reverse=True)
    return pairs[:k]


def threshold_predictions(predictions, min_score):
    return [prediction for prediction in predictions if prediction.get("score", 0) >= min_score]


def box_area(box):
    return max(0, box[2] - box[0]) * max(0, box[3] - box[1])


def iou(box_a, box_b):
    x1 = max(box_a[0], box_b[0])
    y1 = max(box_a[1], box_b[1])
    x2 = min(box_a[2], box_b[2])
    y2 = min(box_a[3], box_b[3])
    inter = box_area([x1, y1, x2, y2])
    union = box_area(box_a) + box_area(box_b) - inter
    return inter / union if union else 0


def non_max_suppression(predictions, iou_threshold=0.5):
    remaining = sorted(predictions, key=lambda p: p.get("score", 0), reverse=True)
    kept = []
    while remaining:
        current = remaining.pop(0)
        kept.append(current)
        remaining = [p for p in remaining if iou(current["box"], p["box"]) <= iou_threshold]
    return kept


def confusion_matrix(actual, predicted, labels):
    index = {label: i for i, label in enumerate(labels)}
    matrix = [[0 for _ in labels] for _ in labels]
    for a, p in zip(actual, predicted):
        matrix[index[a]][index[p]] += 1
    return matrix


if __name__ == "__main__":
    print("[TEST] output_tools")

    try:
        probs = softmax([1, 2])
        assert round(sum(probs), 6) == 1
        assert argmax([1, 3, 2]) == 1
        assert top_k([0.1, 0.9], ["no", "yes"], 1) == [("yes", 0.9)]
        assert threshold_predictions([{"score": 0.8}, {"score": 0.1}], 0.5) == [{"score": 0.8}]
        assert box_area([0, 0, 2, 2]) == 4
        assert round(iou([0, 0, 2, 2], [1, 1, 3, 3]), 3) == 0.143
        assert len(non_max_suppression([{"score": 1, "box": [0, 0, 2, 2]}, {"score": 0.9, "box": [0, 0, 2, 2]}])) == 1
        assert confusion_matrix(["a"], ["b"], ["a", "b"]) == [[0, 1], [0, 0]]
        print("[OK] output helpers")
        print("[DONE]")

    except Exception as e:
        print("[FAIL]", e)
