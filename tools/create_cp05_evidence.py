from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from human_action.config import load_config  # noqa: E402
from human_action.features import export_evidence_clip, extract_evidence_frame  # noqa: E402


def main() -> None:
    config_path = ROOT / "configs/cp05.yaml"
    config = load_config(config_path)
    timeline_dir = ROOT / "results/cp05/evaluation"
    output_dir = timeline_dir / "evidence"
    output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for video_id in sorted(configured_test_ids(config)):
        timeline_path = timeline_dir / f"{video_id}_mstcn_timeline.json"
        timeline = json.loads(timeline_path.read_text(encoding="utf-8"))
        video = Path(config["dataset"]["video_roots"][0]) / "front" / f"{video_id}.mp4"
        capture = cv2.VideoCapture(str(video))
        if not capture.isOpened():
            raise OSError(f"Cannot open source video {video}")
        fps = float(capture.get(cv2.CAP_PROP_FPS))
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        capture.release()
        for event_index, event in enumerate(timeline["events"], 1):
            if event["action"] == "NULL":
                continue
            frame_index = min(max(0, int(event["start_frame"])), frame_count - 1)
            observed_time = frame_index / fps
            if abs(observed_time - float(event["start_time"])) > 1 / fps + 1e-4:
                raise ValueError(f"Event/frame timestamp mismatch for {video_id} event {event_index}")
            stem = f"{video_id}_mstcn_{event_index:03d}_{frame_index}"
            image_path = output_dir / f"{stem}.jpg"
            clip_path = output_dir / f"{stem}.mp4"
            if not cv2.imwrite(str(image_path), extract_evidence_frame(video, frame_index)):
                raise OSError(f"Could not write evidence snapshot {image_path}")
            timestamp = float(event["start_time"])
            export_evidence_clip(video, clip_path, max(0, timestamp - 1), timestamp + 1, 10)
            records.append({
                "video_id": video_id,
                "model": "mstcn",
                "action": event["action"],
                "prediction_timestamp_seconds": timestamp,
                "action_event_timestamp_seconds": float(event["start_time"]),
                "action_event_start_frame": int(event["start_frame"]),
                "source_video_fps": fps,
                "source_video_frame_count": frame_count,
                "source_video_resolution": [width, height],
                "timestamp_frame_delta_seconds": abs(observed_time - timestamp),
                "confidence": float(event["confidence"]),
                "workflow_decision": "NOT_EVALUATED: no process-owner-approved workflow specification",
                "snapshot": str(image_path),
                "clip": str(clip_path),
                "clip_context_seconds": [max(0, timestamp - 1), timestamp + 1],
            })
    report = {
        "evidence_kind": "actual model inference events from held-out test videos",
        "model": "MS-TCN",
        "workflow_status": "NOT EVALUATED",
        "records": records,
    }
    (output_dir / "evidence_index.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"events": len(records), "index": str(output_dir / 'evidence_index.json')}))


def configured_test_ids(config: dict) -> list[str]:
    from human_action.impact_release import read_official_split
    protocol = config["dataset"]["official_split"]
    split_dir = ROOT / protocol["split_dir"]
    return read_official_split(split_dir, int(protocol["split_id"]), "test", protocol["procedure"], protocol["view"])


if __name__ == "__main__":
    main()
