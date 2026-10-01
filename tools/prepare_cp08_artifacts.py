from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_evidence_handoff(project_root: Path, review_manifest: dict) -> None:
    rows = [
        "# CP08 Human Evidence Review Handoff",
        "",
        "Status: `HUMAN_REVIEW_REQUIRED`. This queue contains the 13 unique CP07-selected events (21 category selections deduplicated). No reviewer judgments are present in the repository.",
        "",
        "## Review instructions",
        "",
        "For each row, open the source video around the listed timestamp and inspect the linked snapshot and context clip. Judge only whether the predicted action is visually supported and whether its temporal boundary is acceptable. Do not infer workflow compliance, mistake, recovery, or process policy from this action-only review. Do not write judgments into official annotations or training labels.",
        "",
        "Write the completed rows to `experiments/CP08/human_evidence_review.csv` using exactly these columns:",
        "",
        "```csv",
        "event_id,reviewer,judgment,corrected_action,boundary_judgment,semantic_note,reviewer_confidence",
        "```",
        "",
        "Allowed `judgment`: `correct`, `incorrect`, `ambiguous`, `not_enough_visual_evidence`. Allowed `boundary_judgment`: `acceptable`, `incorrect`, `uncertain`. `corrected_action` is required only when judgment is `incorrect` and the replacement label is clearly identifiable; otherwise leave it blank. `reviewer_confidence` is reviewer confidence on a 1–5 scale, not model confidence. Keep `semantic_note` brief and limited to the visible evidence.",
        "",
        "The CP05/TAS-S ground-truth label is deliberately not included in this review queue, so it does not prime the visual judgment. The CP07 evidence manifest remains unchanged.",
        "",
        "## Canonical review events",
        "",
        "| Event ID | Execution | Timestamp (s) | Predicted action | Source video | Snapshot | Clip |",
        "|---|---|---:|---|---|---|---|",
    ]
    for event in review_manifest.get("events", []):
        rows.append(
            f"| `{event['event_id']}` | `{event['video_id']}` | {float(event['timestamp_seconds']):.3f} "
            f"| `{event['predicted_action']}` | `{event['source_video']}` | `{event['snapshot']}` | `{event['clip']}` |"
        )
    rows.extend([
        "",
        "## Validation and resume point",
        "",
        "The reviewer should provide exactly one row per event ID (13 rows total), no duplicate IDs, no unknown IDs, and values from the allowed enums. CP08 may validate the CSV schema and event IDs after it is returned. Reviewer judgments remain a separate reviewed artifact; they are not automatically converted to dataset labels, workflow decisions, or model-training data.",
        "",
    ])
    (project_root / "HUMAN_HANDOFF_CP08_EVIDENCE_REVIEW.md").write_text("\n".join(rows), encoding="utf-8")


def prepare_artifacts(project_root: Path) -> tuple[dict, dict, dict]:
    """Repackage frozen CP05 predictions and verify their existing evidence links."""
    from human_action.config import load_config
    from human_action.schemas import ActionEvent, ActionSegment, to_dict
    from human_action.temporal import to_action_events

    project_root = project_root.resolve()
    cp05_dir = project_root / "results" / "cp05" / "evaluation"
    evidence_index_path = project_root / "experiments" / "CP05" / "evidence_index.json"
    review_manifest_path = project_root / "experiments" / "CP07" / "evidence_review_manifest.json"
    frozen_test_metrics_path = cp05_dir / "test_metrics.json"
    executable_workflow = project_root / "configs" / "workflows" / "disassembly_A.yaml"
    if executable_workflow.exists():
        raise ValueError("Executable workflow exists; do not use the no-workflow CP08 artifact preparation path")
    for review_path in (
        project_root / "experiments" / "CP07" / "human_evidence_review.csv",
        project_root / "experiments" / "CP08" / "human_evidence_review.csv",
    ):
        if review_path.exists():
            raise ValueError(f"Human evidence review exists and must be reconciled before preparation: {review_path}")
    config = load_config(project_root / "configs" / "cp05.yaml")
    expected_ids = set(
        _read_json(project_root / "experiments" / "CP06" / "action_metrics.json")["video_ids"]
    )
    frozen_test_results = _read_json(frozen_test_metrics_path)["results"]
    video_paths = {
        row["video_id"]: row["video_path"]
        for row in frozen_test_results if row.get("model") == "mstcn"
    }
    if set(video_paths) != expected_ids:
        raise ValueError("Frozen CP05 MS-TCN test results do not cover the expected held-out executions")

    evidence_rows = _read_json(evidence_index_path)["records"]
    evidence_by_key: dict[tuple[str, str, int], dict] = {}
    for index, row in enumerate(evidence_rows, start=1):
        key = (row["video_id"], row["action"], int(row["action_event_start_frame"]))
        if key in evidence_by_key:
            raise ValueError(f"Duplicate CP05 evidence identity: {key}")
        evidence_by_key[key] = {**row, "_record_index": index}

    review_manifest = _read_json(review_manifest_path)
    if review_manifest.get("status") != "HUMAN_REVIEW_REQUIRED":
        raise ValueError("CP07 evidence review manifest must remain HUMAN_REVIEW_REQUIRED")
    review_ids_by_key: dict[tuple[str, str, int], str] = {}
    for review in review_manifest.get("events", []):
        matches = [
            (key, row) for key, row in evidence_by_key.items()
            if key[0] == review["video_id"] and key[1] == review["predicted_action"]
            and abs(float(row["action_event_timestamp_seconds"]) - float(review["timestamp_seconds"])) <= 1e-6
        ]
        if len(matches) != 1:
            raise ValueError(f"Review event {review['event_id']} maps to {len(matches)} frozen evidence records")
        key = matches[0][0]
        if key in review_ids_by_key:
            raise ValueError(f"Multiple review IDs map to one action event: {key}")
        review_ids_by_key[key] = review["event_id"]

    timeline_paths = sorted(cp05_dir.glob("*_mstcn_timeline.json"))
    timelines: dict[str, tuple[Path, dict]] = {}
    for path in timeline_paths:
        timeline = _read_json(path)
        if timeline.get("model") != "mstcn":
            raise ValueError(f"Unexpected model in frozen timeline: {path}")
        video_id = timeline.get("video_id")
        if not video_id or video_id in timelines:
            raise ValueError(f"Missing or duplicate execution ID in timeline: {path}")
        timelines[video_id] = (path, timeline)
    if set(timelines) != expected_ids:
        raise ValueError(f"Frozen timeline execution IDs differ from CP06: {sorted(set(timelines) ^ expected_ids)}")

    records = []
    link_rows = []
    per_execution = []
    matched_evidence = set()
    for video_id in sorted(timelines):
        timeline_path, timeline = timelines[video_id]
        source_events = timeline.get("events", [])
        segments = [ActionSegment(**row) for row in timeline.get("segments", [])]
        worker_ids = {row.get("worker_id") for row in source_events}
        if len(worker_ids) > 1:
            raise ValueError(f"Frozen timeline mixes worker IDs: {video_id}")
        worker_id = next(iter(worker_ids), None)
        if source_events and not worker_id:
            raise ValueError(f"Frozen timeline is missing worker ID: {video_id}")
        events = to_action_events(
            segments, str(worker_id or ""), video_id,
            background=str(config["actions"]["background"]), view=str(config["dataset"]["view"]),
        )
        if len(events) != len(source_events):
            raise ValueError(f"Temporal-segment conversion changed event count for {video_id}")
        for converted, saved in zip(events, source_events):
            for field in ("worker_id", "action", "video_id", "start_frame", "end_frame"):
                if getattr(converted, field) != saved[field]:
                    raise ValueError(f"Frozen temporal conversion mismatch for {video_id}: field {field}")
            for field in ("start_time", "end_time", "duration", "confidence"):
                if abs(getattr(converted, field) - float(saved[field])) > 1e-6:
                    raise ValueError(f"Frozen temporal conversion mismatch for {video_id}: field {field}")
        linked_count = 0
        for event in events:
            key = (video_id, event.action, event.start_frame)
            evidence = evidence_by_key.get(key)
            if evidence is None:
                raise ValueError(f"Frozen event has no CP05 evidence record: {key}")
            if key in matched_evidence:
                raise ValueError(f"Frozen event matched more than once: {key}")
            matched_evidence.add(key)
            fps = float(evidence["source_video_fps"])
            delta_frames = abs(event.start_time - float(evidence["action_event_timestamp_seconds"])) * fps
            if delta_frames > 1.0 + 1e-6:
                raise ValueError(f"Frozen event/evidence timestamp differs by {delta_frames:.3f} frames: {key}")
            if abs(event.confidence - float(evidence["confidence"])) > 1e-6:
                raise ValueError(f"Frozen event/evidence confidence mismatch: {key}")
            if event.end_frame < event.start_frame:
                raise ValueError(f"Frozen event has reversed frame bounds: {key}")
            if event.end_frame >= int(evidence["source_video_frame_count"]):
                raise ValueError(f"Frozen event exceeds source video frame count: {key}")
            if abs((event.end_time - event.start_time) - event.duration) > 1e-3:
                raise ValueError(f"Frozen event duration does not match time bounds: {key}")
            source_video = Path(video_paths[video_id])
            snapshot = Path(evidence["snapshot"])
            clip = Path(evidence["clip"])
            missing = [str(path) for path in (source_video, snapshot, clip) if not path.is_file()]
            if missing:
                raise FileNotFoundError(f"Evidence media missing for {key}: {missing}")
            event = ActionEvent(**{
                **to_dict(event), "evidence_refs": (str(snapshot), str(clip)),
            })
            records.append({
                "action_event": to_dict(event),
                "cp05_evidence_record_index": evidence["_record_index"],
                "human_review_event_id": review_ids_by_key.get(key),
                "frozen_prediction_timeline": str(timeline_path.relative_to(project_root)),
            })
            link_rows.append({
                "event_id": event.event_id, "video_id": video_id, "action": event.action,
                "start_frame": event.start_frame, "timestamp_delta_frames": delta_frames,
                "source_video_exists": True, "snapshot_exists": True, "clip_exists": True,
                "human_review_event_id": review_ids_by_key.get(key),
            })
            linked_count += 1
        per_execution.append({
            "execution_id": video_id,
            "worker_id": timeline["events"][0]["worker_id"] if events else None,
            "source_view": config["dataset"]["view"],
            "frozen_action_event_count": len(events),
            "evidence_linked_event_count": linked_count,
            "workflow_execution_status": "BLOCKED_PENDING_VALIDATED_SPEC",
            "workflow_trace_generated": False,
            "process_performance": "NOT_EVALUATED",
        })

    if matched_evidence != set(evidence_by_key):
        missing = sorted(set(evidence_by_key) - matched_evidence)
        raise ValueError(f"CP05 evidence records without a frozen action event: {missing}")
    if len(review_ids_by_key) != int(review_manifest.get("unique_event_count", -1)):
        raise ValueError("CP07 unique review event count does not match resolved CP05 evidence")

    event_artifact = {
        "status": "VERIFIED_FROM_FROZEN_CP05_PREDICTION_TIMELINES",
        "model": "MS-TCN seed-17 frozen outputs",
        "dataset_protocol": "IMPACT v1.1 TAS-S S2 split2 Disassembly_A/front held-out test",
        "event_count": len(records),
        "confidence_interpretation": "descriptive only; not evidence sufficiency",
        "evidence_status": "unknown; no validated evidence policy",
        "sources": {
            "cp05_config": "configs/cp05.yaml",
            "cp05_best_checkpoint_sha256": _sha256(project_root / "models" / "cp05_mstcn_best.pt"),
            "cp05_evidence_index_sha256": _sha256(evidence_index_path),
            "cp05_test_metrics_sha256": _sha256(frozen_test_metrics_path),
            "cp07_review_manifest_sha256": _sha256(review_manifest_path),
            "timelines": {
                path.relative_to(project_root).as_posix(): _sha256(path)
                for path, _ in timelines.values()
            },
        },
        "events": records,
    }
    evidence_audit = {
        "status": "PASS" if len(link_rows) == len(evidence_rows) else "FAIL",
        "frozen_action_event_count": len(records),
        "cp05_evidence_record_count": len(evidence_rows),
        "one_to_one_identity_matches": len(matched_evidence),
        "missing_source_video_snapshot_or_clip": 0,
        "human_review_unique_events": len(review_ids_by_key),
        "human_review_judgments_available": False,
        "media_validation_scope": "file existence and event identity/timestamp link; no visual semantic review performed",
        "events": link_rows,
    }
    trace_summary = {
        "workflow_execution_status": "BLOCKED_PENDING_VALIDATED_SPEC",
        "validated_workflow_exists": False,
        "process_performance": "NOT_EVALUATED",
        "reason": "configs/workflows/disassembly_A.yaml is absent; draft remains HUMAN_REVIEW_REQUIRED",
        "frozen_action_event_count": len(records),
        "evidence_linked_action_event_count": len(link_rows),
        "execution_summaries": per_execution,
    }
    return event_artifact, evidence_audit, trace_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare CP08 artifacts from frozen CP05 predictions; does not run inference.")
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    args = parser.parse_args()
    event_artifact, evidence_audit, trace_summary = prepare_artifacts(args.project_root)
    output_dir = args.project_root / "experiments" / "CP08"
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "action_events_frozen.json": event_artifact,
        "evidence_link_audit.json": evidence_audit,
        "process_trace_summary.json": trace_summary,
    }
    for filename, data in outputs.items():
        (output_dir / filename).write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"[ok] wrote {filename}")
    _write_evidence_handoff(args.project_root.resolve(), _read_json(args.project_root / "experiments" / "CP07" / "evidence_review_manifest.json"))
    print("[ok] wrote HUMAN_HANDOFF_CP08_EVIDENCE_REVIEW.md")
    print(f"[ok] verified {event_artifact['event_count']} frozen events and their evidence links")


if __name__ == "__main__":
    main()
