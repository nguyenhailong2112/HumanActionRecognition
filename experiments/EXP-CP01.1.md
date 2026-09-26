# EXP-CP01.1 — Same-Procedure Data Readiness and Baseline Validation

**Status: PARTIAL — data audit and protocol validated; model training/evaluation blocked by unavailable official I3D feature bundle, and workflow policy awaits process-owner review.**

## Objective

Establish a valid same-procedure action-segmentation setup for IMPACT v1.1 Disassembly A, front camera, and retrain the existing framewise and MS-TCN heads without using test data for tuning.

## Dataset and protocol

- Source: official IMPACT v1.1 TAS-S annotations, versioned JSON, downloaded from the official `KratosWen/IMPACT` release. Annotation archive SHA-256 was checked against its published release manifest by the download utility.
- Dataset version: `v1.1`; target: `Disassembly_A`, `front`.
- Split: official TAS-S S2 bundle split 2, protocol name `IMPACT TAS-S S2 (cross-subject)`.
- Same-procedure executions: train 39, validation 5, test 4. Execution IDs are disjoint; held-out test worker `SS07EL13` is disjoint from train workers. Train/val/test represent 12/4/1 workers.
- Annotation QA: 112/112 front-view TAS-S JSON records pass structural checks. For the target procedure, 48 are KEEP and 64 out-of-scope procedures are EXCLUDE. All 17 observed target action labels plus NULL are represented in the configured vocabulary.
- Per-frame TAS-S action segments are inclusive `[f_start, f_end]` intervals. QA checks class membership, interval ordering, bounds, overlap, gaps, and exact coverage. Five ground-truth SVG timelines were generated (one held-out validation and four test executions).
- IMPACT PPR per-hand labels exist and their frame lengths/class vocabulary pass QA, but they describe NORMAL/ANOMALY/RECOVERY procedural phases, not TAS-S actions or ground-truth workflow violations. They are not scored as process compliance.
- Video quality review is NOT VERIFIED. Only 2/48 target videos are available locally in the public sample bundle; no visual quality claim is made.
- Release terms recorded from the official dataset card: CC BY-NC-SA 4.0, intended non-commercial research/education.

## Models, configuration, environment

- Retained models: existing `FramewiseBaseline` and `MSTCN`; no architecture changes for training.
- Config: [`configs/cp01_1.yaml`](../configs/cp01_1.yaml); input feature expectation 1024-D I3D at 5 FPS; 18 output classes including NULL; seed 17; CPU; 12 configured epochs.
- Feature release expected at `data/raw/impact/v1.1/features/IMPACT-v1.1-features-I3D.zip`, official SHA-256 `97f9d81443d1a3978e77b5db119b69089ecd470af77d6bb60bd20f792446a111`.
- Environment used for deterministic checks: repository `.venv`, Python and PyTorch versions are recorded by the training utility when training eventually runs.

## Execution and results

- Dataset audit: executed; output in `experiments/CP01.1/dataset_audit_CP01.1.{md,csv,json}`.
- Ground-truth visualization: executed; SVGs in `results/cp01_1/ground_truth/` for validation/test executions.
- Critical tests: `python -m unittest discover -s tests -v` — **19 passed**.
- Official feature archive download: attempted twice through the official IMPACT downloader (second attempt with Hugging Face Xet disabled). Neither produced the expected feature archive; the second transfer remained without a destination/partial file and was interrupted. The archive is absent locally. Full model data inspection shows current sample set has only 2 same-procedure videos and no held-out S2 test executions.
- Framewise retraining: NOT RUN; required 39/5/4 feature sequences are unavailable. No checkpoint or action metric is reported.
- MS-TCN retraining: NOT RUN for the same reason. No checkpoint or action metric is reported.
- Action accuracy, macro-F1, edit score, segmental F1, boundary quality, and runtime: NOT MEASURED.
- Workflow evaluation: NOT EVALUATED. A verified industrial SOP / process-owner-approved path is absent. No duration thresholds or legal recovery routes inferred from observed label order/frequency.
- Process anomaly precision/recall: NOT EVALUATED; no violation ground truth exists for this setup.

## Failure analysis and conclusion

The data protocol blocker in CP01 has been resolved: train, validation, and test now share one procedure/vocabulary, with official cross-execution and cross-subject separation. Annotation integrity is verified structurally. Visual footage quality is not reviewed. Baseline weakness cannot be assessed until the official feature bundle becomes available and both existing models are trained/evaluated on the fixed protocol. Do not attribute any performance gap to the model yet.

Current next bottlenecks, in order:

1. **Data availability:** retrieve the official I3D feature archive or a sufficient, license-compliant full-resolution input bundle.
2. **Workflow truth:** have the process owner supply/review the Disassembly A SOP and approve ordered/conditional/rework actions; see [`HUMAN_HANDOFF.md`](../HUMAN_HANDOFF.md).
3. **Representation/model diagnosis:** only after the same split has been trained and evaluated.

## KEEP / CHANGE / DROP

- **KEEP:** official S2 cross-subject split; procedure-scoped target labels; current framewise and MS-TCN models; test-set isolation; PPR/workflow truth separation.
- **CHANGE:** source action labels from the verified v1.1 JSON rather than stale local dense labels; include the observed rare `RETRIEVE_LOCKING_LEVER_ASSEMBLY` class in the target vocabulary.
- **DROP:** CP01 illustrative route and any compliance interpretation from raw TAS-S sequence or PPR phase labels.

## Resume commands

1. Ensure the official feature archive exists and matches the published SHA-256 in `data/raw/impact/v1.1/SHA256SUMS`.
2. Run `.venv/Scripts/python.exe tools/audit_cp01_1.py` and inspect all 48 target rows.
3. Run `.venv/Scripts/python.exe tools/train_baseline.py --config configs/cp01_1.yaml --epochs 12`.
4. Run `.venv/Scripts/python.exe tools/evaluate.py --config configs/cp01_1.yaml --split test --model both`.
5. Inspect all four held-out-worker timelines and per-video/class metrics; only then classify data/annotation/representation/temporal/feature/model errors.
6. Enable workflow evaluation only after the process-owner handoff passes `tools/validate_workflow.py` and ground-truth violations exist for process scoring.
