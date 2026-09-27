# EXP-CP05 — Our Framewise and Temporal Baselines on IMPACT

**Status: PARTIAL (historical checkpoint).** Both baselines and held-out action evaluation were complete at CP05; workflow grounding was human-dependent. The ZIP was absent at CP05 execution time, but its integrity was subsequently verified during CP06. Current workflow status is recorded in EXP-CP07.

## Objective and hypothesis
Establish an evidence-backed, procedure-scoped baseline and determine whether our MS-TCN improves temporal action segmentation over our simpler framewise classifier on the same official released features and fixed split.

## Dataset and scope
- IMPACT v1.1, official TAS-S action annotations and official S2 split 2 membership.
- Procedure-scoped subset: `Disassembly_A`, `front`; 39 train / 5 validation / 4 test. Execution-disjoint with held-out test worker `SS07EL13`.
- This filtered subset is a research protocol, not a full official leaderboard partition or leaderboard reproduction.
- Data stays external at `D:\HaiLongRnD\Datasets\HumanActionRecognition\IMPACT\v1.1`.

## Feature source and integrity
- Extracted official I3D directory, `T×1024`, float32, sampled from aligned 30 FPS descriptors at 5 FPS; official convention in the corpus defines centered 16-frame RGB clips and 224 crop.
- Historical CP05 archive state: no original `IMPACT-v1.1-features-I3D.zip` was found at CP05 execution time, so it was not verified then. CP06 later verified the supplied archive SHA-256 (`97f9d81443d1a3978e77b5db119b69089ecd470af77d6bb60bd20f792446a111`) against the local official release manifest and passed the official structure/CRC verifier; see `experiments/CP06/CP06_context_and_audit.md`.
- CP05-time extracted target feature QA: 48/48 present, expected 1024 dimensions, finite, and exact frame-count match to extracted official TAS-S metadata. Archive integrity at CP05 was unverified; CP06 subsequently verified it.

## Labels and preprocessing
- Preserve the 17 observed non-background Disassembly_A/front action labels plus `NULL` in `configs/cp05.yaml`.
- Official released features and TAS-S labels are sampled on the same frame indices (5 FPS from the 30 FPS source); normalization mean/std are fitted on train sequences only.
- No class remapping or test-informed tuning.

## Models and hyperparameters
- `FramewiseBaseline` and repository `MSTCN`; architecture is unchanged.
- Model input: 1024; MS-TCN hidden 32, 5 layers, 3 stages, dropout 0.2.
- AdamW, learning rate 0.001, weight decay 0.0001; 12 epochs; seed 17; existing inverse-square-root train class weights; per-sequence updates and gradient clipping at 5.
- Device: CUDA (`cuda:0`) when verified available on this PC.
- Best checkpoint selected only by unweighted validation cross-entropy. Final-epoch checkpoint saved separately.

## Validation and test protocol
- Select best epoch by validation loss only; test is deferred until both models complete and configuration is frozen.
- Final test evaluation used the unchanged frozen config/checkpoints; a second deterministic invocation was made to persist newly added confusion-matrix output. No test results informed training, hyperparameter changes, or model selection. Report Frame Accuracy, action Macro-F1 (non-background supported classes), normalized Edit, Segmental F1@10/25/50, and per-class support/precision/recall/F1.
- Generate ground-truth/prediction timelines for all held-out executions. Document the repository's metric implementation and limitations.

## Workflow and process boundary
- Workflow remains disabled pending the process-owner Research Workflow Specification. Action segmentation results do not imply process compliance. Process anomaly performance is not evaluated without matching reviewed violation labels.
- Runtime is offline full-sequence feature inference; it does not represent streaming latency. Feature extraction is not included in this model-only timing.

## Environment snapshot
- CP05 environment: Python 3.12.14, CUDA-enabled PyTorch wheel `2.14.0+cu132`, NumPy 2.5.3, OpenCV 4.14.0; GPU/VRAM/driver from NVIDIA-SMI and `torch.cuda` verification recorded in final artifacts.
- Exact config and SHA-256 recorded by the training report.

## Freeze
- Frozen prior to training on 2026-09-27 local PC execution.
- Validation may select epoch/checkpoint; no changes to labels, split, sampling, architecture, or hyperparameters based on test results.

## Executed results (2026-09-27)

- Full CP05 preflight: split, annotations, extracted features and source videos all PASS; 48/48 target features valid and aligned; 48/48 front videos fully decoded, each 30 FPS at 1280×720 and with decoded frame count equal to the TAS-S annotation count.
- Dataset root contains 560 extracted I3D `.npy` files across five views, full front/top RGB (112 files per view), annotations, depth, eye tracking and sample files. Left/right/ego RGB are absent. No more camera downloads are needed for this front-view experiment.
- At the CP05 checkpoint, the I3D ZIP was absent and archive integrity was not verified. This historical limitation was resolved in CP06; see the CP06 archive audit for exact hash and CRC evidence. Extracted target feature arrays had separately passed structural and finite-value checks in CP05.
- Environment: Python 3.12.14; NumPy 2.5.3; OpenCV 4.14.0; PyTorch 2.14.0+cu132; CUDA 13.2; NVIDIA RTX 5060 Ti 16 GiB; driver 596.21. Existing tests: **24 passed**.
- Training on the fixed 39/5/4 split: Framewise, 12 epochs, best epoch 11, validation CE 1.60675, 22.68 seconds; our MS-TCN, 12 epochs, best epoch 11, validation CE 1.27032, 31.49 seconds. Selection used validation loss only. Both best and final checkpoint artifacts are saved.
- Held-out S2 test metrics averaged over four executions: Framewise Frame Accuracy .445, Macro-F1 .319, Edit 11.70, F1@10 .149, F1@25 .094, F1@50 .032. Our MS-TCN: .569, .390, 50.39, .445, .445, .207 (deltas +.124, +.071, +38.69, +.296, +.351, +.175).
- Pooled MS-TCN action F1 is strongest on EXTRACT_BEARING_PLATE_ASSEMBLY (.683), REMOVE_ROTOR_ASSEMBLY (.653), and DETACH_ADAPTER_PLATE (.656). Weak supported classes include STORE_GEARBOX_HOUSING (0/6 frames), STORE_ANTI_VIBRATION_HANDLE (.047/34), STORE_BEARING_PLATE_ASSEMBLY (.138/216), and STORE_TOOL (0/30). Four action classes have no test support. Dominant errors include NULL→EXTRACT_BEARING_PLATE_ASSEMBLY (179 frames), STORE_BEARING_PLATE_ASSEMBLY→DETACH_ADAPTER_PLATE (169), and REMOVE_LOCKING_LEVER_ASSEMBLY→EXTRACT_BEARING_PLATE_ASSEMBLY (138).
- 69 actual non-background MS-TCN events on held-out videos were linked to the matching event timestamp/frame, snapshot, and two-second context clip. Maximum timestamp/frame delta is below one frame. Workflow decision is explicitly NOT EVALUATED.
- Offline timing uses cached I3D features; it excludes extraction and decode and is not streaming latency. Per-video inference times vary due first-run CUDA initialization. CPU/GPU utilization and peak memory were not captured.
- Human workflow handoff remains open. The official PSR prerequisite graph is data-mined and defines component-state dependencies for a distinct task; it cannot be treated as a canonical route or substituted for process-owner semantics.
- Our FramewiseBaseline and MS-TCN are **our baselines on IMPACT** on a procedure-scoped research subset. Official TAS-S lists LTContext, ASQuery, DiffAct and FACT; CP05 is not their reproduction or a leaderboard result.

