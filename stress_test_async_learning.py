import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
import matplotlib.pyplot as plt
from main import PCNModel

# -----------------------------
# Reproducibility
# -----------------------------
def set_seed(seed):
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)

# -----------------------------
# Synthetic Task (ASAT)
# -----------------------------
def generate_batch(batch_size=64, seq_len=20, k=5):
    x = torch.rand(batch_size, seq_len) * 2 - 1
    y = x[:, -k:].sum(dim=1, keepdim=True)
    return x, y

# -----------------------------
# Module Definition
# -----------------------------
class Module(nn.Module):
    def __init__(self, input_dim=20, hidden_dim=32, output_dim=8):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x):
        return self.net(x)

# -----------------------------
# Event-Driven Model
# -----------------------------
class AsyncEventDrivenModel(nn.Module):
    def __init__(self, num_modules=3):
        super().__init__()
        self.modules_list = nn.ModuleList([Module() for _ in range(num_modules)])
        self.integrator_weights = nn.ParameterList(
            [nn.Parameter(torch.randn(8, 8) * 0.1) for _ in range(num_modules)]
        )
        self.head = nn.Linear(8, 1)

    def forward(self, x):
        batch_size = x.size(0)
        artifact = torch.zeros(batch_size, 8)

        # Simulated asynchronous completion times
        delays = [random.random() for _ in range(len(self.modules_list))]
        execution_order = sorted(range(len(delays)), key=lambda i: delays[i])

        # Event-driven integration
        for i in execution_order:
            y_i = self.modules_list[i](x)
            artifact = artifact + y_i @ self.integrator_weights[i].T

        return self.head(artifact)

# -----------------------------
# Training Loop
# -----------------------------
def run_training(seed, steps=5000):
    set_seed(seed)
    model = PCNModel(num_agents=3)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.MSELoss()

    losses = []

    for step in range(steps):
        x, y = generate_batch()
        y_hat = model(x)
        loss = loss_fn(y_hat, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        losses.append(loss.item())

        if step % 500 == 0:
            print(f"[seed {seed}] step {step} | loss {loss.item():.4f}")

    return np.array(losses)

# -----------------------------
# Multi-Seed Stress Test
# -----------------------------
def stress_test(num_seeds=5, steps=5000):
    all_losses = []

    for seed in range(num_seeds):
        print(f"\n=== Running seed {seed} ===")
        losses = run_training(seed, steps)
        all_losses.append(losses)

    return np.stack(all_losses)

# -----------------------------
# Plotting
# -----------------------------
def plot_results(all_losses):
    mean = all_losses.mean(axis=0)
    std = all_losses.std(axis=0)

    plt.figure(figsize=(8, 5))
    plt.plot(mean, label="Mean Loss")
    plt.fill_between(
        range(len(mean)),
        mean - std,
        mean + std,
        alpha=0.3,
        label="±1 std",
    )
    plt.xlabel("Training Step")
    plt.ylabel("MSE Loss")
    plt.title("Asynchronous Learning Stress Test")
    plt.legend()
    plt.tight_layout()
    plt.show()

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    all_losses = stress_test(num_seeds=5, steps=5000)
    np.save("async_stress_test_losses.npy", all_losses)
    plot_results(all_losses)
