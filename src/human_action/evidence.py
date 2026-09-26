from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import cv2

from .features import export_evidence_clip, extract_evidence_frame
from .schemas import Violation


def attach_evidence(violations: list[Violation], video_path: Path, output_dir: Path, context_seconds: float, fps_out: float, save_clip: bool) -> list[Violation]:
    evidence_dir = output_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    enriched = []
    for index, violation in enumerate(violations, start=1):
        frame_index = violation.evidence_frame
        if frame_index is None:
            capture = cv2.VideoCapture(str(video_path))
            fps = float(capture.get(cv2.CAP_PROP_FPS))
            frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
            capture.release()
            frame_index = min(max(0, int(violation.timestamp * fps)), max(0, frame_count - 1))
        else:
            capture = cv2.VideoCapture(str(video_path))
            frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
            capture.release()
            frame_index = min(max(0, int(frame_index)), max(0, frame_count - 1))
        stem = f"{index:03d}_{violation.violation_type.lower()}_{max(0, int(frame_index))}"
        image_path = evidence_dir / f"{stem}.jpg"
        image = extract_evidence_frame(video_path, frame_index)
        if not cv2.imwrite(str(image_path), image):
            raise OSError(f"Could not write evidence image: {image_path}")
        clip_path = None
        if save_clip:
            clip_path = evidence_dir / f"{stem}.mp4"
            export_evidence_clip(
                video_path,
                clip_path,
                max(0.0, violation.timestamp - context_seconds),
                violation.timestamp + context_seconds,
                fps_out,
            )
        enriched.append(replace(violation, evidence_image=str(image_path), evidence_clip=str(clip_path) if clip_path else None))
    return enriched
