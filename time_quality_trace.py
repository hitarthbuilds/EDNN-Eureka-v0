import torch
import torch.nn as nn
import matplotlib.pyplot as plt

from main import PCNModel
from stress_test_async_learning import generate_batch

# -----------------------------
# Setup
# -----------------------------
loss_fn = nn.MSELoss(reduction="mean")

model = PCNModel(num_agents=3)
model.eval()

x, y = generate_batch(batch_size=64)

# -----------------------------
# Run time-traced forward pass
# -----------------------------
trace = model.forward_with_trace(x)

times = []
losses = []

for t, artifact in trace:
    y_hat = model.head(artifact)
    loss = loss_fn(y_hat, y).item()
    times.append(t)
    losses.append(loss)

# -----------------------------
# Normalize quality using FINAL loss
# -----------------------------
initial_loss = losses[0]
final_loss = losses[-1]

qualities = [
    (initial_loss - l) / (initial_loss - final_loss)
    for l in losses
]

# Clamp for safety
qualities = [max(0.0, min(q, 1.0)) for q in qualities]
# -----------------------------
# Synchronous baseline
# -----------------------------
sync_time = times[-1]
sync_quality_times = [0.0, sync_time, sync_time]
sync_quality_values = [0.0, 0.0, 1.0]


# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(8, 5))

plt.plot(times, qualities, marker="o", label="EDNN (Event-Driven)")
plt.plot(
    sync_quality_times,
    sync_quality_values,
    linestyle="--",
    label="Synchronous Baseline",
)

plt.xlabel("Wall-Clock Time (seconds)")
plt.ylabel("Normalized Output Quality")
plt.title("Quality vs Wall-Clock Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# -----------------------------
# Print trace (for paper logs)
# -----------------------------
for t, q in zip(times, qualities):
    print(f"[t={t:.2f}s] normalized_quality={q:.3f}")
