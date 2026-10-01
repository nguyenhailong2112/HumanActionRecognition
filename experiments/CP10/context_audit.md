# CP10 Context Audit

Audit performed 2026-10-01 before CP10 code changes.

## Objective

Resolve the CP09 workflow-validator contradiction between complete project-scope disposition coverage and excluding `out_of_scope` actions from the workflow vocabulary. Recheck the human semantic gate, then stop before real trace unless a genuinely approved executable workflow exists.

## Repository and local state

- Branch: `main`.
- HEAD: `c7a436eceaf85a2e581ec91b231d156068294341` (`CP09`), matching the supplied current checkpoint.
- `git status --short` was empty before CP10 edits: local worktree matched HEAD.
- Required project guidance reviewed: `CODEX.md`, `ROADMAP.md`, `SCOPEOFWORK.md`, `PROJECTREADINESSPACKAGE.md`, and current CP09 `CHECKSHEET.md` status.
- CP09 context, experiment report, semantic gate, workflow integrity and reconciliation artifacts are present.

## Baseline and direct implementation audit

- Baseline command: `.venv-cp05\Scripts\python.exe -m unittest discover -s tests -v`.
- Baseline observed before CP10 changes: **73 tests passed**.
- `tools/validate_workflow.py` requires disposition keys to equal the supplied project/model action scope. It also requires `action_vocabulary` to equal the non-`out_of_scope` disposition set. But the current early check rejects any action in the disposition map that is absent from `action_vocabulary`, so a valid `out_of_scope` disposition conflicts with vocabulary semantics. Confirmed CP10 validator contract bug.
- Validator receives the configured project/model scope from `configs/cp01_1.yaml`; this remains 17 non-NULL actions. The full official mapping is 25 non-NULL + NULL. The frozen model vocabulary will not be changed.
- Current tests do not verify a valid mixed disposition configuration containing `out_of_scope`; a regression test is required.

## CP08/CP09 artifacts and human gate

- CP08 frozen ActionEvent/evidence outputs and CP09 audit/reconciliation/handoff are present. Prior CP09 reports 69 frozen events; CP10 does not need to regenerate them.
- `configs/workflows/disassembly_A.yaml` is absent. `disassembly_A.draft.yaml` remains a review scaffold with `HUMAN_REVIEW_REQUIRED` and empty transitions.
- `HumanSemanticWorksheet.md` is present and human-owned. Source-grounded and reconstructed worksheets remain research artifacts; neither is a recorded human approval.
- No human evidence review CSV was found at the CP08 requested path. Human semantic decisions, genuine reviewer identity/date/version, workflow paths/prerequisites, completion, uncertainty/evidence, repeat/rework and timing remain unresolved.
- The only safe CP10 branch is validator fix and deterministic tests, then handoff. No real held-out trace or process metric is authorized by repository evidence.

## CP08/CP09 claims independently verified vs not

- **Directly reverified:** current HEAD/branch/clean initial worktree; baseline 73 tests; validator contradiction in source; no executable workflow config; draft is unapproved.
- **Available as artifacts but not re-executed here yet:** CP08's frozen 69-event media linkage audit and CP09's frozen hashes. CP10 does not alter/regenerate CP05/CP06 results.
- **Not established by files:** visual correctness judgments or human workflow approval. Existence of handoff/worksheet/reconstructed interpretation is not human approval.

## Safe execution boundary

Fix only disposition/vocabulary relationship validation and its tests. Preserve workflow activation gates, the human worksheet, model vocabulary/order, frozen events/models/results, and the rule that no real process trace runs without an approved enabled workflow.
