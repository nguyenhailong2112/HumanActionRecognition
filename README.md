# Human Action R&D — Current System (CP07)

This repository is an R&D prototype, not a factory-ready process-compliance system. The current executable research slice evaluates temporal action segmentation on one fixed IMPACT v1.1 procedure/view. Workflow semantics remain human-dependent; process compliance is not evaluated.

## Current validated experiment

- Dataset: IMPACT v1.1, TAS-S, S2 split 2; `Disassembly_A`, `front` view.
- Research subset: 39 train / 5 validation / 4 held-out test executions; test worker SS07EL13. This procedure-scoped subset is **not** a full official leaderboard reproduction.
- Features: official I3D features, sampled at 5 FPS, float32 `T×1024`; target feature/video/annotation coverage 48/48. The verified source archive remains outside the project repository.
- Models: FramewiseBaseline and **our MS-TCN baseline on IMPACT**. CP05 training/evaluation and CP06 three-seed reliability artifacts are preserved.
- Environment used: Python 3.12.14, PyTorch 2.14.0+cu132, CUDA available, RTX 5060 Ti 16 GiB. See experiment reports for configuration and limits.
- CP07: 56 repository tests pass. This includes deterministic synthetic workflow logic; it does not establish real process performance.
- The current machine/environment snapshot is [recorded here](experiments/CP07/environment_audit.json); it is not a locked dependency environment.

## Source and data locations

Project source: `C:\Users\Admin\PycharmProjects\HumanActionRecognition`  
Dataset storage: `D:\HaiLongRnD\Datasets\HumanActionRecognition`

Keep raw data and extracted large assets outside the Git repository. `configs/cp05.yaml` contains the primary-machine data paths and frozen experiment split.

## Reproducible checks

Using the configured Windows environment:

```powershell
.\.venv-cp05\Scripts\python.exe -m unittest discover -s tests -v
.\.venv-cp05\Scripts\python.exe tools\validate_workflow.py --config configs\workflows\disassembly_A.draft.yaml
```

The second command is expected to reject the draft until the process owner supplies and validates semantics. Do not weaken that gate to make the command pass.

## Workflow and evidence gate

The workflow artifact must be a **Research Workflow Specification / Benchmark Procedure Interpretation**, not an official factory SOP. No executable `configs/workflows/disassembly_A.yaml` is present. The draft contains no accepted routes. Workflow logic is disabled unless `workflow.enabled: true` and `workflow.status: HUMAN_VALIDATED`; model-generated ActionEvents default to `evidence_status: unknown` because no confidence/evidence policy has been validated.

Complete [HUMAN_HANDOFF_CP07.md](HUMAN_HANDOFF_CP07.md) for procedure semantics and [HUMAN_HANDOFF_CP07_EVIDENCE_REVIEW.md](HUMAN_HANDOFF_CP07_EVIDENCE_REVIEW.md) for the actual event review. Until valid process ground truth exists, compliance/anomaly metrics and duration violations remain **NOT EVALUATED**.

## Repository map

- `src/human_action/`: IMPACT data loading, frame features, temporal models/metrics, ActionEvent, workflow engine, trace adapter, evidence.
- `configs/`: frozen CP05 experiment, CP06 repeatability configs, and non-executable workflow draft.
- `tools/`: data preflight, training/evaluation, workflow validation, CP06/CP07 analysis.
- `tests/`: data/split, model, temporal, workflow, evidence, and event/aggregation regressions.
- `experiments/`: checkpoint records and machine-readable outputs. Start with [EXP-CP05](experiments/EXP-CP05.md), [EXP-CP06](experiments/EXP-CP06.md), [EXP-CP07](experiments/EXP-CP07.md), and [CP07 closure audit](experiments/CP07/CP07_system_audit_and_closure.md).
- `ResearchDocuments/ResearchDocuments/`: research corpus, matrix and synthesis. Its studies inform the bounded design but do not imply that unimplemented perception branches are present.

## Current limits

The repository does not currently implement person/object/tool/hand/pose/zone tracking, multi-camera fusion, validated process-compliance performance, streaming latency, a production UI/API, or deployment safeguards. No advanced temporal model is justified until human evidence review and process semantics clarify the actual bottleneck.
