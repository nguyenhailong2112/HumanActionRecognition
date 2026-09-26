from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize same-split framewise vs MS-TCN evaluation results.")
    parser.add_argument("--input", required=True, help="tools/evaluate.py metrics JSON")
    parser.add_argument("--output", help="Output JSON; defaults beside the input")
    args = parser.parse_args()
    source = Path(args.input)
    report = json.loads(source.read_text(encoding="utf-8"))
    by_model: dict[str, dict[str, dict]] = defaultdict(dict)
    for row in report.get("results", []):
        by_model[row["model"]][row["video_id"]] = row["action"]
    required = {"framewise", "mstcn"}
    if set(by_model) != required:
        raise ValueError(f"Expected exactly framewise and mstcn results; found {sorted(by_model)}")
    if set(by_model["framewise"]) != set(by_model["mstcn"]):
        raise ValueError("The two model results do not cover exactly the same videos")

    scalar_keys = ("frame_accuracy", "macro_f1_actions", "normalized_edit_score")
    segment_keys = ("F1@10", "F1@25", "F1@50")
    summary = {
        "experiment_id": report.get("experiment_id"),
        "split": report.get("split"),
        "aggregation": "Unweighted mean over videos; per-action F1 averages only videos with ground-truth support for that action.",
        "video_ids": sorted(by_model["framewise"]),
        "models": {},
        "delta_mstcn_minus_framewise": {},
    }
    for model_name, results in by_model.items():
        metrics = list(results.values())
        summary["models"][model_name] = {
            key: sum(item[key] for item in metrics) / len(metrics) for key in scalar_keys
        }
        summary["models"][model_name]["segmental"] = {
            key: sum(item["segmental"][key]["f1"] for item in metrics) / len(metrics)
            for key in segment_keys
        }
        class_rows: dict[str, list[float]] = defaultdict(list)
        for item in metrics:
            for label, values in item["per_class"].items():
                if values["support"] > 0:
                    class_rows[label].append(float(values["f1"]))
        summary["models"][model_name]["per_action_f1_mean_over_present_videos"] = {
            label: sum(values) / len(values) for label, values in sorted(class_rows.items())
        }
    for key in scalar_keys:
        summary["delta_mstcn_minus_framewise"][key] = summary["models"]["mstcn"][key] - summary["models"]["framewise"][key]
    summary["delta_mstcn_minus_framewise"]["segmental"] = {
        key: summary["models"]["mstcn"]["segmental"][key] - summary["models"]["framewise"]["segmental"][key]
        for key in segment_keys
    }
    output = Path(args.output) if args.output else source.with_name("baseline_comparison.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"[ok] baseline comparison: {output}")


if __name__ == "__main__":
    main()
