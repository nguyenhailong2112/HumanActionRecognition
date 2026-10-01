import sys
import unittest
import json
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from human_action.metrics import action_metrics
from human_action.schemas import ActionEvent, to_dict
from human_action.temporal import to_action_events
from human_action.workflow import WorkflowEngine, workflow_is_enabled
from human_action.workflow_trace import build_workflow_trace
from tools.analyze_cp06 import summarize
from tools.validate_workflow import validate_workflow
from tools.prepare_cp08_artifacts import prepare_artifacts


class CP07ContractAndAggregationTests(unittest.TestCase):
    def test_action_event_round_trip_preserves_workflow_and_evidence_fields(self):
        event = ActionEvent("W1", "A", 1.0, 2.0, 1.0, 0.8, "exec-1", 5, 9,
                            "sufficient", "front", "exec-1:5-9:A", ("snapshot.jpg", "clip.mp4"))
        self.assertEqual(ActionEvent.from_dict(to_dict(event)), event)

    def test_temporal_conversion_populates_stable_execution_view_event_id(self):
        from human_action.schemas import ActionSegment
        items = to_action_events([ActionSegment("A", 1, 2, 1, .8, 5, 9)], "W1", "exec-1", view="front")
        self.assertEqual(items[0].view, "front")
        self.assertEqual(items[0].video_id, "exec-1")
        self.assertEqual(items[0].event_id, "exec-1:5-9:A")
        self.assertEqual(items[0].evidence_status, "unknown")

    def test_pooled_temporal_metrics_keep_execution_boundaries(self):
        order = ["NULL", "A", "B"]
        sequences = [
            (np.array([1, 1]), np.array([1, 1])),
            (np.array([1, 1]), np.array([1, 1])),
        ]
        rows = [{"gt": gt, "pred": pred, "action": action_metrics(gt, pred, order, background_label="NULL")} for gt, pred in sequences]
        result = summarize(rows, order)["pooled_frames"]
        self.assertEqual(result["normalized_edit_score"], 100.0)
        self.assertEqual(result["segmental"]["F1@50"]["f1"], 1.0)
        naive = action_metrics(np.concatenate([x[0] for x in sequences]), np.concatenate([x[1] for x in sequences]), order, background_label="NULL")
        self.assertNotEqual(naive["gt_action_segments"], result["gt_action_segments"])
        self.assertEqual(naive["gt_action_segments"], 1)
        self.assertEqual(result["gt_action_segments"], 2)

    def test_workflow_evidence_link_does_not_change_semantic_decision(self):
        event = ActionEvent("W1", "A", 0, 1, 1, .9, "exec-1", 0, 4,
                            "sufficient", "front", "exec-1:0-4:A", ("snapshot.jpg",))
        engine = WorkflowEngine({"workflow": {"id": "toy", "valid_paths": [{"id": "r", "steps": ["A"]}]}}, "W1", "exec-1")
        result = engine.consume([event])
        self.assertEqual(result.event_statuses, ["completed"])
        self.assertEqual(event.evidence_refs, ("snapshot.jpg",))

    def test_workflow_instances_isolate_execution_state(self):
        cfg = {"workflow": {"id": "toy", "valid_paths": [{"id": "r", "steps": ["A", "B"]}]}}
        first = WorkflowEngine(cfg, "W1", "exec-1")
        second = WorkflowEngine(cfg, "W1", "exec-2")
        first.consume([ActionEvent("W1", "A", 0, 1, 1, .9, "exec-1", evidence_status="sufficient")])
        self.assertEqual(first.state().expected_step, "B")
        self.assertEqual(second.state().expected_step, "A")

    def test_malformed_event_is_not_applied(self):
        engine = WorkflowEngine({"workflow": {"id": "toy", "valid_paths": [{"id": "r", "steps": ["A"]}]}}, "W1", "exec")
        malformed = ActionEvent("W1", "A", 2, 1, 1, .9, "exec")
        self.assertEqual(engine.consume([malformed]).event_statuses, ["insufficient_evidence"])
        self.assertFalse(engine.state().completed)

    def test_synthetic_workflow_trace_links_event_evidence_and_keeps_uncertainty(self):
        cfg = {"workflow": {"id": "toy", "valid_paths": [{"id": "r", "steps": ["A"]}]}}
        event = ActionEvent("W1", "A", 0, 1, 1, .9, "exec", 0, 4, "sufficient", "front", "evt-1", ("snapshot.jpg",))
        trace = build_workflow_trace(cfg, [event], "W1", "exec", "front", synthetic_validation=True)
        row = trace["events"][0]
        self.assertEqual(row["transition_result"], "completed")
        self.assertEqual(row["evidence_refs"], ["snapshot.jpg"])
        self.assertEqual(trace["scope"], "synthetic_logic_validation")
        self.assertEqual(trace["process_performance"], "NOT_EVALUATED_WITHOUT_VALID_PROCESS_GROUND_TRUTH")

    def test_trace_keeps_observation_end_distinct_from_procedure_end(self):
        cfg = {"workflow": {"id": "toy", "valid_paths": [{"id": "r", "steps": ["A", "B"]}]}}
        event = ActionEvent("W1", "A", 0, 1, 1, .9, "exec", 0, 4, "ambiguous")
        trace = build_workflow_trace(cfg, [event], "W1", "exec", "front", synthetic_validation=True)
        self.assertEqual(trace["finalization_status"], "observation_ended_unconfirmed")
        self.assertEqual([v["violation_type"] for v in trace["final_violations"]], ["AMBIGUOUS_EVIDENCE"])
        ended = build_workflow_trace(cfg, [event], "W1", "exec", "front",
                                     synthetic_validation=True, procedure_ended=True)
        self.assertEqual(ended["finalization_status"], "procedure_ended_incomplete")
        self.assertEqual([v["violation_type"] for v in ended["final_violations"]], ["AMBIGUOUS_EVIDENCE", "INCOMPLETE_PROCEDURE"])

    def test_cp08_frozen_event_preparation_preserves_unknown_evidence_and_links(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for directory in ("configs/workflows", "experiments/CP05", "experiments/CP06", "experiments/CP07", "models", "results/cp05/evaluation/evidence"):
                (root / directory).mkdir(parents=True, exist_ok=True)
            (root / "configs/cp05.yaml").write_text("dataset:\n  view: front\nactions:\n  background: NULL\n", encoding="utf-8")
            (root / "models/cp05_mstcn_best.pt").write_bytes(b"frozen-checkpoint-fixture")
            source_video = root / "source.mp4"
            snapshot = root / "results/cp05/evaluation/evidence/evt.jpg"
            clip = root / "results/cp05/evaluation/evidence/evt.mp4"
            for path in (source_video, snapshot, clip):
                path.write_bytes(b"fixture")
            video_id = "exec-1"
            event = {"worker_id": "W1", "action": "A", "start_time": .4, "end_time": .6,
                     "duration": .2, "confidence": .8, "video_id": video_id,
                     "start_frame": 12, "end_frame": 17}
            segment = {key: value for key, value in event.items() if key not in {"worker_id", "video_id"}}
            timeline = {"video_id": video_id, "model": "mstcn", "events": [event], "segments": [segment]}
            (root / "results/cp05/evaluation/exec-1_mstcn_timeline.json").write_text(json.dumps(timeline), encoding="utf-8")
            evidence = {"video_id": video_id, "action": "A", "action_event_start_frame": 12,
                        "action_event_timestamp_seconds": .4, "confidence": .8,
                        "source_video_fps": 30, "source_video_frame_count": 100,
                        "source_video": str(source_video), "snapshot": str(snapshot), "clip": str(clip)}
            (root / "experiments/CP05/evidence_index.json").write_text(json.dumps({"records": [evidence]}), encoding="utf-8")
            (root / "experiments/CP06/action_metrics.json").write_text(json.dumps({"video_ids": [video_id]}), encoding="utf-8")
            (root / "results/cp05/evaluation/test_metrics.json").write_text(
                json.dumps({"results": [{"model": "mstcn", "video_id": video_id, "video_path": str(source_video)}]}),
                encoding="utf-8",
            )
            review = {"status": "HUMAN_REVIEW_REQUIRED", "unique_event_count": 1,
                      "events": [{"event_id": "review-1", "video_id": video_id,
                                  "predicted_action": "A", "timestamp_seconds": .4}]}
            (root / "experiments/CP07/evidence_review_manifest.json").write_text(json.dumps(review), encoding="utf-8")

            action_events, link_audit, trace_summary = prepare_artifacts(root)
            record = action_events["events"][0]
            self.assertEqual(record["action_event"]["evidence_status"], "unknown")
            self.assertEqual(record["action_event"]["evidence_refs"], (str(snapshot), str(clip)))
            self.assertEqual(record["human_review_event_id"], "review-1")
            self.assertEqual(link_audit["one_to_one_identity_matches"], 1)
            self.assertEqual(trace_summary["workflow_execution_status"], "BLOCKED_PENDING_VALIDATED_SPEC")

    def test_trace_rejects_cross_execution_events(self):
        cfg = {"workflow": {"id": "toy", "valid_paths": [{"id": "r", "steps": ["A"]}]}}
        event = ActionEvent("W1", "A", 0, 1, 1, .9, "other")
        with self.assertRaises(ValueError):
            build_workflow_trace(cfg, [event], "W1", "exec", "front", synthetic_validation=True)

    def test_trace_refuses_human_review_required_workflow(self):
        cfg = {"workflow": {"id": "draft", "status": "HUMAN_REVIEW_REQUIRED", "synthetic_fixture": True, "valid_paths": [{"id": "r", "steps": ["A"]}]}}
        with self.assertRaisesRegex(ValueError, "HUMAN_VALIDATED"):
            build_workflow_trace(cfg, [], "W1", "exec", "front")

    def test_trace_refuses_human_validated_but_disabled_workflow(self):
        cfg = {"workflow": {"id": "approved", "status": "HUMAN_VALIDATED", "enabled": False, "valid_paths": [{"id": "r", "steps": ["A"]}]}}
        with self.assertRaisesRegex(ValueError, "workflow.enabled"):
            build_workflow_trace(cfg, [], "W1", "exec", "front")

    def test_trace_runs_after_explicit_validated_enablement(self):
        cfg = {"workflow": {"id": "toy", "status": "HUMAN_VALIDATED", "enabled": True, "valid_paths": [{"id": "r", "steps": ["A"]}]}}
        event = ActionEvent("W1", "A", 0, 1, 1, .9, "exec", evidence_status="sufficient")
        trace = build_workflow_trace(cfg, [event], "W1", "exec", "front")
        self.assertEqual(trace["scope"], "deterministic_workflow_interpretation")
        self.assertTrue(trace["final_state"]["completed"])

    def test_workflow_is_disabled_by_default_and_requires_approval_when_enabled(self):
        self.assertFalse(workflow_is_enabled({"workflow": {"valid_paths": [{"id": "demo", "steps": ["A"]}]}}))
        self.assertFalse(workflow_is_enabled({"workflow": {"enabled": False, "status": "HUMAN_REVIEW_REQUIRED"}}))
        with self.assertRaisesRegex(ValueError, "HUMAN_VALIDATED"):
            workflow_is_enabled({"workflow": {"enabled": True, "status": "HUMAN_REVIEW_REQUIRED"}})
        self.assertTrue(workflow_is_enabled({"workflow": {"enabled": True, "status": "HUMAN_VALIDATED"}}))
        with self.assertRaisesRegex(ValueError, "boolean"):
            workflow_is_enabled({"workflow": {"enabled": "false", "status": "HUMAN_VALIDATED"}})

    def test_action_metrics_reject_length_mismatch_and_empty_inputs(self):
        self.assertEqual(action_metrics(np.array([1]), np.array([1]), ["NULL", "A"], background_label="NULL")["frame_accuracy"], 1.0)
        with self.assertRaisesRegex(ValueError, "lengths are not aligned: 2 != 1"):
            action_metrics(np.array([1, 1]), np.array([1]), ["NULL", "A"], background_label="NULL")
        with self.assertRaisesRegex(ValueError, "empty sequence"):
            action_metrics(np.array([], dtype=int), np.array([], dtype=int), ["NULL", "A"], background_label="NULL")
        with self.assertRaisesRegex(ValueError, "Specify background_id or background_label"):
            action_metrics(np.array([1]), np.array([1]), ["NULL", "A"])

    def test_background_is_resolved_by_label_not_fixed_id_zero(self):
        result = action_metrics(np.array([0, 1]), np.array([0, 1]), ["A", "NULL"], background_label="NULL")
        self.assertEqual(result["macro_f1_actions"], 1.0)
        self.assertEqual(result["gt_action_segments"], 1)

    def test_workflow_retains_uncertain_observation_without_advancing(self):
        engine = WorkflowEngine({"workflow": {"id": "toy", "valid_paths": [{"id": "r", "steps": ["A", "B"]}]}}, "W1", "exec")
        uncertain = ActionEvent("W1", "A", 0, 1, 1, .99, "exec", evidence_status="ambiguous")
        result = engine.consume([uncertain])
        self.assertEqual(engine.observations, [uncertain])
        self.assertEqual(result.event_statuses, ["ambiguous"])
        self.assertEqual(result.state.expected_step, "A")
        self.assertEqual(engine.events, [])

    def test_route_skip_uses_selected_candidate_position(self):
        cfg = {"workflow": {"id": "routes", "valid_paths": [
            {"id": "long-skip", "steps": ["P", "X", "Y", "Z", "D"]},
            {"id": "selected", "steps": ["P", "B", "D", "E"]},
        ]}}
        engine = WorkflowEngine(cfg, "W1")
        # Exercise a valid branched engine state with differing route positions.
        engine.candidates = [(0, 2), (1, 1)]
        result = engine.consume([ActionEvent("W1", "D", 0, 1, 1, .9, "demo", evidence_status="sufficient")])
        skipped = [v.expected_step for v in result.violations if v.violation_type == "SKIPPED_STEP"]
        self.assertEqual(skipped, ["B"])
        self.assertNotIn("X", skipped)
        self.assertNotIn("Y", skipped)
        self.assertEqual(engine.candidates, [(1, 3)])

    def test_prerequisite_workflow_accepts_both_partial_orders(self):
        cfg = {"workflow": {"id": "dag", "required_actions": ["A", "B", "C"],
                             "prerequisites": {"A": [], "B": [], "C": ["A", "B"]}}}
        for order in (("A", "B", "C"), ("B", "A", "C")):
            engine = WorkflowEngine(cfg, "W1", "exec")
            events = [ActionEvent("W1", action, i * 2, i * 2 + 1, 1, .9, "exec", evidence_status="sufficient")
                      for i, action in enumerate(order)]
            result = engine.consume(events)
            self.assertTrue(result.state.completed)
            self.assertEqual(result.violations, [])

    def test_prerequisite_workflow_rejects_action_before_prerequisites(self):
        cfg = {"workflow": {"id": "dag", "required_actions": ["A", "B", "C"],
                             "prerequisites": {"A": [], "B": [], "C": ["A", "B"]}}}
        engine = WorkflowEngine(cfg, "W1", "exec")
        event = ActionEvent("W1", "C", 0, 1, 1, .9, "exec", evidence_status="sufficient")
        result = engine.consume([event])
        self.assertFalse(result.state.completed)
        self.assertEqual(result.event_statuses, ["invalid_transition"])
        self.assertEqual(engine.completed_actions, set())
        self.assertEqual(len(engine.observations), 1)
        self.assertEqual(engine.events, [event])

    def test_validator_accepts_acyclic_prerequisite_schema_without_route_enumeration(self):
        workflow = {"workflow": {
            "status": "HUMAN_VALIDATED", "id": "synthetic", "version": "test-v1",
            "approved_by": "test reviewer", "approved_on": "2026-09-27",
            "action_vocabulary": ["A", "B", "C"],
            "action_disposition": {action: "required" for action in ("A", "B", "C")},
            "required_actions": ["A", "B", "C"],
            "prerequisites": {"A": [], "B": [], "C": ["A", "B"]},
            "completion": {"condition": "all required actions accepted"},
            "timeout_policy": {"enabled": False},
        }}
        self.assertEqual(validate_workflow(workflow, {"A", "B", "C"}), [])
        workflow["workflow"]["prerequisites"]["A"] = ["C"]
        self.assertTrue(any("cycle" in error for error in validate_workflow(workflow, {"A", "B", "C"})))


if __name__ == "__main__":
    unittest.main()
