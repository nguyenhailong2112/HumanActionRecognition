# CP08 Action Error Review

## Verified facts

- The evaluated stream is the frozen CP05 seed-17 MS-TCN output over four held-out executions. CP08 did not run inference or alter test predictions.
- The four execution-level results are heterogeneous. Execution 001 has substantially weaker frozen frame accuracy/Macro-F1 than executions 003–004; execution 002 is intermediate. The detailed measurements remain in `experiments/CP07/action_error_structure.json` and frozen CP05/CP06 results.
- Across those executions, the direction of segment-count error differs: some predictions are over-segmented relative to GT and others under-segmented.
- CP06 repeatedly recorded NULL-to-action leakage and confusion among bearing-plate, adapter-plate, locking-lever and rotor actions. Error categories overlap and frame-confusion counts are not independent events.
- The four test executions are too few to establish that action duration, class support, NULL proportion, boundary density, or any one action pair causes execution-level performance differences.
- Visual correctness of the 13 selected evidence events remains unreviewed. Existing snapshots/clips are linked to events and exist as files; no semantic judgment is implied.

## Plausible hypotheses — not established causes

- Some short/rare actions may be difficult to classify because they contribute few frames or have sparse training support.
- High NULL share and transitions among visually similar assemblies may contribute to background leakage and class confusion.
- View occlusion, coarse TAS-S labels, and temporal boundary ambiguity may contribute to errors, but the cached probabilities/timelines alone cannot establish these explanations.
- Temporal smoothing may suppress short actions or shift boundaries; CP08 did not tune or redesign decoding against the held-out set.

## Unresolved and human-dependent

The reviewer must inspect the source video, snapshot and clip for each entry in `HUMAN_HANDOFF_CP08_EVIDENCE_REVIEW.md`, and return `experiments/CP08/human_evidence_review.csv`. Review judgments are not training labels and must not be used to rewrite the frozen benchmark. A reviewer may identify an action as visually ambiguous or unsupported; that is a semantic observation, not proof of annotation error or process deviation.

No root cause is assigned from model output alone. Current bottleneck assessment is **semantic/workflow gating plus unresolved visual evidence review**, with action baseline errors characterized but not causally attributed. Model-capacity escalation is not supported by this evidence.
