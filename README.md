# **EDNN-eureka-v0**

### *Event-Driven Neural Networks: Breaking Layer-Synchronous Execution*

---

## Overview

This repository investigates **Event-Driven Neural Networks (EDNNs)** — a class of neural architectures in which the forward pass is **asynchronous**, **event-driven**, and **temporally extended**, rather than strictly layer-synchronous and atomic.

In standard neural networks (e.g., Transformers, Mixture-of-Experts), the forward pass produces an output only after *all* components finish computation. EDNNs relax this assumption by allowing intermediate neural components to contribute to an evolving output artifact as soon as they complete execution.

The goal of this project is to establish **existence, trainability, and execution semantics**, not performance supremacy.

---

## Core Concept

Traditional neural execution assumes:

> **Output exists only after all layers complete.**

EDNN challenges this assumption.

In EDNN:

* Multiple neural components (“agents”) execute asynchronously
* Agents write outputs to a shared, differentiable **blackboard**
* An **integrator** continuously aggregates available results
* The model produces a **living output artifact** that improves over wall-clock time
* The entire system remains **fully differentiable** and trainable via backpropagation

The forward pass is therefore a **trajectory over time**, not a single atomic operation.

---

## What This Repository Demonstrates

This repository provides empirical evidence for the following claims:

* ✅ Asynchronous neural execution is compatible with gradient-based learning
* ✅ Randomized execution order does **not** destabilize training
* ✅ Credit assignment remains well-defined under temporal non-determinism
* ✅ Event-driven neural architectures can converge reliably across seeds

These claims are validated via controlled synthetic stress tests.

---

## Repository Structure

```
.
├── agent.py                      # Neural agent modules
├── blackboard.py                 # Shared differentiable memory
├── integrator.py                 # Event-driven integrator
├── main.py                       # Core EDNN architecture wiring
├── stress_test_async_learning.py # Asynchronous learning stress test
├── utils.py
└── README.md
```

---

## Stress Test: Asynchronous Learning Dynamics

The file `stress_test_async_learning.py` implements a **synthetic learning task** designed to stress-test learning dynamics under asynchronous execution.

### Test Properties

* Execution order randomized every forward pass
* No layer-synchronization barriers
* Same task, loss, optimizer, and hyperparameters across seeds
* Multi-seed evaluation

### Result

Loss decreases smoothly and consistently across all seeds, demonstrating that **asynchronous execution does not impede convergence**.

This experiment serves as an **existence proof**, not a benchmark.

---

## What EDNN Is *Not*

* ❌ Not a Transformer replacement
* ❌ Not a performance benchmark
* ❌ Not a cognitive or brain model
* ❌ Not a production-ready system

This work focuses on **execution semantics**, not optimization or scale.

---

## Current Research Status

**Phase:** Existence proof & architectural grounding

**Completed:**

* Asynchronous learning stress test
* Architecture-grounded validation (Agents + Blackboard + Integrator)

**In Progress:**

* Wall-clock time instrumentation
* Partial output quality vs. time analysis
* Comparison with strictly synchronous baselines

---

## Naming Note

Early drafts referred to this architecture as **PCN (Parallel Cognition Network)**.
The name has been updated to **EDNN (Event-Driven Neural Network)** to more accurately reflect the architectural contribution.

Internal class names may still reflect early naming and will be updated once the architecture stabilizes.

---

## Disclaimer

This repository represents **active research**.
APIs, abstractions, and naming may change as experiments and theory mature.

---

## Maintainer

**Hitarth Desai**
Research-focused exploration. Feedback and discussion welcome.

---

