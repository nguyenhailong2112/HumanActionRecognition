# CP05 Context Recovery

## Current project state
- This is the existing Human Action research repository and corpus, not a new project. Research corpus matrix/synthesis are at `ResearchDocuments/ResearchDocuments/ResearchMatrix.md` and `ResearchSynthesis.md` in this checkout.
- CP01/CP01.1 established a vertical slice and corrected split/protocol; CP02–CP04 audited data/protocol but did not train valid models. CP01 checkpoints are legacy cross-procedure smoke artifacts and were not reused.
- CP05 now has a frozen procedure-scoped experiment, trained baselines, one held-out S2 action evaluation, timelines, confusion/error analysis, and actual event evidence. Overall CP05 remains PARTIAL because workflow policy is human-dependent and the source ZIP is unavailable for byte-level audit.

## Completed capabilities
- Existing code: official IMPACT TAS-S parsing, S2 split integrity, frame-aligned I3D loading, 5 FPS sample alignment, FramewiseBaseline, MS-TCN, segmentation metrics, event decoding, deterministic workflow logic, and evidence utilities.
- CP05 independently passed split/annotation/feature/video readiness for 48 target executions; both models trained on CUDA and were evaluated on the frozen test split. Report/checkpoint paths are in `experiments/EXP-CP05.md` and `experiments/CP05/`.
- Existing workflow and evidence tests pass; workflow tests are synthetic deterministic logic tests, not process performance.

## Current blockers
- No original `IMPACT-v1.1-features-I3D.zip` found anywhere on D:. The extracted target arrays are structurally/numerically valid (48/48), but SHA-256 and ZIP CRC of the source archive cannot be rechecked.
- No process-owner Research Workflow Specification for Disassembly_A. Official PSR prerequisites are data-mined component-state relations for another task, not TAS-S action policy. Workflow/compliance and real anomaly performance remain NOT EVALUATED.
- One representative frame was inspected visually; the full subset was machine-decoded and frame-aligned, but not manually reviewed for action semantics.

## Available data
- Dataset root: `D:\HaiLongRnD\Datasets\HumanActionRecognition\IMPACT\v1.1`; raw data remains outside Git.
- Extracted annotations, 560 I3D arrays across five views, 112 front + 112 top RGB videos, depth, eye-tracking, sample data, and official release metadata are present. Left/right/ego RGB are absent.
- Fixed target: IMPACT v1.1 TAS-S S2 split 2, Disassembly_A/front; 39 train / 5 validation / 4 test. All 48 target features are finite, 1024-D and frame-aligned; all 48 front videos decode and match annotation frame counts.

## Available models
- Existing FramewiseBaseline and MS-TCN implementations.
- CP05 best/final checkpoints for both models are saved under `models/cp05_*`; model logs, config, test metrics, per-class/confusion tables, timelines, and evidence index are under `experiments/CP05/` and `results/cp05/`.
- These are **our baselines on IMPACT**, not official TAS-S methods or a complete leaderboard reproduction.

## Current environment
- Windows; NVIDIA GeForce RTX 5060 Ti, 16 GiB VRAM, driver 596.21, system CUDA 13.2.
- Inherited `.venv` is not executable on this PC. `.venv-cp05` was rebuilt using Python 3.12.14, NumPy 2.5.3, OpenCV 4.14.0, PyTorch 2.14.0+cu132; CUDA availability and device identity pass.

## Pending human actions
- Process owner: supply `configs/workflows/disassembly_A.yaml` using `HUMAN_HANDOFF_CP05.md`, with source/revision, step IDs/meanings/action mapping/order, optional/conditional/alternative/rework paths, completion, and official timing only if documented.
- No extra camera download is needed for this front-only feature experiment. Download left/right/ego RGB only if a future multi-view video experiment requires them.
- If the source I3D ZIP survives outside D:, provide its path for checksum/CRC audit; do not redownload solely for this CP05 result unless byte-level archive provenance is required.

## CP05 execution boundary
- The action path uses official extracted I3D features derived from front videos → trained model → temporal action events → held-out action metrics/timelines and timestamp-linked video evidence. Raw-video I3D extraction/streaming was not run.
- No workflow decision or process anomaly score is claimed until human policy and matching reviewed ground truth are supplied. Offline feature-vector inference is not streaming real-time performance.
- Do not escalate model complexity until the remaining action confusions and data/representation issues are resolved and measured.
