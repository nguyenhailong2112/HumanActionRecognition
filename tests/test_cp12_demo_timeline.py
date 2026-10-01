import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "demos"))

from run_human_action_demo import _validate_segments, frame_to_segment_index, segment_index_at_time
from human_action.schemas import ActionSegment


class CP12DemoTimelineTests(unittest.TestCase):
    def setUp(self):
        self.segments = [
            {"action": "NULL", "start_time": 0.0, "end_time": 1.0},
            {"action": "PICK", "start_time": 1.0, "end_time": 2.5},
            {"action": "PLACE", "start_time": 2.5, "end_time": 4.0},
        ]

    def test_frame_time_uses_half_open_segments_and_exact_boundaries(self):
        self.assertEqual(frame_to_segment_index(0, 30.0, self.segments), 0)
        self.assertEqual(frame_to_segment_index(29, 30.0, self.segments), 0)
        self.assertEqual(frame_to_segment_index(30, 30.0, self.segments), 1)
        self.assertEqual(frame_to_segment_index(75, 30.0, self.segments), 2)
        self.assertIsNone(frame_to_segment_index(120, 30.0, self.segments))

    def test_invalid_frame_or_timestamp_has_no_segment(self):
        self.assertIsNone(frame_to_segment_index(-1, 30.0, self.segments))
        self.assertIsNone(frame_to_segment_index(5, 0.0, self.segments))
        self.assertIsNone(segment_index_at_time(float("nan"), self.segments))

    def test_segment_validation_clamps_end_to_video_duration_and_checks_class(self):
        decoded = [ActionSegment("PICK", 0.0, 1.2, 1.2, .8, 0, 29)]
        rows = _validate_segments(decoded, ["NULL", "PICK"], frame_count=30, fps=30.0)
        self.assertEqual(rows[0]["end_time"], 1.0)
        self.assertEqual(rows[0]["duration"], 1.0)
        with self.assertRaisesRegex(ValueError, "outside configured model vocabulary"):
            _validate_segments([ActionSegment("UNKNOWN", 0, 1, 1, .8, 0, 20)],
                               ["NULL", "PICK"], 30, 30.0)

    def test_segment_validation_rejects_negative_time_and_invalid_score(self):
        with self.assertRaisesRegex(ValueError, "Invalid predicted segment interval"):
            _validate_segments([ActionSegment("PICK", -0.1, .5, .6, .8, 0, 10)],
                               ["NULL", "PICK"], 30, 30.0)
        with self.assertRaisesRegex(ValueError, "Invalid model score"):
            _validate_segments([ActionSegment("PICK", 0, .5, .5, 1.1, 0, 10)],
                               ["NULL", "PICK"], 30, 30.0)


if __name__ == "__main__":
    unittest.main()
