"""
AIShard: Torch-based neuro-symbolic shard.
"""

import torch
import torch.nn as nn

class AIShard(nn.Module):
    """
    Basic linear shard with guards for bounded reality.
    """
    def __init__(self, input_dim: int, output_dim: int):
        super().__init__()
        self.linear = nn.Linear(input_dim, output_dim)
        self.guard = lambda x: torch.clamp(x, -1.0, 1.0)  # Bounded reality

    def forward(self, x):
        out = self.linear(x)
        return self.guard(out)