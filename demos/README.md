# CP01 demo

The end-to-end video entry point is `run_pipeline.py` at the project root. Example:

```powershell
.\.venv\Scripts\python.exe run_pipeline.py --config configs/cp01.yaml --input data/processed/impact/v1.1/IMPACT-v1.1/sample/videos/front/ER07AD15_Disassembly_A_001_front.mp4 --video-id ER07AD15_Disassembly_A_001_front --model framewise
```

The result JSON, evidence snapshots/clips and timeline are written under ignored `results/cp01/` by default. This demo verifies pipeline execution only; current action and workflow predictions are not valid compliance decisions.
