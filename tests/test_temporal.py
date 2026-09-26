import unittest
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from human_action.temporal import decode_segments, merge_short_segments, smooth_labels, temporal_windows


class TemporalTests(unittest.TestCase):
    def test_windows_cover_full_sequence(self):
        windows = temporal_windows(11, 5, 4)
        self.assertEqual(windows[0], (0, 5))
        self.assertEqual(windows[-1], (6, 11))

    def test_temporal_smoothing_removes_single_frame_flicker(self):
        labels = np.array([1, 1, 0, 1, 1])
        self.assertEqual(smooth_labels(labels, 3).tolist(), [1, 1, 1, 1, 1])

    def test_short_segment_is_merged(self):
        labels = np.array([1, 1, 2, 1, 1])
        self.assertEqual(merge_short_segments(labels, 2).tolist(), [1, 1, 1, 1, 1])

    def test_decode_returns_timestamps_duration_and_confidence(self):
        labels = np.array([0, 1, 1, 0])
        probs = np.zeros((4, 2), dtype=np.float32)
        probs[:, 0] = 0.2
        probs[1:3, 1] = 0.9
        segments = decode_segments(labels, probs, ["NULL", "PICK"], np.array([0.0, 0.2, 0.4, 0.6]), np.array([0, 6, 12, 18]), 1, 0.0)
        pick = next(item for item in segments if item.action == "PICK")
        self.assertAlmostEqual(pick.start_time, 0.2)
        self.assertAlmostEqual(pick.duration, 0.4)
        self.assertGreater(pick.confidence, 0.8)


if __name__ == "__main__":
    unittest.main()
