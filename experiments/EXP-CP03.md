# EXP-CP03 — First Validated Action Baseline & Procedure Grounding

**Status: PARTIAL — official protocol and annotation integrity pass, but full feature/video inputs and process-owner SOP are still absent. Training and model/process evaluation were not run.**

## Objective

Execute the official IMPACT v1.1 TAS-S S2 Disassembly_A/front protocol with the retained framewise and MS-TCN baselines; connect actual predictions to an approved process workflow and evaluate only against valid ground truth.

## Audit and data readiness

- Current implementation inspected: `configs/cp01_1.yaml`, `src/human_action/impact_release.py`, model/training/evaluation tools, workflow validator/engine, tests, and EXP-CP01/CP01.1/CP02 records.
- Dataset: official IMPACT v1.1; frozen official TAS-S S2 split 2; procedure `Disassembly_A`, camera `front`; action vocabulary retains the 17 observed labels plus `NULL` as configured. No remapping or class pruning was made.
- Split: 39 train / 5 validation / 4 test. Existing split QA reports execution-disjoint and held-out test worker `SS07EL13`; no split changes were made.
- Current execution: `.venv\\Scripts\\python.exe tools\\cp02_preflight.py --output experiments\\CP03_data_readiness.json` exited successfully. Results: split PASS, annotations PASS (48/48), features INCOMPLETE (2/48 valid; 46 missing), videos INCOMPLETE (2/48 present; 46 missing). The two sample feature sequences passed the existing shape/finite/alignment checks. The two available videos decode at 30 FPS, 1280×720 and align to their annotation frame counts; they are both train-side and do not support held-out testing.
- The generated readiness artifact is `experiments/CP03_data_readiness.json`.
- Official feature source, expected artifact name, SHA-256 and placement/verification steps are already specified in `HUMAN_HANDOFF_CP02.md`. Prior HF attempts and local extractor constraints are recorded in EXP-CP02; they were not repeated. The current host has CPU-only PyTorch; the reference I3D extractor is CUDA-dependent. No alternative, unrelated, pseudo, validation-as-train, or test-as-train features were used.
- Annotation archive integrity was verified in CP02 against the official release checksum manifest. CP03 preflight independently revalidated split/annotation structure.

## Frozen experiment protocol

| Item | Frozen value |
|---|---|
| Dataset/version | IMPACT v1.1 official release |
| Procedure/view | Disassembly_A / front |
| Split | TAS-S S2 split 2, 39/5/4; execution-disjoint, held-out test worker |
| Input | Official frame-aligned I3D, 1024-D, 5 FPS config |
| Vocabulary | 17 observed action labels + `NULL`, as `configs/cp01_1.yaml` |
| Models | Existing FramewiseBaseline and MSTCN |
| Selection | Validation-only, per existing training protocol |
| Test protocol | Deferred; no test run until full data and trained checkpoints are available |
| Process policy | Disabled pending approved SOP; no invented duration limits |

No model/configuration changes or test-set tuning were performed.

## Training and action evaluation

- Framewise training: **NOT RUN** — 46 required sequences are missing.
- MS-TCN training: **NOT RUN** — same blocker.
- Checkpoints, validation selection, final test metrics, class metrics, GT/prediction timelines, temporal error review: **NOT GENERATED / NOT EVALUATED**.
- CP01 smoke-test scores are not reused as evidence for CP03 because that split mixed procedures and was not a valid target protocol.

## Procedure and process evaluation

- No process-owner-approved Disassembly_A SOP is present under `configs/workflows/`; workflow remains disabled. Current annotations and observed action order are not used to infer official policy.
- Exact SOP template and required owner decisions (action disposition, ordered/alternative paths, completion, source/revision; timing only if specified) are in `HUMAN_HANDOFF_CP02.md`.
- Official PPR `NORMAL/ANOMALY/RECOVERY` labels are not workflow deviation labels. Real process precision/recall and duration anomaly metrics are **NOT EVALUATED**.
- Synthetic workflow tests validate deterministic engine behavior only. They do not demonstrate process performance.
- Model-prediction → action event → approved workflow → evidence integration: **NOT RUN**. Synthetic evidence unit coverage is not real inference evidence.

## Runtime and tests

- Runtime: **NOT MEASURED**; there is no CP03 checkpoint for inference. CUDA is unavailable; do not interpret existing offline timing code as a measured streaming result.
- `python -m unittest discover -s tests -v`: **24 tests passed**. Coverage includes annotation parsing/alignment, official split integrity, model tensor behavior, temporal decoding, workflow transitions/skip/repeat/wrong-order/branch/rework/reset/duration/incomplete and synthetic evidence snapshot linkage.
- `pytest` is not installed in `.venv`; the repository tests were executed successfully through built-in `unittest` discovery.

## Error analysis and decision

- Observed failure: experiment execution cannot reach model evaluation because 46/48 official I3D sequences are unavailable; no inference errors can be diagnosed from two train samples.
- Dominant immediate blocker: **DATA / feature availability**. Separate process-semantic blocker: **WORKFLOW grounding** pending process owner. Current evidence does not support blaming representation or temporal model.
- Conclusion: **F — System still cannot yet be evaluated reliably.**
- Decision: **INVESTIGATE** the official feature acquisition and process-owner handoff; do not increase model complexity.
- Next checkpoint direction (choose one): **Improve Data**. Rationale: full S2 feature sequences are the gating dependency for training and same-protocol action evaluation. SOP collection remains a separate required human action before compliance evaluation.

## Human actions and resume path

1. Follow `HUMAN_HANDOFF_CP02.md` section A to obtain the official feature ZIP, verify the published SHA-256, and place it at the configured location. After placement, run `tools/cp02_preflight.py`; acceptance requires all 48 sequences present and valid with split counts 39/5/4.
2. Process owner supplies and approves the SOP in `configs/workflows/disassembly_A.yaml` using section B of that handoff. Do not infer missing semantics or duration limits.
3. Once features pass preflight, train both retained baselines, select checkpoints using validation only, freeze configuration, then perform one final test evaluation and generate per-class/timeline analyses.
4. Once SOP is validated, enable workflow integration. Real process precision/recall still requires human-reviewed held-out violation labels; otherwise report NOT EVALUATED.

## Evidence status

- **VERIFIED BY EXECUTION:** current preflight output; 48/48 annotations structurally pass; official S2 split check passes; 2/48 feature arrays pass; 2/48 videos present; 24 deterministic tests pass.
- **NOT VERIFIED:** full feature archive/inference input availability; all 48 raw video decode/visual quality; any action-model result; SOP semantics; process-level anomaly performance; real inference evidence; inference runtime.
- **NOT EVALUATED:** frame accuracy, macro-F1, edit, segmental F1, per-class/confusion analysis, temporal boundary quality, workflow/process precision/recall and duration anomalies.
- **HUMAN-DEPENDENT:** acquisition of the full official feature artifact and process-owner approval of workflow policy.
