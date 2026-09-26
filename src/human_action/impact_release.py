from __future__ import annotations

import io
import json
import re
from pathlib import Path
from typing import Any
from zipfile import ZipFile

import numpy as np

from .dataset import SequenceData


def read_official_split(split_dir: Path, split_id: int, split: str, procedure: str, view: str) -> list[str]:
    path = split_dir / f"{split}.split{split_id}.bundle"
    if not path.is_file():
        raise FileNotFoundError(f"Official IMPACT split bundle missing: {path}")
    suffix = f"_{view}"
    ids = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    filtered = [video_id for video_id in ids if video_id.endswith(suffix) and f"_{procedure}_" in video_id]
    if not filtered:
        raise ValueError(f"No {procedure}/{view} trials in {path}")
    return filtered


def validate_official_split_integrity(split_dir: Path, split_id: int, procedure: str, view: str, cross_worker_test: bool = False) -> dict[str, Any]:
    ids = {name: read_official_split(split_dir, split_id, name, procedure, view) for name in ("train", "val", "test")}
    execution_sets = {name: set(values) for name, values in ids.items()}
    worker_sets = {name: {video_id.split("_", 1)[0] for video_id in values} for name, values in ids.items()}
    overlaps = {
        f"{left}_{right}": sorted(execution_sets[left] & execution_sets[right])
        for left, right in (("train", "val"), ("train", "test"), ("val", "test"))
    }
    worker_overlaps = {
        f"{left}_{right}": sorted(worker_sets[left] & worker_sets[right])
        for left, right in (("train", "val"), ("train", "test"), ("val", "test"))
    }
    if any(overlaps.values()):
        raise ValueError(f"Official split has execution leakage: {overlaps}")
    if cross_worker_test and worker_overlaps["train_test"]:
        raise ValueError(f"Expected worker-disjoint test, found overlap: {worker_overlaps['train_test']}")
    return {
        "split_id": split_id,
        "procedure": procedure,
        "view": view,
        "video_ids": ids,
        "counts": {name: len(values) for name, values in ids.items()},
        "worker_counts": {name: len(values) for name, values in worker_sets.items()},
        "worker_ids": {name: sorted(values) for name, values in worker_sets.items()},
        "execution_overlap": overlaps,
        "worker_overlap": worker_overlaps,
        "cross_worker_test": not worker_overlaps["train_test"],
    }


def annotation_member(video_id: str, view: str) -> str:
    return f"IMPACT-v1.1/annotations/TAS-S/{view}/{video_id}.json"


def feature_member(video_id: str, feature_name: str = "I3D") -> str:
    return f"IMPACT-v1.1/features/{feature_name}/{video_id}.npy"


def parse_tas_s_annotation(payload: bytes, video_id: str, class_order: list[str]) -> tuple[np.ndarray, dict[str, Any]]:
    annotation = json.loads(payload.decode("utf-8"))
    if annotation.get("video_id") != video_id:
        raise ValueError(f"Annotation ID mismatch: requested {video_id}, got {annotation.get('video_id')}")
    metadata = annotation.get("meta_data", {})
    frame_count = int(metadata.get("num_frames", 0))
    view_start = int(annotation.get("view_start", metadata.get("view_start", 0)))
    view_end = int(annotation.get("view_end", metadata.get("view_end", frame_count - 1)))
    if frame_count <= 0 or view_start < 0 or view_end < view_start or view_end >= frame_count:
        raise ValueError(f"Invalid TAS-S frame metadata for {video_id}: {metadata}")
    class_to_id = {label: index for index, label in enumerate(class_order)}
    if len(class_to_id) != len(class_order):
        raise ValueError("class_order contains duplicate labels")
    if "NULL" not in class_to_id:
        raise ValueError("class_order must include NULL background")
    labels = np.full(frame_count, class_to_id["NULL"], dtype=np.int64)
    coverage = np.zeros(frame_count, dtype=np.uint8)
    previous_end = view_start - 1
    segments = annotation.get("segments", [])
    if not segments:
        raise ValueError(f"No TAS-S segments for {video_id}")
    for row_number, segment in enumerate(segments, start=1):
        start, end = int(segment["f_start"]), int(segment["f_end"])
        label = str(segment["label"]).upper()
        if label not in class_to_id:
            raise ValueError(f"Unknown TAS-S label {label!r} in {video_id} segment {row_number}")
        if start < view_start or end >= view_end + 1 or start > end:
            raise ValueError(f"Invalid segment bounds [{start}, {end}] in {video_id} segment {row_number}")
        if start <= previous_end:
            raise ValueError(f"Overlap or out-of-order segment at {video_id} segment {row_number}")
        if start != previous_end + 1:
            raise ValueError(f"Annotation gap [{previous_end + 1}, {start - 1}] in {video_id}")
        labels[start:end + 1] = class_to_id[label]
        coverage[start:end + 1] += 1
        previous_end = end
    if previous_end != view_end:
        raise ValueError(f"Annotation ends at {previous_end}, expected {view_end} for {video_id}")
    if np.any(coverage[view_start:view_end + 1] != 1):
        raise ValueError(f"TAS-S annotation does not cover each view frame exactly once: {video_id}")
    if view_start:
        labels[:view_start] = class_to_id["NULL"]
    if view_end + 1 < frame_count:
        labels[view_end + 1:] = class_to_id["NULL"]
    meta = {
        "video_id": video_id,
        "view": annotation.get("view"),
        "fps": float(metadata["fps"]),
        "width": int(metadata["resolution"]["width"]),
        "height": int(metadata["resolution"]["height"]),
        "frame_count": frame_count,
        "view_start": view_start,
        "view_end": view_end,
        "segment_count": len(segments),
        "unique_labels": sorted({str(segment["label"]).upper() for segment in segments}),
    }
    return labels, meta


def load_release_sequence(config: dict[str, Any], video_id: str, split: str, config_path: str | Path) -> SequenceData:
    project_root = Path(config_path).resolve().parent.parent
    dataset = config["dataset"]
    view = dataset["view"]
    annotation_zip_path = project_root / dataset["annotation_archive"]
    feature_archive_value = dataset.get("feature_archive")
    feature_zip_path = project_root / feature_archive_value if feature_archive_value else None
    feature_root_values = dataset.get("feature_roots", [])
    if dataset.get("feature_root"):
        feature_root_values = [dataset["feature_root"], *feature_root_values]
    feature_roots = [project_root / value for value in feature_root_values]
    with ZipFile(annotation_zip_path) as archive:
        member = annotation_member(video_id, view)
        if member not in archive.namelist():
            raise FileNotFoundError(f"TAS-S JSON missing in official annotation bundle: {member}")
        labels, metadata = parse_tas_s_annotation(archive.read(member), video_id, config["actions"]["class_order"])
    fps = metadata["fps"]
    sample_fps = float(dataset.get("sample_fps", fps))
    stride = max(1, int(round(fps / sample_fps)))
    frame_indices = np.arange(0, metadata["frame_count"], stride, dtype=np.int64)
    if frame_indices[-1] > metadata["view_end"]:
        frame_indices = frame_indices[frame_indices <= metadata["view_end"]]
    labels = labels[frame_indices]
    member = feature_member(video_id, dataset.get("feature_name", "I3D"))
    feature_name = dataset.get("feature_name", "I3D")
    directory_features = [root / feature_name / f"{video_id}.npy" for root in feature_roots]
    if feature_zip_path and feature_zip_path.is_file():
        with ZipFile(feature_zip_path) as archive:
            if member not in archive.namelist():
                raise FileNotFoundError(f"Released video feature missing: {member}")
            features = np.load(io.BytesIO(archive.read(member)), allow_pickle=False)
    elif any(path.is_file() for path in directory_features):
        directory_feature = next(path for path in directory_features if path.is_file())
        features = np.load(directory_feature, allow_pickle=False)
    else:
        searched = [str(path) for path in ([feature_zip_path] if feature_zip_path else []) + directory_features]
        raise FileNotFoundError(
            f"Official feature data is unavailable for {video_id}; searched {searched}"
        )
    if features.ndim != 2 or features.shape[0] != metadata["frame_count"]:
        raise ValueError(f"Feature/annotation frame mismatch for {video_id}: {features.shape} vs {metadata['frame_count']}")
    features = np.asarray(features[frame_indices], dtype=np.float32)
    if not np.isfinite(features).all():
        raise ValueError(f"Non-finite feature values for {video_id}")
    timestamps = (frame_indices / fps).astype(np.float32)
    video_path = project_root / dataset.get("video_root", "") / view / f"{video_id}.mp4"
    return SequenceData(video_id, video_path, annotation_zip_path, video_id.split("_", 1)[0], features, labels, timestamps, frame_indices, fps, metadata["frame_count"])


def audit_release_annotation(archive: ZipFile, video_id: str, view: str, class_order: list[str]) -> dict[str, Any]:
    payload = archive.read(annotation_member(video_id, view))
    labels, metadata = parse_tas_s_annotation(payload, video_id, class_order)
    metadata["label_frame_counts"] = {class_order[index]: int(count) for index, count in enumerate(np.bincount(labels, minlength=len(class_order))) if count}
    return metadata


def procedure_from_video_id(video_id: str) -> str | None:
    match = re.search(r"_(Disassembly|Reassembly)_([A-Z])_", video_id)
    return f"{match.group(1)}_{match.group(2)}" if match else None
