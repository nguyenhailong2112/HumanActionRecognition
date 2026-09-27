# EXP-CP06 — Workflow Semantics and MS-TCN Reliability

**Status: PARTIAL.** The archive, action metric audit, per-execution/pooled analysis, multi-seed action baseline check, workflow validator/golden logic tests, and held-out evidence review package are completed. The workflow meaning/order is awaiting human interpretation; process compliance/anomaly and human visual conclusions remain NOT EVALUATED.

## Frozen protocol

- Dataset: IMPACT v1.1 official TAS-S, S2 split 2; `Disassembly_A`, front; 39 train / 5 validation / 4 test; held-out test worker SS07EL13.
- Feature: official I3D, 5 FPS, float32 `T×1024`; CP05 confirms target feature/video readiness and aligned annotations. ZIP SHA-256 matches manifest and official release verifier passed archive structure/CRC.
- Model reliability: existing MS-TCN, unchanged CP05 architecture and preprocessing; hidden 32, 5 layers, 3 stages, dropout .2; AdamW lr .001, weight decay .0001; 12 epochs; validation CE only selects checkpoint. Frozen data/split/vocabulary/normalization/preprocessing/evaluation.
- Seeds: 17 is the prior CP05 run; seeds 23 and 41 were run with the same recipe. The existing paired training command also trained FramewiseBaseline for the two new seeds, but seed reliability findings here concern MS-TCN. Test metrics were not used to tune/select.
- Evaluation remains our baseline on a procedure-scoped IMPACT subset, not official leaderboard reproduction.

## Executed artifacts

- `experiments/CP06/metric_definition_audit.md` and `action_metrics.json`: exact definitions, four per-execution metrics, equal-execution mean/sample SD, and pooled-frame result.
- `experiments/CP06/seed_reliability.md`, `.json`, and `seed_training.log`: best validation epoch/loss, every seed's held-out metrics, per-execution results, mean and sample SD. Training reports preserve epoch losses and configs/checkpoints are saved at `configs/cp06_seed*.yaml` and `models/cp06_mstcn_seed*`.
- `experiments/CP06/action_error_analysis.md` and `action_error_events.json`: 159 contiguous mismatch runs, frame-weighted class confusions, deterministic error tags, per-execution segment-count diagnosis, and raw-vs-decoded postprocessing comparison. Visual causes are not inferred.
- `HUMAN_HANDOFF_CP06_EVIDENCE_REVIEW.md` and `evidence_review_manifest.json`: selected actual CP05 inference events and linked video/snapshot/clip. Every item remains HUMAN_REVIEW_REQUIRED.
- Existing `src/human_action/workflow.py` was extended for explicit event outcomes and unknown/ambiguous/insufficient evidence isolation. Existing validator extended for graph state/transition integrity and policies. Synthetic workflow coverage is in `tests/test_cp06_workflow_golden.py`.
- A checkpoint-path collision in the first seed-run invocation was caught by direct CP05 metric comparison. Seed-41 Framewise artifacts were isolated under CP06 paths; the frozen CP05 seed-17 Framewise checkpoint was reproduced, matching stored best and final validation losses plus every held-out metric. Evidence: `cp05_framewise_reproduction.json`, `artifact_reconciliation.json`, and `seeds/`. Future CP06 seed runs now write both models to CP06-specific checkpoint paths.

## Findings and boundary

Per-execution held-out MS-TCN accuracy / macro-F1 / edit / F1@10 / @25 / @50:

| Execution | Acc | Macro-F1 | Edit | F1@10 | F1@25 | F1@50 | GT/pred segments |
|---|---:|---:|---:|---:|---:|---:|---:|
| SS07EL13…001 | .278 | .123 | 39.29 | .275 | .275 | .078 | 23/28 |
| SS07EL13…002 | .486 | .367 | 53.57 | .391 | .391 | .087 | 28/18 |
| SS07EL13…003 | .770 | .507 | 52.17 | .537 | .537 | .293 | 23/18 |
| SS07EL13…004 | .743 | .562 | 56.52 | .579 | .579 | .368 | 23/15 |

MS-TCN mean test accuracy stayed near .55–.57 across three seeds, but macro-F1/edit/segmental metrics varied meaningfully, especially Edit (seed mean range 32.30–50.39; across-seed sample SD 9.52). This is too much variation to treat a single result as a precise estimate. Pooled action accuracy is .522, macro-F1 .361, execution-boundary-preserving Edit 50.00, F1@10/.25/.50 .432/.432/.193, with 79 predicted versus 97 GT action segments. The paired Framewise equal-execution means are .445/.319/11.70/.149/.094/.032; per-execution and pooled results for both models are in `action_metrics.json`. Largest repeated frame confusions are NULL→EXTRACT_BEARING_PLATE_ASSEMBLY (179), STORE_BEARING_PLATE_ASSEMBLY→DETACH_ADAPTER_PLATE (169), and REMOVE_LOCKING_LEVER_ASSEMBLY→EXTRACT_BEARING_PLATE_ASSEMBLY (138). No human visual review has adjudicated whether these reflect view limits, representation, label issues, or model errors.

`configs/workflows/disassembly_A.yaml` was not supplied. `configs/workflows/disassembly_A.draft.yaml` is explicitly non-executable and contains no transition rules. Process workflow traces/compliance, violation/anomaly performance, and duration violations are NOT EVALUATED. Synthetic tests are logic validation only. Offline cached-feature inference is not streaming latency.

Validation executed: `.venv-cp05\Scripts\python.exe -m unittest discover -s tests -v` — **44 passed**, including 20 CP06 synthetic workflow tests. All 69 existing evidence event records have unique event keys and extant snapshots/clips; all remain workflow NOT EVALUATED. The CP05 framewise reproduction matches its prior training and held-out metrics.

## Decision

**INVESTIGATE** the representation/annotation/observation causes through the prepared human evidence review and complete the Research Workflow Specification. Keep MS-TCN as the current temporal baseline for comparison; do not escalate model capacity yet. CP06 remains PARTIAL until human workflow semantics and evidence review are supplied. See `experiments/CP06/seed_reliability.md` and `action_error_analysis.md` for details.
