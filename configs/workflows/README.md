# Workflow configuration status

The `Disassembly_A` Research Workflow Specification / Benchmark Procedure Interpretation remains `HUMAN_REVIEW_REQUIRED`. `disassembly_A.draft.yaml` is a review scaffold, not an executable workflow. Do not add `disassembly_A.yaml` or enable workflow execution until the project owner validates the semantics. Do not convert TAS-S frequencies, observed video order, or the PSR graph into procedure rules.

Current owner handoffs: `HUMAN_HANDOFF_CP07.md` and `HUMAN_HANDOFF_CP07_EVIDENCE_REVIEW.md`. Workflow evaluation is opt-in and requires both `enabled: true` and `status: HUMAN_VALIDATED`; validate the completed artifact with `tools/validate_workflow.py` before any real event trace. The engine supports either reviewed route constraints or a generic prerequisite DAG; no `Disassembly_A` route or prerequisite semantics are supplied here. Keep process metrics NOT EVALUATED until matching process ground truth exists.
