import torch
import torch.nn as nn

class Integrator(nn.Module):
    def __init__(self, artifact_dim=8):
        super().__init__()
        self.weights = nn.ParameterDict()
        self.artifact_dim = artifact_dim

    def register_agent(self, agent_name):
        self.weights[agent_name] = nn.Parameter(
            torch.randn(self.artifact_dim, self.artifact_dim) * 0.1
        )

    def forward(self, blackboard, batch_size):
        artifact = torch.zeros(batch_size, self.artifact_dim)

        for agent_name, output in blackboard.read_all().items():
            artifact = artifact + output @ self.weights[agent_name].T

        return artifact
