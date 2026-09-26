from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


def frame_feature(frame_bgr: np.ndarray, previous_gray: np.ndarray | None, image_size: int = 16, difference_size: int = 8) -> tuple[np.ndarray, np.ndarray]:
    """Small deterministic RGB/appearance/motion descriptor, no pretrained model."""
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    rgb_small = cv2.resize(rgb, (image_size, image_size), interpolation=cv2.INTER_AREA)
    appearance = rgb_small.astype(np.float32).reshape(-1) / 255.0

    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    hist_parts = [
        cv2.calcHist([hsv], [channel], None, [8], [0, 180] if channel == 0 else [0, 256]).reshape(-1)
        for channel in range(3)
    ]
    color_hist = np.concatenate(hist_parts).astype(np.float32)
    color_hist /= np.maximum(color_hist.sum(), 1.0)

    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    gray_small = cv2.resize(gray, (difference_size, difference_size), interpolation=cv2.INTER_AREA)
    gray_small = gray_small.astype(np.float32) / 255.0
    if previous_gray is None:
        motion = np.zeros_like(gray_small)
        motion_mean = np.zeros(3, dtype=np.float32)
    else:
        delta = gray_small - previous_gray
        motion = np.abs(delta)
        motion_mean = np.asarray([delta.mean(), motion.mean(), motion.max()], dtype=np.float32)

    result = np.concatenate([appearance, color_hist, motion.reshape(-1), motion_mean])
    # 16x16 RGB + 24 color bins + 8x8 motion + 3 summary values = 283.
    return result.astype(np.float32), gray_small


def extract_video_features(video_path: str | Path, sample_fps: float, image_size: int = 16, difference_size: int = 8) -> tuple[np.ndarray, np.ndarray, float, int]:
    video_path = Path(video_path)
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise OSError(f"Could not open video: {video_path}")
    fps = float(capture.get(cv2.CAP_PROP_FPS))
    if not np.isfinite(fps) or fps <= 0:
        capture.release()
        raise ValueError(f"Invalid video FPS {fps} for {video_path}")
    stride = max(1, int(round(fps / sample_fps)))
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    features: list[np.ndarray] = []
    timestamps: list[float] = []
    frame_indices: list[int] = []
    previous_gray = None
    index = 0
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            if index % stride == 0:
                feature, previous_gray = frame_feature(frame, previous_gray, image_size, difference_size)
                features.append(feature)
                timestamps.append(index / fps)
                frame_indices.append(index)
            index += 1
    finally:
        capture.release()
    if not features:
        raise ValueError(f"No frames decoded from {video_path}")
    return np.stack(features), np.asarray(timestamps, np.float32), fps, frame_count or index


def extract_evidence_frame(video_path: str | Path, frame_index: int) -> np.ndarray:
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise OSError(f"Could not open video: {video_path}")
    try:
        capture.set(cv2.CAP_PROP_POS_FRAMES, max(0, int(frame_index)))
        ok, frame = capture.read()
        if not ok:
            raise ValueError(f"Cannot read evidence frame {frame_index} from {video_path}")
        return frame
    finally:
        capture.release()


def export_evidence_clip(video_path: str | Path, output_path: str | Path, start_time: float, end_time: float, fps_out: float = 10.0) -> None:
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise OSError(f"Could not open video: {video_path}")
    source_fps = float(capture.get(cv2.CAP_PROP_FPS))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if source_fps <= 0 or width <= 0 or height <= 0:
        capture.release()
        raise ValueError(f"Invalid video metadata for evidence clip: {video_path}")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(output_path), cv2.VideoWriter_fourcc(*"mp4v"), fps_out, (width, height))
    if not writer.isOpened():
        capture.release()
        raise OSError(f"Could not create evidence clip: {output_path}")
    first = max(0, int(start_time * source_fps))
    last = max(first, int(end_time * source_fps))
    step = max(1, int(round(source_fps / fps_out)))
    try:
        capture.set(cv2.CAP_PROP_POS_FRAMES, first)
        frame_index = first
        while frame_index <= last:
            ok, frame = capture.read()
            if not ok:
                break
            if (frame_index - first) % step == 0:
                writer.write(frame)
            frame_index += 1
    finally:
        writer.release()
        capture.release()
