from __future__ import annotations

from typing import Any

from .schemas import ActionEvent, to_dict
from .workflow import WorkflowEngine, workflow_is_enabled


def build_workflow_trace(
    config: dict[str, Any],
    events: list[ActionEvent],
    worker_id: str,
    execution_id: str,
    view: str,
    branch_decisions: dict[str, bool] | None = None,
    finalize_timestamp: float | None = None,
    *,
    synthetic_validation: bool = False,
    procedure_ended: bool = False,
) -> dict[str, Any]:
    """Interpret one execution's structured events; caller validates workflow config first.

    Returned statuses are deterministic workflow interpretations, not empirical
    process-performance labels. Each invocation owns exactly one execution.
    """
    workflow_config = config.get("workflow", config)
    if not synthetic_validation:
        if workflow_config.get("status") != "HUMAN_VALIDATED":
            raise ValueError("workflow trace is disabled until workflow.status is HUMAN_VALIDATED")
        if not workflow_is_enabled(config):
            raise ValueError("workflow trace requires workflow.enabled: true")
    engine = WorkflowEngine(config, worker_id, execution_id, branch_decisions)
    records = []
    for event in events:
        if event.video_id and event.video_id != execution_id:
            raise ValueError(f"event {event.event_id or event.action!r} belongs to {event.video_id}, not {execution_id}")
        before = to_dict(engine.state())
        result = engine.consume([event])
        after = to_dict(result.state)
        status = result.event_statuses[-1]
        records.append({
            "execution_id": execution_id,
            "worker_id": worker_id,
            "source_view": view,
            "event_id": event.event_id,
            "predicted_action": event.action,
            "start_time": event.start_time,
            "end_time": event.end_time,
            "duration": event.duration,
            "start_frame": event.start_frame,
            "end_frame": event.end_frame,
            "workflow_state_before": before,
            "transition_attempted": event.action,
            "transition_result": status,
            "workflow_state_after": after,
            "compliance_interpretation": _interpret(status),
            "evidence_refs": list(event.evidence_refs),
            "confidence": event.confidence,
            "evidence_status": event.evidence_status,
            "uncertainty_flags": [] if event.evidence_status == "sufficient" else [event.evidence_status],
        })
    final = engine.finalize(finalize_timestamp, procedure_ended=procedure_ended)
    return {
        "scope": "synthetic_logic_validation" if synthetic_validation else "deterministic_workflow_interpretation",
        "execution_id": execution_id,
        "worker_id": worker_id,
        "source_view": view,
        "events": records,
        "final_state": to_dict(final.state),
        "finalization_status": final.finalization_status,
        "final_violations": [to_dict(item) for item in final.violations],
        "process_performance": "NOT_EVALUATED_WITHOUT_VALID_PROCESS_GROUND_TRUTH",
    }


def _interpret(status: str) -> str:
    return {
        "accepted_transition": "accepted_transition",
        "completed": "workflow_completion",
        "skipped_step": "workflow_deviation",
        "invalid_transition": "invalid_observed_transition",
        "repeated_step": "repeated_step",
        "unknown_action": "unexpected_action",
        "ambiguous_evidence": "unknown_or_ambiguous",
        "unknown": "unknown_or_ambiguous",
        "insufficient": "insufficient_evidence",
        "insufficient_evidence": "insufficient_evidence",
    }.get(status, status)
