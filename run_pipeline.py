from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from human_action.config import load_config  # noqa: E402
from human_action.evidence import attach_evidence  # noqa: E402
from human_action.pipeline import predict_video, write_timeline_svg  # noqa: E402
from human_action.schemas import to_dict  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the CP01 video → action → workflow → anomaly → evidence pipeline.")
    parser.add_argument("--config", default="configs/cp01.yaml")
    parser.add_argument("--input", required=True, help="Input video file")
    parser.add_argument("--model", choices=("mstcn", "framewise"), default="mstcn")
    parser.add_argument("--worker-id", default="W1")
    parser.add_argument("--video-id", default="", help="Known IMPACT identifier to load matching labels/features")
    parser.add_argument("--checkpoint", default="")
    parser.add_argument("--output-dir", default="")
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    config = load_config(config_path)
    video_path = Path(args.input).resolve()
    if not video_path.is_file():
        raise FileNotFoundError(video_path)
    output_dir = Path(args.output_dir).resolve() if args.output_dir else Path(config["evidence"]["output_dir"])
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir
    result = predict_video(video_path, args.video_id, args.worker_id, config, config_path, args.model, args.checkpoint or None)
    violations = attach_evidence(
        result["violations"],
        video_path,
        output_dir,
        float(config["evidence"]["context_seconds"]),
        float(config["evidence"]["clip_fps"]),
        bool(config["evidence"]["save_clip"]),
    )
    result["violations"] = violations
    result_path = output_dir / f"{result['video_id']}_{args.model}_result.json"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    serializable = {
        key: ([to_dict(item) for item in value] if key in {"events", "segments", "violations"} else (to_dict(value) if key == "workflow_state" else value))
        for key, value in result.items()
    }
    result_path.write_text(json.dumps(serializable, indent=2), encoding="utf-8")
    # The inference timeline is also rendered for direct review; GT is populated when this is a known dataset video.
    if args.video_id:
        from human_action.dataset import load_sequence
        sequence = load_sequence(config, args.video_id, "inference", config_path)
        gt = sequence.labels
        pred = result["segments"]
        pred_values = [0] * len(gt)
        class_to_id = {name: idx for idx, name in enumerate(config["actions"]["class_order"])}
        for segment in pred:
            start = int(round(segment.start_time / max(float(sequence.timestamps[1] - sequence.timestamps[0]), 1e-6))) if len(sequence.timestamps) > 1 else 0
            end = start + max(1, int(round(segment.duration / max(float(sequence.timestamps[1] - sequence.timestamps[0]), 1e-6)))) if len(sequence.timestamps) > 1 else len(gt)
            pred_values[max(0, start):min(len(gt), end)] = [class_to_id[segment.action]] * max(0, min(len(gt), end) - max(0, start))
        write_timeline_svg(output_dir / f"{args.video_id}_{args.model}_timeline.svg", sequence.timestamps, gt, __import__("numpy").asarray(pred_values), config["actions"]["class_order"])
    print(json.dumps({"result": str(result_path), "state": serializable["workflow_state"], "violations": [item["violation_type"] for item in serializable["violations"]], "events": len(serializable["events"])}, indent=2))


if __name__ == "__main__":
    main()
