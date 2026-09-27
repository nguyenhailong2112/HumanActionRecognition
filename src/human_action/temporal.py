from __future__ import annotations

from collections import Counter

import numpy as np

from .schemas import ActionEvent, ActionSegment


def temporal_windows(length: int, window_size: int, stride: int) -> list[tuple[int, int]]:
    if length < 0 or window_size < 1 or stride < 1:
        raise ValueError("length must be non-negative and window_size/stride positive")
    if length == 0:
        return []
    if length <= window_size:
        return [(0, length)]
    starts = list(range(0, length - window_size + 1, stride))
    if starts[-1] + window_size < length:
        starts.append(length - window_size)
    return [(start, min(start + window_size, length)) for start in starts]


def smooth_labels(labels: np.ndarray, window: int = 5) -> np.ndarray:
    labels = np.asarray(labels, dtype=np.int64)
    if window <= 1 or len(labels) < 3:
        return labels.copy()
    if window % 2 == 0:
        window += 1
    radius = window // 2
    result = labels.copy()
    for i in range(len(labels)):
        local = labels[max(0, i - radius):min(len(labels), i + radius + 1)]
        counts = Counter(local.tolist())
        # Stable tie-break: keep the center prediction where possible.
        best = max(counts.values())
        choices = {label for label, count in counts.items() if count == best}
        result[i] = labels[i] if labels[i] in choices else min(choices)
    return result


def merge_short_segments(labels: np.ndarray, min_frames: int) -> np.ndarray:
    result = np.asarray(labels, dtype=np.int64).copy()
    if min_frames <= 1:
        return result
    for _ in range(max(1, len(result))):
        starts = np.r_[0, np.flatnonzero(result[1:] != result[:-1]) + 1]
        ends = np.r_[starts[1:], len(result)]
        changed = False
        for i, (start, end) in enumerate(zip(starts, ends)):
            if end - start >= min_frames:
                continue
            if i == 0 and i + 1 < len(starts):
                result[start:end] = result[starts[i + 1]]
            elif i + 1 == len(starts) and i > 0:
                result[start:end] = result[start - 1]
            elif 0 < i < len(starts) - 1:
                left, right = result[start - 1], result[end]
                result[start:end] = left if left == right else left
            changed = True
        if not changed:
            break
    return result


def decode_segments(labels: np.ndarray, probabilities: np.ndarray, class_order: list[str], timestamps: np.ndarray, frame_indices: np.ndarray, smoothing_window: int, min_segment_seconds: float) -> list[ActionSegment]:
    labels = smooth_labels(labels, smoothing_window)
    if len(timestamps) > 1:
        sample_period = float(np.median(np.diff(timestamps)))
    else:
        sample_period = 0.2
    labels = merge_short_segments(labels, max(1, int(round(min_segment_seconds / max(sample_period, 1e-6)))))
    if len(labels) == 0:
        return []
    starts = np.r_[0, np.flatnonzero(labels[1:] != labels[:-1]) + 1]
    ends = np.r_[starts[1:], len(labels)]
    segments: list[ActionSegment] = []
    for start, end in zip(starts, ends):
        action_id = int(labels[start])
        start_time = float(timestamps[start])
        end_time = float(timestamps[end - 1] + sample_period)
        confidence = float(probabilities[start:end, action_id].mean())
        segments.append(ActionSegment(
            action=class_order[action_id],
            start_time=start_time,
            end_time=end_time,
            duration=max(0.0, end_time - start_time),
            confidence=confidence,
            start_frame=int(frame_indices[start]),
            end_frame=int(frame_indices[end - 1]),
        ))
    return segments


def to_action_events(segments: list[ActionSegment], worker_id: str, video_id: str, background: str = "NULL", view: str = "") -> list[ActionEvent]:
    return [
        ActionEvent(worker_id, s.action, s.start_time, s.end_time, s.duration, s.confidence, video_id, s.start_frame, s.end_frame,
                    view=view, event_id=f"{video_id}:{s.start_frame}-{s.end_frame}:{s.action}")
        for s in segments if s.action != background
    ]
