import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from human_action.config import load_config
from human_action.schemas import ActionEvent
from human_action.workflow import WorkflowEngine, workflow_is_enabled
from human_action.workflow_trace import build_workflow_trace
from tools.validate_workflow import validate_workflow


WORKFLOW_PATH = ROOT / "configs/workflows/disassembly_A.yaml"
CORE = [
    "UNSCREW_ANTI_VIBRATION_HANDLE",
    "REMOVE_LOCKING_LEVER_ASSEMBLY",
    "EXTRACT_BEARING_PLATE_ASSEMBLY",
    "DETACH_ADAPTER_PLATE",
    "REMOVE_ROTOR_ASSEMBLY",
]


def event(action, start, *, worker="W1", execution="exec-1", status="sufficient"):
    return ActionEvent(worker, action, start, start + 1, 1, .9, execution,
                       int(start * 30), int((start + 1) * 30), status,
                       "front", f"{execution}:{start}:{action}", ("evidence.jpg",))


class CP11ResearchWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_config(WORKFLOW_PATH)
        cls.workflow = cls.config["workflow"]
        cls.actions = set(cls.workflow["action_disposition"])

    def test_cp11_workflow_passes_project_scope_validator(self):
        self.assertEqual(validate_workflow(self.config, self.actions), [])
        self.assertEqual(self.workflow["status"], "RESEARCH_APPROVED")
        self.assertFalse(self.workflow["factory_sop_validated"])

    def test_research_approval_is_narrowly_scoped_and_enabled(self):
        self.assertTrue(workflow_is_enabled(self.config))
        invalid = {"workflow": dict(self.workflow, factory_sop_validated=True)}
        with self.assertRaisesRegex(ValueError, "factory_sop_validated: false"):
            workflow_is_enabled(invalid)
        invalid = {"workflow": dict(self.workflow, approval_scope="FACTORY")}
        with self.assertRaisesRegex(ValueError, "PROJECT_RESEARCH"):
            workflow_is_enabled(invalid)

    def test_validator_rejects_research_approval_without_explicit_factory_boundary(self):
        invalid = {"workflow": dict(self.workflow, factory_sop_validated=None)}
        errors = validate_workflow(invalid, self.actions)
        self.assertTrue(any("factory_sop_validated: false" in item for item in errors))
        invalid = {"workflow": dict(self.workflow, approval_basis="")}
        errors = validate_workflow(invalid, self.actions)
        self.assertTrue(any("approval_basis" in item for item in errors))

    def test_both_partial_orders_complete_without_mutual_removal_order(self):
        orders = [CORE, [CORE[0], CORE[2], CORE[1], CORE[4], CORE[3]]]
        for order in orders:
            engine = WorkflowEngine(self.config, "W1", "exec-1")
            result = engine.consume([event(action, index * 2) for index, action in enumerate(order)])
            self.assertTrue(result.state.completed)
            self.assertEqual(result.violations, [])
            self.assertEqual(result.event_statuses[-1], "completed")

    def test_major_removal_requires_unscrew_but_removals_remain_unordered(self):
        engine = WorkflowEngine(self.config, "W1", "exec-1")
        result = engine.consume([event(CORE[1], 0)])
        self.assertEqual(result.event_statuses, ["invalid_transition"])
        self.assertEqual(engine.completed_actions, set())
        self.assertIn("UNSCREW_ANTI_VIBRATION_HANDLE", engine.state().next_valid_steps)
        self.assertEqual(self.workflow["prerequisites"][CORE[1]], [CORE[0]])
        for action in CORE[2:]:
            self.assertEqual(self.workflow["prerequisites"][action], [CORE[0]])

    def test_out_of_scope_store_retrieve_install_are_preserved_and_ignored(self):
        actions = ["STORE_GEARBOX_HOUSING", "RETRIEVE_BEARING_PLATE_ASSEMBLY", "INSTALL_ROTOR_ASSEMBLY"]
        engine = WorkflowEngine(self.config, "W1", "exec-1")
        before = engine.state()
        events = [event(action, index * 2, status="unknown") for index, action in enumerate(actions)]
        result = engine.consume(events)
        self.assertEqual(result.event_statuses, ["out_of_scope_ignored"] * 3)
        self.assertEqual(engine.observations, events)
        self.assertEqual(engine.events, [])
        self.assertEqual(result.state, before)
        self.assertEqual(result.violations, [])

    def test_trace_surfaces_out_of_scope_observation_without_claiming_violation(self):
        trace = build_workflow_trace(self.config, [event("STORE_TOOL", 0, status="unknown")],
                                     "W1", "exec-1", "front")
        record = trace["events"][0]
        self.assertEqual(record["transition_result"], "out_of_scope_ignored")
        self.assertEqual(record["compliance_interpretation"], "out_of_scope_ignored")
        self.assertEqual(record["evidence_status"], "unknown")
        self.assertEqual(trace["final_violations"], [])
        self.assertFalse(trace["final_state"]["completed"])

    def test_unknown_ambiguous_wrong_worker_and_unknown_action_do_not_complete(self):
        engine = WorkflowEngine(self.config, "W1", "exec-1")
        observed = [
            event(CORE[0], 0, status="unknown"),
            event(CORE[0], 2, status="ambiguous"),
            event(CORE[0], 4, worker="W2"),
            event("NOT_A_PROJECT_ACTION", 6),
        ]
        result = engine.consume(observed)
        self.assertEqual(result.event_statuses, ["unknown", "ambiguous", "insufficient_evidence", "unknown_action"])
        self.assertEqual(engine.observations, observed)
        self.assertEqual(engine.completed_actions, set())

    def test_repeat_is_reported_without_becoming_a_mistake(self):
        engine = WorkflowEngine(self.config, "W1", "exec-1")
        result = engine.consume([event(CORE[0], 0), event(CORE[0], 2)])
        self.assertEqual(result.event_statuses, ["accepted_transition", "repeated_step"])
        self.assertEqual([v.violation_type for v in result.violations], ["REPEATED_STEP"])
        self.assertEqual(len(engine.observations), 2)
        self.assertEqual(len(engine.events), 1)

    def test_observation_end_is_not_incomplete_but_explicit_end_is(self):
        engine = WorkflowEngine(self.config, "W1", "exec-1")
        engine.consume([event(CORE[0], 0)])
        self.assertEqual(engine.finalize().finalization_status, "observation_ended_unconfirmed")
        ended = engine.finalize(procedure_ended=True)
        self.assertEqual(ended.finalization_status, "procedure_ended_incomplete")
        self.assertIn("INCOMPLETE_PROCEDURE", [item.violation_type for item in ended.violations])

    def test_explicit_completion_and_execution_isolation(self):
        engine = WorkflowEngine(self.config, "W1", "exec-1")
        result = engine.consume([event(action, index * 2) for index, action in enumerate(CORE)])
        self.assertTrue(result.state.completed)
        self.assertEqual(engine.finalize(procedure_ended=True).finalization_status, "procedure_ended_complete")
        fresh = WorkflowEngine(self.config, "W1", "exec-2")
        self.assertFalse(fresh.state().completed)
        self.assertEqual(fresh.state().next_valid_steps, (CORE[0],))


if __name__ == "__main__":
    unittest.main()
