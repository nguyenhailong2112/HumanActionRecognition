from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any

from .schemas import ActionEvent, Violation, WorkflowState


@dataclass
class WorkflowResult:
    state: WorkflowState
    violations: list[Violation]
    selected_path: str | None
    event_statuses: list[str] | None = None
    finalization_status: str | None = None


def workflow_is_enabled(config: dict[str, Any]) -> bool:
    """Workflow evaluation is opt-in and requires explicit semantic approval."""
    workflow = config.get("workflow") or {}
    if not isinstance(workflow, dict):
        raise ValueError("workflow configuration must be a mapping")
    enabled = workflow.get("enabled", False)
    if not isinstance(enabled, bool):
        raise ValueError("workflow.enabled must be a boolean")
    if not enabled:
        return False
    if workflow.get("status") != "HUMAN_VALIDATED":
        raise ValueError("workflow.enabled requires workflow.status: HUMAN_VALIDATED")
    return True


class WorkflowEngine:
    """Deterministic evaluator for reviewed routes or prerequisite DAGs; perception stays outside."""

    def __init__(self, config: dict[str, Any], worker_id: str, video_id: str = "", branch_decisions: dict[str, bool] | None = None) -> None:
        workflow = config["workflow"]
        self.workflow_id = workflow["id"]
        self.worker_id = worker_id
        self.video_id = video_id
        self.partial_order = "prerequisites" in workflow
        self.prerequisites = {
            str(action): set(steps) for action, steps in workflow.get("prerequisites", {}).items()
        }
        self.required_actions = set(workflow.get("required_actions", self.prerequisites))
        self.completed_actions: set[str] = set()
        self.observations: list[ActionEvent] = []
        self.paths = [(str(path["id"]), list(path["steps"])) for path in workflow.get("valid_paths", [])]
        self.path_conditions = {str(item["path_id"]): str(item["condition_id"]) for item in workflow.get("conditional_paths", []) if isinstance(item, dict) and item.get("path_id") and item.get("condition_id")}
        self.branch_decisions = dict(branch_decisions or {})
        if any(not isinstance(value, bool) for value in self.branch_decisions.values()):
            raise ValueError("branch_decisions values must be explicit booleans")
        if self.partial_order and (not self.prerequisites or not self.required_actions):
            raise ValueError("Prerequisite workflow must define prerequisites and required_actions")
        if not self.partial_order and (not self.paths or any(not steps for _, steps in self.paths)):
            raise ValueError("Workflow must define non-empty valid_paths")
        duration_policy = workflow.get("duration_policy", {})
        self.duration_limits = workflow.get("duration_limits_seconds", {})
        if not self.duration_limits and isinstance(duration_policy, dict) and duration_policy.get("enabled"):
            self.duration_limits = duration_policy.get("rules", {})
        self.timeout_policy = workflow.get("timeout_policy", {"enabled": False})
        self.candidates: list[tuple[int, int]] = [(i, 0) for i in range(len(self.paths))]
        self.events: list[ActionEvent] = []
        self.violations: list[Violation] = []
        self.event_statuses: list[str] = []

    def reset(self, worker_id: str | None = None, video_id: str | None = None, branch_decisions: dict[str, bool] | None = None) -> None:
        """Start a fresh procedure execution without carrying state across videos/workers."""
        if worker_id is not None:
            self.worker_id = worker_id
        if video_id is not None:
            self.video_id = video_id
        self.candidates = [(i, 0) for i in range(len(self.paths))]
        self.completed_actions.clear()
        self.observations.clear()
        self.events.clear()
        self.violations.clear()
        self.event_statuses.clear()
        self.branch_decisions = dict(branch_decisions or {})
        if any(not isinstance(value, bool) for value in self.branch_decisions.values()):
            raise ValueError("branch_decisions values must be explicit booleans")

    def _violation(self, kind: str, expected: str | None, event: ActionEvent | None, reason: str, timestamp: float | None = None, confidence: float | None = None) -> Violation:
        return Violation(
            worker_id=self.worker_id,
            workflow=self.workflow_id,
            expected_step=expected,
            observed_action=event.action if event else None,
            violation_type=kind,
            timestamp=float(event.start_time if event else (timestamp or 0.0)),
            duration=float(event.duration) if event else None,
            confidence=float(event.confidence if event else (confidence or 1.0)),
            reason=reason,
            video_id=self.video_id,
            evidence_frame=event.start_frame if event else None,
        )

    def state(self) -> WorkflowState:
        if self.partial_order:
            ready = tuple(sorted(
                action for action in self.required_actions - self.completed_actions
                if self.prerequisites.get(action, set()) <= self.completed_actions
            ))
            completed = self.required_actions <= self.completed_actions
            current = self.events[-1].action if self.events else None
            return WorkflowState(self.workflow_id, len(self.completed_actions), current,
                                 ready[0] if len(ready) == 1 else None, ready, None, completed)
        if not self.candidates:
            return WorkflowState(self.workflow_id, -1, self.events[-1].action if self.events else None, None, (), None, False)
        next_steps = tuple(dict.fromkeys(self.paths[path_id][1][position] for path_id, position in self.candidates if position < len(self.paths[path_id][1])))
        completed_paths = [(path_id, position) for path_id, position in self.candidates if position >= len(self.paths[path_id][1])]
        if completed_paths and not next_steps:
            chosen_id, position = min(completed_paths, key=lambda entry: entry[0])
            return WorkflowState(self.workflow_id, position, self.events[-1].action if self.events else None, None, (), self.paths[chosen_id][0], True)
        path_id, position = self.candidates[0]
        path_name = self.paths[path_id][0] if len(self.candidates) == 1 else None
        current = self.events[-1].action if self.events else None
        return WorkflowState(self.workflow_id, position, current, next_steps[0] if len(next_steps) == 1 else None, next_steps, path_name, False)

    def consume(self, events: list[ActionEvent]) -> WorkflowResult:
        for event in events:
            self.event_statuses.append(self._consume_one(event))
        state = self.state()
        return WorkflowResult(state, list(self.violations), state.selected_path, list(self.event_statuses))

    def _consume_one(self, event: ActionEvent) -> str:
        # Preserve every received observation for audit, including uncertain or malformed events.
        self.observations.append(event)
        if event.worker_id != self.worker_id:
            self.violations.append(self._violation("INSUFFICIENT_EVIDENCE", self.state().expected_step, event, "Event worker does not match this workflow execution; event was isolated."))
            return "insufficient_evidence"
        if (not math.isfinite(event.start_time) or not math.isfinite(event.end_time)
                or not math.isfinite(event.duration) or event.start_time < 0
                or event.end_time < event.start_time or event.duration < 0
                or abs((event.end_time - event.start_time) - event.duration) > 1e-3):
            self.violations.append(self._violation("INSUFFICIENT_EVIDENCE", self.state().expected_step, event, "Malformed event interval; event was not applied."))
            return "insufficient_evidence"
        if not math.isfinite(event.confidence) or not 0.0 <= event.confidence <= 1.0:
            self.violations.append(self._violation("INSUFFICIENT_EVIDENCE", self.state().expected_step, event, "Confidence must be finite and in [0, 1]; event was not applied."))
            return "insufficient_evidence"
        if event.evidence_status not in {"sufficient", "unknown", "ambiguous", "insufficient"}:
            self.violations.append(self._violation("INSUFFICIENT_EVIDENCE", self.state().expected_step, event, "Unrecognized evidence status; event was not applied."))
            return "insufficient_evidence"
        if event.evidence_status != "sufficient":
            kind = "UNKNOWN_ACTION" if event.evidence_status == "unknown" else "AMBIGUOUS_EVIDENCE" if event.evidence_status == "ambiguous" else "INSUFFICIENT_EVIDENCE"
            self.violations.append(self._violation(kind, self.state().expected_step, event, f"Evidence status is {event.evidence_status}; workflow state was not advanced."))
            return event.evidence_status
        if self.events and event.start_time < self.events[-1].end_time:
            self.violations.append(self._violation("INSUFFICIENT_EVIDENCE", self.state().expected_step, event, "Overlapping event interval; event was not applied."))
            return "insufficient_evidence"
        # Keep the prior event-history meaning: evidence-valid observations are
        # recorded before the workflow transition is judged.
        self.events.append(event)
        state = self.state()
        expected_steps = set(state.next_valid_steps)

        limits = self.duration_limits.get(event.action)
        if limits:
            minimum, maximum = float(limits.get("min", 0.0)), float(limits.get("max", float("inf")))
            if event.duration < minimum:
                self.violations.append(self._violation("TOO_FAST", event.action, event, f"{event.action} took {event.duration:.2f}s; minimum is {minimum:.2f}s."))
            if event.duration > maximum:
                self.violations.append(self._violation("TOO_SLOW", event.action, event, f"{event.action} took {event.duration:.2f}s; maximum is {maximum:.2f}s."))
                self.violations.append(self._violation("TIMEOUT", event.action, event, f"{event.action} exceeded its {maximum:.2f}s timeout."))

        if self.partial_order:
            return self._consume_partial_order(event)

        direct: list[tuple[int, int]] = []
        unresolved_direct: list[tuple[int, int]] = []
        for path_id, position in self.candidates:
            steps = self.paths[path_id][1]
            path_name = self.paths[path_id][0]
            condition_id = self.path_conditions.get(path_name)
            decision = self.branch_decisions.get(condition_id) if condition_id else True
            if decision is False:
                continue
            if position < len(steps) and steps[position] == event.action:
                (unresolved_direct if decision is None else direct).append((path_id, position + 1))
        if unresolved_direct and not direct:
            self.violations.append(self._violation("AMBIGUOUS_EVIDENCE", state.expected_step, event, "This transition depends on an unresolved conditional branch; supply an explicit branch decision."))
            return "ambiguous_evidence"
        if unresolved_direct:
            direct.extend(unresolved_direct)
        if direct:
            self.candidates = direct
            return "completed" if self.state().completed else "accepted_transition"

        # The observed action exists on a valid route but is ahead of the expected step.
        future_matches: list[tuple[int, int, int]] = []
        unresolved_future = False
        for path_id, position in self.candidates:
            steps = self.paths[path_id][1]
            path_name = self.paths[path_id][0]
            condition_id = self.path_conditions.get(path_name)
            decision = self.branch_decisions.get(condition_id) if condition_id else True
            if decision is False:
                continue
            for later in range(position + 1, len(steps)):
                if steps[later] == event.action:
                    if decision is None:
                        unresolved_future = True
                    else:
                        future_matches.append((later - position, path_id, position, later))
                    break
        if unresolved_future:
            self.violations.append(self._violation("AMBIGUOUS_EVIDENCE", state.expected_step, event, "Skip interpretation depends on an unresolved conditional branch."))
            return "ambiguous_evidence"
        if future_matches:
            smallest_skip = min(match[0] for match in future_matches)
            selected = [(path_id, position, later) for count, path_id, position, later in future_matches if count == smallest_skip]
            expected = state.expected_step or (next(iter(expected_steps)) if expected_steps else None)
            selected_path, selected_position, later = selected[0]
            for skipped in self.paths[selected_path][1][selected_position:later]:
                self.violations.append(self._violation("SKIPPED_STEP", skipped, event, f"{skipped} was expected before observed {event.action}."))
            self.violations.append(self._violation("WRONG_SEQUENCE", expected, event, f"Observed {event.action} before the expected step {expected or 'completion'}."))
            # The future-matching event itself was observed, so resume after it.
            self.candidates = [(path_id, later + 1) for path_id, _, later in selected]
            return "skipped_step"

        previous_actions = {prior.action for prior in self.events[:-1]}
        if event.action in previous_actions:
            expected = state.expected_step
            self.violations.append(self._violation("REPEATED_STEP", expected, event, f"{event.action} was observed again while it was not the next valid step."))
            return "repeated_step"

        all_steps = {step for _, steps in self.paths for step in steps}
        if event.action in all_steps:
            self.violations.append(self._violation("WRONG_SEQUENCE", state.expected_step, event, f"{event.action} is in the workflow but is not valid at this state."))
            return "invalid_transition"
        else:
            self.violations.append(self._violation("UNEXPECTED_ACTION", state.expected_step, event, f"{event.action} is not defined by workflow {self.workflow_id}."))
            return "unknown_action"

    def _consume_partial_order(self, event: ActionEvent) -> str:
        if event.action not in self.required_actions:
            self.violations.append(self._violation("UNEXPECTED_ACTION", self.state().expected_step, event,
                                                   f"{event.action} is not a required action in workflow {self.workflow_id}."))
            return "unknown_action"
        if event.action in self.completed_actions:
            self.violations.append(self._violation("REPEATED_STEP", self.state().expected_step, event,
                                                   f"{event.action} was already accepted in this procedure execution."))
            return "repeated_step"
        missing = self.prerequisites.get(event.action, set()) - self.completed_actions
        if missing:
            self.violations.append(self._violation("WRONG_SEQUENCE", self.state().expected_step, event,
                                                   f"{event.action} is missing prerequisites: {sorted(missing)}."))
            for action in sorted(missing):
                self.violations.append(self._violation("SKIPPED_STEP", action, event,
                                                       f"Prerequisite {action} was not accepted before {event.action}."))
            return "invalid_transition"
        self.completed_actions.add(event.action)
        return "completed" if self.state().completed else "accepted_transition"

    def finalize(self, timestamp: float | None = None, *, procedure_ended: bool = False) -> WorkflowResult:
        """Finalize an observation; only an explicit procedure end proves incompletion."""
        state = self.state()
        if self.timeout_policy.get("enabled") and timestamp is not None and float(timestamp) > float(self.timeout_policy["seconds"]):
            self.violations.append(self._violation("TIMEOUT", state.expected_step, None, f"Execution duration {float(timestamp):.2f}s exceeded configured {float(self.timeout_policy['seconds']):.2f}s timeout.", float(timestamp)))
        finalization_status = "completed"
        if not state.completed:
            if procedure_ended:
                expected = state.expected_step or (state.next_valid_steps[0] if state.next_valid_steps else None)
                self.violations.append(self._violation("INCOMPLETE_PROCEDURE", expected, None, f"Procedure ended before completion; expected {expected or 'a valid route' }.", timestamp))
                finalization_status = "procedure_ended_incomplete"
            else:
                finalization_status = "observation_ended_unconfirmed"
        final_state = self.state()
        return WorkflowResult(final_state, list(self.violations), final_state.selected_path,
                              list(self.event_statuses), finalization_status)
