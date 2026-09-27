from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class VideoRecord:
    video_id: str
    path: str
    annotation_path: str
    worker_id: str
    workflow_id: str
    split: str


@dataclass(frozen=True)
class FrameSample:
    frame_index: int
    timestamp: float
    feature: list[float]
    label: str


@dataclass(frozen=True)
class ActionSegment:
    action: str
    start_time: float
    end_time: float
    duration: float
    confidence: float
    start_frame: int
    end_frame: int


@dataclass(frozen=True)
class ActionEvent:
    worker_id: str
    action: str
    start_time: float
    end_time: float
    duration: float
    confidence: float
    video_id: str = ""
    start_frame: int = 0
    end_frame: int = 0
    evidence_status: str = "unknown"
    view: str = ""
    event_id: str = ""
    evidence_refs: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "ActionEvent":
        data = dict(value)
        if "evidence_refs" in data:
            data["evidence_refs"] = tuple(data["evidence_refs"])
        return cls(**data)


@dataclass(frozen=True)
class WorkflowState:
    workflow_id: str
    current_step_index: int
    current_step: str | None
    expected_step: str | None
    next_valid_steps: tuple[str, ...]
    selected_path: str | None
    completed: bool


@dataclass(frozen=True)
class Violation:
    worker_id: str
    workflow: str
    expected_step: str | None
    observed_action: str | None
    violation_type: str
    timestamp: float
    duration: float | None
    confidence: float
    reason: str
    video_id: str = ""
    evidence_frame: int | None = None
    evidence_image: str | None = None
    evidence_clip: str | None = None


def to_dict(value: Any) -> dict[str, Any]:
    return asdict(value)
