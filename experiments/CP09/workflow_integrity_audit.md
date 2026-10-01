# CP09 Workflow Integrity Audit

## Engine history semantics

Before CP09, `_consume_one()` appended any structurally valid, sufficient-evidence event to `self.events` before deciding whether a route/DAG transition was accepted. This was confirmed by direct inspection. A repeated or invalid action could therefore become `state().current_step` and enter repeat history despite rejection. `self.observations` already retained every received ActionEvent.

CP09 now appends to `self.events` only when the event is applied to the workflow representation:

- Route direct transition: accepted and recorded.
- Route future match interpreted as a skipped-step/resume transition: recorded because the event advances the selected route, while the deviation remains reported.
- Prerequisite transition: recorded only after prerequisites pass and the action is newly accepted.
- Wrong sequence with no accepted route transition, repeated step, unexpected action, unresolved branch, unknown/ambiguous/insufficient evidence, malformed/overlapping event, and worker mismatch: observation retained; accepted event history and workflow state are not changed.

Repeat detection now checks all previously accepted events. A rejected duplicate no longer disappears from repeat context or poisons later valid progression.

## Finalization and pipeline

The CP08 `procedure_ended` parameter and result field are present in current HEAD; the prompt's alleged implementation mismatch was not reproduced. CP09 makes finalization outcomes explicit: explicit termination yields `procedure_ended_complete` if workflow state is complete, otherwise `procedure_ended_incomplete` plus the incomplete violation. Without explicit termination, finalization is `observation_ended_unconfirmed` and does not emit `INCOMPLETE_PROCEDURE`, even if accepted workflow state had completed.

Both `predict_video()` and `evaluate_video()` call `finalize()` at EOF without passing `procedure_ended=True`; these call sites now expose the returned `finalization_status`. EOF therefore denotes observation boundary only.

## Workflow representation and recovery

The existing single engine supports route and prerequisite-DAG modes, with validator-enforced exclusivity. No actual `Disassembly_A` semantics were activated. The prerequisite engine's accepted-action set cannot represent arbitrary reversible component state; no recovery/rework policy is human-approved, so CP09 does not add state-effect machinery.

## Validation boundary

The no-workflow branch remains active: no real process trace was run. The draft is expected to fail executable validation. Synthetic tests remain engineering tests only and do not claim process performance.
