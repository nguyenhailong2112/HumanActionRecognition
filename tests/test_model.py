import unittest
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from human_action.model import FramewiseBaseline, MSTCN, mstcn_loss


class ModelTests(unittest.TestCase):
    def test_mstcn_preserves_temporal_length_and_refines(self):
        model = MSTCN(input_dim=8, hidden_dim=4, layers=2, stages=3, num_classes=5, dropout=0.0)
        features = torch.randn(1, 8, 17)
        outputs = model(features)
        self.assertEqual(tuple(outputs.shape), (3, 1, 5, 17))
        targets = torch.randint(0, 5, (1, 17))
        loss = mstcn_loss(outputs, targets)
        loss.backward()
        self.assertTrue(torch.isfinite(loss))

    def test_framewise_model_output_shape(self):
        model = FramewiseBaseline(8, 5)
        self.assertEqual(tuple(model(torch.randn(1, 8, 17)).shape), (1, 1, 5, 17))


if __name__ == "__main__":
    unittest.main()
