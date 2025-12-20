import torch
import torch.nn as nn
import random
import time
from agent import Agent
from blackboard import Blackboard
from integrator import Integrator

class PCNModel(nn.Module):
    def __init__(self, num_agents=3):
        super().__init__()

        self.agents = nn.ModuleList([
            Agent(name=f"agent_{i}") for i in range(num_agents)
        ])

        self.integrator = Integrator(artifact_dim=8)
        for agent in self.agents:
            self.integrator.register_agent(agent.name)

        self.head = nn.Linear(8, 1)

    def forward(self, x):
        batch_size = x.size(0)
        blackboard = Blackboard()

        # Simulated asynchronous completion
        delays = [random.random() for _ in self.agents]
        execution_order = sorted(range(len(self.agents)), key=lambda i: delays[i])

        for i in execution_order:
            agent = self.agents[i]
            y = agent(x)
            blackboard.write(agent.name, y)

        artifact = self.integrator(blackboard, batch_size)
        return self.head(artifact)

    def forward_with_trace(self, x):
        batch_size = x.size(0)
        blackboard = Blackboard()

        trace = []  # (time, artifact)
        t0 = time.perf_counter()
    # Simulated heterogeneous compute delays (seconds)
        delays = [0.2, 0.6, 1.0]

    # Fixed execution order, different completion times
        execution_order = list(range(len(self.agents)))

        for i in execution_order:
            agent = self.agents[i]
            time.sleep(delays[i])

        # Agent finishes and writes result
            y = agent(x)
            blackboard.write(agent.name, y)

        # Integrator reacts immediately
            artifact = self.integrator(blackboard, batch_size)

        # Record wall-clock time
            t = time.perf_counter() - t0
            trace.append((t, artifact.detach()))

        return trace