# EXP-CP02 — Validated Action Baseline & Procedure Grounding

**Status: PARTIAL — official protocol and available-input QA verified; full feature acquisition, model training/test evaluation, and procedure policy remain human-dependent.**

## Objective

Use the official IMPACT v1.1 `Disassembly_A/front` TAS-S setup to train the existing framewise and MS-TCN baselines on an execution-disjoint S2 protocol; ground workflow only in an approved SOP; keep task-specific anomaly labels separate from workflow-violation truth.

## Dataset and split

- Source/version: official IMPACT v1.1 annotation release, CC BY-NC-SA 4.0, non-commercial research/education.
- Target and camera: `Disassembly_A`, fixed exocentric front view.
- Official split: TAS-S S2 split 2, cross-subject. Train 39 / validation 5 / test 4 executions. IDs are execution-disjoint; test worker `SS07EL13` is held out from train. Train/validation/test contain 12/4/1 workers, respectively.
- Annotation QA: all 48 selected target JSON records pass exact per-frame coverage, label, ordering, gap/overlap, and frame-bound validation. Internal action mapping is identity after uppercasing the original official TAS-S labels; vocabulary is frozen in `configs/cp01_1.yaml` with 17 observed action labels plus `NULL` background.
- Local media/input state: the official annotation archive is present. Preflight confirms 48/48 annotations; only 2/48 official I3D arrays and 2/48 front videos are local. Both existing videos decode fully at 30 FPS, 1280×720, and their decoded frame counts match TAS-S metadata (ER07AD15: 3478; AL07EJ17: 3998). No representative validation or test source video is local; full video-quality generalization is therefore not checked.
- Data report: `experiments/CP02/data_readiness.json`; preflight entrypoint: `tools/cp02_preflight.py`.
- Official PPR-L/R test annotations are present: test counts include L ANOMALY=674 frames and R ANOMALY=4071 frames. These are procedural-phase labels, distinct from workflow violations such as skip, wrong order, repeat, timeout, or SOP non-compliance. They are not scored as workflow truth.

## Feature path investigation

- Primary source: official `features/IMPACT-v1.1-features-I3D.zip`, documented as 15.7 GiB, 1024-D, frame-aligned `T×1024`; published SHA-256: `97f9d81443d1a3978e77b5db119b69089ecd470af77d6bb60bd20f792446a111`.
- Across CP01.1 and CP02, tried the official I3D selective download three times from Hugging Face, including a retry with Xet disabled, and tried the smaller official MViTv2 feature archive once as an alternate representation path. None produced a verifiable archive. Feature schema remains frozen to I3D; no switch was made. Official Google Drive mirror is documented as carrying the same versioned archives; exact human download/verification instructions are in `HUMAN_HANDOFF_CP02.md`.
- Official extraction fallback inspected: `ResearchDocuments/01_IMPACT/code/IMPACT/tools/features/extract_i3d.py`. It uses centered 16-frame RGB clips, 224 center crop, `[-1,1]` input normalization, `T×1024` output, external `piergiaj/pytorch-i3d` code, and RGB ImageNet/Kinetics pretrained weights. The reference code calls CUDA directly. Current PyTorch is CPU-only and the full raw front-video package cannot fit on the current volume. Extraction is documented but not reproducible in this environment; no alternate or synthetic features were generated.
- Loader now accepts either the official ZIP member or individual `.npy` files from the official feature-release/extractor directory. Unit tests verify frame alignment for both routes.

## Model and training protocol

- Models retained: `FramewiseBaseline` and existing `MSTCN`; no new architecture.
- Config: `configs/cp01_1.yaml`; frozen seed 17, CPU, 5 FPS sampling, 1024-D I3D, 18 output IDs including background, 12 configured epochs.
- Checkpoint selection: lowest unweighted validation cross-entropy; test metrics are deferred. `train_baseline.py --defer-test-eval` separates training/validation from a single final test run and records training pipeline time and config hash.
- Training: **NOT RUN**. Full official feature sequences are unavailable. No CP02 model checkpoints, loss curves, selected epoch, or model performance are claimed.

## Action, temporal, workflow, and process evaluation

- Action accuracy, macro-F1, edit score, segmental F1@10/25/50, per-class comparison, and temporal boundary analysis: **NOT EVALUATED**; models were not trained.
- Five ground-truth-only timelines from CP01.1 remain available under `results/cp01_1/ground_truth/`; no CP02 prediction timelines exist.
- Workflow/SOP: **HUMAN-DEPENDENT**. No approved Disassembly A SOP is present. `workflow.enabled` remains false; duration thresholds remain unset. Exact policy template is in `HUMAN_HANDOFF_CP02.md` and `configs/workflows/README.md`.
- Deterministic workflow logic: correct completion, alternate branch, finite explicit rework path, skip, repeat, wrong order, unexpected action, reset, incomplete route, and duration rule behavior are synthetic logic tests only—not process benchmark results.
- Process anomaly metrics: **NOT EVALUATED**. Official PPR anomaly/recovery phases are real labels for a different prediction target; no matching workflow-violation labels exist for the current engine. Do not report workflow precision/recall from PPR counts.
- Model-generated action-event → approved workflow → violation → real image/clip evidence: **NOT RUN**. No CP02 model and no test videos are available. Existing deterministic evidence tests use synthetic input only.

## Runtime and environment

- Environment: local Windows, `.venv`, PyTorch `2.14.0+cpu`; CUDA unavailable.
- Offline sequence inference FPS/latency, peak memory, GPU utilization: **NOT MEASURED**, because no CP02 checkpoint exists. Evaluation code records whole-sequence inference timing for future runs; it is not presented as streaming latency. CPU RSS instrumentation is not installed and remains unmeasured.
- Input data throughput/extraction runtime: not measured as a benchmark.

## Failure analysis

| Category | Evidence / status |
|---|---|
| Data availability | Dominant immediate blocker: 46/48 S2 I3D features and front videos absent; two official download attempts wrote no archive. |
| Annotation | PASS structurally for all 48 target trials. Semantic correctness has not had process-owner review. |
| Feature | Official I3D representation is defined and two arrays pass shape/finite/frame-alignment checks; full release not present. |
| Representation / action ambiguity / class imbalance | Not diagnosable until both baselines run on the fixed split. |
| Temporal model | Not diagnosable without validation/test results; do not escalate model size. |
| Workflow | Dominant blocker for compliance meaning: missing approved SOP and process violation truth. |

## Verified by execution / Not verified / Not evaluated / Human-dependent

**Verified by execution:** official split integrity (39/5/4), 48/48 target TAS-S structural QA, 2/2 available official I3D arrays aligned, 2/2 available front videos fully decoded and frame-aligned, CPU-only PyTorch, synthetic deterministic tests (24 pass), and archive absence after attempted downloads.

**Not verified:** visual quality for unavailable executions; process-owner validation of label meaning/SOP; complete 48/48 feature and video input integrity; official feature archive checksum locally.

**Not evaluated:** action or temporal test metrics; baseline comparison; real workflow compliance/anomaly precision/recall; model-generated evidence; model runtime/memory.

**Human-dependent:** download/provision the official feature bundle (or provide licensed full input on adequate GPU/storage); approve the operational SOP; optionally annotate workflow violations on only the four held-out test executions after SOP approval.

## Decisions

- **KEEP:** IMPACT v1.1, official S2, same-procedure labels, I3D representation when available, existing framewise/MS-TCN implementations, validation-only checkpoint selection.
- **CHANGE:** add direct directory `.npy` support for the official extractor/release; defer test evaluation until after validation/model/config freeze; make CP02 preflight report split/annotation/feature/video coverage.
- **DROP:** any inferred canonical route; any use of PPR labels as workflow violation truth; any training on sample videos or held-out test data.
- **INVESTIGATE:** resume with checksummed official I3D features; inspect test videos; train both heads; compare classes/segmentation and measured runtime; integrate only a process-owner-approved workflow.

## Resume path

Follow `HUMAN_HANDOFF_CP02.md`. After data delivery, run `tools/cp02_preflight.py`, train with `tools/train_baseline.py --defer-test-eval`, inspect validation results and freeze configuration, run final test evaluation once with `tools/evaluate.py`, then summarize with `tools/compare_baselines.py`. Do not enable process scoring until an approved SOP and matching held-out process annotations are available.
