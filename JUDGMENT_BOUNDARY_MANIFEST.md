# Judgment Boundary Manifest

> **Purpose**
> This document defines the shared problem space and fixed axes across the Judgment Boundary work.
> It is a map, not a framework.

---

## 1. Problem Statement

Most AI safety discussions optimize *answer quality*, *alignment*, or *model behavior*.
This work starts from a different failure mode.

**The real cost of AI systems is not being wrong,
but executing when they should not.**

Modern systems lack a clear, provable boundary between:

* observing,
* judging,
* and executing.

As a result, responsibility is blurred, and non-execution is invisible.

---

## 2. What Existing Systems Miss

* **Guardrails** treat judgment as a post-processing filter on outputs.
* **RAG systems** optimize retrieval accuracy, not execution risk.
* **Agent frameworks** collapse intent, judgment, and action into a single loop.
* **RLHF / alignment** modify model behavior without externalizing authority.
* **Safety layers** focus on content, not on *whether execution occurred*.

The common failure:
**judgment is embedded in generation, not separated and provable.**

---

## 3. Fixed Axes (Non-Negotiable)

1. **STOP is a first-class outcome**
   Not an error, not a fallback — a valid result.

2. **Judgment precedes execution**
   Execution is conditional, not assumed.

3. **Non-execution must be observable**
   Systems must prove *that they did not act*.

4. **Authority must be attributable**
   It must be clear whether a human or a system decided.

These axes apply regardless of model, language, or deployment context.

---

## 4. Repository Map

| Layer              | Repository                                                                 |
| ------------------ | -------------------------------------------------------------------------- |
| Entry / Philosophy | stop-first-rag                                                             |
| Execution Boundary | llm-execution-boundary                                                     |
| Judgment Pipeline  | two-stage-judgment-pipeline                                                |
| Benchmarks         | llm-gating-bench, math-solver-benchmark                                    |
| Semantics (KR)     | k-judgment-gate                                                            |
| Governance / Spec  | agent-judgment-spec, execution-governance-spec, ai-execution-boundary-spec |
| Observability      | decision-only-observability, semantic-conventions                          |

Each repository addresses one layer of the same boundary problem.

---

## 5. Non-Goals

* We do **not** block AI.
* We do **not** judge correctness of answers.
* We do **not** optimize answer rate.
* We do **not** replace human decision-making.

This work exists to **preserve responsibility**, not to automate it.

---

## 6. One-Line Positioning

**This work is about preserving human responsibility
by proving when AI did not decide.**

---

**Status**: Living document
**Last updated**: 2026-02-02
