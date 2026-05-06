"""
Name: Model Metrics Tools (no deps)

Why:
- Edge validation often needs small classification metrics on-device
- Pure Python metrics are enough for small test sets

Features:
- accuracy
- precision / recall / F1
- confusion matrix helpers
- moving averages and drift scores
"""


def accuracy(actual, predicted):
    actual = list(actual)
    predicted = list(predicted)
    if not actual:
        return 0
    return sum(1 for a, p in zip(actual, predicted) if a == p) / float(len(actual))


def confusion_counts(actual, predicted, positive):
    tp = fp = tn = fn = 0
    for a, p in zip(actual, predicted):
        if a == positive and p == positive:
            tp += 1
        elif a != positive and p == positive:
            fp += 1
        elif a != positive and p != positive:
            tn += 1
        elif a == positive and p != positive:
            fn += 1
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn}


def precision(actual, predicted, positive):
    c = confusion_counts(actual, predicted, positive)
    denom = c["tp"] + c["fp"]
    return c["tp"] / float(denom) if denom else 0


def recall(actual, predicted, positive):
    c = confusion_counts(actual, predicted, positive)
    denom = c["tp"] + c["fn"]
    return c["tp"] / float(denom) if denom else 0


def f1_score(actual, predicted, positive):
    p = precision(actual, predicted, positive)
    r = recall(actual, predicted, positive)
    return 2 * p * r / (p + r) if p + r else 0


def per_class_counts(labels):
    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    return counts


def label_distribution(labels):
    counts = per_class_counts(labels)
    total = sum(counts.values())
    return {label: count / float(total) for label, count in counts.items()} if total else {}


def moving_average(values, size):
    values = list(values)
    return [sum(values[i:i + size]) / float(size) for i in range(0, len(values) - size + 1)]


def confidence_average(predictions):
    scores = [p.get("score", 0) for p in predictions]
    return sum(scores) / float(len(scores)) if scores else 0


def majority_vote(labels):
    counts = per_class_counts(labels)
    return max(counts, key=counts.get) if counts else None


def debounce_predictions(predictions, min_repeat=2):
    output = []
    last = None
    count = 0
    for item in predictions:
        count = count + 1 if item == last else 1
        last = item
        if count >= min_repeat:
            output.append(item)
    return output


def drift_score(reference_scores, current_scores):
    ref = sum(reference_scores) / float(len(reference_scores)) if reference_scores else 0
    cur = sum(current_scores) / float(len(current_scores)) if current_scores else 0
    return cur - ref


if __name__ == "__main__":
    print("[TEST] metrics_tools")
    try:
        a = ["yes", "no", "yes"]
        p = ["yes", "yes", "yes"]
        assert round(accuracy(a, p), 3) == 0.667
        assert confusion_counts(a, p, "yes") == {"tp": 2, "fp": 1, "tn": 0, "fn": 0}
        assert precision(a, p, "yes") == 2 / 3
        assert recall(a, p, "yes") == 1
        assert round(f1_score(a, p, "yes"), 3) == 0.8
        assert per_class_counts(a)["yes"] == 2
        assert label_distribution(a)["yes"] == 2 / 3
        assert moving_average([1, 3, 5], 2) == [2, 4]
        assert confidence_average([{"score": 1}, {"score": 0}]) == 0.5
        assert majority_vote(["a", "b", "a"]) == "a"
        assert debounce_predictions(["a", "a", "b"], 2) == ["a"]
        assert drift_score([1], [2]) == 1
        print("[OK] metric helpers")
        print("[DONE]")
    except Exception as e:
        print("[FAIL]", e)
