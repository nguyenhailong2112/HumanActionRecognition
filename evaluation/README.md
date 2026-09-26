# CP01 evaluation entry

Run the action and process output evaluator with:

```powershell
.\.venv\Scripts\python.exe tools\evaluate.py --config configs\cp01.yaml --split test --model both
```

Metric implementation is in `src/human_action/metrics.py`; reports and GT-vs-prediction timelines are written to ignored `results/cp01/evaluation/`. Process anomaly precision/recall is explicitly NOT EVALUATED until violation ground truth is available.
