from __future__ import annotations

import copy

import torch
from torch import nn
from torch.nn import functional as F


class DilatedResidualLayer(nn.Module):
    def __init__(self, dilation: int, channels: int, dropout: float) -> None:
        super().__init__()
        self.conv_dilated = nn.Conv1d(channels, channels, kernel_size=3, padding=dilation, dilation=dilation)
        self.conv_1x1 = nn.Conv1d(channels, channels, kernel_size=1)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = self.conv_dilated(x)
        out = F.relu(out)
        out = self.conv_1x1(out)
        out = self.dropout(out)
        return x + out


class SingleStageTCN(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, layers: int, num_classes: int, dropout: float) -> None:
        super().__init__()
        self.input_projection = nn.Conv1d(input_dim, hidden_dim, kernel_size=1)
        self.layers = nn.ModuleList(
            [copy.deepcopy(DilatedResidualLayer(2**i, hidden_dim, dropout)) for i in range(layers)]
        )
        self.output_projection = nn.Conv1d(hidden_dim, num_classes, kernel_size=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = self.input_projection(x)
        for layer in self.layers:
            out = layer(out)
        return self.output_projection(out)


class MSTCN(nn.Module):
    """Classic MS-TCN: predict once, then refine class probabilities in later stages."""

    def __init__(self, input_dim: int, hidden_dim: int, layers: int, stages: int, num_classes: int, dropout: float) -> None:
        super().__init__()
        if stages < 1:
            raise ValueError("MS-TCN requires at least one stage")
        self.prediction = SingleStageTCN(input_dim, hidden_dim, layers, num_classes, dropout)
        self.refinements = nn.ModuleList(
            [SingleStageTCN(num_classes, hidden_dim, layers, num_classes, dropout) for _ in range(stages - 1)]
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = self.prediction(x)
        outputs = [out]
        for stage in self.refinements:
            out = stage(torch.softmax(out, dim=1))
            outputs.append(out)
        return torch.stack(outputs, dim=0)  # [stages, batch, classes, time]


class FramewiseBaseline(nn.Module):
    """Level-1 reference: independent linear classification at every sampled frame."""

    def __init__(self, input_dim: int, num_classes: int) -> None:
        super().__init__()
        self.classifier = nn.Conv1d(input_dim, num_classes, kernel_size=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(x).unsqueeze(0)


def mstcn_loss(outputs: torch.Tensor, targets: torch.Tensor, smoothing_weight: float = 0.15, ignore_index: int = -100) -> torch.Tensor:
    """Stagewise CE plus clipped temporal smoothing, matching the classic MS-TCN objective."""
    total = torch.zeros((), device=outputs.device)
    valid = targets != ignore_index
    for logits in outputs:
        ce = F.cross_entropy(logits, targets, ignore_index=ignore_index)
        log_prob = F.log_softmax(logits, dim=1)
        if logits.shape[-1] > 1:
            delta = log_prob[:, :, 1:] - log_prob.detach()[:, :, :-1]
            smooth = torch.clamp(delta.square(), max=16.0)
            pair_mask = (valid[:, 1:] & valid[:, :-1]).unsqueeze(1)
            smooth = (smooth * pair_mask).sum() / (pair_mask.sum() * logits.shape[1]).clamp_min(1)
        else:
            smooth = torch.zeros((), device=outputs.device)
        total = total + ce + smoothing_weight * smooth
    return total
