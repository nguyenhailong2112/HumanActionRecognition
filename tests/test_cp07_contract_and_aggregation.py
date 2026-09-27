import sys
import unittest
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
        rows = [{"gt": gt, "pred": pred, "action": action_metrics(gt, pred, order)} for gt, pred in sequences]
        result = summarize(rows, order)["pooled_frames"]
        self.assertEqual(result["normalized_edit_score"], 100.0)
        self.assertEqual(result["segmental"]["F1@50"]["f1"], 1.0)
        naive = action_metrics(np.concatenate([x[0] for x in sequences]), np.concatenate([x[1] for x in sequences]), order)
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


if __name__ == "__main__":
    unittest.main()
