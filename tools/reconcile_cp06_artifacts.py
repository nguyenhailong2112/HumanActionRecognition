from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    summary = []
    for seed in (23, 41):
        seed_dir = ROOT / "experiments/CP06/seeds"
        cfg_snapshot = seed_dir / f"seed{seed}_run_config_as_executed.yaml"
        cfg_hash = hashlib.sha256(cfg_snapshot.read_bytes()).hexdigest()
        report_path = ROOT / "results/cp06" / f"seed{seed}" / "training_report.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        if cfg_hash != report["config_sha256"]:
            raise RuntimeError(f"seed {seed} archived config does not match executed config hash")
        best = ROOT / f"models/cp06_framewise_seed{seed}_best.pt"
        final = ROOT / f"models/cp06_framewise_seed{seed}_final.pt"
        if not best.is_file() or not final.is_file():
            raise RuntimeError(f"seed {seed} Framewise checkpoint/final artifact missing")
        report["executed_config_path_original"] = report.get("config_path")
        report["config_path"] = str(cfg_snapshot)
        report["run_config_snapshot"] = f"experiments/CP06/seeds/{cfg_snapshot.name}"
        report["models"]["framewise"]["checkpoint"] = str(best)
        report["models"]["framewise"]["final_checkpoint"] = str(final)
        report["models"]["framewise"]["artifact_copy_note"] = "CP06 paired-run Framewise checkpoints are stored under CP06-specific paths; seed 41 was copied before reproducing and restoring the CP05 seed-17 checkpoint."
        out = seed_dir / f"seed{seed}_training_report.json"
        out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        # Rewrite the convenience configs to safe distinct output paths. The exact
        # as-executed config remains in seed_dir and its hash remains in report.
        cfg_path = ROOT / "configs" / f"cp06_seed{seed}.yaml"
        config = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
        config["model"]["baseline_checkpoint"] = f"models/cp06_framewise_seed{seed}_best.pt"
        config["model"]["baseline_final_checkpoint"] = f"models/cp06_framewise_seed{seed}_final.pt"
        cfg_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
        (ROOT / "results/cp06" / f"seed{seed}" / "training_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        summary.append({"seed": seed, "executed_config_sha256": cfg_hash, "current_rerun_config_sha256": hashlib.sha256(cfg_path.read_bytes()).hexdigest(), "framewise_best": str(best), "framewise_best_sha256": hashlib.sha256(best.read_bytes()).hexdigest(), "framewise_final": str(final), "framewise_final_sha256": hashlib.sha256(final.read_bytes()).hexdigest()})
    (ROOT / "experiments/CP06/artifact_reconciliation.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("[ok] CP06 paired-run Framewise artifacts are isolated from CP05 paths; executed configs preserved and hash-checked")


if __name__ == "__main__":
    main()
