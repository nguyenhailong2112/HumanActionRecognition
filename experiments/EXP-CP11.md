# EXP-CP11 — Research Workflow Specification v1

**Status:** CLOSED for project research workflow specification and synthetic deterministic validation. Frozen trace = READY / BLOCKED BY EVIDENCE REVIEW. Factory-SOP validation and process-performance metrics are not evaluated.

## Objective

Establish a conservative executable Research Workflow Specification / Benchmark Procedure Interpretation for `Disassembly_A` without representing it as an official IMPACT workflow or factory SOP.

## Scope and frozen inputs

- Dataset: IMPACT v1.1, TAS-S, S2 split 2, `Disassembly_A`, front; frozen research slice remains 39 train / 5 validation / 4 held-out test executions.
- Model/action class order, frozen predictions, CP05/CP06 checkpoints and metrics were not changed.
- Project-level modeled scope: 17 non-NULL actions; full official TAS-S vocabulary remains 25 non-NULL actions plus NULL.
- Research semantics are taken from CP11's explicit project-owner delegation and recorded in `experiments/CP11/research_semantic_decision_record.md`.

## Specification

Five required process actions. UNSCREW is the prerequisite for each of the four major component removals; the four removals have no mutual ordering constraints. This edge follows CP11's explicit “mechanical preparation” interpretation, while observed order frequencies are not used as normative evidence. START is a boundary marker. Eleven auxiliary/logistics/retrieval/install/attach/tool actions are out of scope and retained as observations without violations. Completion means all five core actions accepted: research-defined observable subprocedure completion, not full physical teardown. Repeats are interpreted as `REPEATED_STEP`, never automatically as mistakes. Duration and timeout policies are disabled. Unknown/ambiguous evidence does not advance workflow state. `factory_sop_validated: false`.

## Implementation

- Added `configs/workflows/disassembly_A.yaml` with explicit `RESEARCH_APPROVED` / `PROJECT_RESEARCH` scope and complete 17-action disposition coverage.
- Added narrowly scoped validator and activation support for research approval, requiring approval basis and explicit false factory-SOP validation.
- Added deterministic `out_of_scope_ignored` handling; observations are preserved and workflow state/violations remain unchanged.
- Trace interpretation surfaces the out-of-scope status.
- Existing frozen workflow/events are not run as a real trace because all 69 frozen events have `evidence_status: unknown`.

## Verification

Executed results:

- Validator command: `.venv-cp05\Scripts\python.exe tools\validate_workflow.py --config configs\workflows\disassembly_A.yaml` — **PASS**, covers all 17 configured project/model actions.
- Full suite: `.venv-cp05\Scripts\python.exe -m unittest discover -s tests -v` — **85 tests passed**.
- Compile check: `.venv-cp05\Scripts\python.exe -m compileall -q src tools tests` — **PASS** (exit code 0).
- GitHub CI: not checked or claimed; these are local executions.

Synthetic tests are engineering logic validation only, not real process performance.

## Boundaries

- CP11 does not establish official author ground truth, factory SOP validity, or process violation labels.
- CP11 does not promote frozen evidence status, alter historical action labels/metrics, retrain models, tune on test data, or produce a real workflow trace.
- Remaining evidence review is the human visual review of the existing 69-event evidence set; a sufficiency policy for reviewed observations must remain explicit.
