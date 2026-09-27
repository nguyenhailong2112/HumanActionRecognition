from __future__ import annotations

import json
import hashlib
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCALARS = ("frame_accuracy", "macro_f1_actions", "normalized_edit_score")
SEGS = ("F1@10", "F1@25", "F1@50")


def main() -> None:
    cp05 = json.loads((ROOT / "experiments/CP06/action_metrics.json").read_text(encoding="utf-8"))
    per_seed = {}
    for seed in (17, 23, 41):
        if seed == 17:
            rows = cp05["per_execution"]
            report = json.loads((ROOT / "results/cp05/training_report.json").read_text(encoding="utf-8"))
        else:
            folder = ROOT / "results" / "cp06" / f"seed{seed}"
            rows = json.loads((folder / "evaluation/test_metrics.json").read_text(encoding="utf-8"))["results"]
            report = json.loads((folder / "training_report.json").read_text(encoding="utf-8"))
        model = report["models"]["mstcn"]
        metrics_by_video = {row["video_id"]: row["action"] for row in rows}
        vals = {m: [] for m in (*SCALARS, *SEGS)}
        for metric in metrics_by_video.values():
            for key in SCALARS:
                vals[key].append(float(metric[key]))
            for key in SEGS:
                vals[key].append(float(metric["segmental"][key]["f1"]))
        per_seed[str(seed)] = {
            "best_validation_epoch": model["best_epoch"],
            "best_validation_loss": model["best_val_loss"],
            "train_seconds": model["train_seconds"],
            "checkpoint": model["checkpoint"],
            "checkpoint_sha256": hashlib.sha256(Path(model["checkpoint"]).read_bytes()).hexdigest(),
            "final_checkpoint": model["final_checkpoint"],
            "final_checkpoint_sha256": hashlib.sha256(Path(model["final_checkpoint"]).read_bytes()).hexdigest(),
            "test_mean_per_execution": {key: statistics.mean(v) for key, v in vals.items()},
            "test_metrics_by_execution": {video: metrics for video, metrics in metrics_by_video.items()},
        }
    metric_keys = list(next(iter(per_seed.values()))["test_mean_per_execution"])
    across = {key: [per_seed[s]["test_mean_per_execution"][key] for s in per_seed] for key in metric_keys}
    result = {
        "protocol": "Frozen CP05 recipe, unchanged dataset/split/preprocessing/model/hyperparameters/schedule; test metrics are reporting only and did not select checkpoints.",
        "device": "cuda:0",
        "seed_17_source": "CP05 frozen run; reused as first repeatability seed",
        "new_training_seeds": [23, 41],
        "per_seed": per_seed,
        "across_seed_test_mean": {key: statistics.mean(values) for key, values in across.items()},
        "across_seed_test_sample_std": {key: statistics.stdev(values) for key, values in across.items()},
    }
    out = ROOT / "experiments/CP06/seed_reliability.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    logs = []
    for seed, row in per_seed.items():
        if int(seed) == 17:
            report = json.loads((ROOT / "results/cp05/training_report.json").read_text(encoding="utf-8"))
        else:
            report = json.loads((ROOT / "results/cp06" / f"seed{seed}" / "training_report.json").read_text(encoding="utf-8"))
        model = report["models"]["mstcn"]
        logs.append(f"seed={seed} best_epoch={model['best_epoch']} best_val_loss={model['best_val_loss']:.8f} device={report['environment']['device']}")
        logs.extend(f"epoch={item['epoch']} train_loss={item['train_loss']:.8f} val_loss={item['val_loss']:.8f}" for item in model["history"])
    (ROOT / "experiments/CP06/seed_training.log").write_text("\n".join(logs) + "\n", encoding="utf-8")
    print(f"[ok] seed reliability: {out}")


if __name__ == "__main__":
    main()
