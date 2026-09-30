from __future__ import annotations

from collections import Counter

import numpy as np


def _segments(labels: np.ndarray) -> list[tuple[int, int, int]]:
    labels = np.asarray(labels, dtype=np.int64)
    if len(labels) == 0:
        return []
    starts = np.r_[0, np.flatnonzero(labels[1:] != labels[:-1]) + 1]
    ends = np.r_[starts[1:], len(labels)]
    return [(int(labels[s]), int(s), int(e)) for s, e in zip(starts, ends)]


def _edit_distance(a: list[int], b: list[int]) -> int:
    previous = list(range(len(b) + 1))
    for i, value in enumerate(a, start=1):
        current = [i]
        for j, other in enumerate(b, start=1):
            current.append(min(current[-1] + 1, previous[j] + 1, previous[j - 1] + (value != other)))
        previous = current
    return previous[-1]


def _segment_f1(gt: list[tuple[int, int, int]], pred: list[tuple[int, int, int]], threshold: float) -> tuple[float, int, int, int]:
    matched: set[int] = set()
    tp = 0
    for label, start, end in gt:
        best_idx, best_iou = None, -1.0
        for idx, (pred_label, pred_start, pred_end) in enumerate(pred):
            if idx in matched or pred_label != label:
                continue
            intersection = max(0, min(end, pred_end) - max(start, pred_start))
            union = max(end, pred_end) - min(start, pred_start)
            iou = intersection / union if union else 0.0
            if iou > best_iou:
                best_idx, best_iou = idx, iou
        if best_idx is not None and best_iou >= threshold:
            matched.add(best_idx)
            tp += 1
    fp, fn = len(pred) - tp, len(gt) - tp
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return f1, tp, fp, fn


def action_metrics(
    gt: np.ndarray,
    pred: np.ndarray,
    class_order: list[str],
    background_id: int | None = None,
    background_label: str | None = None,
) -> dict:
    gt = np.asarray(gt, dtype=np.int64)
    pred = np.asarray(pred, dtype=np.int64)
    if gt.ndim != 1 or pred.ndim != 1:
        raise ValueError(f"Ground truth and prediction must be 1D label sequences; got {gt.shape} and {pred.shape}")
    if len(gt) != len(pred):
        raise ValueError(f"Ground truth and prediction lengths are not aligned: {len(gt)} != {len(pred)}")
    if len(gt) == 0:
        raise ValueError("Cannot evaluate an empty sequence")
    if background_id is None and background_label is None:
        raise ValueError("Specify background_id or background_label for action metrics")
    if background_id is None:
        try:
            background_id = class_order.index(background_label)
        except ValueError as exc:
            raise ValueError(f"Background label {background_label!r} is absent from class_order") from exc
    if not 0 <= background_id < len(class_order):
        raise ValueError(f"background_id {background_id} is outside class_order")
    if np.any((gt < 0) | (gt >= len(class_order))) or np.any((pred < 0) | (pred >= len(class_order))):
        raise ValueError("Ground truth or prediction contains a class ID outside class_order")
    length = len(gt)
    confusion = np.zeros((len(class_order), len(class_order)), dtype=np.int64)
    np.add.at(confusion, (gt, pred), 1)
    report = {}
    f1s = []
    for class_id, name in enumerate(class_order):
        true_pos = int(np.sum((gt == class_id) & (pred == class_id)))
        false_pos = int(np.sum((gt != class_id) & (pred == class_id)))
        false_neg = int(np.sum((gt == class_id) & (pred != class_id)))
        precision = true_pos / (true_pos + false_pos) if true_pos + false_pos else 0.0
        recall = true_pos / (true_pos + false_neg) if true_pos + false_neg else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        report[name] = {"precision": precision, "recall": recall, "f1": f1, "support": int(np.sum(gt == class_id))}
        if class_id != background_id and np.sum(gt == class_id) > 0:
            f1s.append(f1)
    gt_segments = _segments(gt)
    pred_segments = _segments(pred)
    gt_labels = [label for label, _, _ in gt_segments if label != background_id]
    pred_labels = [label for label, _, _ in pred_segments if label != background_id]
    edit = 100.0 * (1.0 - _edit_distance(gt_labels, pred_labels) / max(len(gt_labels), len(pred_labels), 1))
    segmental = {}
    for threshold in (0.1, 0.25, 0.5):
        f1, tp, fp, fn = _segment_f1(
            [segment for segment in gt_segments if segment[0] != background_id],
            [segment for segment in pred_segments if segment[0] != background_id],
            threshold,
        )
        segmental[f"F1@{int(threshold * 100)}"] = {"f1": f1, "tp": tp, "fp": fp, "fn": fn}
    return {
        "frame_accuracy": float(np.mean(gt == pred)),
        "macro_f1_actions": float(np.mean(f1s)) if f1s else 0.0,
        "normalized_edit_score": edit,
        "segmental": segmental,
        "per_class": report,
        "confusion_matrix": {
            "labels": list(class_order),
            "rows_true_columns_predicted": confusion.tolist(),
        },
        "gt_action_segments": len([s for s in gt_segments if s[0] != background_id]),
        "pred_action_segments": len([s for s in pred_segments if s[0] != background_id]),
        "frames_evaluated": int(length),
    }


def sequence_exact_match(gt_actions: list[str], pred_actions: list[str]) -> bool:
    return gt_actions == pred_actions


def violation_counts(violations: list[dict]) -> dict[str, int]:
    return dict(Counter(str(item["violation_type"]) for item in violations))
