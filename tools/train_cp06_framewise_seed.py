from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from human_action.config import load_config  # noqa: E402
from tools.train_baseline import train_one  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the paired CP06 FramewiseBaseline without touching CP05 checkpoints.")
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    config_path = ROOT / "configs" / f"cp06_seed{args.seed}.yaml"
    config = load_config(config_path)
    config["model"]["baseline_checkpoint"] = f"models/cp06_framewise_seed{args.seed}_best.pt"
    config["model"]["baseline_final_checkpoint"] = f"models/cp06_framewise_seed{args.seed}_final.pt"
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.set_num_threads(min(8, torch.get_num_threads()))
    device = torch.device(config["runtime"]["device"])
    report = train_one(config, config_path, "framewise", ROOT / config["model"]["baseline_checkpoint"], ROOT / config["model"]["baseline_final_checkpoint"], int(config["model"]["epochs"]), device)
    artifact = {"seed": args.seed, "run_config_snapshot": f"experiments/CP06/seeds/seed{args.seed}_run_config_as_executed.yaml", "trained_from_config": str(config_path), "artifact_paths": {key: report[key] for key in ("checkpoint", "final_checkpoint")}, "best_epoch": report["best_epoch"], "best_validation_loss": report["best_val_loss"], "train_seconds": report["train_seconds"], "history": report["history"]}
    for key in ("checkpoint", "final_checkpoint"):
        artifact[key + "_sha256"] = hashlib.sha256(Path(report[key]).read_bytes()).hexdigest()
    out = ROOT / "experiments/CP06/seeds" / f"seed{args.seed}_framewise_reproduction.json"
    out.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    print(f"[ok] saved separate Framewise seed-{args.seed} artifacts and report: {out}")


if __name__ == "__main__":
    main()
