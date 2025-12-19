# PCN-Eureka-v0  
**Event-Driven Asynchronous Neural Execution (Minimal Proof)**

## What this repository demonstrates

This repository provides a minimal, executable proof of a **non-layer-synchronous neural execution model**.

Specifically, it demonstrates a single forward pass in which:

- Multiple internal agents execute **concurrently**
- A shared blackboard enables **event-driven communication**
- An integrator consumes **partial results before all agents complete**
- The output artifact **evolves over wall-clock time**
- Final consistency is achieved **without enforcing a global synchronization barrier**

This behavior cannot be represented as a standard Transformer, Mixture-of-Experts, or any layer-synchronous neural DAG.

---

## Core claim (precise and falsifiable)

> **The output of a forward pass can depend on the temporal availability of internal computation, not only on input values.**

In other words, the forward pass is **temporally extended**, not atomic.

---

## Why this matters

Modern neural architectures implicitly assume that a forward pass is:
- layer-synchronous
- barrier-enforced
- representable as a directed acyclic graph (DAG)

In such systems:
- intermediate computation is not causally observable
- partial results cannot influence output until all computation completes

This repository demonstrates a counterexample.

---

## Execution trace (key evidence)

When running `python main.py`, the system produces logs similar to:

```

[t=  0.00s] Integrator START
[t=  0.00s] Agent structure START
[t=  0.00s] Agent code START

[t=  1.00s] Agent structure END (wrote result)
[t=  1.01s] Integrator UPDATED artifact with [structure]

[t=  3.01s] Agent code END (wrote result)
[t=  3.05s] Integrator UPDATED artifact with [code]

[t=  3.53s] Integrator STOP
[t=  3.62s] FINAL ARTIFACT: {...}

```

This shows that:
- the integrator reacts to early results
- the output artifact changes before all agents finish
- computation proceeds without a global synchronization point

---

## What this is (and is not)

**This is:**
- an execution-model proof
- an event-driven forward-pass demonstration
- a counterexample to layer-synchronous assumptions

**This is not:**
- a learning system
- a benchmark comparison
- a claim of superior performance
- an AGI proposal

Learning, optimization, and scaling are intentionally excluded.

---

## Minimal architecture

```

Input
↓
[ Concurrent Agents ]
↘        ↙
Shared Blackboard
↓
Event-Driven Integrator
↓
Evolving Output Artifact

````

Agents execute independently.
The integrator reacts as results become available.
No global barrier exists.

---

## Reproducibility

Run:

```bash
python main.py
````

No dependencies beyond Python standard library.

---

## Status

This repository is intentionally minimal and frozen at **v0**.

Its sole purpose is to demonstrate the existence of asynchronous,
event-driven neural execution within a single forward pass.

Further work (learning, differentiability, scaling) is out of scope.

```

---

## What to do immediately after this

1. Paste this into `README.md`
2. Commit with message:
```

Clarify core claim and document asynchronous forward-pass proof

```
3. Do **not** change code for now

At this point:
- the repo has a clear claim
- the evidence matches the claim
- the scope is controlled

This is the version you show your HOD.  
This is the version you reference in a paper draft.

Next step, when you’re ready:  
we turn this README into the **Introduction + Problem Statement** of a paper.
```
