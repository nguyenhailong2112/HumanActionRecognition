from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CP = ROOT / "experiments/CP06"


def main() -> None:
    metrics = json.loads((CP / "action_metrics.json").read_text(encoding="utf-8"))
    errors = json.loads((CP / "action_error_events.json").read_text(encoding="utf-8"))
    reliability = json.loads((CP / "seed_reliability.json").read_text(encoding="utf-8"))
    event_review = json.loads((CP / "evidence_review_manifest.json").read_text(encoding="utf-8"))
    cats = {}
    for error in errors["errors"]:
        cats[error["error_category"]] = cats.get(error["error_category"], 0) + 1
    md = ["# CP06 MS-TCN Action Error Analysis", "",
          "Scope: frozen CP05 MS-TCN frame predictions versus official TAS-S labels on the four held-out S2 executions. This is action-label error analysis, not process compliance evaluation.", "",
          "## Metrics", "",
          "| Aggregation | Accuracy | Macro-F1 | Edit | F1@10 | F1@25 | F1@50 | GT segments | Predicted segments |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    framewise = metrics["framewise_comparison"]
    fw = framewise["mean_per_execution"]
    md.append(f"| Framewise equal-execution mean | {fw['frame_accuracy']:.3f} | {fw['macro_f1_actions']:.3f} | {fw['normalized_edit_score']:.2f} | {fw['F1@10']:.3f} | {fw['F1@25']:.3f} | {fw['F1@50']:.3f} | — | — |")
    fwp = framewise["pooled_frames"]
    md.append(f"| Framewise pooled | {fwp['frame_accuracy']:.3f} | {fwp['macro_f1_actions']:.3f} | {fwp['normalized_edit_score']:.2f} | {fwp['segmental']['F1@10']['f1']:.3f} | {fwp['segmental']['F1@25']['f1']:.3f} | {fwp['segmental']['F1@50']['f1']:.3f} | {fwp['gt_action_segments']} | {fwp['pred_action_segments']} |")
    for label, row in (("Equal-execution mean", metrics["mean_per_execution"]), ("Pooled frames", metrics["pooled_frames"])):
        seg = row.get("segmental", {})
        md.append(f"| {label} | {row['frame_accuracy']:.3f} | {row['macro_f1_actions']:.3f} | {row['normalized_edit_score']:.2f} | {seg.get('F1@10', {}).get('f1', row.get('F1@10', 0)):.3f} | {seg.get('F1@25', {}).get('f1', row.get('F1@25', 0)):.3f} | {seg.get('F1@50', {}).get('f1', row.get('F1@50', 0)):.3f} | {row.get('gt_action_segments', '—')} | {row.get('pred_action_segments', '—')} |")
    md += ["", "Per-execution metrics, including segment counts, are in `action_metrics.json`. Sample standard deviation over the four execution metrics: "]
    md.append(", ".join(f"{k}={v:.3f}" for k, v in metrics["std_per_execution_sample"].items()) + ".")
    md += ["", "## Mismatch runs", "", f"Detected **{len(errors['errors'])}** contiguous raw-frame mismatch runs. Counts by exclusive primary diagnostic label: " + ", ".join(f"{k} {v}" for k, v in sorted(cats.items())) + ".",
           "", "| Rank | GT → prediction | Mismatched frames |", "|---:|---|---:|"]
    for i, item in enumerate(errors["top_confusions_by_frames"][:10], 1):
        md.append(f"| {i} | `{item['gt']}` → `{item['predicted']}` | {item['mismatched_frames']} |")
    per_class = metrics["pooled_frames"]["per_class"]
    supported = [(name, value) for name, value in per_class.items() if name != "NULL" and value["support"] > 0]
    md += ["", "## Class profile", "", "| Group | Action | Support (frames) | Precision | Recall | F1 |", "|---|---|---:|---:|---:|---:|"]
    for group, picked in (("Strong", sorted(supported, key=lambda pair: (-pair[1]["f1"], -pair[1]["support"]))[:4]), ("Weak", sorted(supported, key=lambda pair: (pair[1]["f1"], pair[1]["support"]))[:5])):
        for name, value in picked:
            md.append(f"| {group} | `{name}` | {value['support']} | {value['precision']:.3f} | {value['recall']:.3f} | {value['f1']:.3f} |")
    md += ["", "Additional patterns: pooled predicted action segments = 79 versus 97 GT segments (net under-segmentation by count), while one of four executions has more predicted than GT segments. That is not proof that all errors are merges/fragments. See `execution_diagnostics` for counts. Rule-based multi-tags: " + ", ".join(f"{k} {v}" for k, v in sorted(errors["diagnostic_tag_counts"].items())) + ".",
           "", f"Post-decoding comparison: temporal smoothing/short-segment processing changed {errors['temporal_postprocessing_comparison']['raw_correct_decoded_wrong_frames']} raw-correct frames to decoded-wrong and corrected {errors['temporal_postprocessing_comparison']['raw_wrong_decoded_correct_frames']} raw-wrong frames. This is a descriptive sample-level observation, not a tuning decision.",
           "", "`likely_visual_reason` and bottleneck attribution remain UNKNOWN / HUMAN_REVIEW_REQUIRED in `action_error_events.json`. Raw neural output cannot establish visibility, occlusion, annotation correctness, or camera ambiguity. Visual ambiguity and insufficient observation are reserved for human review. No duration or process anomaly metrics were evaluated."]
    (CP / "action_error_analysis.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    rows = []
    for category, items in event_review["selection"].items():
        rows.append(f"\n### {category}\n")
        rows.append("| Event ID | Execution | Time (s) | GT at event start | Predicted | Confidence | Source video | Snapshot | Clip | Status |")
        rows.append("|---|---|---:|---|---|---:|---|---|---|---|")
        for item in items:
            rows.append(f"| {item['event_id']} | `{item['video_id']}` | {item['timestamp_seconds']:.3f} | `{item['gt_action_at_event_start']}` | `{item['predicted_action']}` | {item['confidence']:.3f} | `{item['source_video']}` | `{item['snapshot']}` | `{item['clip']}` | HUMAN_REVIEW_REQUIRED |")
    handoff = ["# HUMAN HANDOFF — CP06 Evidence Review", "",
               "Review-only package from CP05 MS-TCN held-out inference. Event links point to the source video and matching CP05 snapshot/two-second context clip. The label shown as GT is the official TAS-S label at the event start, not a human-corrected label. Do not edit ground truth from this form. Each review remains HUMAN_REVIEW_REQUIRED until a human saves the form output.", "",
               "## Steps", "", "1. Open the clip, then use the source video at the timestamp when context is insufficient. Confirm the snapshot corresponds to the same event/time.", "2. Complete one form row per event below. Select only what is visually supportable; `ambiguous`, `occluded`, `out_of_view`, and `insufficient_observation` are valid outcomes.", "3. Keep all original IDs and fields. Save completed forms as `experiments/CP06/human_evidence_review.csv`. Do not edit TAS-S annotations or convert review results into labels automatically.", "",
               "## Fixed review form", "", "```csv", "event_id,reviewer,review_status,visually_supported_action,action_visible,occluded,out_of_view,ambiguous,insufficient_observation,notes", "CP05-MSTCN-XXX,<name>,<correct|incorrect|ambiguous|occluded|out_of_view|insufficient_observation>,<action ID or UNKNOWN>,<yes|no|partial>,<yes|no>,<yes|no>,<yes|no>,<yes|no>,<brief observation>", "```", "",
               "`review_status` and semantic judgments are human-owned. These selected candidates are stratified by confidence, mismatch, class rarity, boundary proximity and NULL leakage. A low-confidence event is only a review candidate, not automatically ambiguous.", ""]
    handoff.extend(rows)
    (ROOT / "HUMAN_HANDOFF_CP06_EVIDENCE_REVIEW.md").write_text("\n".join(handoff), encoding="utf-8")

    seeds = reliability["per_seed"]
    md = ["# CP06 MS-TCN Seed Reliability", "", reliability["protocol"], "", "Seed 17 is the frozen CP05 run; seeds 23 and 41 were newly trained with identical recipe and validation-only best-checkpoint selection. Test metrics below were only reported, never used for tuning.", "",
          "| Seed | Best val epoch | Best val loss | Train sec | Accuracy | Macro-F1 | Edit | F1@10 | F1@25 | F1@50 |", "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for seed, row in seeds.items():
        v = row["test_mean_per_execution"]
        md.append(f"| {seed} | {row['best_validation_epoch']} | {row['best_validation_loss']:.4f} | {row['train_seconds']:.1f} | {v['frame_accuracy']:.3f} | {v['macro_f1_actions']:.3f} | {v['normalized_edit_score']:.2f} | {v['F1@10']:.3f} | {v['F1@25']:.3f} | {v['F1@50']:.3f} |")
    md += ["", "| Metric | Mean across seed-level test means | Sample SD across seeds |", "|---|---:|---:|"]
    for metric, value in reliability["across_seed_test_mean"].items():
        md.append(f"| {metric} | {value:.4f} | {reliability['across_seed_test_sample_std'][metric]:.4f} |")
    md += ["", "Complete per-execution metrics for all three seeds are in `seed_reliability.json`. New checkpoints: `models/cp06_mstcn_seed23_best.pt`, `models/cp06_mstcn_seed23_final.pt`, and corresponding seed41 files. Configs are `configs/cp06_seed23.yaml` and `configs/cp06_seed41.yaml`; training reports retain every epoch's train/validation loss and separate test outputs. Framewise runs were also executed by the existing paired trainer for these seeds; the reliability comparison here is MS-TCN only.", ""]
    (CP / "seed_reliability.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
