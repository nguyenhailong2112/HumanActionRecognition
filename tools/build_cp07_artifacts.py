from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from human_action.config import load_config
from human_action.dataset import load_sequence
from human_action.metrics import _segments
OUT = ROOT / "experiments" / "CP07"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    old = json.loads((ROOT / "experiments/CP06/evidence_review_manifest.json").read_text(encoding="utf-8"))
    unique: dict[str, dict] = {}
    for category, records in old["selection"].items():
        for record in records:
            event = unique.setdefault(record["event_id"], {**record, "review_reasons": []})
            event["review_reasons"].append(category)
    manifest = {
        "status": "HUMAN_REVIEW_REQUIRED",
        "source": "Existing CP06 selection from the 69 actual CP05 MS-TCN held-out evidence records",
        "selection_note": "CP06 has 21 category selections; some refer to the same event. This manifest deduplicates by event_id and preserves all reasons.",
        "unique_event_count": len(unique),
        "category_selection_count": sum(len(items) for items in old["selection"].values()),
        "events": list(unique.values()),
    }
    (OUT / "evidence_review_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    metrics = json.loads((ROOT / "experiments/CP06/action_metrics.json").read_text(encoding="utf-8"))
    errors = json.loads((ROOT / "experiments/CP06/action_error_events.json").read_text(encoding="utf-8"))
    timelines = {}
    for path in sorted((ROOT / "results/cp05/evaluation").glob("*_mstcn_timeline.json")):
        row = json.loads(path.read_text(encoding="utf-8"))
        timelines[row["video_id"]] = row
    per_exec = {item["video_id"]: item["action"] for item in metrics["per_execution"]}
    config_path = ROOT / "configs/cp05.yaml"
    config = load_config(config_path)
    class_order = config["actions"]["class_order"]
    error_by_exec: dict[str, list[dict]] = {key: [] for key in timelines}
    for item in errors["errors"]:
        error_by_exec.setdefault(item["execution_id"], []).append(item)
    result = []
    for video_id, timeline in timelines.items():
        action = per_exec[video_id]
        segs = timeline["segments"]
        non_null = [s for s in segs if s["action"] != "NULL"]
        duration = max((s["end_time"] for s in segs), default=0.0)
        gt_class = action["per_class"]
        gt_frames = sum(x["support"] for x in gt_class.values())
        null_frames = gt_class.get("NULL", {}).get("support", 0)
        mismatches = error_by_exec.get(video_id, [])
        mismatch_frames = sum(x["frame_count"] for x in mismatches)
        confusion = action["confusion_matrix"]
        gt_labels = np.asarray(load_sequence(config, video_id, "test", config_path).labels, dtype=np.int64)
        gt_runs = _segments(gt_labels)
        gt_by_action = {name: [] for name in class_order}
        for label, start, end in gt_runs:
            gt_by_action[class_order[label]].append((start, end))
        pred_by_action = {name: [] for name in class_order}
        for segment in segs:
            pred_by_action[segment["action"]].append(segment)
        per_action = []
        for index, name in enumerate(class_order):
            support = int(action["per_class"][name]["support"])
            if name == "NULL":
                continue
            gt_durations = [(end - start) / float(config["dataset"]["sample_fps"]) for start, end in gt_by_action[name]]
            pred_durations = [float(segment["duration"]) for segment in pred_by_action[name]]
            false_negative = sum(confusion["rows_true_columns_predicted"][index][j] for j in range(len(class_order)) if j != index)
            false_positive = sum(confusion["rows_true_columns_predicted"][j][index] for j in range(len(class_order)) if j != index)
            per_action.append({
                "action": name,
                "gt_support_frames": support,
                "gt_frequency_segments": len(gt_by_action[name]),
                "gt_total_duration_seconds": sum(gt_durations),
                "gt_mean_segment_duration_seconds": sum(gt_durations) / len(gt_durations) if gt_durations else None,
                "pred_frequency_segments": len(pred_by_action[name]),
                "pred_total_duration_seconds": sum(pred_durations),
                "pred_mean_segment_duration_seconds": sum(pred_durations) / len(pred_durations) if pred_durations else None,
                "mismatched_gt_frames": int(false_negative),
                "mismatched_pred_frames": int(false_positive),
            })
        top_pairs = []
        for i, row in enumerate(confusion["rows_true_columns_predicted"]):
            for j, count in enumerate(row):
                if count and i != j:
                    top_pairs.append({"gt": confusion["labels"][i], "predicted": confusion["labels"][j], "frames": count})
        top_pairs.sort(key=lambda x: -x["frames"])
        result.append({
            "execution_id": video_id,
            "frames": action["frames_evaluated"],
            "duration_seconds": duration,
            "frame_accuracy": action["frame_accuracy"],
            "macro_f1_actions": action["macro_f1_actions"],
            "normalized_edit_score": action["normalized_edit_score"],
            "mismatched_frames": mismatch_frames,
            "mismatch_run_count": len(mismatches),
            "gt_action_support_frames": gt_frames - null_frames,
            "gt_null_frames": null_frames,
            "gt_null_fraction": null_frames / gt_frames if gt_frames else None,
            "gt_action_segments": action["gt_action_segments"],
            "predicted_action_segments": action["pred_action_segments"],
            "gt_boundary_density_per_minute": action["gt_action_segments"] / max(duration / 60, 1e-12),
            "predicted_boundary_density_per_minute": len(non_null) / max(duration / 60, 1e-12),
            "mean_predicted_non_null_segment_duration_seconds": sum(s["duration"] for s in non_null) / len(non_null) if non_null else None,
            "predicted_null_duration_fraction": sum(s["duration"] for s in segs if s["action"] == "NULL") / max(duration, 1e-12),
            "top_frame_confusions": top_pairs[:5],
            "per_action_frequency_duration_support_and_mismatch": per_action,
            "interpretation": "descriptive only; four executions do not support causal attribution",
        })
    payload = {
        "scope": "Frozen CP05 seed-17 MS-TCN predictions; test only; no model/workflow tuning",
        "measurements": result,
        "error_category_counts": errors["diagnostic_tag_counts"],
        "top_confusions_by_mismatched_frames": errors["top_confusions_by_frames"][:10],
        "temporal_postprocessing_comparison": errors["temporal_postprocessing_comparison"],
        "human_review_required_for_visual_reason": True,
    }
    (OUT / "action_error_structure.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    handoff = [
        "# HUMAN HANDOFF — CP07 Evidence Review",
        "",
        "Review these actual CP05 MS-TCN evidence events for semantic/visual judgments. The CP06 package contains 21 category selections but only 13 unique event IDs; this handoff lists each unique event once and preserves its review reasons. The TAS-S label shown below is dataset ground truth at the event start, not a human-corrected label. Do not edit annotations or feed responses into training automatically.",
        "",
        "## Steps",
        "",
        "1. Open the linked clip and snapshot. If context is insufficient, use the source video at the listed timestamp.",
        "2. Complete one response row per event in `experiments/CP07/human_evidence_review.csv` using the fixed form below.",
        "3. Choose `ambiguous` or `not_enough_visual_evidence` when the action cannot be established. Do not infer the action from the model confidence or workflow order.",
        "4. Keep all event IDs. Save the completed file at the exact output path; leave the manifest unchanged.",
        "",
        "## Fixed response form",
        "",
        "```csv",
        "event_id,reviewer,judgment,corrected_action,boundary_judgment,semantic_note,reviewer_confidence",
        "<event_id>,<name>,<correct|incorrect|ambiguous|not_enough_visual_evidence>,<action_id|UNKNOWN>,<acceptable|incorrect|uncertain>,<brief visual basis>,<low|medium|high>",
        "```",
        "",
        "`corrected_action` is required only when judgment is incorrect and an action is clearly identifiable. Boundary judgment refers to whether the predicted event extent is acceptable on visual evidence. These are human review annotations, not official benchmark labels and not process-violation ground truth.",
        "",
        "## Event list",
        "",
        "| Event ID | Execution | Time (s) | TAS-S action at event start | Predicted | Confidence | Review reasons | Snapshot | Clip | Source video | Status |",
        "|---|---|---:|---|---|---:|---|---|---|---|---|",
    ]
    for event in manifest["events"]:
        handoff.append(
            f"| `{event['event_id']}` | `{event['video_id']}` | {event['timestamp_seconds']:.3f} | `{event['gt_action_at_event_start']}` | `{event['predicted_action']}` | {event['confidence']:.3f} | {', '.join(event['review_reasons'])} | `{event['snapshot']}` | `{event['clip']}` | `{event['source_video']}` | HUMAN_REVIEW_REQUIRED |"
        )
    (ROOT / "HUMAN_HANDOFF_CP07_EVIDENCE_REVIEW.md").write_text("\n".join(handoff) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
