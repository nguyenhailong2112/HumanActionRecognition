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
        result = engine.finalize(10.0, procedure_ended=True)
        self.assertTrue(result.state.completed)
        self.assertEqual(result.violations, [])
        self.assertEqual(result.finalization_status, "procedure_ended_complete")

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
        self.assertEqual([item.action for item in engine.events], ["A", "C"])

    def test_rejected_repeat_does_not_pollute_history_or_block_later_valid_step(self):
        engine = WorkflowEngine(workflow(), "W1")
        result = engine.consume([event("A"), event("A"), event("B")])
        self.assertEqual(result.event_statuses, ["accepted_transition", "repeated_step", "accepted_transition"])
        self.assertEqual([item.action for item in engine.observations], ["A", "A", "B"])
        self.assertEqual([item.action for item in engine.events], ["A", "B"])
        self.assertEqual(result.state.current_step, "B")
        self.assertEqual(result.state.expected_step, "C")
        self.assertEqual([item.violation_type for item in result.violations], ["REPEATED_STEP"])

    def test_rejected_repetition_does_not_change_current_accepted_step(self):
        engine = WorkflowEngine(workflow(), "W1")
        result = engine.consume([event("A"), event("A")])
        self.assertEqual(result.event_statuses, ["accepted_transition", "repeated_step"])
        self.assertEqual([item.action for item in engine.observations], ["A", "A"])
        self.assertEqual([item.action for item in engine.events], ["A"])
        self.assertEqual(result.state.current_step, "A")
        self.assertEqual(result.state.expected_step, "B")

    def test_unknown_action_does_not_mutate_accepted_state(self):
        engine = WorkflowEngine(workflow(), "W1")
        result = engine.consume([event("X")])
        self.assertEqual(result.event_statuses, ["unknown_action"])
        self.assertEqual([item.action for item in engine.observations], ["X"])
        self.assertEqual(engine.events, [])
        self.assertIsNone(result.state.current_step)
        self.assertEqual(result.state.expected_step, "A")

    def test_ambiguous_and_insufficient_evidence_remain_observations_only(self):
        engine = WorkflowEngine(workflow(), "W1")
        ambiguous = ActionEvent("W1", "A", 0, 1, 1, .9, "demo", 0, 29, "ambiguous")
        insufficient = ActionEvent("W1", "A", 3, 4, 1, .9, "demo", 90, 119, "insufficient")
        result = engine.consume([ambiguous, insufficient])
        self.assertEqual(result.event_statuses, ["ambiguous", "insufficient"])
        self.assertEqual(engine.observations, [ambiguous, insufficient])
        self.assertEqual(engine.events, [])
        self.assertIsNone(result.state.current_step)
        self.assertEqual(result.state.expected_step, "A")

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
        finalized = engine.finalize(15.0, procedure_ended=True)
        self.assertIn("INCOMPLETE_PROCEDURE", [item.violation_type for item in finalized.violations])
        self.assertEqual(finalized.finalization_status, "procedure_ended_incomplete")

    def test_observation_end_does_not_claim_procedure_incomplete(self):
        engine = WorkflowEngine(workflow(), "W1")
        engine.consume([event("A")])
        finalized = engine.finalize(3.0)
        self.assertEqual(finalized.finalization_status, "observation_ended_unconfirmed")
        self.assertNotIn("INCOMPLETE_PROCEDURE", [item.violation_type for item in finalized.violations])

    def test_completed_workflow_without_termination_signal_remains_observation_end(self):
        engine = WorkflowEngine(workflow([{"id": "one", "steps": ["A"]}]), "W1")
        engine.consume([event("A")])
        finalized = engine.finalize(2.0)
        self.assertTrue(finalized.state.completed)
        self.assertEqual(finalized.finalization_status, "observation_ended_unconfirmed")
        self.assertNotIn("INCOMPLETE_PROCEDURE", [item.violation_type for item in finalized.violations])


if __name__ == "__main__":
    unittest.main()
