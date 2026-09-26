from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from human_action.config import load_config  # noqa: E402
from human_action.dataset import load_split  # noqa: E402
from human_action.pipeline import evaluate_video, write_timeline_svg  # noqa: E402
from human_action.schemas import to_dict  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate action segmentation and procedure outputs on a configured split.")
    parser.add_argument("--config", default="configs/cp01.yaml")
    parser.add_argument("--split", choices=("train", "val", "test"), default="test")
    parser.add_argument("--model", choices=("mstcn", "framewise", "both"), default="both")
    args = parser.parse_args()
    config_path = Path(args.config).resolve()
    config = load_config(config_path)
    models = ("framewise", "mstcn") if args.model == "both" else (args.model,)
    result = {"experiment_id": config["experiment_id"], "split": args.split, "evidence_boundary": "Action metrics use official TAS-S labels. Process workflow metrics are NOT EVALUATED until the process owner approves a workflow; PPR anomaly/recovery labels have a different per-hand procedural-phase target and are not equivalent to workflow violation ground truth.", "results": []}
    output_dir = PROJECT_ROOT / config["evidence"]["output_dir"] / "evaluation"
    output_dir.mkdir(parents=True, exist_ok=True)
    split_ids = [sequence.video_id for sequence in load_split(config, args.split, config_path)]
    for model_kind in models:
        for video_id in split_ids:
            item = evaluate_video(video_id, args.split, config, config_path, model_kind)
            result["results"].append({key: value for key, value in item.items() if key not in {"probabilities", "timestamps", "frame_indices", "ground_truth_labels", "predicted_labels", "segments", "events"}})
            import numpy as np
            write_timeline_svg(
                output_dir / f"{video_id}_{model_kind}_gt_vs_pred.svg",
                np.asarray(item["timestamps"]),
                np.asarray(item["ground_truth_labels"]),
                np.asarray(item["predicted_labels"]),
                config["actions"]["class_order"],
            )
            # Save full decoded timelines (small temporal arrays) for error inspection.
            timeline = {
                "video_id": video_id,
                "model": model_kind,
                "segments": item["segments"],
                "events": item["events"],
                "workflow_state": item["process"]["completed"],
            }
            (output_dir / f"{video_id}_{model_kind}_timeline.json").write_text(json.dumps(timeline, indent=2), encoding="utf-8")
    report_path = output_dir / f"{args.split}_metrics.json"
    report_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"[ok] evaluation report: {report_path}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
