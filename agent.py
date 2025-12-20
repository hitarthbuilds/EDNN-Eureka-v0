import torch
import torch.nn as nn

class Agent(nn.Module):
    def __init__(self, input_dim=20, hidden_dim=32, output_dim=8, name="agent"):
        super().__init__()
        self.name = name
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x):
        return self.net(x)
