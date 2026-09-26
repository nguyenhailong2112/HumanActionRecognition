from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from human_action.impact_release import (  # noqa: E402
    annotation_member,
    audit_release_annotation,
    feature_member,
    validate_official_split_integrity,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit CP02 IMPACT annotation, split, feature, and local video readiness.")
    parser.add_argument("--config", default="configs/cp01_1.yaml")
    parser.add_argument("--output", default="experiments/CP02/data_readiness.json")
    args = parser.parse_args()
    config_path = (PROJECT_ROOT / args.config).resolve()
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    dataset = config["dataset"]
    protocol = dataset["official_split"]
    split_dir = PROJECT_ROOT / protocol["split_dir"]
    split_report = validate_official_split_integrity(
        split_dir, int(protocol["split_id"]), protocol["procedure"], protocol["view"],
        bool(protocol.get("require_cross_worker_test", False)),
    )
    annotation_path = PROJECT_ROOT / dataset["annotation_archive"]
    feature_path = PROJECT_ROOT / dataset["feature_archive"]
    feature_roots = [PROJECT_ROOT / value for value in dataset.get("feature_roots", [])]
    video_roots = [PROJECT_ROOT / value for value in dataset.get("video_roots", [])]
    if dataset.get("video_root"):
        video_roots.append(PROJECT_ROOT / dataset["video_root"])
    class_order = config["actions"]["class_order"]
    report = {
        "dataset": dataset["name"],
        "version": dataset["version"],
        "procedure": protocol["procedure"],
        "view": protocol["view"],
        "split": split_report,
        "annotation_archive": str(annotation_path),
        "feature_archive": {"path": str(feature_path), "present": feature_path.is_file()},
        "annotation_qa": {"checked": 0, "passed": 0, "failed": [], "metadata": {}},
        "feature_qa": {"expected": 0, "present": 0, "passed": 0, "missing": [], "invalid": []},
        "video_qa": {"expected": 0, "present": 0, "metadata": [], "missing": []},
    }
    ids = [video_id for values in split_report["video_ids"].values() for video_id in values]
    annotation_metadata = {}
    report["annotation_qa"]["checked"] = len(ids)
    try:
        with ZipFile(annotation_path) as annotation_zip:
            for video_id in ids:
                try:
                    annotation_metadata[video_id] = audit_release_annotation(annotation_zip, video_id, protocol["view"], class_order)
                    report["annotation_qa"]["metadata"][video_id] = annotation_metadata[video_id]
                    report["annotation_qa"]["passed"] += 1
                except Exception as exc:
                    report["annotation_qa"]["failed"].append({"video_id": video_id, "error": str(exc)})
            feature_zip = ZipFile(feature_path) if feature_path.is_file() else None
            feature_members = set(feature_zip.namelist()) if feature_zip is not None else set()
            try:
                for video_id in ids:
                    report["feature_qa"]["expected"] += 1
                    feature_file = next(
                        (root / dataset.get("feature_name", "I3D") / f"{video_id}.npy"
                         for root in feature_roots
                         if (root / dataset.get("feature_name", "I3D") / f"{video_id}.npy").is_file()),
                        None,
                    )
                    member = feature_member(video_id, dataset.get("feature_name", "I3D"))
                    try:
                        if feature_zip is not None:
                            if member not in feature_members:
                                raise FileNotFoundError(member)
                            features = np.load(io.BytesIO(feature_zip.read(member)), allow_pickle=False)
                        elif feature_file is not None:
                            features = np.load(feature_file, allow_pickle=False)
                        else:
                            report["feature_qa"]["missing"].append(video_id)
                            continue
                    except Exception as exc:
                        report["feature_qa"]["invalid"].append({"video_id": video_id, "error": str(exc)})
                        continue
                    report["feature_qa"]["present"] += 1
                    annotation = annotation_zip.read(annotation_member(video_id, protocol["view"]))
                    metadata = json.loads(annotation)["meta_data"]
                    shape_ok = features.shape == (int(metadata["num_frames"]), int(dataset["feature_dimension"]))
                    finite_ok = bool(np.isfinite(features).all())
                    if shape_ok and finite_ok:
                        report["feature_qa"]["passed"] += 1
                    else:
                        report["feature_qa"]["invalid"].append({
                            "video_id": video_id, "shape": list(features.shape),
                            "expected": [int(metadata["num_frames"]), int(dataset["feature_dimension"])],
                            "finite": finite_ok,
                        })
                if feature_zip is not None:
                    feature_zip.close()
            finally:
                if feature_zip is not None and feature_zip.fp is not None:
                    feature_zip.close()
    except Exception as exc:
        report["annotation_qa"]["failed"].append({"archive_error": str(exc)})

    try:
        import cv2
        for video_id in ids:
            report["video_qa"]["expected"] += 1
            video_path = next(
                (root / protocol["view"] / f"{video_id}.mp4" for root in video_roots
                 if (root / protocol["view"] / f"{video_id}.mp4").is_file()),
                None,
            )
            if video_path is None:
                report["video_qa"]["missing"].append(video_id)
                continue
            capture = cv2.VideoCapture(str(video_path))
            opened = capture.isOpened()
            row = {
                "video_id": video_id, "path": str(video_path), "opened": opened,
                "fps": float(capture.get(cv2.CAP_PROP_FPS)),
                "frame_count_reported": int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),
                "width": int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height": int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            }
            if opened:
                decoded = 0
                while True:
                    ok, _ = capture.read()
                    if not ok:
                        break
                    decoded += 1
                row["decoded_frames"] = decoded
                annotation_info = annotation_metadata.get(video_id, {})
                expected = annotation_info.get("frame_count")
                row["annotation_frame_count"] = expected
                row["annotation_alignment"] = decoded == expected if expected is not None else None
                row["reported_count_matches_annotation"] = row["frame_count_reported"] == expected if expected is not None else None
                row["fps_matches_annotation"] = abs(row["fps"] - annotation_info["fps"]) < 1e-3 if "fps" in annotation_info else None
                row["resolution_matches_annotation"] = (
                    row["width"] == annotation_info["width"] and row["height"] == annotation_info["height"]
                    if "width" in annotation_info and "height" in annotation_info else None
                )
                report["video_qa"]["present"] += 1
            capture.release()
            report["video_qa"]["metadata"].append(row)
    except ImportError:
        report["video_qa"]["error"] = "OpenCV unavailable; video metadata not inspected"

    report["readiness"] = {
        "split": "PASS",
        "annotations": "PASS" if report["annotation_qa"]["passed"] == len(ids) else "FAIL",
        "features": "PASS" if report["feature_qa"]["passed"] == len(ids) else "INCOMPLETE",
        "videos": "PASS" if report["video_qa"]["present"] == len(ids) else "INCOMPLETE",
    }
    output = PROJECT_ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"report": str(output), "readiness": report["readiness"], "feature_counts": report["feature_qa"], "video_counts": {key: report["video_qa"][key] for key in ("expected", "present")}}, indent=2))


if __name__ == "__main__":
    main()
