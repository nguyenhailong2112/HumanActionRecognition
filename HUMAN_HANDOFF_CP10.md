# HUMAN HANDOFF — CP10 Remaining Semantic Decisions

The CP10 validator now supports a complete disposition table while excluding `out_of_scope` actions from executable workflow vocabulary. **No workflow file is approved or executable yet.** Please use the existing human-owned `HumanSemanticWorksheet.md` and return the decisions below; prior source review is summarized in the CP09 handoff and semantic audit, so no research reconstruction is requested.

Requested artifact: a reviewed **Research Workflow Specification / Benchmark Procedure Interpretation** at `configs/workflows/disassembly_A.yaml`. It is not an official factory SOP.

## Decisions still required

1. For each of the 17 frozen project model actions, provide one owner-approved disposition: `required`, `optional`, `conditional`, `rework`, or `out_of_scope`, with a reason/source for conditional and out-of-scope cases. The `action_vocabulary` must then include exactly the non-`out_of_scope` actions.
2. Specify the valid workflow representation and semantics using only the considered, model-observable actions: approved `valid_paths` or approved `required_actions` plus `prerequisites`; define any conditional branch and its condition.
3. Confirm handling for action/state ambiguity already identified in the CP09 handoff: UNSCREW vs removal, STORE vs removal (especially gearbox housing), RETRIEVE, INSTALL/ATTACH, and repeated actions. State unsupported effects as unknown; do not map the eight unmodeled official actions into the frozen model.
4. Define completion, restart, and any applicable recovery/rework behavior. If none is approved, say so explicitly. Do not create repeat limits by assumption.
5. Define evidence and uncertainty behavior for ambiguous, unknown, out-of-view, or insufficient events. Confidence remains separate from evidence sufficiency.
6. Keep timing disabled unless an authoritative timing rule and citation are provided.
7. Supply actual workflow version, approving owner/reviewer, review date, sources, and explicit approval. These values cannot be supplied by Codex.

## Return and resume

Complete the worksheet yourself and provide the reviewed YAML at `configs/workflows/disassembly_A.yaml`. Do not mark it `HUMAN_VALIDATED` or `enabled: true` until you have approved the contents. CP10 can then run the validator and synthetic tests; a frozen held-out trace is permitted only after the approved enabled workflow validates. The separate CP08 13-event visual review remains pending at `experiments/CP08/human_evidence_review.csv`; it is not a process ground-truth annotation.
