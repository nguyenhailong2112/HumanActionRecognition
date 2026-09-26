import sys
import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from human_action.evidence import attach_evidence  # noqa: E402
from human_action.schemas import Violation  # noqa: E402


class EvidenceTests(unittest.TestCase):
    def test_violation_snapshot_uses_event_frame_and_is_linked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            video = root / "fixture.mp4"
            writer = cv2.VideoWriter(str(video), cv2.VideoWriter_fourcc(*"mp4v"), 10.0, (64, 48))
            if not writer.isOpened():
                self.skipTest("OpenCV mp4v encoder unavailable")
            for frame in range(20):
                writer.write(np.full((48, 64, 3), frame * 10, dtype=np.uint8))
            writer.release()
            violation = Violation("W1", "proc", "B", "C", "WRONG_SEQUENCE", 1.2, 0.4, 0.9, "C observed before B", "fixture", 12)
            result = attach_evidence([violation], video, root / "out", 0.2, 10, False)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0].evidence_frame, 12)
            self.assertTrue(Path(result[0].evidence_image).is_file())
            self.assertIsNone(result[0].evidence_clip)


if __name__ == "__main__":
    unittest.main()
