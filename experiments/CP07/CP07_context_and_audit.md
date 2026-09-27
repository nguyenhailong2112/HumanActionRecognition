# CP07 Context and CP06 Audit

## CP06 claims checked

CP06 reports a frozen IMPACT v1.1 TAS-S S2 split-2 experiment on `Disassembly_A/front` (39/5/4 executions; held-out worker SS07EL13), verified I3D features, CUDA training, Framewise and MS-TCN evaluation, three-seed MS-TCN reliability, boundary-preserving pooled metrics, 159 error runs, 44 passing repository tests, and a 21-selection human evidence-review package. It leaves workflow semantics and process performance unevaluated.

## Direct verification

- `configs/cp05.yaml`, CP05 evaluation JSON/timelines, CP05 evidence index, CP06 `action_metrics.json`, `seed_reliability.json`, and training/checkpoint files exist. Four held-out MS-TCN per-execution rows and all three seed records are present.
- CP06 `analyze_cp06.summarize` computes per-execution action metrics first. Framewise counts pool over frames; Edit is recomputed by summing each execution's edit distance and denominator; segmental TP/FP/FN are summed per execution. Equal-execution means and sample SD (`ddof=1`) are explicit. No temporal measure relies on concatenated execution boundaries.
- CP06 workflow code and validator exist; golden suite exists. `configs/workflows/disassembly_A.yaml` is absent. `disassembly_A.draft.yaml` remains `HUMAN_REVIEW_REQUIRED` and contains no transitions.
- CP06 evidence manifest has 21 category selections but duplicate event IDs across categories; CP07 creates a deduplicated manifest while preserving reasons. CP06 report calls this a 21-event package, which is accurate only as 21 selections, not necessarily 21 unique events.
- CP05/CP06 training reports/checkpoints and CP06 artifact reconciliation are present. No new training is needed for this checkpoint.

## Discrepancies / limits

The CP06 metric audit is consistent with implementation. Its phrase “pooled frames” can obscure that Edit and segmental metrics are execution-boundary-preserving pooled statistics, not a metric on one concatenated timeline; CP07 documents the exact formulas. The actual CP05 timelines contain predicted segments only, so CP07 uses CP06 saved confusion/support/error outputs for GT structure and timeline files for prediction duration/boundary diagnostics. Four test executions permit description, not causal correlation claims.

The full pipeline audit found material semantic-safety hazards: `configs/cp01.yaml` contained illustrative routes and invented duration thresholds, while `pipeline.py` previously treated a missing `workflow.enabled` key as enabled. Model-generated ActionEvents also defaulted to `evidence_status=sufficient` despite no validated evidence threshold. CP07 removed the legacy routes/thresholds, marked that config disabled/HUMAN_REVIEW_REQUIRED, made workflow evaluation opt-in with a HUMAN_VALIDATED activation requirement, required explicit enablement for real traces, and changed model-generated events to `unknown` by default. Synthetic tracing requires an explicit call argument and emits a synthetic scope marker; a YAML flag cannot bypass the gate. Regression tests cover these safeguards.

## Safe CP07 foundation

Build on the frozen seed-17 CP05 MS-TCN predictions, CP06 metric/error artifacts, existing `ActionEvent` and workflow engine/validator. Add only an explicit event ID, source view, evidence references, and deserialization needed for trace/evidence linking. Keep `workflow_semantics=HUMAN_REVIEW_REQUIRED` and `process_compliance=NOT_EVALUATED` until a human-approved workflow and valid process ground truth exist. No model escalation or test tuning is authorized by these artifacts.
