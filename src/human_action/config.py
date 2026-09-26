from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    if not isinstance(config, dict):
        raise ValueError(f"Config must be a YAML mapping: {path}")
    return config


def project_path(config_path: str | Path, configured_path: str | Path) -> Path:
    """Resolve config paths from the project root, not the caller's CWD."""
    project_root = Path(config_path).resolve().parent.parent
    value = Path(configured_path)
    return value if value.is_absolute() else project_root / value
