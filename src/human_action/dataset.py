from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from .features import extract_video_features


@dataclass
class SequenceData:
    video_id: str
    video_path: Path
    annotation_path: Path
    worker_id: str
    features: np.ndarray  # [T, D]
    labels: np.ndarray  # [T], IDs in configured action order
    timestamps: np.ndarray  # [T], seconds from video start
    frame_indices: np.ndarray  # [T], source video frame indices
    fps: float
    frame_count: int


def read_class_mapping(path: Path) -> dict[int, str]:
    mapping: dict[int, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        class_id, name = line.split(maxsplit=1)
        mapping[int(class_id)] = name.strip()
    if not mapping:
        raise ValueError(f"Empty class mapping: {path}")
    return mapping


def read_dense_labels(path: Path, mapping: dict[int, str], source_to_action: dict[str, str], class_order: list[str], background: str) -> list[int]:
    names_to_ids = {name: class_id for class_id, name in mapping.items()}
    action_to_id = {name: idx for idx, name in enumerate(class_order)}
    if background not in action_to_id:
        raise ValueError(f"Background class {background!r} is missing from class_order")
    dense: list[int] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        name = raw.strip()
        if name not in names_to_ids:
            raise ValueError(f"Unknown source label {name!r} at {path}:{line_number}")
        action_name = source_to_action.get(mapping[names_to_ids[name]], background)
        action = action_to_id.get(action_name, action_to_id[background])
        dense.append(action)
    if not dense:
        raise ValueError(f"No frame labels found: {path}")
    return dense


def _find_annotation(config: dict[str, Any], video_id: str, project_root: Path) -> Path:
    candidates = [
        project_root / config["dataset"]["root"] / config["dataset"].get("annotation_dir", "") / f"{video_id}.txt",
        project_root / config["dataset"]["source_annotation_dir"] / f"{video_id}.txt",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    root = project_root / config["dataset"]["root"]
    if root.exists():
        matches = list(root.glob(f"**/{video_id}.txt"))
        if matches:
            return matches[0]
    raise FileNotFoundError(f"No TAS-S annotation found for {video_id}; searched {candidates}")


def load_sequence(config: dict[str, Any], video_id: str, split: str, config_path: str | Path) -> SequenceData:
    if config.get("dataset", {}).get("source") == "impact_official_release":
        from .impact_release import load_release_sequence
        return load_release_sequence(config, video_id, split, config_path)
    project_root = Path(config_path).resolve().parent.parent
    data_root = project_root / config["dataset"]["root"]
    view = config["dataset"]["view"]
    video_path = data_root / "videos" / view / f"{video_id}.mp4"
    if not video_path.is_file():
        raise FileNotFoundError(f"Video missing for {video_id}: {video_path}. Download/extract IMPACT v1.1 sample first.")
    annotation_path = _find_annotation(config, video_id, project_root)
    source_mapping_path = data_root / config["dataset"].get("annotation_mapping", "")
    if not source_mapping_path.is_file():
        source_mapping_path = project_root / config["dataset"]["source_mapping"]
    source_mapping = read_class_mapping(source_mapping_path)
    class_order = config["actions"]["class_order"]
    action_to_id = {name: idx for idx, name in enumerate(class_order)}
    dense = read_dense_labels(annotation_path, source_mapping, config["actions"]["source_to_action"], class_order, config["actions"]["background"])

    cache_dir = project_root / config["dataset"]["cache_dir"]
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{video_id}_fps{config['dataset']['sample_fps']:g}.npz"
    stat = video_path.stat()
    if cache_path.is_file():
        cached = np.load(cache_path, allow_pickle=False)
        if int(cached["video_size"]) == stat.st_size and int(cached["video_mtime_ns"]) == stat.st_mtime_ns:
            features = cached["features"]
            timestamps = cached["timestamps"]
            frame_indices = cached["frame_indices"]
            sampled_labels = cached["labels"]
            fps = float(cached["fps"])
            frame_count = int(cached["frame_count"])
            return SequenceData(video_id, video_path, annotation_path, video_id.split("_")[0], features, sampled_labels, timestamps, frame_indices, fps, frame_count)

    features, timestamps, fps, frame_count = extract_video_features(
        video_path,
        float(config["dataset"]["sample_fps"]),
        int(config["features"]["image_size"]),
        int(config["features"]["difference_size"]),
    )
    stride = max(1, int(round(fps / float(config["dataset"]["sample_fps"]))))
    frame_indices = np.arange(len(features), dtype=np.int64) * stride
    ann_indices = np.minimum(np.rint(frame_indices * len(dense) / max(frame_count, 1)).astype(np.int64), len(dense) - 1)
    sampled_labels = np.asarray(dense, dtype=np.int64)[ann_indices]
    np.savez_compressed(
        cache_path,
        features=features,
        timestamps=timestamps,
        frame_indices=frame_indices,
        labels=sampled_labels,
        fps=np.asarray(fps),
        frame_count=np.asarray(frame_count),
        video_size=np.asarray(stat.st_size),
        video_mtime_ns=np.asarray(stat.st_mtime_ns),
    )
    return SequenceData(video_id, video_path, annotation_path, video_id.split("_")[0], features, sampled_labels, timestamps, frame_indices, fps, frame_count)


def load_split(config: dict[str, Any], split: str, config_path: str | Path) -> list[SequenceData]:
    dataset = config.get("dataset", {})
    if dataset.get("source") == "impact_official_release":
        from .impact_release import load_release_sequence, read_official_split
        protocol = dataset["official_split"]
        split_dir = Path(config_path).resolve().parent.parent / protocol["split_dir"]
        video_ids = read_official_split(split_dir, int(protocol["split_id"]), split, protocol["procedure"], protocol["view"])
        return [load_release_sequence(config, video_id, split, config_path) for video_id in video_ids]
    entries = config["dataset"]["splits"].get(split, [])
    if not entries:
        raise ValueError(f"Configured {split} split is empty")
    return [load_sequence(config, video_id, split, config_path) for video_id in entries]


def mapped_sequence(label_ids: np.ndarray, class_order: list[str]) -> list[str]:
    """Collapse frame labels into segments; omit background but preserve repeats separated by another label."""
    names = [class_order[int(value)] for value in label_ids]
    sequence: list[str] = []
    previous = None
    for name in names:
        if name != previous and name != "NULL":
            sequence.append(name)
        previous = name
    return sequence
