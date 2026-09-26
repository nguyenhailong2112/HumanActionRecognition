# Human Action & Procedure Understanding — CP01

CP01 is an executable research slice for one fixed IMPACT camera view. It extracts a compact, deterministic RGB/colour/motion descriptor, compares an independent framewise classifier with a classic multi-stage temporal convolutional network (MS-TCN), decodes temporal segments to action events, evaluates configured procedure paths, and exports violation evidence and GT/prediction timelines.

## Environment and data

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe tools\prepare_data.py
```

The official IMPACT v1.1 quick-start sample is used (three executions, `front` view). Its source data is published for non-commercial research/education use under CC BY-NC-SA 4.0. Do not use this release commercially without checking the official terms. The archive stays under ignored `data/raw`; extracted data and feature caches are also ignored.

```powershell
.\.venv\Scripts\python.exe tools\inspect_dataset.py --config configs\cp01.yaml --split train
.\.venv\Scripts\python.exe tools\train_baseline.py --config configs\cp01.yaml
.\.venv\Scripts\python.exe tools\evaluate.py --config configs\cp01.yaml --split test --model both
.\.venv\Scripts\python.exe run_pipeline.py --config configs\cp01.yaml --input data/processed/impact/v1.1/IMPACT-v1.1/sample/videos/front/ER07AD15_Disassembly_A_001_front.mp4 --video-id ER07AD15_Disassembly_A_001_front --model framewise
```

The split contains one training trial, one cross-procedure validation trial, and one held-out-worker disassembly test trial. This intentionally exercises the full data flow but is too small and mismatched to support a useful performance claim. See [EXP-CP01](experiments/EXP-CP01.md) before interpreting metrics. Action labels are coarse groups collapsed from the official TAS-S dense annotations; the `NULL` background is retained for frame-level training and omitted from event streams.

## Layout

- `src/human_action/`: data loading, features, MS-TCN, temporal decoding, workflow, evidence, metrics.
- `configs/cp01.yaml`: paths, action mapping, model, temporal and procedure thresholds.
- `tools/`: dataset preparation/inspection, training and evaluation.
- `run_pipeline.py`: one-command video to result/evidence demo.
- `tests/`: deterministic logic checks (`python -m unittest discover -s tests -v`).
- `results/cp01/`: local run products; ignored by Git.

The handcrafted appearance features and models run offline on CPU. Runtime/FPS and industrial deployment performance have NOT been benchmarked.
