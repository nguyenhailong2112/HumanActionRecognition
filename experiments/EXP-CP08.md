# EXP-CP08 — Workflow Activation and Semantic Integrity

**Status: PARTIAL — human semantic gate remains open.** CP08 audited the CP07 state, reconciled the available research interpretations without promoting them to policy, verified links from frozen CP05 MS-TCN ActionEvents to all existing evidence media, and corrected workflow finalization so observation end is not confused with known procedure termination.

## Scope and preservation

Frozen scope: IMPACT v1.1 TAS-S S2 split 2, `Disassembly_A/front`, 39 train / 5 validation / 4 held-out test executions; CP05 seed-17 MS-TCN predictions. CP08 did not retrain, tune on test, alter the split, regenerate benchmark metrics, or modify CP05/CP06 artifacts/checkpoints. No executable workflow YAML was created. `HumanSemanticWorksheet.md` remains human-owned and unchanged.

## Verified / executed

- The CP05 saved timelines contain 69 ActionEvents over the four test executions. All 69 uniquely match the CP05 evidence index and have existing source video, snapshot and clip files. Timestamp/frame, confidence and interval bounds were checked programmatically. This is linkage validation, not visual semantic review.
- The 21 CP07 evidence selections resolve to 13 unique review events. No reviewer judgment CSV exists. CP08 produced a fixed review handoff and preserved `HUMAN_REVIEW_REQUIRED` status.
- `experiments/CP08/semantic_integrity_audit.md` reconciles official TAS-S/PSR/PPR source distinctions, human worksheets, descriptive annotation facts, and unresolved mappings. Every action in the ledger remains non-executable.
- The workflow finalizer now distinguishes an observation ending without confirmed procedure termination from an explicitly ended incomplete procedure. The former preserves state and observations without creating an unsupported `INCOMPLETE_PROCEDURE` decision.
- Frozen event/evidence artifacts were generated without rerunning the model. `process_trace_summary.json` explicitly reports workflow execution blocked by absent validated semantics and process performance `NOT_EVALUATED`.

## Human-dependent / not evaluated

`configs/workflows/disassembly_A.yaml` is absent. The draft remains unapproved. No actual held-out workflow state/transition trace or compliance interpretation was generated. Statistical compliance, violation, mistake, anomaly, and duration-violation metrics remain `NOT_EVALUATED`; no suitable process-level ground truth or approved duration policy is present. Visual judgments on the review events remain pending. No official factory SOP is claimed.

## Frozen artifacts

The CP05/CP06 model checkpoints, timelines, metrics, error outputs and seed artifacts were not regenerated or edited. Their SHA-256 values are recorded in `CP08_context_and_audit.md`; rerun final hash checks before closing this report.

Final hash verification reproduced the four audit hashes exactly: CP05 MS-TCN checkpoint `2e1f06a248973dad925f449ad9588064bbade4f9c2f4ed9c961a5196008f567d`; CP05 Framewise checkpoint `c3f0089d2d942856420954a636a3f02ec8ba661dcc531ae7afa2e8e37c7739a3`; CP06 action metrics `9179bccc5698e242fe628944b66b07abab4b23d14861a97ff3e690a441aa7605`; CP06 seed reliability `f1119402de1338208ad4a4188e1adf2b49ff0d4b41367a01d45e042bfc024ea3`.

## Final verification

- `\.venv-cp05\Scripts\python.exe -m unittest discover -s tests -v` — **66 tests passed**.
- `\.venv-cp05\Scripts\python.exe -m compileall -q src tools tests` — passed.
- `\.venv-cp05\Scripts\python.exe tools/validate_workflow.py --config configs/workflows/disassembly_A.draft.yaml` — exit 1 as expected: unapproved status, missing identity/approval, action dispositions, approved path, completion, and reachable start/terminal states. No validator rules were weakened.
- `\.venv-cp05\Scripts\python.exe tools/prepare_cp08_artifacts.py` — passed; 69 frozen events and evidence links verified, 13 unique review events mapped, zero missing source/snapshot/clip files.
- `configs/workflows/disassembly_A.yaml` remains absent; no real workflow trace was activated.
- `HumanSemanticWorksheet.md` was not edited. Evidence review remains pending.

## Decision

Keep the frozen action baseline as the current research reference. Do not escalate model capacity. The immediate blocker to a semantically valid procedure-understanding system is the absence of an owner-validated workflow specification and human semantic review, not a demonstrated model-capacity failure. Resume at workflow validation and evidence review when both handoff artifacts are returned.
