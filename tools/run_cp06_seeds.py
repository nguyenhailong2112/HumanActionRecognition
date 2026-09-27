from __future__ import annotations

import argparse
import copy
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Repeat the frozen CP05 MS-TCN recipe with new random seeds.")
    parser.add_argument("--seeds", nargs="+", type=int, default=[23, 41])
    args = parser.parse_args()
    base = yaml.safe_load((ROOT / "configs/cp05.yaml").read_text(encoding="utf-8"))
    for seed in args.seeds:
        config = copy.deepcopy(base)
        config["experiment_id"] = f"EXP-CP06-seed{seed}"
        config["seed"] = seed
        config["model"]["seed"] = seed
        config["model"]["checkpoint"] = f"models/cp06_mstcn_seed{seed}_best.pt"
        config["model"]["final_checkpoint"] = f"models/cp06_mstcn_seed{seed}_final.pt"
        config["model"]["baseline_checkpoint"] = f"models/cp06_framewise_seed{seed}_best.pt"
        config["model"]["baseline_final_checkpoint"] = f"models/cp06_framewise_seed{seed}_final.pt"
        config["evidence"]["output_dir"] = f"results/cp06/seed{seed}"
        config_path = ROOT / "configs" / f"cp06_seed{seed}.yaml"
        config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
        subprocess.run([sys.executable, str(ROOT / "tools/train_baseline.py"), "--config", str(config_path), "--defer-test-eval"], cwd=ROOT, check=True)
        subprocess.run([sys.executable, str(ROOT / "tools/evaluate.py"), "--config", str(config_path), "--split", "test", "--model", "mstcn"], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
