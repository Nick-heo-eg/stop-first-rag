# STOP-first RAG Gate

**Detecting when AI decisions should *not* be made**

---

## Project Status

This repository represents an ongoing research exploration.

It is **not a product**, **not a finalized solution**, and **not a commercial offering**.
The goal is to explore where AI governance concepts break when confronted with real workflows.

Several hypotheses in this repository are intentionally unvalidated.
They exist to provoke discussion and enable learning — not to claim readiness.

---

## Overview

This repository demonstrates a judgment gate that verifies **whether an AI decision is permissible** before any answer is produced.

It does **not** automate decisions.
It automates the detection of **decision-impossible states**.

---

## Why this exists

In high-risk domains (HR, Finance, Medical), most incidents are not caused by *wrong answers*,
but by **answers produced without sufficient evidence**.

Current RAG/LLM systems assume that evidence exists.
This project explicitly checks **whether evidence actually exists** — and stops if it does not.

---

## What this system does

* Accepts raw structured inputs (JSON)
* Uses real document text → extracted RAG chunks
* Applies **JD-style policies** (`must / should / must_not`)
* Enforces a **deterministic judgment gate**
* Produces one of three outcomes:

  * **ALLOW** – decision is permitted
  * **REVIEW** – human judgment required
  * **STOP** – decision prohibited (with logged reason)

Every STOP produces a **negative proof log** explaining *why* the decision was blocked.

---

## What this system does NOT do

* ❌ It does not rank candidates
* ❌ It does not approve loans
* ❌ It does not make medical diagnoses
* ❌ It does not replace human responsibility

This repository is a **validation artifact**, not a production decision system.

---

## Verified results (measured, not assumed)

| Domain  | Total | ALLOW | REVIEW | STOP |
| ------- | ----: | ----: | -----: | ---: |
| HR      |    60 |    38 |      0 |   22 |
| Finance |    40 |    17 |      5 |   18 |
| Medical |    30 |    15 |      2 |   13 |

These ratios are **not tuned**.
They emerge solely from **evidence existence checks**.

---

## Architecture (one page)

```
Input
  ↓
JD Policy (YAML)
  ↓
Documents (resume / portfolio / consent / reports)
  ↓
RAG Chunks + Evidence Tags
  ↓
Judgment Gate (enforcement)
  ↓
ALLOW / REVIEW / STOP (+ negative_proof.jsonl)
```

---

## Run the demo (reproducible)

```bash
cd demos/multidomain
python3 ajt_gate_multidomain_jd.py \
  hr/data/candidates \
  hr/data/chunks \
  hr/policy/jd_policy.yaml \
  hr/out
```

You will see ALLOW / REVIEW / STOP counts printed deterministically.

---

## Key idea (one sentence)

> AI should not be optimized to answer more questions.
> It should be optimized to **refuse answers when judgment is not permitted**.

---

## Scope Clarification

### What this repository explores:
- AI risk boundaries in high-stakes domains
- Structural assumptions about evidence sufficiency
- Failure modes when AI proceeds without adequate evidence
- Deterministic judgment gates as research artifacts

### What this repository does NOT attempt:
- Replace HR, Finance, or Medical workflows
- Define market-ready governance products
- Claim enterprise adoption readiness
- Provide legal or regulatory compliance solutions

This is a **research exploration**, not a deployment-ready system.

---

## License & intent

This project is published for research, validation, and discussion.
It is intended to inform safer AI system design, not to bypass domain regulations.

---

## Related work

- [judgment-state-canon](https://github.com/Nick-heo-eg/judgment-state-canon) - Constitutional framework for judgment systems
- [Echo Memory Governor](https://github.com/Nick-heo-eg/echo-memory-governor) - Constitutional memory system (v0.1-constitution)
