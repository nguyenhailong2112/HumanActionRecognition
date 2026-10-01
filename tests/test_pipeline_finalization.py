import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from human_action import pipeline
from human_action.schemas import ActionEvent


class PipelineFinalizationTests(unittest.TestCase):
    def test_video_eof_is_passed_as_observation_end_in_both_pipeline_paths(self):
        video_id = "exec-1"
        event = ActionEvent("W1", "A", 0, 1, 1, .9, video_id, 0, 29, "sufficient")
        sequence = SimpleNamespace(
            features=np.zeros((1, 2), dtype=np.float32),
            labels=np.array([1]),
            timestamps=np.array([0.0]),
            frame_indices=np.array([0]),
            fps=30.0,
            frame_count=30,
            worker_id="W1",
            video_path=Path("fixture.mp4"),
        )
        config = {
            "workflow": {
                "id": "toy",
                "enabled": True,
                "status": "HUMAN_VALIDATED",
                "valid_paths": [{"id": "route", "steps": ["A", "B"]}],
                "duration_limits_seconds": {},
            },
            "actions": {"class_order": ["NULL", "A"], "background": "NULL"},
            "dataset": {"view": "front"},
            "temporal": {"smoothing_window": 1, "min_segment_seconds": 0.0},
        }

        with (
            patch.object(pipeline, "load_sequence", return_value=sequence),
            patch.object(pipeline, "load_checkpoint", return_value=(object(), np.zeros(2), np.ones(2), pipeline.torch.device("cpu"), "fixture.pt")),
            patch.object(pipeline, "predict_features", return_value=(np.array([1]), np.array([[.1, .9]]))),
            patch.object(pipeline, "decode_segments", return_value=[]),
            patch.object(pipeline, "to_action_events", return_value=[event]),
            patch.object(pipeline, "action_metrics", return_value={}),
            patch.object(pipeline, "mapped_sequence", return_value=[]),
        ):
            evaluated = pipeline.evaluate_video(video_id, "test", config, "config.yaml", "mstcn")
            predicted = pipeline.predict_video(Path("fixture.mp4"), video_id, "W1", config, "config.yaml", "mstcn")

        self.assertEqual(evaluated["process"]["finalization_status"], "observation_ended_unconfirmed")
        self.assertNotIn("INCOMPLETE_PROCEDURE", [row["violation_type"] for row in evaluated["process"]["predicted_violations"]])
        self.assertEqual(predicted["workflow_finalization_status"], "observation_ended_unconfirmed")
        self.assertNotIn("INCOMPLETE_PROCEDURE", [row.violation_type for row in predicted["violations"]])


if __name__ == "__main__":
    unittest.main()
