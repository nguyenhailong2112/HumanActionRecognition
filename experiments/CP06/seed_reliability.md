# CP06 MS-TCN Seed Reliability

Frozen CP05 recipe, unchanged dataset/split/preprocessing/model/hyperparameters/schedule; test metrics are reporting only and did not select checkpoints.

Seed 17 is the frozen CP05 run; seeds 23 and 41 were newly trained with identical recipe and validation-only best-checkpoint selection. Test metrics below were only reported, never used for tuning.

| Seed | Best val epoch | Best val loss | Train sec | Accuracy | Macro-F1 | Edit | F1@10 | F1@25 | F1@50 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 17 | 11 | 1.2703 | 31.5 | 0.569 | 0.390 | 50.39 | 0.445 | 0.445 | 0.207 |
| 23 | 11 | 1.5317 | 12.2 | 0.574 | 0.405 | 46.48 | 0.488 | 0.421 | 0.330 |
| 41 | 6 | 1.2537 | 12.2 | 0.550 | 0.310 | 32.30 | 0.357 | 0.318 | 0.215 |

| Metric | Mean across seed-level test means | Sample SD across seeds |
|---|---:|---:|
| frame_accuracy | 0.5645 | 0.0125 |
| macro_f1_actions | 0.3684 | 0.0509 |
| normalized_edit_score | 43.0549 | 9.5196 |
| F1@10 | 0.4302 | 0.0670 |
| F1@25 | 0.3947 | 0.0676 |
| F1@50 | 0.2506 | 0.0687 |

Complete per-execution metrics for all three seeds are in `seed_reliability.json`. New checkpoints: `models/cp06_mstcn_seed23_best.pt`, `models/cp06_mstcn_seed23_final.pt`, and corresponding seed41 files. Configs are `configs/cp06_seed23.yaml` and `configs/cp06_seed41.yaml`; training reports retain every epoch's train/validation loss and separate test outputs. Framewise runs were also executed by the existing paired trainer for these seeds; the reliability comparison here is MS-TCN only.
