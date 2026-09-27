# EXP-CP07 — Procedure Grounding and ActionEvent Integration

**Status: PASS — CP07 checkpoint closed.** The existing workflow engine, metric aggregation, and frozen action errors were audited; ActionEvent now carries execution/view/event/evidence links and a reusable deterministic trace adapter is covered by synthetic tests. No owner-validated procedure YAML or valid process-violation ground truth was available, so no actual held-out workflow trace or process-compliance result is claimed. Overall system status remains **PARTIAL** at that human gate.

**Checkpoint closure:** CP07 implementation/audit deliverables are complete and frozen. Overall project progress remains PARTIAL at the explicit human semantic gate; this closure does not mean process-level completion.

## Frozen boundary

IMPACT v1.1 TAS-S S2 split 2, `Disassembly_A/front`, 39 train / 5 validation / 4 held-out test executions, worker SS07EL13. CP07 uses frozen CP05 seed-17 MS-TCN outputs and CP06 reports only. No retraining, test tuning, acquisition audit, or workflow tuning was performed.

## Audit and implementation

- CP06 report/artifact audit is recorded in `experiments/CP07/CP07_context_and_audit.md`. CP06 report outputs agree with current metrics, timelines, checkpoints, and golden tests; the 21 evidence selections deduplicate to 13 unique events.
- `experiments/CP07/metric_aggregation_audit.md` gives formulas for frame-weighted pooled Accuracy/Macro-F1, execution-boundary-preserving pooled Edit and segment F1, equal-execution mean, and sample SD. A synthetic test checks that concatenating separate same-action executions spuriously merges a temporal segment.
- `ActionEvent` is extended in place with `view`, deterministic `event_id`, optional `evidence_refs`, and `from_dict`; the inference pipeline passes configured view. No model-specific workflow code was added.
- `build_workflow_trace` emits per-event state-before/after, attempted transition/status, confidence, uncertainty flags, evidence links, final state, and an explicit process-performance NOT_EVALUATED marker. Synthetic use requires an explicit argument and is labelled `synthetic_logic_validation`; real use requires validated + enabled config. CP07 did not invoke it on held-out events.
- Running the current validator on `disassembly_A.draft.yaml` correctly fails because the draft is not HUMAN_VALIDATED and contains no approved action dispositions, paths, or completion rule. This is the intended human gate, not a validator defect.
- Full-pipeline audit found and corrected a legacy CP01 risk: missing `workflow.enabled` previously defaulted to enabled, and its illustrative config carried unsupported paths/duration limits. Workflow execution is now disabled by default, requires HUMAN_VALIDATED when enabled, and the legacy illustrative routes/limits were removed. Regression tests cover the activation gate.
- Predicted ActionEvents now default to `evidence_status=unknown`; CP07 has no validated confidence threshold that can authorize a prediction as sufficient for compliance reasoning. Model confidence remains separately recorded.

## Action error structure

Machine-readable measurements are in `experiments/CP07/action_error_structure.json`; interpretation and limitations are in `experiments/CP07/action_error_structure.md`. Execution 001 has the lowest action metrics and more predicted than GT action segments (28/23); executions 002–004 have fewer predicted than GT segments (18/28, 18/23, 15/23). CP06's largest recurring frame confusions remain NULL→EXTRACT_BEARING_PLATE_ASSEMBLY (179), STORE_BEARING_PLATE_ASSEMBLY→DETACH_ADAPTER_PLATE (169), and REMOVE_LOCKING_LEVER_ASSEMBLY→EXTRACT_BEARING_PLATE_ASSEMBLY (138). Four executions are insufficient for causal attribution. Human visual review is required for visual/semantic causes.

## Evidence and workflow status

`experiments/CP07/evidence_review_manifest.json` deduplicates the CP06 21 category selections into 13 unique actual CP05 event records, preserving all selection reasons. `HUMAN_HANDOFF_CP07_EVIDENCE_REVIEW.md` lists source video, timestamp, prediction, TAS-S label at event start, snapshot, clip, status and fixed semantic response format. No human labels are inferred or generated.

`configs/workflows/disassembly_A.yaml` is absent. The draft is not executable. Consequently actual CP05 ActionEvents were not fed into workflow semantics, no held-out workflow trace was emitted, process compliance accuracy/violation precision-recall/mistake rate/anomaly F1/duration violations are NOT EVALUATED, and no duration/timeout policy is asserted. The trace API accepts the future workflow mapping, but the CLI does not yet load a separate workflow YAML and new inference events do not automatically receive evidence references. These are bounded CP08 integration tasks, not reasons to fabricate traces now.

## Validation

Environment queried on the current machine: Python 3.12.14, PyTorch 2.14.0+cu132 (CUDA available), RTX 5060 Ti 16 GiB, driver 596.21, NumPy 2.5.3, OpenCV 4.14.0, PyYAML 6.0.3; see `experiments/CP07/environment_audit.json`. No clean-room environment rebuild was attempted.

CP06's prior full suite was 44 passing tests. CP07 adds twelve contract/aggregation/isolation/evidence/synthetic trace and activation-gate checks. Executed `.venv-cp05\Scripts\python.exe -m unittest discover -s tests -v`: **56 passed**. `python -m compileall -q src tools tests` completed successfully. The validator was run on the draft and failed with the expected HUMAN_VALIDATED, action-disposition, approved-route and completion requirements.

## Human-dependent next step

Complete `HUMAN_HANDOFF_CP07.md` and save a reviewed candidate to `configs/workflows/disassembly_A.yaml`. Complete the event form in `HUMAN_HANDOFF_CP07_EVIDENCE_REVIEW.md` and save `experiments/CP07/human_evidence_review.csv`. CP08 should validate owner semantics, add small workflow-YAML/evidence-reference plumbing to the existing API, then run frozen ActionEvent traces. Keep process ground-truth performance NOT EVALUATED until semantically matching labels exist.

## Decision

**INVESTIGATE** semantic/workflow definition and human evidence review; keep MS-TCN as the current action baseline and do not escalate model capacity. CP07 is closed as a deliverable-complete checkpoint; the end-to-end process system remains **PARTIAL** until owner-validated workflow semantics and visual judgments are available.
