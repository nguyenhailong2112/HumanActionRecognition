# EXP-CP04 — Official Data Recovery, Benchmark Alignment & First Real Baseline

**Status: PARTIAL — official protocol/code and local readiness were re-audited; no full feature archive or approved SOP is present, so training, test evaluation and process integration did not run.**

## Objective

Resolve the remaining CP03 dependencies where possible, align our experiment description with the official IMPACT TAS-S protocol, and execute a valid baseline only if its required input exists.

## Audit and data acquisition

- Read current project direction and CP01/CP01.1/CP02/CP03 records; inspected the configured split, feature loader, preflight, retained models/checkpoints, task wrappers and official IMPACT v1.1 release/task documentation.
- Acquisition inventory: official `tools/download_impact.py` supports `features:I3D`, `features:MViTv2`, and `features:VideoMAEv2`; official docs expose Hugging Face selective download and a Google Drive mirror. Earlier attempts (documented in CP02) tried HF I3D three times and MViTv2 once without a verifiable complete archive. CP04 did not repeat those same transfers. The web retrieval tool could not access the official Drive folder URL. No unofficial source was used.
- Official I3D bundle: `features/IMPACT-v1.1-features-I3D.zip`, 15.7 GiB, SHA-256 `97f9d81443d1a3978e77b5db119b69089ecd470af77d6bb60bd20f792446a111`; these values match the local official `SHA256SUMS`. Destination and verification/resume steps are in `HUMAN_HANDOFF_CP04.md`.
- Current free C: space at audit: 18,955,083,776 bytes (about 17.65 GiB), tight for a 15.7 GiB direct download if temporary staging is needed. Keep the archive compressed and download directly to its destination or use a volume with adequate headroom.
- Fresh CP04 preflight: `.venv\\Scripts\\python.exe tools\\cp02_preflight.py --config configs\\cp01_1.yaml --output experiments\\CP04_data_readiness.json`. Split PASS, annotations PASS (48/48), features INCOMPLETE (2/48), videos INCOMPLETE (2/48). No full test video is available locally.
- Existing `models/cp01_framewise.pt` and `models/cp01_mstcn.pt` are CP01 smoke-test checkpoints from the invalid cross-procedure setup; they are not CP04 checkpoints and were not reused.

## Official IMPACT TAS-S alignment

- Official TAS-S task: framewise step-level labels/background. Official split family S1–S4; S2 is Cross-Subject. Official metrics: framewise Accuracy, Edit score, F1@10/25/50. Official listed TAS-S methods: LTContext, ASQuery, DiffAct, FACT (official `docs/BENCHMARK.md`, `tasks/TAS/README.md`, and wrappers under `tasks/TAS/{ltcontext,asquery,diffact,fact}`).
- Our CP01.1/CP02/CP03 data target filters S2 membership to 48 `Disassembly_A/front` executions (39/5/4), with 17 observed procedure-specific labels plus NULL. It is a **procedure-scoped research subset drawn from official S2 membership**, not the complete official TAS-S benchmark test partition; metrics from it must not be presented as leaderboard-equivalent official results.
- The retained `MSTCN` is our temporal baseline on IMPACT. It is not one of the official TAS-S methods and no official benchmark reproduction is claimed. The repository’s official TAS-S methods remain candidates for a future separate aligned reproduction, but no method was trained here.
- Feature convention from official `docs/FEATURES.md`: I3D `T×1024`, centered 16-frame clip per output frame, 224 crop, RGB normalized `[-1,1]`; MViTv2-B `T×768`; VideoMAEv2-G `1408×T`. Official feature arrays align with released RGB stream. Our current experiment config is frozen to I3D and 1024 dimensions; no representation switch was made.

## Environment and extraction

- Verified: PyTorch `2.14.0+cpu`; `torch.cuda.is_available()` false; device count zero; `nvidia-smi` unavailable.
- Official extraction entrypoint: `ResearchDocuments/01_IMPACT/code/IMPACT/tools/features/extract_i3d.py`. It calls CUDA directly and implements the release I3D convention. This laptop cannot reproduce it as configured; official GPU extraction is deferred to a CUDA-capable machine if the released features cannot be acquired. Do not describe CPU extraction as verified.
- No full front video or feature release arrived during CP04. The sample features are not sufficient for the specified cross-subject validation/test experiment.

## Training and evaluation

- FramewiseBaseline training: **NOT RUN**; full 39/5/4 feature setup unavailable.
- Our MS-TCN training: **NOT RUN** for the same reason.
- Official TAS-S baseline reproduction (LTContext/ASQuery/DiffAct/FACT): **NOT RUN**; data absent, wrappers expect full released features and GPU-list training, and our filtered one-procedure split is not the complete official benchmark evaluation.
- Validation selection, frozen final test, action metrics, per-class analysis, confusion, prediction timelines and temporal error analysis: **NOT EVALUATED**. CP01 checkpoint/results are excluded as invalid evidence for CP04.

## Workflow and process

- No approved `configs/workflows/disassembly_A.yaml`; workflow remains disabled. Exact process-owner SOP handoff is in `HUMAN_HANDOFF_CP04.md`.
- Real process deviation labels remain absent. PPR hand-level procedural phase labels are not a substitute. Real process precision/recall and duration violations are **NOT EVALUATED**.
- Actual model-to-workflow integration and inference evidence are **NOT RUN**. Existing synthetic logic/evidence tests are not process performance.

## Tests and runtime

- `python -m unittest discover -s tests -v`: **24 passed**. No implementation code changed in CP04.
- Inference runtime/FPS/latency/memory: **NOT MEASURED**; no CP04 model checkpoint/inference. Streaming real-time behavior is not claimed.

## Decision

- Evidence-backed state: **F — still cannot evaluate reliably**.
- Immediate dominant bottleneck: **DATA (full, checksum-verified feature artifact)**. Separate workflow bottleneck: process-owner grounding.
- Decision: **INVESTIGATE**; keep the two current model baselines and protocol config; do not escalate model complexity.
- Next recommended direction: **Improve Data**. Resume after the official feature archive is placed and preflight confirms 48/48 target arrays. If training on the laptop CPU is impractical, run the prepared same-protocol experiment on the future RTX 5060 PC. SOP approval remains necessary before process compliance claims.

## Evidence status

- **VERIFIED BY EXECUTION:** CP04 preflight status; 48/48 annotation structure and split checks pass; 2/48 features valid; 2/48 videos present; official feature checksum value matches local release manifest; environment is CPU-only; 24 tests pass.
- **NOT VERIFIED:** downloaded full official features; full video quality; action model performance; official-method reproduction; process-owner policy; actual inference evidence and runtime.
- **NOT EVALUATED:** action/temporal/per-class metrics, process anomaly metrics, duration violations.
- **HUMAN-DEPENDENT:** provide the official feature ZIP if browser/mounted Drive access succeeds; process owner must supply and approve SOP. Optional real process metrics need owner-reviewed labels on held-out executions.
