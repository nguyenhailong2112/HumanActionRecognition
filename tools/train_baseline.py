from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
import time
from pathlib import Path

import numpy as np
import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from human_action.config import load_config  # noqa: E402
from human_action.dataset import load_split  # noqa: E402
from human_action.metrics import action_metrics  # noqa: E402
from human_action.model import FramewiseBaseline, MSTCN, mstcn_loss  # noqa: E402
from human_action.pipeline import predict_features  # noqa: E402


def _normalize(sequences):
    joined = np.concatenate([sequence.features for sequence in sequences], axis=0)
    return joined.mean(axis=0).astype(np.float32), np.maximum(joined.std(axis=0), 1e-4).astype(np.float32)


def _class_weights(sequences, num_classes: int, device: torch.device) -> torch.Tensor:
    counts = np.zeros(num_classes, dtype=np.float64)
    for sequence in sequences:
        counts += np.bincount(sequence.labels, minlength=num_classes)
    weights = np.zeros_like(counts)
    present = counts > 0
    weights[present] = 1.0 / np.sqrt(counts[present])
    weights[present] /= weights[present].mean()
    return torch.as_tensor(weights, dtype=torch.float32, device=device)


def _new_model(config, kind: str, num_classes: int):
    model_cfg = config["model"]
    if kind == "mstcn":
        return MSTCN(int(model_cfg["input_dim"]), int(model_cfg["hidden_dim"]), int(model_cfg["layers"]), int(model_cfg["stages"]), num_classes, float(model_cfg["dropout"]))
    return FramewiseBaseline(int(model_cfg["input_dim"]), num_classes)


def train_one(config, config_path: Path, kind: str, checkpoint_path: Path, epochs: int, device: torch.device) -> dict:
    started_at = time.perf_counter()
    train_sequences = load_split(config, "train", config_path)
    val_sequences = load_split(config, "val", config_path)
    mean, std = _normalize(train_sequences)
    num_classes = len(config["actions"]["class_order"])
    model = _new_model(config, kind, num_classes).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(config["model"]["learning_rate"]), weight_decay=float(config["model"]["weight_decay"]))
    criterion = torch.nn.CrossEntropyLoss(weight=_class_weights(train_sequences, num_classes, device))
    val_criterion = torch.nn.CrossEntropyLoss()
    best_val = float("inf")
    best_epoch = 0
    history = []

    for epoch in range(1, epochs + 1):
        model.train()
        random.Random(int(config["seed"]) + epoch).shuffle(train_sequences)
        train_loss = 0.0
        for sequence in train_sequences:
            x_np = ((sequence.features - mean[None, :]) / std[None, :]).astype(np.float32)
            x = torch.from_numpy(x_np.T.copy()).unsqueeze(0).to(device)
            y = torch.from_numpy(sequence.labels.copy()).long().unsqueeze(0).to(device)
            optimizer.zero_grad(set_to_none=True)
            outputs = model(x)
            if kind == "mstcn":
                loss = mstcn_loss(outputs, y)
            else:
                loss = criterion(outputs[0], y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
            optimizer.step()
            train_loss += float(loss.detach().cpu())

        model.eval()
        val_loss = 0.0
        val_count = 0
        with torch.inference_mode():
            for sequence in val_sequences:
                x_np = ((sequence.features - mean[None, :]) / std[None, :]).astype(np.float32)
                x = torch.from_numpy(x_np.T.copy()).unsqueeze(0).to(device)
                y = torch.from_numpy(sequence.labels.copy()).long().unsqueeze(0).to(device)
                outputs = model(x)
                logits = outputs[-1] if kind == "mstcn" else outputs[0]
                # Do not apply train-derived inverse-frequency weights to validation:
                # absent train classes would receive zero weight and hide their errors.
                loss = val_criterion(logits, y)
                val_loss += float(loss.cpu())
                val_count += 1
        val_loss /= max(val_count, 1)
        epoch_row = {"epoch": epoch, "train_loss": train_loss / max(len(train_sequences), 1), "val_loss": val_loss}
        history.append(epoch_row)
        print(f"[{kind}] epoch {epoch:02d}/{epochs} train_loss={epoch_row['train_loss']:.5f} val_loss={val_loss:.5f}")
        if val_loss <= best_val:
            best_val, best_epoch = val_loss, epoch
            checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            torch.save({
                "model_kind": kind,
                "model_state_dict": model.state_dict(),
                "feature_mean": torch.as_tensor(mean),
                "feature_std": torch.as_tensor(std),
                "class_order": config["actions"]["class_order"],
                "model_config": config["model"],
                "best_epoch": best_epoch,
                "best_val_loss": best_val,
            }, checkpoint_path)
    return {"checkpoint": str(checkpoint_path), "best_epoch": best_epoch, "best_val_loss": best_val, "history": history, "train_seconds": time.perf_counter() - started_at, "train_videos": [item.video_id for item in train_sequences], "val_videos": [item.video_id for item in val_sequences]}


def evaluate_split(config, config_path, kind: str, checkpoint_path: Path, split: str, device: torch.device) -> list[dict]:
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=True)
    model = _new_model(config, kind, len(config["actions"]["class_order"])).to(device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    results = []
    with torch.inference_mode():
        for sequence in load_split(config, split, config_path):
            predicted, probabilities = predict_features(model, sequence.features, checkpoint["feature_mean"], checkpoint["feature_std"], device)
            results.append({"video_id": sequence.video_id, "metrics": action_metrics(sequence.labels, predicted, config["actions"]["class_order"]), "predicted": predicted, "probabilities": probabilities, "sequence": sequence})
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Train framewise and MS-TCN temporal baselines for CP01.")
    parser.add_argument("--config", default="configs/cp01.yaml")
    parser.add_argument("--epochs", type=int)
    parser.add_argument("--defer-test-eval", action="store_true", help="Keep final test evaluation separate from training and run it once after configuration freeze.")
    args = parser.parse_args()
    config_path = Path(args.config).resolve()
    config = load_config(config_path)
    seed = int(config["seed"])
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(min(8, torch.get_num_threads()))
    device = torch.device(config.get("runtime", {}).get("device", "cpu"))
    epochs = args.epochs or int(config["model"]["epochs"])
    train_report = {}
    for kind, key in (("framewise", "baseline_checkpoint"), ("mstcn", "checkpoint")):
        checkpoint = PROJECT_ROOT / config["model"][key]
        train_report[kind] = train_one(config, config_path, kind, checkpoint, epochs, device)
        train_report[kind]["test_evaluation"] = (
            "DEFERRED: run tools/evaluate.py once after training/configuration freeze"
            if args.defer_test_eval
            else [
                {"video_id": item["video_id"], "metrics": item["metrics"]}
                for item in evaluate_split(config, config_path, kind, checkpoint, "test", device)
            ]
        )
    output_dir = PROJECT_ROOT / config["evidence"]["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "training_report.json"
    config_bytes = config_path.read_bytes()
    if config.get("dataset", {}).get("source") == "impact_official_release":
        from human_action.impact_release import read_official_split
        protocol = config["dataset"]["official_split"]
        split_dir = PROJECT_ROOT / protocol["split_dir"]
        split_summary = {
            split: read_official_split(split_dir, int(protocol["split_id"]), split, protocol["procedure"], protocol["view"])
            for split in ("train", "val", "test")
        }
    else:
        split_summary = {
            split: list(config["dataset"]["splits"].get(split, []))
            for split in ("train", "val", "test")
        }
    training_report = {
        "experiment_id": config.get("experiment_id"),
        "dataset": config.get("dataset", {}).get("name"),
        "dataset_version": config.get("dataset", {}).get("version"),
        "feature_name": config.get("dataset", {}).get("feature_name", "handcrafted"),
        "official_split": config.get("dataset", {}).get("official_split"),
        "action_classes": config["actions"]["class_order"],
        "config_path": str(config_path),
        "config_sha256": hashlib.sha256(config_bytes).hexdigest(),
        "environment": {"python": sys.version, "pytorch": torch.__version__, "numpy": np.__version__, "device": str(device)},
        "split_video_ids": split_summary,
        "epochs_requested": epochs,
        "models": train_report,
    }
    report_path.write_text(json.dumps(training_report, indent=2), encoding="utf-8")
    print(f"[ok] training report: {report_path}")


if __name__ == "__main__":
    main()
