from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch

from .dataset import load_sequence, mapped_sequence
from .features import extract_video_features
from .metrics import action_metrics, sequence_exact_match, violation_counts
from .model import FramewiseBaseline, MSTCN
from .schemas import ActionEvent, to_dict
from .temporal import decode_segments, to_action_events
from .workflow import WorkflowEngine, workflow_is_enabled


def create_model(config: dict[str, Any], model_kind: str) -> torch.nn.Module:
    model_cfg = config["model"]
    num_classes = len(config["actions"]["class_order"])
    if model_kind == "mstcn":
        return MSTCN(int(model_cfg["input_dim"]), int(model_cfg["hidden_dim"]), int(model_cfg["layers"]), int(model_cfg["stages"]), num_classes, float(model_cfg["dropout"]))
    if model_kind == "framewise":
        return FramewiseBaseline(int(model_cfg["input_dim"]), num_classes)
    raise ValueError(f"Unknown model kind: {model_kind}")


def load_checkpoint(config: dict[str, Any], config_path: str | Path, model_kind: str, checkpoint_path: str | Path | None = None):
    project_root = Path(config_path).resolve().parent.parent
    default = config["model"]["checkpoint"] if model_kind == "mstcn" else config["model"]["baseline_checkpoint"]
    path = Path(checkpoint_path) if checkpoint_path else project_root / default
    if not path.is_absolute():
        path = project_root / path
    if not path.is_file():
        raise FileNotFoundError(f"Model checkpoint not found: {path}. Train the configured model with `python tools/train_baseline.py --config {config_path}` first.")
    device = torch.device(config.get("runtime", {}).get("device", "cpu"))
    checkpoint = torch.load(path, map_location=device, weights_only=True)
    if checkpoint.get("class_order") != config["actions"]["class_order"]:
        raise ValueError("Checkpoint action classes do not match the current config")
    model = create_model(config, model_kind).to(device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    mean = np.asarray(checkpoint["feature_mean"].cpu(), dtype=np.float32)
    std = np.asarray(checkpoint["feature_std"].cpu(), dtype=np.float32)
    return model, mean, std, device, path


def predict_features(model: torch.nn.Module, features: np.ndarray, mean: np.ndarray, std: np.ndarray, device: torch.device) -> tuple[np.ndarray, np.ndarray]:
    mean = np.asarray(mean.detach().cpu() if isinstance(mean, torch.Tensor) else mean, dtype=np.float32)
    std = np.asarray(std.detach().cpu() if isinstance(std, torch.Tensor) else std, dtype=np.float32)
    normalized = (features - mean[None, :]) / np.maximum(std[None, :], 1e-5)
    x = torch.from_numpy(normalized.T.copy()).unsqueeze(0).to(device)
    with torch.inference_mode():
        outputs = model(x)
        logits = outputs[-1] if outputs.ndim == 4 else outputs[0]
        probabilities = torch.softmax(logits, dim=1)[0].cpu().numpy().T
    return probabilities.argmax(axis=1), probabilities


def predict_video(video_path: Path, video_id: str, worker_id: str, config: dict[str, Any], config_path: str | Path, model_kind: str, checkpoint_path: str | Path | None = None):
    run_workflow = workflow_is_enabled(config)
    model, mean, std, device, actual_checkpoint = load_checkpoint(config, config_path, model_kind, checkpoint_path)
    if video_id:
        # Prefer annotation-aligned cached loader for a known IMPACT release sample.
        sequence = load_sequence(config, video_id, "inference", config_path)
        features, timestamps, frame_indices = sequence.features, sequence.timestamps, sequence.frame_indices
        fps, frame_count = sequence.fps, sequence.frame_count
    else:
        features, timestamps, fps, frame_count = extract_video_features(
            video_path,
            float(config["dataset"]["sample_fps"]),
            int(config["features"]["image_size"]),
            int(config["features"]["difference_size"]),
        )
        stride = max(1, int(round(fps / float(config["dataset"]["sample_fps"]))))
        frame_indices = np.arange(len(features), dtype=np.int64) * stride
    predictions, probabilities = predict_features(model, features, mean, std, device)
    temporal = config["temporal"]
    segments = decode_segments(
        predictions,
        probabilities,
        config["actions"]["class_order"],
        timestamps,
        frame_indices,
        int(temporal["smoothing_window"]),
        float(temporal["min_segment_seconds"]),
    )
    events = to_action_events(segments, worker_id, video_id or video_path.stem, config["actions"]["background"], config["dataset"].get("view", ""))
    final_result = None
    if run_workflow:
        engine = WorkflowEngine(config, worker_id, video_id or video_path.stem)
        engine.consume(events)
        final_result = engine.finalize(float(frame_count / fps))
    return {
        "video_path": str(video_path),
        "video_id": video_id or video_path.stem,
        "worker_id": worker_id,
        "fps": fps,
        "frame_count": frame_count,
        "duration_seconds": frame_count / fps,
        "model": model_kind,
        "checkpoint": str(actual_checkpoint),
        "events": events,
        "segments": segments,
        "workflow_state": final_result.state if final_result else None,
        "violations": final_result.violations if final_result else [],
    }


def evaluate_video(video_id: str, split: str, config: dict[str, Any], config_path: str | Path, model_kind: str, checkpoint_path: str | Path | None = None) -> dict:
    run_workflow = workflow_is_enabled(config)
    sequence = load_sequence(config, video_id, split, config_path)
    model, mean, std, device, actual_checkpoint = load_checkpoint(config, config_path, model_kind, checkpoint_path)
    if device.type == "cuda":
        torch.cuda.synchronize(device)
    inference_started = time.perf_counter()
    predicted, probabilities = predict_features(model, sequence.features, mean, std, device)
    if device.type == "cuda":
        torch.cuda.synchronize(device)
    inference_seconds = time.perf_counter() - inference_started
    metrics = action_metrics(sequence.labels, predicted, config["actions"]["class_order"], background_id=0)
    temporal = config["temporal"]
    segments = decode_segments(predicted, probabilities, config["actions"]["class_order"], sequence.timestamps, sequence.frame_indices, int(temporal["smoothing_window"]), float(temporal["min_segment_seconds"]))
    events = to_action_events(segments, sequence.worker_id, video_id, config["actions"]["background"], config["dataset"].get("view", ""))
    process = None
    if run_workflow:
        engine = WorkflowEngine(config, sequence.worker_id, video_id)
        engine.consume(events)
        process = engine.finalize(float(sequence.frame_count / sequence.fps))
    gt_events = mapped_sequence(sequence.labels, config["actions"]["class_order"])
    pred_events = [event.action for event in events]
    return {
        "video_id": video_id,
        "split": split,
        "model": model_kind,
        "checkpoint": str(actual_checkpoint),
        "action": metrics,
        "runtime": {
            "mode": "offline_full_sequence_inference",
            "device": str(device),
            "feature_vectors": int(len(sequence.features)),
            "sequence_inference_seconds": inference_seconds,
            "feature_vectors_per_second": float(len(sequence.features) / max(inference_seconds, 1e-12)),
            "milliseconds_per_feature_vector": float(1000.0 * inference_seconds / max(len(sequence.features), 1)),
            "offline_speedup_x": float((sequence.frame_count / sequence.fps) / max(inference_seconds, 1e-12)),
        },
        "process": {
            "ground_truth_action_sequence": gt_events,
            "predicted_action_sequence": pred_events,
            "sequence_exact_match": sequence_exact_match(gt_events, pred_events),
            "workflow_status": "EVALUATED" if process else "NOT EVALUATED: awaiting process-owner-approved procedure path",
            "selected_workflow_path": process.selected_path if process else None,
            "completed": process.state.completed if process else None,
            "predicted_violations": [to_dict(item) for item in process.violations] if process else [],
            "predicted_violation_counts": violation_counts([to_dict(item) for item in process.violations]) if process else {},
            "ground_truth_violation_labels": "NOT AVAILABLE for this CP01 action-level split; procedure anomaly metrics are NOT EVALUATED.",
        },
        "segments": [to_dict(item) for item in segments],
        "events": [to_dict(item) for item in events],
        "ground_truth_labels": sequence.labels.tolist(),
        "predicted_labels": predicted.tolist(),
        "timestamps": sequence.timestamps.tolist(),
        "frame_indices": sequence.frame_indices.tolist(),
        "probabilities": probabilities.tolist(),
        "video_path": str(sequence.video_path),
    }


def write_timeline_svg(path: Path, timestamps: np.ndarray, gt: np.ndarray, pred: np.ndarray, class_order: list[str], max_width: int = 1600) -> None:
    length = min(len(timestamps), len(gt), len(pred))
    if length <= 0:
        raise ValueError("Cannot render empty timeline")
    duration = max(float(timestamps[length - 1]), 1e-6)
    width, height, left, top = max_width, 160, 140, 35
    plot_width = width - left - 20
    row_h = 35
    colors = ["#d1d5db", "#2563eb", "#ef4444", "#f59e0b", "#7c3aed", "#10b981", "#06b6d4", "#64748b"]
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>']
    for row, (title, values) in enumerate((("Ground Truth", gt[:length]), ("Prediction", pred[:length]))):
        y = top + row * 55
        svg.append(f'<text x="12" y="{y + 22}" font-family="Arial" font-size="14">{title}</text>')
        starts = np.r_[0, np.flatnonzero(values[1:] != values[:-1]) + 1]
        ends = np.r_[starts[1:], length]
        for start, end in zip(starts, ends):
            x0 = left + int(float(timestamps[start]) / duration * plot_width)
            x1 = left + int((float(timestamps[min(end - 1, length - 1)]) + duration / length) / duration * plot_width)
            class_id = int(values[start])
            color = colors[class_id % len(colors)]
            label = class_order[class_id]
            segment_width = max(1, x1 - x0)
            svg.append(f'<rect x="{x0}" y="{y}" width="{segment_width}" height="{row_h}" fill="{color}" stroke="white"/>')
            if segment_width > 44:
                svg.append(f'<text x="{x0 + 3}" y="{y + 22}" fill="white" font-family="Arial" font-size="11">{label}</text>')
    svg.append(f'<text x="{left}" y="{height - 12}" font-family="Arial" font-size="11">0s</text><text x="{left + plot_width - 35}" y="{height - 12}" font-family="Arial" font-size="11">{duration:.1f}s</text>')
    svg.append('</svg>')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(svg), encoding="utf-8")
