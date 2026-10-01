# CP10 — Workflow Specification Gate and Validator Integrity

## Status

**PARTIAL — validator contract fixed and tested; human semantic gate remains open.**

## Executive Summary

At HEAD `c7a436eceaf85a2e581ec91b231d156068294341`, the validator had a real contract contradiction: it required dispositions for every project/model action, yet prevented a valid `out_of_scope` action from being omitted from executable workflow vocabulary. CP10 separated those sets without changing the frozen model class order or weakening path/reference validation. A synthetic configuration with required, optional, rework and out-of-scope dispositions passes; specified invalid cases fail.

No owner-approved `Disassembly_A` workflow exists. CP10 stopped before workflow activation, frozen real-event tracing, and process interpretation.

## CP09 Audit / Reconciliation

Repository branch/HEAD matched the supplied CP09 state and the worktree was clean at preflight. The baseline suite reproduced **73 passing tests**. CP09's 69 frozen ActionEvents and prior event-history/finalization work are treated as existing evidence; CP10 did not regenerate those artifacts or any CP05/CP06 result.

## Validator Contract

The validator now explicitly enforces:

```text
keys(action_disposition) = supplied project/model action scope
action_vocabulary = project/model actions whose disposition is not out_of_scope
```

All executable path/prerequisite references remain restricted to the workflow vocabulary. An action outside model scope remains rejected even if present in official TAS-S. Exact behavior and regression cases are documented in `experiments/CP10/validator_integrity_audit.md`.

## Human Semantic Gate

**HUMAN_REVIEW_REQUIRED.** `configs/workflows/disassembly_A.yaml` is absent. The draft remains unapproved. `HumanSemanticWorksheet.md` remains human-owned and unmodified. The source-grounded and reconstructed worksheets remain research interpretation, not owner approval. No reviewer/date/version, action dispositions, approved routes/prerequisites, completion policy, or evidence/uncertainty policy was fabricated.

## Workflow Validation

The draft validator was run and failed as expected due to missing `HUMAN_VALIDATED` status, identity/approval, action dispositions, executable route/completion and reachable state configuration. No validator rules were weakened. Since no approved candidate YAML exists, the branch that validates an owner submission is not applicable. No `workflow_validation.json` is produced.

## Frozen ActionEvent Trace

**NOT EVALUATED / NOT RUN.** Real trace activation requires a human-approved, enabled workflow that passes validation. CP10 did not rerun inference and did not create fake trace files.

## Evidence Integrity

Prior CP09 evidence establishes file/link integrity for 69 frozen events, not visual correctness. CP08's 13-event human review remains pending. No reviewer decision was converted to a training label or process ground truth.

## Finalization Semantics

CP09 API remains present: observation end is unconfirmed, explicit procedure termination returns complete/incomplete status according to workflow state. This CP10 checkpoint did not change it.

## Accepted Event History

CP09 accepted-history boundary remains intact: received observations are retained separately from accepted/applied events. CP10 does not modify workflow engine behavior.

## Process Metrics

**NOT EVALUATED.** No validated workflow and no matching process-level ground truth are present. No compliance, violation, mistake, anomaly, or duration-violation performance is claimed.

## Model Escalation Decision

**NO ESCALATION.** The frozen model vocabulary and action outputs are unchanged. CP10 addresses validator semantics only.

## Remaining Human Decisions

See the compact [CP10 human handoff](../HUMAN_HANDOFF_CP10.md): action dispositions and considered vocabulary; route/prerequisite and branch semantics; action/state meaning; completion/restart/recovery; uncertainty/evidence behavior; any authoritative timing policy; actual version/owner/date/approval. CP08 event visual review also remains pending.

## Remaining Technical Risks

- Prerequisite mode does not represent arbitrary reversible component state; implement no recovery abstraction until approved semantics require it.
- Eight official TAS-S actions are outside the frozen project model scope and cannot be observed by this model.
- Confidence is not calibrated evidence sufficiency.
- No process ground truth exists for process metrics.

## Verification Commands

- Baseline before CP10 edits: `.venv-cp05\Scripts\python.exe -m unittest discover -s tests -v` — **73 passed**.
- Final full suite: `.venv-cp05\Scripts\python.exe -m unittest discover -s tests -v` — **Ran 74 tests; OK**.
- Syntax compilation: `.venv-cp05\Scripts\python.exe -m compileall -q src tools tests` — exit 0.
- `.venv-cp05\Scripts\python.exe tools/validate_workflow.py --config configs/workflows/disassembly_A.draft.yaml` — expected nonzero failure; draft remains safely non-executable.

## Acceptance Gate

- Validator disposition/vocabulary distinction: **IMPLEMENTED / TESTED**.
- Complete disposition scope and invalid-reference rejection: **TESTED**.
- Human-approved workflow: **ABSENT**.
- Workflow validation for a real owner-approved file: **NOT APPLICABLE / NOT RUN**.
- Frozen ActionEvent trace: **NOT EVALUATED / NOT RUN**.
- Process metrics: **NOT EVALUATED**.

CP10 is **PARTIAL**, not CLOSED.

## Recommendation for CP11

Wait for the owner-reviewed Research Workflow Specification and the separate CP08 evidence-review return. Then validate the submitted YAML without changing validator rules. If it is genuinely human-validated, enabled, and passes, run the existing frozen ActionEvent trace path. Keep process metrics unevaluated until matching process ground truth exists.
