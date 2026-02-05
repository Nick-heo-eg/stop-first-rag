# stop-first-rag

> **This is the entry point to the Judgment Boundary work.**
> **If you are new, start here.**

---

**AI systems fail not when they are wrong,
but when they execute when they should not.**

---

## What This Repository Is

This repository introduces **STOP as a first-class outcome** in AI systems.

It reframes Retrieval-Augmented Generation (RAG) and agent pipelines
around a single question:

**"Should the system execute at all?"**

The goal is not to improve answers,
but to **prevent costly execution when judgment is uncertain or inappropriate**.

---

## The Problem

Most AI systems share the same structural flaws:

* **Execution is the default** — generation implies action
* **Judgment is implicit** — buried inside model behavior
* **Non-execution is invisible** — you cannot prove that nothing happened

As a result, responsibility is blurred and failure costs explode.

---

## The Judgment Boundary

This work separates *judgment* from *execution*.

Instead of optimizing for answers, systems explicitly decide between:

* **STOP** — do not execute
* **HOLD** — defer to a human or another authority
* **ALLOW** — execution is permitted

Correctness is secondary.
**Execution control is primary.**

For the full conceptual map, see:

→ **[JUDGMENT_BOUNDARY_MANIFEST.md](JUDGMENT_BOUNDARY_MANIFEST.md)**

---

## Repository Map

This repository is the **front door** to a larger body of work.
Navigate from here:

### **Tier 1: Specifications (Conceptual Foundation)**

* **[judgment-topology](https://github.com/Nick-heo-eg/judgment-topology)** — Minimal judgment topology (states, transitions, constraints)
* **[execution-governance-spec](https://github.com/Nick-heo-eg/execution-governance-spec)** — Execution governance framework
* **[ai-execution-boundary-spec](https://github.com/Nick-heo-eg/ai-execution-boundary-spec)** — Pre-incident execution boundaries
* **[agent-judgment-spec](https://github.com/Nick-heo-eg/agent-judgment-spec)** — Judgment authority transfer in autonomous agents
* **[spec](https://github.com/Nick-heo-eg/spec)** — Structured log schema for AI decision accountability

### **Tier 2: Proofs & Demonstrations**

* **[judgment-topology-poc](https://github.com/Nick-heo-eg/judgment-topology-poc)** ⭐ — Claude legal plugin judgment layer (NDA triage)
* **[mail-sentinel](https://github.com/Nick-heo-eg/mail-sentinel)** — Email mistake checkpoint (no install, browser-based)
* **[genai-judgment-boundary](https://github.com/Nick-heo-eg/genai-judgment-boundary)** — GenAI judgment boundary implementation
* **[decision-infrastructure](https://github.com/Nick-heo-eg/decision-infrastructure)** — Decision preparation infrastructure

### **Tier 3: Benchmarks & Measurement**

* **[llm-gating-bench](https://github.com/Nick-heo-eg/llm-gating-bench)** — Pre-generation gating benchmark (5.17× speedup)
* **[stop-strategy-comparison](https://github.com/Nick-heo-eg/stop-strategy-comparison)** — 25-task explicit stop mechanism study
* **[decision-only-observability](https://github.com/Nick-heo-eg/decision-only-observability)** — Observing non-executed operations

### **Tier 4: Language/Domain-Specific**

* **[k-judgment-gate](https://github.com/Nick-heo-eg/k-judgment-gate)** — Korean LLM governance-first judgment detection
* **[judgment-refinement-public](https://github.com/Nick-heo-eg/judgment-refinement-public)** — Korean judgment detection (50% FP reduction)

---

**Start with Tier 1 (specs) for concepts, Tier 2 (proofs) for evidence.**

---

## Who This Is For

* Platform / infrastructure engineers
* AI governance, audit, and compliance teams
* Agent and orchestration framework designers

**Not** intended for:

* Prompt engineering
* End-user AI tooling
* Content filtering use cases

---

## What This Is Not

* ❌ Not a filter
* ❌ Not alignment or RLHF
* ❌ Not content moderation
* ❌ Not "AI safety" by blocking outputs

This work exists to **preserve human responsibility**
by proving when AI systems **did not decide**.

---

## Start Here

If you arrived from another repository:

→ **Start here:** `stop-first-rag`
→ **Understand the map:** `JUDGMENT_BOUNDARY_MANIFEST.md`
→ **Then explore individual layers**

---

### Status

* Public reference point
* Documentation-first
* No code execution required to understand the system

---

## License

MIT — See [LICENSE](LICENSE) file for details.
