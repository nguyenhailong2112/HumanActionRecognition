# EXP-CP01 — First executable baseline

## Objective

Exercise video loading → per-frame representation → framewise/MS-TCN segmentation → temporal segments/events → deterministic workflow/anomaly decisions → snapshots/clips → action/process report and GT-vs-prediction visualization.

## Dataset and split

- Dataset: official IMPACT v1.1 quick-start sample, TAS-S dense annotations, `front` fixed camera.
- Dataset version: v1.1; official archive SHA-256 was verified by `tools/prepare_data.py` during download.
- Split: `AL07EJ17_Disassembly_A_001_front` train; `AL07EJ17_Reassembly_A_002_front` validation; `ER07AD15_Disassembly_A_001_front` test.
- Test trial: 3,478 source frames at 30 FPS, 580 sampled frames at 5 FPS; GT has 10 START, 443 REMOVE, 95 STORE and 32 NULL samples after coarse mapping.
- This is a three-execution pipeline smoke-test split, not a defensible benchmark. Validation is a different procedure mode; the train trial has just one worker/execution. The test disassembly labels contain no examples of RETRIEVE/INSTALL/ATTACH/FINISH.
- Source: [official IMPACT dataset card](https://huggingface.co/datasets/KratosWen/IMPACT), local official release protocol `ResearchDocuments/01_IMPACT/code/IMPACT/docs/DATA_RELEASE.md` and benchmark guide `.../docs/BENCHMARK.md`. Terms recorded from the release: CC BY-NC-SA 4.0 for non-commercial research/education.

## Model and configuration

- Input descriptor: 283 dimensions, 5 FPS: 8×8 RGB thumbnail, 24-bin HSV histogram, 8×8 absolute frame-difference map and 3 motion summaries.
- Baseline: independent framewise 1×1 Conv classifier.
- Temporal model: classic 3-stage MS-TCN, 5 dilated residual layers per stage, hidden width 32, dropout 0.2, stagewise cross-entropy plus clipped temporal smoothing. No pretrained features.
- Device: CPU; Python 3.12, PyTorch 2.14.0+cpu, OpenCV 4.14, NumPy 2.5.3; 8 epochs in the recorded run; seed 17.
- Feature mean/std are computed from train only. Best checkpoint is selected by validation cross-entropy.
- Exact settings: `configs/cp01.yaml`; training history/checkpoints: local `results/cp01/training_report.json` and `models/` (ignored local artifacts).

## Execution and result

- `python tools/inspect_dataset.py --config configs/cp01.yaml --split {train,val,test}` decoded all three videos, aligned annotations and emitted GT timeline SVGs.
- `python tools/train_baseline.py --config configs/cp01.yaml --epochs 8` trained both models. Framewise best unweighted validation loss 3.0544 at epoch 8; MS-TCN best unweighted validation loss 2.0614 at epoch 1.
- `python tools/evaluate.py --config configs/cp01.yaml --split test --model both` ran action and event evaluation and wrote timelines.
- Framewise test: frame accuracy 0.0310; macro F1 over present action classes 0.0015; normalized edit 9.375; segment F1@10/25/50 all 0.000.
- MS-TCN test: frame accuracy 0.000; macro F1 0.000; normalized edit 0.000; segment F1@10/25/50 all 0.000.
- The action models failed to generalize. This is a measured failure, not a successful recognition result.
- Process anomaly precision/recall and duration anomaly precision/recall: **NOT EVALUATED**; IMPACT TAS-S sample has action labels, not ground-truth compliance/mistake labels.
- `run_pipeline.py` executed successfully using the selected framewise checkpoint on the held-out test video. It emitted 10 action events, 13 workflow violations, a JSON result, event snapshots/clips and a GT/prediction SVG. The action prediction itself was poor, so those violations are an execution-path demonstration, not valid compliance findings.

## Verified by execution

- Official sample archive download/extraction and SHA-256 validation.
- Three fixed-view videos and TAS-S annotations loaded; sampled labels and timelines produced.
- Both classifier training loops and checkpoint save/load.
- Test action metrics and timeline generation.
- End-to-end command generated structured result and recoverable video evidence.
- 12 deterministic unit tests passed after fixes to workflow completion, source-action mapping and end-of-video evidence frame clamping.

## Not verified / limitations

- No meaningful action-recognition performance; split is too small and class/procedure distributions are mismatched.
- No measured throughput/latency or real-time claim.
- No mistake/compliance ground truth, hence process detection precision/recall not available.
- Configured example valid paths are illustrative and do not encode the repeated component-level TAS-S route accurately. A workflow pass/fail on these predictions must not be treated as meaningful procedure compliance. CP01's state/anomaly logic is unit-tested, but integration with a properly annotated canonical route remains incomplete.
- Data splits are preselected sample executions, not a robust worker-independent validation design.
- Evidence is local file output; no persistence service, retention or privacy controls.

## Decision record

- KEEP: deterministic data/annotation loader, train-only normalization, framewise reference, classic MS-TCN comparison, temporal decoder, separate workflow engine, evidence snapshots/clips, action and process evaluation boundary, timeline artifact, config-driven flow.
- CHANGE: obtain more disassembly executions; use a disassembly-only train/validation/test split by worker/execution; preserve fine-grained TAS-S step/object labels until workflow reasoning; improve features or use official pretrained feature bundles after license/protocol verification; encode repeated procedure cycles and validate against route annotations; tune training only after a sound split.
- DROP: any claim that current model or emitted workflow violations are accurate, production-ready or real-time.

## Conclusion

CP01 is **PARTIAL**: data, model, temporal, workflow, evidence and evaluation stages execute end to end and deterministic core logic is tested. The quality gate for a useful action baseline and a semantically valid workflow integration is not met. Recommended next checkpoint: CP01.1 dataset/split and annotation/workflow alignment, then rerun the same baseline before expanding model complexity.
