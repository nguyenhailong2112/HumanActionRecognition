from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from human_action.config import load_config  # noqa: E402
from human_action.dataset import load_split, mapped_sequence  # noqa: E402
from human_action.pipeline import write_timeline_svg  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect an IMPACT split: videos, frame labels, action sequence and timeline.")
    parser.add_argument("--config", default="configs/cp01.yaml")
    parser.add_argument("--split", choices=("train", "val", "test"), default="train")
    args = parser.parse_args()
    config_path = Path(args.config).resolve()
    config = load_config(config_path)
    items = load_split(config, args.split, config_path)
    report = []
    for item in items:
        action_counts = Counter(config["actions"]["class_order"][int(label)] for label in item.labels)
        sequence = mapped_sequence(item.labels, config["actions"]["class_order"])
        report.append({
            "video_id": item.video_id,
            "video": str(item.video_path),
            "annotation": str(item.annotation_path),
            "worker_id": item.worker_id,
            "fps": item.fps,
            "frame_count": item.frame_count,
            "sampled_frames": len(item.labels),
            "duration_seconds": item.frame_count / item.fps,
            "label_frame_counts": dict(action_counts),
            "action_sequence": sequence,
        })
        output = PROJECT_ROOT / "data" / "processed" / "inspection" / f"{item.video_id}_ground_truth.svg"
        write_timeline_svg(output, item.timestamps, item.labels, item.labels, config["actions"]["class_order"])
        print(f"[ok] ground-truth timeline: {output}")
    print(json.dumps({"dataset": config["dataset"]["name"], "version": config["dataset"]["version"], "view": config["dataset"]["view"], "split": args.split, "records": report}, indent=2))


if __name__ == "__main__":
    main()
