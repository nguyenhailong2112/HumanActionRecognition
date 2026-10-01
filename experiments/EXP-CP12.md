# EXP-CP12 — Human Action Inference Demo v1

**Status: READY.** Frozen action inference and visual output were locally executed on all four held-out executions. CP12 does not evaluate workflow compliance or factory process performance.

## Objective

Show the frozen Human Action prediction pipeline on real held-out IMPACT test videos:

`source video + official precomputed I3D -> frozen MS-TCN -> temporal predictions -> ActionEvents + synchronized video overlay + provenance`

This is an inference demo, not a model-improvement or compliance experiment.

## Frozen model and protocol

- Model: repository `MSTCN`, **our MS-TCN baseline on IMPACT**.
- Checkpoint: `models/cp05_mstcn_best.pt`; CP05 seed 17, selected by validation loss. SHA-256: `2e1f06a248973dad925f449ad9588064bbade4f9c2f4ed9c961a5196008f567d`.
- Config: `configs/cp05.yaml`; SHA-256: `bb6052d1b90d6c69466e5b838f36cb8d5d7453dc476bb5b399df1afbf291f2fa`.
- Dataset: IMPACT v1.1, TAS-S, official S2 split 2; `Disassembly_A`, front; 39 train / 5 validation / 4 held-out test. Test worker: `SS07EL13`.
- No training, fine-tuning, test tuning, class remapping, split change, checkpoint replacement or historical metric regeneration occurred.

## Inputs and outputs

The four test inputs were independently resolved from the official split and verified against external source media and I3D arrays:

| Execution | Source frames @ FPS | Official I3D raw -> sampled rows | Predicted segments | Non-background ActionEvents | Inference / render seconds | Verified rendered video |
|---|---:|---:|---:|---:|---:|---|
| `SS07EL13_Disassembly_A_001_front` | 6756 @ 30 | 6756x1024 -> 1126x1024 | 35 | 24 | 0.200 / 72.9 | 6756 frames, 30 FPS, 1280x898 |
| `SS07EL13_Disassembly_A_002_front` | 3939 @ 30 | 3939x1024 -> 657x1024 | 23 | 18 | 0.177 / 44.6 | 3939 frames, 30 FPS, 1280x898 |
| `SS07EL13_Disassembly_A_003_front` | 4040 @ 30 | 4040x1024 -> 674x1024 | 17 | 13 | 0.173 / 46.9 | 4040 frames, 30 FPS, 1280x898 |
| `SS07EL13_Disassembly_A_004_front` | 3543 @ 30 | 3543x1024 -> 591x1024 | 19 | 14 | 0.181 / 41.7 | 3543 frames, 30 FPS, 1280x898 |

The feature arrays contain one row per decoded source frame. CP05's configured sample rate (5 FPS) and existing loader convention select every sixth row. Full feature arrays were checked for shape and finite numeric values. The renderer decodes every input frame and every output frame; output counts and FPS match their sources.

Each local execution directory under `results/cp12/<execution_id>/` contains:

- `demo_video.mp4` — source video with readable action/time/segment/score/model overlay and full predicted-action timeline.
- `prediction_segments.json` and `prediction_segments.csv` — temporally ordered segments, including NULL/background, with model and input provenance.
- `action_events.json` — non-background events using the existing `ActionEvent` contract.
- `manifest.json` — exact input paths/hashes, split membership, checkpoint/config hashes, timings, output size/hash and decode verification.

Aggregate machine-readable execution record: `experiments/CP12/demo_manifest.json`. The rendered videos occupy approximately 388 MB locally and remain under ignored `results/`; they are not committed to Git.

## On-video display

The prediction-only overlay shows the current predicted action, source time, current segment start/end/duration, predicted-class mean softmax score, execution/frame, model/checkpoint identity, I3D sequence dimensions/sample rate/stride, and a full-duration segment timeline with a synchronized playhead. The prediction timeline colors are class-coded; the current segment is outlined. CP12 displays no workflow, compliance, mistake or anomaly judgment.

The confidence field is derived from model probabilities but is uncalibrated and is not evidence sufficiency. ActionEvent evidence status remains `unknown`. OpenCV's video-only writer does not copy source audio.

## Exact command used to reproduce all four

Run from the project root in PowerShell:

```powershell
$videoRoot = 'D:\HaiLongRnD\Datasets\HumanActionRecognition\IMPACT\v1.1\videos\IMPACT-v1.1-videos-front\IMPACT-v1.1\videos\front'
$featureRoot = 'D:\HaiLongRnD\Datasets\HumanActionRecognition\IMPACT\v1.1\features\IMPACT-v1.1-features-I3D\IMPACT-v1.1\features\I3D'
$ids = @('SS07EL13_Disassembly_A_001_front','SS07EL13_Disassembly_A_002_front','SS07EL13_Disassembly_A_003_front','SS07EL13_Disassembly_A_004_front')
foreach ($id in $ids) {
  & .venv-cp05\Scripts\python.exe demos\run_human_action_demo.py --video (Join-Path $videoRoot ($id + '.mp4')) --features (Join-Path $featureRoot ($id + '.npy')) --checkpoint models\cp05_mstcn_best.pt --config configs\cp05.yaml --output-dir (Join-Path 'results\cp12' $id)
  if ($LASTEXITCODE -ne 0) { throw "CP12 demo failed for $id" }
}
```

## Verification status

| Category | Result |
|---|---|
| SOURCE-VERIFIED | Frozen split membership/counts, worker, source-video existence/metadata, official feature file existence/shape and external-data paths checked against repository config and official split bundles. |
| CODE-VERIFIED | CLI reuses existing checkpoint loader, model factory, prediction path, temporal decoder and ActionEvent conversion; feature/frame alignment, class labels, interval order, timeline coverage, source/output FPS and decoded frame counts are guarded. |
| TEST-VERIFIED | `.venv-cp05\Scripts\python.exe -m unittest discover -s tests -v` — **89 passed**. CP12 adds deterministic timeline/frame boundary tests. |
| TEST-VERIFIED | `.venv-cp05\Scripts\python.exe -m compileall -q src tools tests demos` — passed. |
| LOCALLY-EXECUTED | All 4 frozen held-out inputs ran on CUDA. All 4 overlay videos reopened and fully decoded with matching source frame count/FPS. JSON, CSV, ActionEvents and individual manifests exist for every execution. A rendered frame from execution 002 was visually inspected for readability and synchronization. |
| CI-VERIFIED | Not claimed; GitHub CI was not checked. |
| NOT-EVALUATED | Prediction correctness against GT, new aggregate action metrics, visual semantic correctness of every predicted event, process compliance/anomaly performance, workflow integration and streaming latency. |

## Preservation and limitations

- CP05/CP06 checkpoints, historical metrics/prediction artifacts, model class order and official split are unchanged.
- CP11 workflow config/semantics were not invoked or changed in CP12. README/checksheet wording and the requested CP11 action-count correction are documentation-only cleanup.
- `.idea/vcs.xml` was restored to its CP10-parent contents; no unrelated IDE mapping change is included.
- The demo consumes cached 30 FPS-aligned I3D and is an offline, full-sequence inference/rendering pipeline. It does not include video feature extraction, audio, streaming latency or runtime compliance.
- Showing a prediction does not establish that it is correct. Process interpretation remains outside the demo.
