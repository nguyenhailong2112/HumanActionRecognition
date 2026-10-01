from __future__ import annotations

import argparse
import bisect
import csv
import hashlib
import json
import math
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from human_action.config import load_config, project_path  # noqa: E402
from human_action.impact_release import read_official_split  # noqa: E402
from human_action.pipeline import load_checkpoint, predict_features  # noqa: E402
from human_action.schemas import ActionEvent, ActionSegment, to_dict  # noqa: E402
from human_action.temporal import decode_segments, to_action_events  # noqa: E402


CSV_FIELDS = (
    "execution_id", "worker_id", "view", "action", "start_time", "end_time",
    "duration", "start_frame", "end_frame", "model_id", "checkpoint",
    "feature_source", "confidence",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def segment_index_at_time(timestamp: float, segments: list[dict[str, Any]]) -> int | None:
    """Return the half-open interval segment covering source-video time."""
    if not segments or not math.isfinite(timestamp):
        return None
    starts = [float(segment["start_time"]) for segment in segments]
    index = bisect.bisect_right(starts, timestamp) - 1
    if index < 0 or timestamp >= float(segments[index]["end_time"]):
        return None
    return index


def frame_to_segment_index(frame_index: int, fps: float, segments: list[dict[str, Any]]) -> int | None:
    if frame_index < 0 or not math.isfinite(fps) or fps <= 0:
        return None
    return segment_index_at_time(frame_index / fps, segments)


def _split_membership(config: dict[str, Any], config_path: Path) -> dict[str, list[str]]:
    protocol = config["dataset"]["official_split"]
    split_dir = project_path(config_path, protocol["split_dir"])
    return {
        split_name: read_official_split(
            split_dir, int(protocol["split_id"]), split_name,
            str(protocol["procedure"]), str(protocol["view"]),
        )
        for split_name in ("train", "val", "test")
    }


def _verify_test_execution(video_id: str, config: dict[str, Any], config_path: Path) -> dict[str, list[str]]:
    membership = _split_membership(config, config_path)
    counts = {name: len(ids) for name, ids in membership.items()}
    if counts != {"train": 39, "val": 5, "test": 4}:
        raise ValueError(f"Frozen CP12 split counts changed: {counts}")
    test_workers = {item.split("_", 1)[0] for item in membership["test"]}
    if test_workers != {"SS07EL13"}:
        raise ValueError(f"Frozen CP12 held-out worker changed: {sorted(test_workers)}")
    if video_id not in membership["test"]:
        raise ValueError(f"{video_id} is not in the configured frozen held-out test split")
    return membership


def _video_metadata(video_path: Path) -> dict[str, Any]:
    capture = cv2.VideoCapture(str(video_path))
    try:
        if not capture.isOpened():
            raise OSError(f"Could not open source video: {video_path}")
        ok, first_frame = capture.read()
        if not ok or first_frame is None:
            raise OSError(f"Could not decode the first source frame: {video_path}")
        fps = float(capture.get(cv2.CAP_PROP_FPS))
        frame_count = int(round(capture.get(cv2.CAP_PROP_FRAME_COUNT)))
        height, width = first_frame.shape[:2]
        if not math.isfinite(fps) or fps <= 0 or frame_count <= 0:
            raise ValueError(f"Invalid source video metadata: fps={fps}, frames={frame_count}")
        return {"fps": fps, "frame_count": frame_count, "width": width, "height": height}
    finally:
        capture.release()


def _load_sampled_features(
    feature_path: Path,
    source_frame_count: int,
    source_fps: float,
    sample_fps: float,
    expected_dimension: int,
) -> tuple[np.ndarray, np.ndarray]:
    raw = np.load(feature_path, allow_pickle=False)
    if raw.ndim != 2 or raw.shape != (source_frame_count, expected_dimension):
        raise ValueError(
            "Official I3D features must be frame-aligned T×D with one row per source frame; "
            f"got {raw.shape}, expected {(source_frame_count, expected_dimension)}"
        )
    if not np.issubdtype(raw.dtype, np.number) or not np.isfinite(raw).all():
        raise ValueError(f"Feature array must contain finite numeric values: {feature_path}")
    stride_value = source_fps / sample_fps
    stride = int(round(stride_value))
    if stride < 1 or not math.isclose(stride_value, stride, rel_tol=0, abs_tol=1e-6):
        raise ValueError(f"Source/sample FPS do not define an integer feature stride: {source_fps}/{sample_fps}")
    indices = np.arange(0, source_frame_count, stride, dtype=np.int64)
    sampled = np.asarray(raw[indices], dtype=np.float32)
    if not np.isfinite(sampled).all() or len(sampled) != len(indices):
        raise ValueError("Sampled feature sequence is invalid")
    return sampled, indices


def _validate_segments(
    decoded: list[ActionSegment],
    class_order: list[str],
    frame_count: int,
    fps: float,
) -> list[dict[str, Any]]:
    duration = frame_count / fps
    rows = []
    previous_start = -1.0
    previous_end = 0.0
    for segment in decoded:
        if segment.action not in class_order:
            raise ValueError(f"Predicted label is outside configured model vocabulary: {segment.action}")
        start = float(segment.start_time)
        end = min(float(segment.end_time), duration)
        confidence = float(segment.confidence)
        if not math.isfinite(start) or not math.isfinite(end) or start < 0 or end <= start:
            raise ValueError(f"Invalid predicted segment interval: [{start}, {end})")
        if not math.isfinite(confidence) or not 0.0 <= confidence <= 1.0:
            raise ValueError(f"Invalid model score for predicted segment: {confidence}")
        if start < previous_start or start < previous_end - 1e-5:
            raise ValueError("Predicted segments are not ordered and non-overlapping")
        if segment.start_frame < 0 or segment.end_frame < segment.start_frame or segment.end_frame >= frame_count:
            raise ValueError(f"Invalid source frame bounds for predicted segment: {segment}")
        rows.append({
            "action": segment.action,
            "start_time": start,
            "end_time": end,
            "duration": end - start,
            "start_frame": int(segment.start_frame),
            "end_frame": int(segment.end_frame),
            "confidence": float(segment.confidence),
        })
        previous_start, previous_end = start, end
    if not rows or rows[0]["start_time"] > 1.0 / fps:
        raise ValueError("Predicted timeline does not start near source-video time zero")
    if rows[-1]["end_time"] < duration - 1.0 / fps:
        raise ValueError("Predicted timeline does not cover the end of the source video")
    return rows


def _class_colors(class_order: list[str]) -> dict[str, tuple[int, int, int]]:
    palette = [
        (115, 115, 115), (220, 105, 45), (65, 145, 225), (80, 180, 100),
        (190, 90, 185), (30, 180, 210), (190, 155, 55), (90, 110, 210),
        (160, 105, 65), (90, 180, 170), (175, 90, 110), (100, 150, 70),
        (130, 100, 190), (70, 130, 180), (175, 145, 90), (75, 170, 125),
        (165, 105, 175), (110, 130, 145),
    ]
    return {label: palette[index % len(palette)] for index, label in enumerate(class_order)}


def _put_text(image: np.ndarray, text: str, point: tuple[int, int], scale: float, color=(245, 248, 252), thickness=1) -> None:
    cv2.putText(image, text, point, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness, cv2.LINE_AA)


def _render_frame(
    frame: np.ndarray,
    timestamp: float,
    duration: float,
    source_fps: float,
    segments: list[dict[str, Any]],
    colors: dict[str, tuple[int, int, int]],
    execution_id: str,
    model_id: str,
    feature_summary: str,
) -> np.ndarray:
    height, width = frame.shape[:2]
    panel_height = 178
    canvas = np.zeros((height + panel_height, width, 3), dtype=np.uint8)
    canvas[:height] = frame
    scale = max(0.48, min(0.78, width / 1650.0))
    index = segment_index_at_time(timestamp, segments)
    current = segments[index] if index is not None else None

    original = canvas[:height].copy()
    overlay = original.copy()
    cv2.rectangle(overlay, (0, 0), (width, min(136, height)), (10, 16, 25), -1)
    canvas[:height] = cv2.addWeighted(overlay, 0.78, original, 0.22, 0)
    _put_text(canvas, "HUMAN ACTION  |  IMPACT v1.1 TAS-S  |  Disassembly_A / FRONT", (22, 28), scale * .78, (120, 220, 255), 2)
    action = current["action"] if current else "NO PREDICTED SEGMENT"
    score = current["confidence"] if current else float("nan")
    action_color = colors.get(action, (230, 230, 230))
    action_scale = max(.52, min(.90, (width - 42) / max(cv2.getTextSize(action, cv2.FONT_HERSHEY_SIMPLEX, .9, 2)[0][0], 1) * .9))
    _put_text(canvas, f"PREDICTED ACTION: {action}", (22, 67), action_scale, action_color, 2)
    if current:
        segment_text = (
            f"TIME {timestamp:.2f}s / {duration:.2f}s    "
            f"SEGMENT {current['start_time']:.2f}s - {current['end_time']:.2f}s    "
            f"LENGTH {current['duration']:.2f}s    MODEL SCORE {score:.3f}"
        )
    else:
        segment_text = f"TIME {timestamp:.2f}s / {duration:.2f}s    MODEL SCORE unavailable"
    _put_text(canvas, segment_text, (22, 103), scale * .67)
    _put_text(canvas, f"EXECUTION {execution_id}    FRAME {round(timestamp * source_fps)}", (22, 128), scale * .53, (205, 213, 224))

    panel_y = height
    cv2.rectangle(canvas, (0, panel_y), (width, height + panel_height), (14, 20, 30), -1)
    _put_text(canvas, "PREDICTED ACTION TIMELINE  |  color = action segment  |  cyan marker = current source time", (20, panel_y + 26), scale * .61, (225, 234, 244))
    left, right = 22, width - 22
    bar_y, bar_height = panel_y + 39, 27
    cv2.rectangle(canvas, (left, bar_y), (right, bar_y + bar_height), (43, 52, 65), -1)
    for segment in segments:
        x0 = left + int((segment["start_time"] / duration) * (right - left))
        x1 = left + int((segment["end_time"] / duration) * (right - left))
        x1 = max(x0 + 1, min(right, x1))
        cv2.rectangle(canvas, (x0, bar_y), (x1, bar_y + bar_height), colors.get(segment["action"], (120, 120, 120)), -1)
        if index is not None and segment is segments[index]:
            cv2.rectangle(canvas, (x0, bar_y - 2), (x1, bar_y + bar_height + 2), (255, 235, 75), 2)
    cursor_x = left + int(min(1.0, max(0.0, timestamp / duration)) * (right - left))
    cv2.line(canvas, (cursor_x, bar_y - 5), (cursor_x, bar_y + bar_height + 5), (255, 255, 255), 2, cv2.LINE_AA)
    _put_text(canvas, "0s", (left, bar_y + 48), scale * .47, (175, 187, 203))
    end_label = f"{duration:.1f}s"
    text_width = cv2.getTextSize(end_label, cv2.FONT_HERSHEY_SIMPLEX, scale * .47, 1)[0][0]
    _put_text(canvas, end_label, (right - text_width, bar_y + 48), scale * .47, (175, 187, 203))
    _put_text(canvas, f"MODEL: {model_id}  |  INFERENCE ONLY", (22, panel_y + 105), scale * .65, (185, 215, 255))
    _put_text(canvas, f"INPUT: official I3D {feature_summary}    VIEW: FRONT", (22, panel_y + 130), scale * .59, (205, 213, 224))
    _put_text(canvas, "Model score is an uncalibrated softmax score  |  Action prediction only  |  No process judgment", (22, panel_y + 155), scale * .57, (175, 187, 203))
    return canvas


def _render_video(
    video_path: Path,
    output_path: Path,
    metadata: dict[str, Any],
    segments: list[dict[str, Any]],
    class_order: list[str],
    execution_id: str,
    model_id: str,
    feature_summary: str,
) -> dict[str, Any]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise OSError(f"Could not reopen source video for rendering: {video_path}")
    fps = metadata["fps"]
    frame_count = metadata["frame_count"]
    duration = frame_count / fps
    colors = _class_colors(class_order)
    writer = None
    rendered = 0
    try:
        first = None
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            if first is None:
                height, width = frame.shape[:2]
                writer = cv2.VideoWriter(
                    str(output_path), cv2.VideoWriter_fourcc(*"mp4v"), fps,
                    (width, height + 178),
                )
                if not writer.isOpened():
                    raise OSError("OpenCV could not initialize an MP4V output writer")
                first = True
            if rendered >= frame_count:
                raise ValueError("Source video decoded more frames than the advertised frame count")
            timestamp = rendered / fps
            if segment_index_at_time(timestamp, segments) is None:
                raise ValueError(f"Prediction timeline does not map source frame {rendered} at {timestamp:.3f}s")
            canvas = _render_frame(frame, timestamp, duration, fps, segments, colors, execution_id,
                                   model_id, feature_summary)
            writer.write(canvas)
            rendered += 1
    finally:
        capture.release()
        if writer is not None:
            writer.release()
    if rendered != frame_count:
        raise ValueError(f"Decoded source frame count mismatch: expected {frame_count}, got {rendered}")
    if not output_path.is_file() or output_path.stat().st_size == 0:
        raise OSError(f"Output video was not written: {output_path}")
    check = cv2.VideoCapture(str(output_path))
    try:
        if not check.isOpened():
            raise OSError(f"Rendered video cannot be reopened: {output_path}")
        ok, sample = check.read()
        output_fps = float(check.get(cv2.CAP_PROP_FPS))
        output_width = int(round(check.get(cv2.CAP_PROP_FRAME_WIDTH)))
        output_height = int(round(check.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        if not ok or sample is None:
            raise ValueError("Rendered video does not decode its first frame")
        output_count = 1
        while True:
            ok, sample = check.read()
            if not ok:
                break
            if sample is None:
                raise ValueError("Rendered video yielded an invalid decoded frame")
            output_count += 1
        if output_count != frame_count:
            raise ValueError(f"Rendered video verification failed: decoded {output_count}/{frame_count} frames")
        if output_width != metadata["width"] or output_height != metadata["height"] + 178:
            raise ValueError(f"Rendered video has unexpected dimensions: {output_width}x{output_height}")
        if not math.isclose(output_fps, fps, rel_tol=.01, abs_tol=.05):
            raise ValueError(f"Rendered FPS {output_fps} does not match source FPS {fps}")
        return {"codec": "mp4v", "frame_count": output_count, "decoded_frame_count_verified": output_count,
                "reopened_and_decoded_all_frames": True, "fps": output_fps,
                "width": output_width, "height": output_height,
                "size_bytes": output_path.stat().st_size,
                "sha256": sha256_file(output_path)}
    finally:
        check.release()


def run_demo(video_path: Path, feature_path: Path, checkpoint_path: Path,
             config_path: Path, output_dir: Path) -> dict[str, Any]:
    for path, name in ((video_path, "video"), (feature_path, "feature"),
                       (checkpoint_path, "checkpoint"), (config_path, "config")):
        if not path.is_file():
            raise FileNotFoundError(f"{name} file does not exist: {path}")
    video_id = video_path.stem
    worker_id = video_id.split("_", 1)[0]
    config = load_config(config_path)
    dataset = config["dataset"]
    if dataset.get("source") != "impact_official_release":
        raise ValueError("CP12 demo expects the frozen official IMPACT release configuration")
    if dataset.get("view") != "front":
        raise ValueError("CP12 demo is frozen to the front view")
    split_ids = _verify_test_execution(video_id, config, config_path)

    video_info = _video_metadata(video_path)
    sample_fps = float(dataset["sample_fps"])
    raw_feature = np.load(feature_path, mmap_mode="r", allow_pickle=False)
    raw_shape, raw_dtype = tuple(raw_feature.shape), str(raw_feature.dtype)
    del raw_feature
    features, frame_indices = _load_sampled_features(
        feature_path, video_info["frame_count"], video_info["fps"], sample_fps,
        int(dataset["feature_dimension"]),
    )
    timestamps = (frame_indices / video_info["fps"]).astype(np.float32)

    model, mean, std, device, actual_checkpoint = load_checkpoint(
        config, config_path, "mstcn", checkpoint_path,
    )
    checkpoint = torch.load(actual_checkpoint, map_location="cpu", weights_only=True)
    if checkpoint.get("model_kind") != "mstcn":
        raise ValueError("Selected checkpoint is not an MS-TCN checkpoint")
    if checkpoint.get("class_order") != config["actions"]["class_order"]:
        raise ValueError("Frozen checkpoint class order differs from experiment config")
    model_id = (
        f"Our MS-TCN | {config.get('experiment_id', 'frozen experiment')} "
        f"seed-{config.get('seed', 'unknown')} | validation-selected {actual_checkpoint.name}"
    )

    if device.type == "cuda":
        torch.cuda.synchronize(device)
    started = time.perf_counter()
    predicted, probabilities = predict_features(model, features, mean, std, device)
    if device.type == "cuda":
        torch.cuda.synchronize(device)
    inference_seconds = time.perf_counter() - started
    if len(predicted) != len(features) or probabilities.shape != (len(features), len(config["actions"]["class_order"])):
        raise ValueError("Model output length/class shape is incompatible with sampled I3D features")
    if not np.isfinite(probabilities).all() or np.any((probabilities < 0) | (probabilities > 1)):
        raise ValueError("Model returned invalid class probabilities")

    temporal = config["temporal"]
    decoded = decode_segments(
        predicted, probabilities, config["actions"]["class_order"], timestamps, frame_indices,
        int(temporal["smoothing_window"]), float(temporal["min_segment_seconds"]),
    )
    segments = _validate_segments(decoded, config["actions"]["class_order"],
                                  video_info["frame_count"], video_info["fps"])
    feature_summary = f"{len(features)}x{features.shape[1]} @ {sample_fps:g} FPS (stride {frame_indices[1] if len(frame_indices) > 1 else 1}) from {raw_shape[0]}x{raw_shape[1]} @ {video_info['fps']:g} FPS"

    output_dir.mkdir(parents=True, exist_ok=True)
    for row in segments:
        row.update({
            "execution_id": video_id,
            "worker_id": worker_id,
            "view": str(dataset["view"]),
            "model_id": model_id,
            "checkpoint": str(actual_checkpoint.resolve()),
            "feature_source": str(feature_path.resolve()),
        })
    segment_payload = {
        "execution_id": video_id,
        "worker_id": worker_id,
        "view": dataset["view"],
        "model_id": model_id,
        "checkpoint": str(actual_checkpoint.resolve()),
        "feature_source": str(feature_path.resolve()),
        "feature_sampling": {"raw_shape": raw_shape, "raw_dtype": raw_dtype,
                             "sampled_shape": list(features.shape), "sample_fps": sample_fps,
                             "stride_frames": int(frame_indices[1] if len(frame_indices) > 1 else 1)},
        "segments": segments,
    }
    prediction_json = output_dir / "prediction_segments.json"
    prediction_json.write_text(json.dumps(segment_payload, indent=2), encoding="utf-8")
    prediction_csv = output_dir / "prediction_segments.csv"
    with prediction_csv.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows({key: row[key] for key in CSV_FIELDS} for row in segments)

    action_segments = [ActionSegment(
        action=row["action"], start_time=row["start_time"], end_time=row["end_time"],
        duration=row["duration"], confidence=row["confidence"],
        start_frame=row["start_frame"], end_frame=row["end_frame"],
    ) for row in segments]
    action_events: list[ActionEvent] = to_action_events(
        action_segments, worker_id, video_id, config["actions"]["background"], dataset["view"],
    )
    events_path = output_dir / "action_events.json"
    events_path.write_text(json.dumps([to_dict(event) for event in action_events], indent=2), encoding="utf-8")

    output_video = output_dir / "demo_video.mp4"
    rendering_started = time.perf_counter()
    rendered_info = _render_video(
        video_path, output_video, video_info, segments, config["actions"]["class_order"],
        video_id, model_id, feature_summary,
    )
    render_seconds = time.perf_counter() - rendering_started
    duration = video_info["frame_count"] / video_info["fps"]
    manifest = {
        "checkpoint": "CP12 Human Action inference demo",
        "status": "LOCALLY_EXECUTED",
        "execution_id": video_id,
        "worker_id": worker_id,
        "view": dataset["view"],
        "split": {"dataset": f"{dataset['name']} {dataset['version']}", "task": "TAS-S",
                  "protocol": dataset["official_split"]["name"],
                  "split_id": int(dataset["official_split"]["split_id"]),
                  "procedure": dataset["official_split"]["procedure"],
                  "membership_verified": True,
                  "execution_ids": {"train": split_ids["train"], "validation": split_ids["val"], "test": split_ids["test"]},
                  "held_out_test_ids": split_ids["test"],
                  "counts": {"train": len(split_ids["train"]), "validation": len(split_ids["val"]), "test": len(split_ids["test"])}},
        "inputs": {
            "video": {"path": str(video_path.resolve()), "size_bytes": video_path.stat().st_size,
                      "sha256": sha256_file(video_path), **video_info},
            "features": {"path": str(feature_path.resolve()), "size_bytes": feature_path.stat().st_size,
                         "sha256": sha256_file(feature_path), "raw_shape": raw_shape,
                         "dtype": raw_dtype, "sampled_shape": list(features.shape),
                         "sample_fps": sample_fps,
                         "stride_frames": int(frame_indices[1] if len(frame_indices) > 1 else 1),
                         "finite_values_verified": True},
            "config": {"path": str(config_path.resolve()), "sha256": sha256_file(config_path)},
            "checkpoint": {"path": str(actual_checkpoint.resolve()), "sha256": sha256_file(actual_checkpoint),
                           "kind": "mstcn", "best_epoch": checkpoint.get("best_epoch"),
                           "best_validation_loss": checkpoint.get("best_val_loss"),
                           "class_order": checkpoint["class_order"]},
        },
        "model": {"id": model_id, "architecture": "MSTCN", "inference_only": True,
                  "device": str(device), "pytorch": str(torch.__version__),
                  "cuda_available": bool(torch.cuda.is_available()),
                  "gpu": torch.cuda.get_device_name(device) if device.type == "cuda" else None,
                  "feature_inference_seconds": inference_seconds,
                  "feature_vectors_per_second": len(features) / max(inference_seconds, 1e-12)},
        "outputs": {
            "video": {"path": str(output_video.resolve()), **rendered_info},
            "segments_json": str(prediction_json.resolve()),
            "segments_csv": str(prediction_csv.resolve()),
            "action_events_json": str(events_path.resolve()),
            "segment_count_including_background": len(segments),
            "action_event_count_excluding_background": len(action_events),
        },
        "rendering_seconds": render_seconds,
        "timeline": {"duration_seconds": duration, "source_frames": video_info["frame_count"],
                     "output_frames": rendered_info["frame_count"],
                     "prediction_timeline_covers_source": True},
        "evidence_status": "unknown",
        "warnings": [
            "Softmax score is an uncalibrated model score, not evidence sufficiency.",
            "Output is action inference only; no workflow or process-compliance interpretation is produced.",
            "OpenCV output is video-only and does not copy source audio.",
        ],
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"execution_id": video_id, "output_video": str(output_video),
                      "segments": len(segments), "events": len(action_events),
                      "inference_seconds": inference_seconds, "render_seconds": render_seconds,
                      "manifest": str(manifest_path)}, indent=2))
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run frozen IMPACT action inference and render an inspectable prediction-only video demo."
    )
    parser.add_argument("--video", required=True, type=Path, help="Held-out source video")
    parser.add_argument("--features", required=True, type=Path, help="Official frame-aligned I3D .npy file")
    parser.add_argument("--checkpoint", required=True, type=Path, help="Frozen CP05/CP06 MS-TCN checkpoint")
    parser.add_argument("--config", required=True, type=Path, help="Frozen CP05 experiment YAML")
    parser.add_argument("--output-dir", required=True, type=Path, help="Execution-specific output directory")
    args = parser.parse_args()
    try:
        run_demo(args.video.resolve(), args.features.resolve(), args.checkpoint.resolve(),
                 args.config.resolve(), args.output_dir.resolve())
    except Exception as error:
        parser.exit(2, f"CP12 demo failed: {error}\n")


if __name__ == "__main__":
    main()
