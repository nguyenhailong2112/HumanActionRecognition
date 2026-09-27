from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from human_action.config import load_config  # noqa: E402
from human_action.dataset import load_split  # noqa: E402
from human_action.metrics import action_metrics, _segments, _edit_distance  # noqa: E402
from human_action.pipeline import evaluate_video  # noqa: E402


def summarize(rows: list[dict], class_order: list[str]) -> dict:
    keys = ("frame_accuracy", "macro_f1_actions", "normalized_edit_score")
    segs = ("F1@10", "F1@25", "F1@50")
    pooled_gt = np.concatenate([np.asarray(r["gt"], dtype=np.int64) for r in rows])
    pooled_pred = np.concatenate([np.asarray(r["pred"], dtype=np.int64) for r in rows])
    pooled = action_metrics(pooled_gt, pooled_pred, class_order)
    # Keep execution boundaries: frame/class counts pool over frames, but edit
    # and segment matches must not treat the last frame of one video as adjacent
    # to the first frame of another.
    edit_distance_total = edit_denominator_total = 0
    segment_counts = {key: {"tp": 0, "fp": 0, "fn": 0} for key in ("F1@10", "F1@25", "F1@50")}
    for row in rows:
        gt_seg = [label for label, _, _ in _segments(np.asarray(row["gt"], dtype=np.int64)) if label != 0]
        pred_seg = [label for label, _, _ in _segments(np.asarray(row["pred"], dtype=np.int64)) if label != 0]
        edit_distance_total += _edit_distance(gt_seg, pred_seg)
        edit_denominator_total += max(len(gt_seg), len(pred_seg), 1)
        for key in segment_counts:
            for stat in segment_counts[key]:
                segment_counts[key][stat] += int(row["action"]["segmental"][key][stat])
    pooled["normalized_edit_score"] = 100.0 * (1.0 - edit_distance_total / max(edit_denominator_total, 1))
    for key, stats in segment_counts.items():
        tp, fp, fn = stats["tp"], stats["fp"], stats["fn"]
        stats["f1"] = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0
        pooled["segmental"][key] = stats
    pooled["gt_action_segments"] = int(sum(row["action"]["gt_action_segments"] for row in rows))
    pooled["pred_action_segments"] = int(sum(row["action"]["pred_action_segments"] for row in rows))
    vals = {key: [r["action"][key] for r in rows] for key in keys}
    vals.update({key: [r["action"]["segmental"][key]["f1"] for r in rows] for key in segs})
    return {
        "mean_per_execution": {key: float(np.mean(v)) for key, v in vals.items()},
        "std_per_execution_sample": {key: float(np.std(v, ddof=1)) if len(v) > 1 else 0.0 for key, v in vals.items()},
        "pooled_frames": pooled,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/cp05.yaml")
    p.add_argument("--checkpoint", default=None)
    p.add_argument("--output", default="experiments/CP06")
    a = p.parse_args()
    config_path = (ROOT / a.config).resolve()
    config = load_config(config_path)
    output = (ROOT / a.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    rows = []
    for seq in load_split(config, "test", config_path):
        item = evaluate_video(seq.video_id, "test", config, config_path, "mstcn", a.checkpoint)
        rows.append({"video_id": seq.video_id, "worker_id": seq.worker_id, "action": item["action"], "gt": item["ground_truth_labels"], "pred": item["predicted_labels"], "probabilities": item["probabilities"], "timestamps": item["timestamps"], "segments": item["segments"], "events": item["events"], "video_path": item["video_path"]})
    baseline_rows = []
    for seq in load_split(config, "test", config_path):
        item = evaluate_video(seq.video_id, "test", config, config_path, "framewise")
        baseline_rows.append({"video_id": seq.video_id, "action": item["action"], "gt": item["ground_truth_labels"], "pred": item["predicted_labels"]})
    framewise_summary = summarize(baseline_rows, config["actions"]["class_order"])
    metrics = {"protocol": "IMPACT v1.1 TAS-S S2 split2 Disassembly_A/front; frozen test; no tuning", "model": "our MS-TCN", "video_ids": [r["video_id"] for r in rows], "per_execution": [{"video_id": r["video_id"], "action": r["action"]} for r in rows], **summarize(rows, config["actions"]["class_order"]), "framewise_comparison": {"model": "our FramewiseBaseline", "per_execution": [{"video_id": r["video_id"], "action": r["action"]} for r in baseline_rows], **framewise_summary}}
    (output / "action_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    # Deterministic mismatch runs. Reasons remain unknown until a person reviews video.
    names = config["actions"]["class_order"]
    errors = []
    pair_counts = Counter()
    sequence_diagnostics = []
    smoothing_introduced = smoothing_corrected = 0
    for r in rows:
        gt, pred = np.asarray(r["gt"]), np.asarray(r["pred"])
        starts = np.r_[0, np.flatnonzero((gt[1:] != gt[:-1]) | (pred[1:] != pred[:-1])) + 1]
        ends = np.r_[starts[1:], len(gt)]
        boundary_points = np.r_[0, np.flatnonzero(gt[1:] != gt[:-1]) + 1]
        support = Counter(gt.tolist())
        for start, end in zip(starts, ends):
            if gt[start] == pred[start]:
                continue
            g, q = int(gt[start]), int(pred[start])
            pair_counts[(names[g], names[q])] += int(end - start)
            near_boundary = bool(np.any(np.abs(boundary_points - start) <= 2) or np.any(np.abs(boundary_points - end) <= 2))
            tags = []
            if g == 0 or q == 0:
                category = "NULL/background leakage"
                tags.append("NULL/background leakage")
            else:
                tags.append("class confusion")
            if end - start <= 2:
                tags.append("short-action failure")
            if near_boundary:
                tags.append("boundary error")
            if g != 0 and support[g] < 100:
                tags.append("rare-class failure")
            if g != 0 and q != 0:
                category = "class confusion"
            elif end - start <= 2:
                category = "short-action failure"
            elif near_boundary:
                category = "boundary error"
            elif g != 0 and support[g] < 100:
                category = "rare-class failure"
            else:
                category = "NULL/background leakage"
            confidence = float(np.mean([r["probabilities"][i][q] for i in range(start, end)]))
            errors.append({"error_id": f"{r['video_id']}-e{start:05d}", "execution_id": r["video_id"], "time_start_seconds": float(r["timestamps"][start]), "time_end_seconds": float(r["timestamps"][min(end - 1, len(r['timestamps']) - 1)]), "gt_action": names[g], "predicted_action": names[q], "error_category": category, "diagnostic_tags": tags, "mean_predicted_class_probability": confidence, "likely_visual_reason": "UNKNOWN — requires linked video review; not inferred from model output", "bottleneck_attribution": "UNDETERMINED pending video/annotation review", "human_review_status": "HUMAN_REVIEW_REQUIRED", "frame_count": int(end - start)})
        decoded = np.zeros(len(gt), dtype=np.int64)
        for seg in r["segments"]:
            label = names.index(seg["action"])
            mask = (np.asarray(r["timestamps"]) >= seg["start_time"]) & (np.asarray(r["timestamps"]) < seg["end_time"])
            decoded[mask] = label
        raw_bad, decoded_bad = pred != gt, decoded != gt
        smoothing_introduced += int(np.sum(~raw_bad & decoded_bad))
        smoothing_corrected += int(np.sum(raw_bad & ~decoded_bad))
        sequence_diagnostics.append({"execution_id": r["video_id"], "ground_truth_action_segments": r["action"]["gt_action_segments"], "predicted_action_segments": r["action"]["pred_action_segments"], "segment_count_pattern": "over-segmentation" if r["action"]["pred_action_segments"] > r["action"]["gt_action_segments"] else "under-segmentation" if r["action"]["pred_action_segments"] < r["action"]["gt_action_segments"] else "equal", "model_only_issue_reason": "UNDETERMINED"})
    errors.sort(key=lambda e: (-e["frame_count"], -e["mean_predicted_class_probability"]))
    tag_counts = Counter(tag for error in errors for tag in error["diagnostic_tags"])
    (output / "action_error_events.json").write_text(json.dumps({"scope": "held-out test; raw frame predictions against TAS-S labels", "errors": errors, "diagnostic_tag_counts": dict(tag_counts), "top_confusions_by_frames": [{"gt": k[0], "predicted": k[1], "mismatched_frames": v} for k, v in pair_counts.most_common()], "execution_diagnostics": sequence_diagnostics, "temporal_postprocessing_comparison": {"raw_correct_decoded_wrong_frames": smoothing_introduced, "raw_wrong_decoded_correct_frames": smoothing_corrected, "evaluation": "post-decoding comparison against TAS-S labels; descriptive diagnosis only"}, "visual_ambiguity_and_insufficient_observation": "HUMAN_REVIEW_REQUIRED; not inferable from model outputs"}, indent=2), encoding="utf-8")

    # Select review events from the existing real-inference evidence index.
    evidence = json.loads((ROOT / "experiments/CP05/evidence_index.json").read_text(encoding="utf-8"))["records"]
    by_id = {r["video_id"]: r for r in rows}
    selected = {}
    for n, rec in enumerate(evidence, start=1):
        r = by_id.get(rec["video_id"])
        if r is None:
            continue
        ix = int(np.argmin(np.abs(np.asarray(r["timestamps"]) - rec["action_event_timestamp_seconds"])))
        gt_name, pred_name = names[int(r["gt"][ix])], names[int(r["pred"][ix])]
        rec2 = {"event_id": f"CP05-MSTCN-{n:03d}", "video_id": rec["video_id"], "source_video": r["video_path"], "timestamp_seconds": rec["action_event_timestamp_seconds"], "gt_action_at_event_start": gt_name, "predicted_action": rec["action"], "confidence": rec["confidence"], "snapshot": rec["snapshot"], "clip": rec["clip"], "review_status": "HUMAN_REVIEW_REQUIRED"}
        correct = gt_name == rec["action"]
        categories = []
        if rec["confidence"] >= .8 and correct: categories.append("high-confidence correct candidate")
        if rec["confidence"] >= .8 and not correct: categories.append("high-confidence wrong candidate")
        if gt_name == "NULL" and rec["action"] != "NULL": categories.append("NULL leakage candidate")
        gt_boundaries = np.flatnonzero(np.asarray(r["gt"])[1:] != np.asarray(r["gt"][:-1]))
        if any(abs(ix - int(b + 1)) <= 2 for b in gt_boundaries): categories.append("ground-truth boundary candidate")
        if sum(1 for x in r["gt"] if names[int(x)] == gt_name) < 100: categories.append("rare-action candidate")
        if not correct: categories.append("confusing-class pair candidate")
        if rec["confidence"] < .5: categories.append("low-confidence / possible ambiguity review candidate")
        for cat in categories:
            bucket = selected.setdefault(cat, [])
            if len(bucket) < 3:
                rec2["review_reason"] = cat
                bucket.append(rec2)
    (output / "evidence_review_manifest.json").write_text(json.dumps({"status": "HUMAN_REVIEW_REQUIRED", "source": "69 actual CP05 MS-TCN held-out event records", "selection": selected}, indent=2), encoding="utf-8")
    print(f"[ok] wrote metrics for {len(rows)} executions, {len(errors)} mismatch runs, and {sum(map(len, selected.values()))} review selections to {output}")


if __name__ == "__main__":
    main()
