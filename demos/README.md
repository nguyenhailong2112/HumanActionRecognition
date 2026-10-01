# CP12 Human Action inference demo

The demo runs the existing frozen MS-TCN implementation on official precomputed I3D features, decodes temporal action segments, converts non-background predictions to the repository's `ActionEvent` contract, and renders the source video with a prediction timeline. It does not train, tune, invoke the workflow engine, or produce process judgments.

## One execution

From the repository root in PowerShell:

```powershell
.\.venv-cp05\Scripts\python.exe demos\run_human_action_demo.py `
  --video 'D:\HaiLongRnD\Datasets\HumanActionRecognition\IMPACT\v1.1\videos\IMPACT-v1.1-videos-front\IMPACT-v1.1\videos\front\SS07EL13_Disassembly_A_001_front.mp4' `
  --features 'D:\HaiLongRnD\Datasets\HumanActionRecognition\IMPACT\v1.1\features\IMPACT-v1.1-features-I3D\IMPACT-v1.1\features\I3D\SS07EL13_Disassembly_A_001_front.npy' `
  --checkpoint models\cp05_mstcn_best.pt `
  --config configs\cp05.yaml `
  --output-dir results\cp12\SS07EL13_Disassembly_A_001_front
```

Use the equivalent paths for the other three IDs listed in the CP12 experiment record. The runner verifies that the video ID is in the configured official held-out test split.

## On-video information

- Predicted action and source time.
- Current segment start, end, duration and predicted-class mean softmax score.
- Full-execution color timeline with a playhead synchronized to source frame time.
- Execution ID, model/checkpoint identity, feature sequence size and sampling stride.
- Clear notice that scores are not calibrated evidence and the output is action inference only.

The original video remains visible behind a compact header. A timeline/details footer adds 178 pixels to output height. OpenCV writes video only; source audio is not copied.

## Outputs

Each execution directory contains:

- `demo_video.mp4`
- `prediction_segments.json` — all temporal segments, including NULL/background.
- `prediction_segments.csv` — same segment table.
- `action_events.json` — non-background `ActionEvent` records; evidence status remains `unknown`.
- `manifest.json` — exact input hashes, split membership, model/checkpoint/config provenance, timings, and output verification.

The source features must be official frame-aligned `T×1024` arrays with one row per decoded source frame. The runner samples them at the configured 5 FPS exactly as the existing release loader does. It refuses incompatible shapes, non-finite features, a video outside the frozen test split, timeline gaps near video end, and output frame/FPS mismatches.

Generated outputs go under ignored `results/`; large rendered videos should not be committed.
