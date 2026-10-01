# CP12 Context Audit

Pre-implementation audit captured 2026-10-01.

## Repository and frozen scope

- HEAD at audit: `198801db5b2413c48ee4163a6597a890278170d7` (`CP11`), branch `main`; initial worktree was clean.
- CP11 report, its three CP11 artifacts, executable research workflow, workflow engine/trace and CP11 tests were inspected.
- CP11 research workflow is `RESEARCH_APPROVED` for `PROJECT_RESEARCH`; `factory_sop_validated: false`. It must not be presented as an official IMPACT procedure or factory SOP.
- CP05/CP06 checkpoint files, `results/cp05/evaluation`, CP08 frozen events and experiment artifacts are historical provenance and must remain unchanged.
- CP11 records 12 out-of-scope actions (5 required from the 17 project/model non-NULL classes); two CP11 artifacts still incorrectly said eleven. README still described CP07 and said the executable workflow was absent.
- CP11 changed `.idea/vcs.xml` by removing the nested research-repository mappings. CP12 restores the file content from the CP10 parent; no other IDE configuration change is in scope.

## Frozen experiment verification

- Dataset protocol in `configs/cp05.yaml`: IMPACT v1.1, TAS-S, official S2 split 2, `Disassembly_A`, front, 39 train / 5 validation / 4 test, cross-worker test.
- Existing loader returned these four test IDs, all worker `SS07EL13`: `SS07EL13_Disassembly_A_001_front`, `_002_front`, `_003_front`, `_004_front`.
- Checkpoint selected without test-performance selection: `models/cp05_mstcn_best.pt`, the CP05 MS-TCN best-validation checkpoint (seed 17). No training or tuning is allowed in CP12.
- Current machine verified: Python 3.12.14, PyTorch 2.14.0+cu132, CUDA available, NVIDIA GeForce RTX 5060 Ti, OpenCV 4.14.0, NumPy 2.5.3.

## Data source verification

- The four source videos and corresponding official I3D feature files exist under the external dataset root configured by `configs/cp05.yaml`.
- All four source videos report 30 FPS and decoded metadata frame counts 6756, 3939, 4040 and 3543.
- All four original feature arrays are float32 and exactly `(video_frame_count, 1024)`. `load_split(..., "test", ...)` yields 5 FPS sampled sequences of 1126, 657, 674 and 591 rows, consistent with the existing 30-to-5 FPS stride of 6.
- This establishes file/shape availability; the demo still must validate full finite-value content, actual video decode count, timeline coverage, output frame count and output reopenability.

## CP12 boundary

Build a single CLI that reuses `load_checkpoint`, `predict_features`, `decode_segments`, and `to_action_events`. Render the frozen model's prediction-only video and export segment JSON/CSV, ActionEvents and provenance manifests for all four held-out executions. Keep evidence status `unknown`; do not invoke workflow semantics, produce compliance labels, retrain, tune, or alter frozen artifacts. Generated videos remain under ignored `results/cp12/`.
