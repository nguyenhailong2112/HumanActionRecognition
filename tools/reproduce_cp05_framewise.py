from __future__ import annotations

import json
import hashlib
import random
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from human_action.config import load_config  # noqa: E402
from human_action.dataset import load_split  # noqa: E402
from human_action.pipeline import evaluate_video  # noqa: E402
from tools.train_baseline import train_one  # noqa: E402


def deep_equal(left, right) -> bool:
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(deep_equal(left[key], right[key]) for key in left)
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(deep_equal(a, b) for a, b in zip(left, right))
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return bool(np.isclose(left, right, atol=1e-8, rtol=0))
    return left == right


def main() -> None:
    config_path = ROOT / "configs/cp05.yaml"
    config = load_config(config_path)
    previous_report = json.loads((ROOT / "results/cp05/training_report.json").read_text(encoding="utf-8"))
    old_eval = json.loads((ROOT / "results/cp05/evaluation/test_metrics.json").read_text(encoding="utf-8"))
    seed = int(config["seed"])
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(min(8, torch.get_num_threads()))
    device = torch.device(config["runtime"]["device"])
    model = train_one(config, config_path, "framewise", ROOT / config["model"]["baseline_checkpoint"], ROOT / config["model"]["baseline_final_checkpoint"], int(config["model"]["epochs"]), device)
    val_expected = previous_report["models"]["framewise"]
    train_match = model["best_epoch"] == val_expected["best_epoch"] and abs(model["best_val_loss"] - val_expected["best_val_loss"]) < 1e-6
    final_val_match = abs(model["history"][-1]["val_loss"] - val_expected["history"][-1]["val_loss"]) < 1e-6
    results = []
    prior = {(r["video_id"], r["model"]): r["action"] for r in old_eval["results"]}
    predictions_match = True
    for seq in load_split(config, "test", config_path):
        item = evaluate_video(seq.video_id, "test", config, config_path, "framewise")
        reference = prior[(seq.video_id, "framewise")]
        match = deep_equal(item["action"], reference)
        predictions_match &= bool(match)
        results.append({"video_id": seq.video_id, "metrics_match_stored_cp05": bool(match), "action": item["action"]})
    best_path = ROOT / config["model"]["baseline_checkpoint"]
    final_path = ROOT / config["model"]["baseline_final_checkpoint"]
    artifact = {"purpose": "Reproduce overwritten local CP05 seed-17 FramewiseBaseline checkpoint from frozen CP05 config; comparison is to prior validation record and held-out stored CP05 metrics.", "seed": seed, "device": str(device), "best_epoch": model["best_epoch"], "best_validation_loss": model["best_val_loss"], "final_validation_loss": model["history"][-1]["val_loss"], "stored_cp05_best_epoch": val_expected["best_epoch"], "stored_cp05_best_validation_loss": val_expected["best_val_loss"], "stored_cp05_final_validation_loss": val_expected["history"][-1]["val_loss"], "checkpoint": str(best_path), "checkpoint_sha256": hashlib.sha256(best_path.read_bytes()).hexdigest(), "final_checkpoint": str(final_path), "final_checkpoint_sha256": hashlib.sha256(final_path.read_bytes()).hexdigest(), "validation_match": bool(train_match), "final_validation_match": bool(final_val_match), "test_metrics_match_stored_cp05": bool(predictions_match), "test_results": results}
    artifact["status"] = "REPRODUCED" if train_match and final_val_match and predictions_match else "REPRODUCTION_MISMATCH"
    out = ROOT / "experiments/CP06/cp05_framewise_reproduction.json"
    out.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    print(json.dumps({k: artifact[k] for k in ("status", "validation_match", "final_validation_match", "test_metrics_match_stored_cp05", "best_epoch", "best_validation_loss")}, indent=2))
    if artifact["status"] != "REPRODUCED":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
