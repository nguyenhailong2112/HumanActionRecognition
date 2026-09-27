import unittest
import sys
import itertools
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from human_action.schemas import ActionEvent
from human_action.workflow import WorkflowEngine


_clock = itertools.count()


def event(action, start=None, duration=2.0, worker="W1"):
    if start is None:
        start = float(next(_clock) * 3)
    return ActionEvent(worker, action, start, start + duration, duration, 0.9, "demo", 30, 90, "sufficient")


def workflow(paths=None):
    return {"workflow": {
        "id": "test",
        "valid_paths": paths or [{"id": "route", "steps": ["A", "B", "C", "D"]}],
        "duration_limits_seconds": {"B": {"min": 1.0, "max": 5.0}},
    }}


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        global _clock
        _clock = itertools.count()

    def test_valid_sequence_and_completion(self):
        engine = WorkflowEngine(workflow(), "W1")
        result = engine.consume([event("A"), event("B"), event("C"), event("D")])
        result = engine.finalize(10.0)
        self.assertTrue(result.state.completed)
        self.assertEqual(result.violations, [])

    def test_reset_clears_execution_state_and_changes_worker_scope(self):
        engine = WorkflowEngine(workflow(), "W1", "video_1")
        engine.consume([event("A"), event("C")])
        self.assertTrue(engine.violations)
        engine.reset(worker_id="W2", video_id="video_2")
        self.assertEqual(engine.state().expected_step, "A")
        self.assertEqual(engine.events, [])
        self.assertEqual(engine.violations, [])
        result = engine.consume([event("A", worker="W2"), event("B", worker="W2"), event("C", worker="W2"), event("D", worker="W2")])
        self.assertTrue(result.state.completed)
        self.assertEqual(result.violations, [])

    def test_configured_valid_variant_is_not_flagged(self):
        engine = WorkflowEngine(workflow([
            {"id": "abc", "steps": ["A", "B", "C", "D"]},
            {"id": "acb", "steps": ["A", "C", "B", "D"]},
        ]), "W1")
        result = engine.consume([event("A"), event("C"), event("B"), event("D")])
        result = engine.finalize(9.0)
        self.assertTrue(result.state.completed)
        self.assertEqual(result.violations, [])

    def test_process_owner_approved_finite_rework_path_is_valid(self):
        engine = WorkflowEngine(workflow([
            {"id": "canonical", "steps": ["A", "B", "C", "D"]},
            {"id": "rework", "steps": ["A", "B", "A", "B", "C", "D"]},
        ]), "W1")
        result = engine.consume([event("A"), event("B"), event("A"), event("B"), event("C"), event("D")])
        result = engine.finalize(15.0)
        self.assertTrue(result.state.completed)
        self.assertEqual(result.selected_path, "rework")
        self.assertEqual(result.violations, [])

    def test_skipped_step_and_wrong_sequence_are_reported(self):
        engine = WorkflowEngine(workflow(), "W1")
        result = engine.consume([event("A"), event("C")])
        kinds = [item.violation_type for item in result.violations]
        self.assertIn("SKIPPED_STEP", kinds)
        self.assertIn("WRONG_SEQUENCE", kinds)

    def test_repeat_is_reported_without_advancing_workflow(self):
        engine = WorkflowEngine(workflow(), "W1")
        result = engine.consume([event("A"), event("A")])
        self.assertIn("REPEATED_STEP", [item.violation_type for item in result.violations])
        self.assertEqual(result.state.expected_step, "B")

    def test_out_of_order_known_action_is_wrong_sequence(self):
        engine = WorkflowEngine(workflow(), "W1")
        result = engine.consume([event("B")])
        self.assertIn("WRONG_SEQUENCE", [item.violation_type for item in result.violations])

    def test_a_c_b_d_marks_wrong_order_after_skip(self):
        engine = WorkflowEngine(workflow(), "W1")
        result = engine.consume([event("A"), event("C"), event("B"), event("D")])
        kinds = [item.violation_type for item in result.violations]
        self.assertIn("SKIPPED_STEP", kinds)
        self.assertIn("WRONG_SEQUENCE", kinds)

    def test_unexpected_action_is_reported_without_advancing(self):
        engine = WorkflowEngine(workflow(), "W1")
        result = engine.consume([event("A"), event("X")])
        self.assertIn("UNEXPECTED_ACTION", [item.violation_type for item in result.violations])
        self.assertEqual(result.state.expected_step, "B")

    def test_too_fast_too_slow_timeout_and_incomplete(self):
        engine = WorkflowEngine(workflow(), "W1")
        result = engine.consume([event("A"), event("B", start=2.0, duration=0.2), event("B", start=3.0, duration=8.0)])
        kinds = [item.violation_type for item in result.violations]
        self.assertIn("TOO_FAST", kinds)
        self.assertIn("TOO_SLOW", kinds)
        self.assertIn("TIMEOUT", kinds)
        self.assertIn("REPEATED_STEP", kinds)
        finalized = engine.finalize(15.0)
        self.assertIn("INCOMPLETE_PROCEDURE", [item.violation_type for item in finalized.violations])


if __name__ == "__main__":
    unittest.main()
