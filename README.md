# Human Action R&D — CP11 / CP12

This repository is an R&D prototype, not a factory-ready process-compliance system. CP11 established a project-approved **Research Workflow Specification / Benchmark Procedure Interpretation** for one bounded study; it is not official IMPACT author ground truth or a factory SOP. CP12 provides a visual demo of frozen action inference on the held-out IMPACT test executions. Process performance remains **NOT EVALUATED**.

## Current validated research slice

- Dataset: IMPACT v1.1, TAS-S, S2 split 2, `Disassembly_A`, `front`.
- Research subset: 39 train / 5 validation / 4 held-out test executions; held-out worker `SS07EL13`. This is not a full official leaderboard reproduction.
- Features: official precomputed I3D features; original arrays are frame-aligned `T×1024` at 30 FPS and sampled by the existing pipeline at 5 FPS for inference. Data remain outside the repository.
- Frozen models: FramewiseBaseline and our MS-TCN on IMPACT. CP05/CP06 checkpoints, vocabularies, split and historical metrics remain unchanged.
- CP11 workflow: `configs/workflows/disassembly_A.yaml` is `RESEARCH_APPROVED` for project research only. It explicitly sets `factory_sop_validated: false`. Unknown evidence does not advance process state.
- CP12 status: **READY**. It runs the frozen CP05 seed-17 MS-TCN best checkpoint on all four held-out executions and writes videos with prediction overlays, a synchronized action timeline, segment JSON/CSV and provenance manifests under ignored `results/cp12/`.

## Run the CP12 demo

PowerShell, from the project root:

```powershell
$videoRoot = 'D:\HaiLongRnD\Datasets\HumanActionRecognition\IMPACT\v1.1\videos\IMPACT-v1.1-videos-front\IMPACT-v1.1\videos\front'
$featureRoot = 'D:\HaiLongRnD\Datasets\HumanActionRecognition\IMPACT\v1.1\features\IMPACT-v1.1-features-I3D\IMPACT-v1.1\features\I3D'
$ids = @(
  'SS07EL13_Disassembly_A_001_front',
  'SS07EL13_Disassembly_A_002_front',
  'SS07EL13_Disassembly_A_003_front',
  'SS07EL13_Disassembly_A_004_front'
)
foreach ($id in $ids) {
  .\.venv-cp05\Scripts\python.exe demos\run_human_action_demo.py `
    --video "$videoRoot\$id.mp4" `
    --features "$featureRoot\$id.npy" `
    --checkpoint models\cp05_mstcn_best.pt `
    --config configs\cp05.yaml `
    --output-dir "results\cp12\$id"
  if ($LASTEXITCODE -ne 0) { throw "CP12 demo failed for $id" }
}
```

Each execution folder contains `demo_video.mp4`, `prediction_segments.json`, `prediction_segments.csv` and `manifest.json`. Generated videos are local outputs and are ignored by Git. The on-video confidence is the model's mean softmax score for the predicted class; it is not calibrated confidence or evidence sufficiency. The overlay shows action inference only and makes no compliance judgment.

## Workflow and evidence boundary

CP11's research workflow has five required observable actions: UNSCREW followed by the four component removals in any order. Twelve modeled auxiliary/logistics/retrieval/install/attach/tool actions are out of scope but preserved as observations. Completion means research-defined observable subprocedure completion, not full physical teardown. No duration or timeout policy is enabled.

The 69 frozen CP05 ActionEvents still have `evidence_status: unknown`. CP12 does not promote them, run workflow traces, or produce process-compliance/anomaly metrics. Human review and a separately validated evidence policy remain required before real process interpretation. Factory SOP validity remains **NOT VALIDATED**.

## Checks and records

```powershell
.\.venv-cp05\Scripts\python.exe -m unittest discover -s tests -v
.\.venv-cp05\Scripts\python.exe -m compileall -q src tools tests demos
```

- CP05 frozen baseline: [experiment record](experiments/EXP-CP05.md)
- CP11 workflow specification: [experiment record](experiments/EXP-CP11.md)
- CP12 visual inference demo: [demo guide](demos/README.md) and [experiment record](experiments/EXP-CP12.md)
- Research corpus and project planning: `ResearchDocuments/`, `ROADMAP.md`, `SCOPEOFWORK.md`, `PROJECTREADINESSPACKAGE.md`, `CHECKSHEET.md`

Raw datasets, large features, checkpoints and generated media are kept out of the project repository unless a specific artifact is intentionally versioned.
