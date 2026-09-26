from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from human_action.config import load_config  # noqa: E402
from human_action.impact_release import (  # noqa: E402
    annotation_member,
    audit_release_annotation,
    parse_tas_s_annotation,
    procedure_from_video_id,
    validate_official_split_integrity,
)
from human_action.pipeline import write_timeline_svg  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit official IMPACT v1.1 TAS-S annotations and the CP01.1 split.")
    parser.add_argument("--config", default="configs/cp01_1.yaml")
    parser.add_argument("--output", default="experiments/CP01.1")
    args = parser.parse_args()
    config_path = Path(args.config).resolve()
    config = load_config(config_path)
    project_root = config_path.parent.parent
    dataset = config["dataset"]
    protocol = dataset["official_split"]
    split_dir = project_root / protocol["split_dir"]
    split_info = validate_official_split_integrity(
        split_dir,
        int(protocol["split_id"]),
        protocol["procedure"],
        protocol["view"],
        bool(protocol.get("require_cross_worker_test", False)),
    )
    archive_path = project_root / dataset["annotation_archive"]
    output_dir = project_root / args.output
    output_dir.mkdir(parents=True, exist_ok=True)
    class_order = config["actions"]["class_order"]
    view = protocol["view"]
    procedure = protocol["procedure"]
    selected = {video_id for values in split_info["video_ids"].values() for video_id in values}
    split_lookup = {video_id: split for split, values in split_info["video_ids"].items() for video_id in values}

    rows = []
    global_label_frames = Counter()
    selected_label_frames = Counter()
    ppr_summary = {split: {hand: Counter() for hand in ("L", "R")} for split in ("train", "val", "test")}
    ppr_qa = Counter()
    timelines = []
    annotation_prefix = f"IMPACT-v1.1/annotations/TAS-S/{view}/"
    with ZipFile(archive_path) as archive:
        mapping_member = "IMPACT-v1.1/annotations/TAS-S/mapping_TAS-S.txt"
        full_class_order = [line.split(maxsplit=1)[1].strip().upper() for line in archive.read(mapping_member).decode("utf-8").splitlines() if line.strip()]
        full_class_order = ["NULL" if label == "NULL" else label for label in full_class_order]
        members = sorted(name for name in archive.namelist() if name.startswith(annotation_prefix) and name.endswith(".json"))
        for member in members:
            video_id = Path(member).stem
            try:
                metadata = audit_release_annotation(archive, video_id, view, full_class_order)
                labels, _ = parse_tas_s_annotation(archive.read(annotation_member(video_id, view)), video_id, full_class_order)
                if procedure_from_video_id(video_id) == procedure:
                    out_of_scope = set(metadata["unique_labels"]) - set(class_order)
                    if out_of_scope:
                        raise ValueError(f"Target procedure labels missing from CP01.1 class_order: {sorted(out_of_scope)}")
                qa_status, qa_reason = "PASS", "segment ranges are ordered, in range, gap-free, and cover the annotated view"
            except (ValueError, KeyError, json.JSONDecodeError) as error:
                metadata, labels = {}, None
                qa_status, qa_reason = "NEEDS REVIEW", str(error)
            counts = metadata.get("label_frame_counts", {})
            global_label_frames.update(counts)
            is_target = procedure_from_video_id(video_id) == procedure
            is_official_split = video_id in selected
            local_video = project_root / dataset.get("video_root", "") / view / f"{video_id}.mp4"
            if qa_status != "PASS":
                disposition = "NEEDS REVIEW"
            elif is_target and is_official_split:
                disposition = "KEEP"
                selected_label_frames.update(counts)
            else:
                disposition = "EXCLUDE"
            rows.append({
                "video_id": video_id,
                "execution": video_id[:-len(f"_{view}")],
                "worker": video_id.split("_", 1)[0],
                "procedure": procedure_from_video_id(video_id) or "UNKNOWN",
                "view": view,
                "action_vocabulary": ";".join(metadata.get("unique_labels", [])),
                "segment_count": metadata.get("segment_count", ""),
                "duration_seconds": round((metadata["view_end"] - metadata["view_start"] + 1) / metadata["fps"], 3) if metadata else "",
                "fps": metadata.get("fps", ""),
                "resolution": f"{metadata['width']}x{metadata['height']}" if metadata else "",
                "annotation_status": qa_status,
                "media_status": "AVAILABLE" if local_video.is_file() else "MISSING_LOCAL_VIDEO",
                "official_split": split_lookup.get(video_id, "NOT_IN_S2"),
                "disposition": disposition,
                "reason": qa_reason if disposition == "NEEDS REVIEW" else ("target procedure and official S2 split" if disposition == "KEEP" else "outside selected procedure or official S2 subset"),
            })
            if disposition == "KEEP" and labels is not None:
                if video_id in split_info["video_ids"]["test"] or (not timelines and split_lookup[video_id] == "val"):
                    timestamps = (range(len(labels)))
                    import numpy as np
                    timestamps = np.asarray(timestamps, dtype=np.float32) / float(metadata["fps"])
                    indices = np.arange(len(labels), dtype=np.int64)
                    svg_path = project_root / "results" / "cp01_1" / "ground_truth" / f"{video_id}.svg"
                    write_timeline_svg(svg_path, timestamps, labels, labels, full_class_order)
                    timelines.append(str(svg_path))

        for video_id in selected:
            expected_frames = None
            annotation_name = annotation_member(video_id, view)
            if annotation_name in archive.namelist():
                tas = json.loads(archive.read(annotation_name).decode("utf-8"))
                expected_frames = int(tas["meta_data"]["num_frames"])
            for hand in ("L", "R"):
                ppr_path = f"IMPACT-v1.1/annotations/PPR/groundTruth_PPR_{hand}/{video_id}.txt"
                if ppr_path not in archive.namelist():
                    ppr_qa[f"MISSING_{split_lookup[video_id]}_{hand}"] += 1
                    continue
                states = [line.strip().upper() for line in archive.read(ppr_path).decode("utf-8").splitlines() if line.strip()]
                if expected_frames is not None and len(states) != expected_frames:
                    ppr_qa[f"LENGTH_MISMATCH_{split_lookup[video_id]}_{hand}"] += 1
                    continue
                unknown_states = set(states) - {"NORMAL", "ANOMALY", "RECOVERY"}
                if unknown_states:
                    ppr_qa[f"UNKNOWN_LABEL_{split_lookup[video_id]}_{hand}"] += 1
                    continue
                ppr_qa[f"PASS_{split_lookup[video_id]}_{hand}"] += 1
                ppr_summary[split_lookup[video_id]][hand].update(states)

    csv_path = output_dir / "dataset_audit_CP01.1.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]) if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    report = {
        "dataset": "IMPACT v1.1",
        "annotation_archive": str(archive_path),
        "annotation_view": view,
        "procedure": procedure,
        "official_split": split_info,
        "front_view_annotation_files": len(rows),
        "annotation_qa": dict(Counter(row["annotation_status"] for row in rows)),
        "disposition": dict(Counter(row["disposition"] for row in rows)),
        "local_video_status": dict(Counter(row["media_status"] for row in rows)),
        "selected_action_label_frames": dict(selected_label_frames),
        "all_front_action_label_frames": dict(global_label_frames),
        "ppr_annotation_qa": dict(ppr_qa),
        "ppr_state_frame_counts_by_split_and_hand": {split: {hand: dict(counts) for hand, counts in hands.items()} for split, hands in ppr_summary.items()},
        "ppr_evaluation_boundary": "PPR ground truth is present per hand (NORMAL/ANOMALY/RECOVERY), but no CP01.1 model predicts that target and it is not equivalent to action-workflow violation labels. Workflow anomaly metrics remain NOT EVALUATED.",
        "gt_timeline_svgs": timelines,
        "process_owner_review_required": "Action ordering/optional/rework semantics and duration tolerances are not inferred from observed TAS-S sequences; see HUMAN_HANDOFF.md.",
    }
    json_path = output_dir / "dataset_audit_CP01.1.json"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    summary = [
        "# CP01.1 Dataset Audit — IMPACT v1.1",
        "",
        "Source of truth: verified official annotation archive `data/raw/impact/v1.1/annotations/IMPACT-v1.1-annotations.zip`; official TAS-S split bundles in the IMPACT repository.",
        "",
        f"- Front-view TAS-S JSON annotations: {len(rows)}",
        f"- Selected same-procedure executions: {len(selected)} ({procedure}, {view})",
        f"- Official S2 split: train {split_info['counts']['train']}, val {split_info['counts']['val']}, test {split_info['counts']['test']} — execution-disjoint.",
        f"- Workers: train {split_info['worker_counts']['train']}, val {split_info['worker_counts']['val']}, test {split_info['worker_counts']['test']}; train/test worker overlap {len(split_info['worker_overlap']['train_test'])}.",
        f"- Local source videos in target split: {sum(row['disposition'] == 'KEEP' and row['media_status'] == 'AVAILABLE' for row in rows)} / {len(selected)}.",
        f"- Annotation QA: {report['annotation_qa']}; dispositions: {report['disposition']}.",
        f"- PPR per-hand phase annotations: QA {dict(ppr_qa)}; state counts by split/hand recorded in JSON. PPR phase labels are distinct from workflow violation labels and are not used to score compliance.",
        "- Annotation unit: official per-frame TAS-S labels represented as ordered inclusive frame intervals; QA checks unknown class, empty segments, invalid/out-of-range bounds, ordering, overlap, gaps, and coverage.",
        "- Annotation/video quality (blur, occlusion, view adequacy) is not assessed automatically and remains NOT VERIFIED.",
        "- Classification labels are data annotations, not approved workflow requirements or mistake/compliance labels.",
        "",
        "| Video | Worker | Procedure | Duration s | FPS / resolution | Segments | Annotation QA | Local video | Split | Disposition |",
        "|---|---|---|---:|---|---:|---|---|---|---|",
    ]
    for row in rows:
        summary.append(f"| {row['video_id']} | {row['worker']} | {row['procedure']} | {row['duration_seconds']} | {row['fps']} / {row['resolution']} | {row['segment_count']} | {row['annotation_status']} | {row['media_status']} | {row['official_split']} | {row['disposition']} |")
    md_path = output_dir / "dataset_audit_CP01.1.md"
    md_path.write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(json_path), "csv": str(csv_path), "markdown": str(md_path), "selected_counts": split_info["counts"], "annotation_qa": report["annotation_qa"], "disposition": report["disposition"], "timelines": timelines}, indent=2))


if __name__ == "__main__":
    main()
