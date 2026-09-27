import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

from human_action.schemas import ActionEvent
from human_action.workflow import WorkflowEngine
from tools.validate_workflow import validate_workflow


def ev(action, t, worker="W1", status="sufficient", duration=1.0, end=None):
    return ActionEvent(worker, action, t, t + duration if end is None else end, duration, .9, "video", 1, 2, status)


def config(paths=None, **extra):
    wf = {"id": "golden", "valid_paths": paths or [{"id": "main", "steps": ["A", "B", "C"]}], "duration_limits_seconds": {}}
    wf.update(extra)
    return {"workflow": wf}


class CP06WorkflowGoldenTests(unittest.TestCase):
    def run_sequence(self, events, cfg=None, decisions=None):
        engine = WorkflowEngine(cfg or config(), "W1", "video", branch_decisions=decisions)
        result = engine.consume(events)
        return engine, result

    def test_01_correct_sequence(self):
        _, r = self.run_sequence([ev("A", 0), ev("B", 2), ev("C", 4)])
        self.assertEqual(r.event_statuses, ["accepted_transition", "accepted_transition", "completed"])

    def test_02_skipped_step(self):
        _, r = self.run_sequence([ev("A", 0), ev("C", 2)])
        self.assertIn("skipped_step", r.event_statuses)

    def test_03_out_of_order_step(self):
        _, r = self.run_sequence([ev("A", 0), ev("C", 2), ev("B", 4)])
        self.assertIn("invalid_transition", r.event_statuses)

    def test_04_repeated_step(self):
        _, r = self.run_sequence([ev("A", 0), ev("A", 2)])
        self.assertIn("repeated_step", r.event_statuses)

    def test_05_valid_finite_recovery_route(self):
        paths = [{"id": "main", "steps": ["A", "B", "C"]}, {"id": "recovery", "steps": ["A", "B", "A", "B", "C"]}]
        engine, _ = self.run_sequence([ev("A", 0), ev("B", 2), ev("A", 4), ev("B", 6), ev("C", 8)], config(paths))
        self.assertEqual(engine.finalize().selected_path, "recovery")

    def test_06_optional_step_is_explicit_route(self):
        cfg = config([{"id": "with", "steps": ["A", "B", "C"]}, {"id": "without", "steps": ["A", "C"]}])
        engine, _ = self.run_sequence([ev("A", 0), ev("C", 2)], cfg)
        self.assertTrue(engine.finalize().state.completed)

    def test_07_conditional_branch_is_explicit_route(self):
        cfg = config([{"id": "x", "steps": ["A", "B", "C"]}, {"id": "y", "steps": ["A", "D", "C"]}])
        cfg["workflow"]["conditional_paths"] = [{"path_id": "y", "condition_id": "extra_step_required", "condition": "owner says extra step is required"}]
        engine, _ = self.run_sequence([ev("A", 0), ev("D", 2), ev("C", 4)], cfg, {"extra_step_required": True})
        self.assertEqual(engine.finalize().selected_path, "y")

    def test_conditional_branch_without_explicit_decision_is_ambiguous(self):
        cfg = config([{"id": "base", "steps": ["A", "C"]}, {"id": "conditional", "steps": ["A", "B", "C"]}], conditional_paths=[{"path_id": "conditional", "condition_id": "needs_b", "condition": "source-backed condition"}])
        engine, r = self.run_sequence([ev("A", 0), ev("B", 2)], cfg)
        self.assertEqual(r.event_statuses[-1], "ambiguous_evidence")
        self.assertIn("B", engine.state().next_valid_steps)

    def test_restart_clears_previous_conditional_decisions(self):
        cfg = config([{"id": "base", "steps": ["A", "C"]}, {"id": "conditional", "steps": ["A", "B", "C"]}], conditional_paths=[{"path_id": "conditional", "condition_id": "needs_b", "condition": "source-backed condition"}])
        engine = WorkflowEngine(cfg, "W1", "video", {"needs_b": True})
        engine.reset(worker_id="W2", video_id="new")
        result = engine.consume([ev("A", 0, worker="W2"), ev("B", 2, worker="W2")])
        self.assertEqual(result.event_statuses[-1], "ambiguous_evidence")

    def test_08_restart_resets_execution_scope(self):
        engine, _ = self.run_sequence([ev("A", 0), ev("B", 2)])
        engine.reset(worker_id="W2", video_id="new")
        self.assertEqual(engine.state().expected_step, "A")

    def test_09_unknown_action(self):
        _, r = self.run_sequence([ev("Z", 0)])
        self.assertIn("unknown_action", r.event_statuses)

    def test_10_ambiguous_and_insufficient_evidence_do_not_advance(self):
        engine, r = self.run_sequence([ev("A", 0, status="ambiguous"), ev("A", 2, status="insufficient")])
        self.assertEqual(r.event_statuses, ["ambiguous", "insufficient"])
        self.assertEqual(engine.state().expected_step, "A")

    def test_11_worker_isolation(self):
        engine, r = self.run_sequence([ev("A", 0), ev("B", 2, worker="W2")])
        self.assertEqual(r.event_statuses[-1], "insufficient_evidence")
        self.assertEqual(engine.state().expected_step, "B")

    def test_12_overlapping_interval_rejected(self):
        engine, r = self.run_sequence([ev("A", 0, duration=3), ev("B", 2)])
        self.assertEqual(r.event_statuses[-1], "insufficient_evidence")
        self.assertEqual(engine.state().expected_step, "B")

    def test_13_duration_policy_disabled(self):
        _, r = self.run_sequence([ev("A", 0, duration=100)])
        self.assertEqual(r.violations, [])

    def test_14_timeout_policy_disabled(self):
        errs = validate_workflow(config(timeout_policy={"enabled": False}), {"A", "B", "C"})
        self.assertFalse(any("timeout" in e for e in errs))

    def test_15_completion(self):
        engine, _ = self.run_sequence([ev("A", 0), ev("B", 2), ev("C", 4)])
        self.assertTrue(engine.finalize().state.completed)

    def test_enabled_timeout_uses_only_configured_policy(self):
        engine = WorkflowEngine(config(timeout_policy={"enabled": True, "seconds": 3, "source": "fixture"}), "W1", "video")
        result = engine.finalize(timestamp=4)
        self.assertIn("TIMEOUT", [v.violation_type for v in result.violations])

    def test_validator_checks_state_ids_edges_reachability_terminal_and_branches(self):
        wf = {"workflow": {"id": "x", "version": "r1", "approved_by": "owner", "approved_on": "2026-09-27",
            "action_vocabulary": ["A", "B"], "action_disposition": {"A": "required", "B": "required"},
            "valid_paths": [{"id": "route", "steps": ["A", "B"]}], "completion": {"condition": "owner confirmed"},
            "states": [{"id": "s", "action": "A"}, {"id": "s", "action": "B"}, {"id": "lost", "action": "B"}],
            "start_state": "s", "terminal_states": ["lost"], "transitions": [{"from": "s", "to": "missing", "conditional": True}]}}
        errors = validate_workflow(wf, {"A", "B"})
        self.assertTrue(any("state IDs" in e for e in errors))
        self.assertTrue(any("undefined state" in e for e in errors))
        self.assertTrue(any("unreachable states" in e for e in errors))
        self.assertTrue(any("conditional transition" in e for e in errors))

    def test_validator_rejects_ambiguous_optional_duration_and_timeout(self):
        wf = {"workflow": {"id": "x", "version": "r1", "approved_by": "owner", "approved_on": "2026-09-27",
            "status": "HUMAN_REVIEW_REQUIRED", "action_vocabulary": ["A", "B"],
            "action_disposition": {"A": "required", "B": "optional"},
            "valid_paths": [{"id": "main", "steps": ["A", "B"]}], "completion": {"condition": "owner confirmed"},
            "optional_steps": ["B", "B"], "conditional_paths": [{"path_id": "main"}],
            "duration_policy": {"enabled": True, "source": "source.pdf#p1", "rules": {"A": {"min": 10, "max": 2}}},
            "timeout_policy": {"enabled": True, "seconds": -1, "source": "source.pdf#p1"}}}
        errors = validate_workflow(wf, {"A", "B"})
        self.assertTrue(any("HUMAN_VALIDATED" in e for e in errors))
        self.assertTrue(any("optional_steps contains duplicates" in e for e in errors))
        self.assertTrue(any("require path_id and" in e for e in errors))
        self.assertTrue(any("invalid finite bounds" in e for e in errors))
        self.assertTrue(any("timeout_policy.seconds" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
