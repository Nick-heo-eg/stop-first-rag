# stop-first-rag

## Historical Context

**This repository was the strategic hub for judgment boundary work (2024-2025).**

It has since been repositioned as a **public conceptual anchor** and **archival entry point**.

Active development has moved to dedicated implementation repositories. This repository remains as a permanent reference for the conceptual foundation and links to publicly accessible specifications, proofs, and benchmarks.

---

## The Problem | The Boundary | The Evidence

**AI systems fail not when they are wrong, but when they execute when they should not.**

**The Problem:** Execution is the default. Judgment is implicit. Non-execution is invisible.

**The Boundary:** Separate judgment (STOP/HOLD/ALLOW) from execution. Make non-execution observable, auditable, attributable.

**The Evidence:** Public specifications (conceptual foundation), public proofs (working demonstrations), public benchmarks (measured outcomes).

→ **See JUDGMENT_BOUNDARY_MANIFEST.md for the full conceptual map.**

---

## What This Repository Is

**No runnable system lives here.**
**No execution artifacts are stored here.**

This is a **conceptual anchor** and **public archive** linking to:
- Specifications (how judgment boundaries work)
- Proofs (that they can be implemented)
- Benchmarks (measuring their effectiveness)

This repository is documentation-only. It aggregates references. It does not execute code.

---

## Active Development

Current active work has moved to:

→ **[execution-authority-runtime-v1](https://github.com/Nick-heo-eg/execution-authority-runtime-v1)** — Execution governance runtime with mandatory mediation

All operational proofs, sealed artifacts, and private development infrastructure are maintained separately and are **not linked from this repository**.

---

## Public Repository Map

### Specifications (Conceptual Foundation)

* **[judgment-topology](https://github.com/Nick-heo-eg/judgment-topology)** — Minimal judgment topology (states, transitions, constraints)
* **[execution-governance-spec](https://github.com/Nick-heo-eg/execution-governance-spec)** — Execution governance framework
* **[ai-execution-boundary-spec](https://github.com/Nick-heo-eg/ai-execution-boundary-spec)** — Pre-incident execution boundaries
* **[agent-judgment-spec](https://github.com/Nick-heo-eg/agent-judgment-spec)** — Judgment authority transfer in autonomous agents
* **[spec](https://github.com/Nick-heo-eg/spec)** — Structured log schema for AI decision accountability

### Proofs & Demonstrations

* **[judgment-topology-poc](https://github.com/Nick-heo-eg/judgment-topology-poc)** ⭐ — Claude legal plugin judgment layer (NDA triage)
* **[mail-sentinel](https://github.com/Nick-heo-eg/mail-sentinel)** — Email mistake checkpoint (browser-based, no install)
* **[genai-judgment-boundary](https://github.com/Nick-heo-eg/genai-judgment-boundary)** — GenAI judgment boundary implementation
* **[decision-infrastructure](https://github.com/Nick-heo-eg/decision-infrastructure)** — Decision preparation infrastructure

### Benchmarks & Measurement

* **[llm-gating-bench](https://github.com/Nick-heo-eg/llm-gating-bench)** — Pre-generation gating benchmark (5.17× speedup)
* **[stop-strategy-comparison](https://github.com/Nick-heo-eg/stop-strategy-comparison)** — 25-task explicit stop mechanism study
* **[decision-only-observability](https://github.com/Nick-heo-eg/decision-only-observability)** — Observing non-executed operations

### Language-Specific (Korean)

* **[k-judgment-gate](https://github.com/Nick-heo-eg/k-judgment-gate)** — Korean LLM governance-first judgment detection
* **[judgment-refinement-public](https://github.com/Nick-heo-eg/judgment-refinement-public)** — Korean judgment detection (50% FP reduction)

**Start with Specifications for concepts, Proofs for evidence, Benchmarks for measurement.**

---

## Sealed Operational Artifacts (Not Public)

The following materials exist but are not publicly accessible:

* **Operational proofs** — Sealed operational artifacts (not public)
* **Private development infrastructure** — Sealed operational artifacts (not public)
* **Execution traces and schemas** — Sealed operational artifacts (not public)
* **Internal pilot results** — Sealed operational artifacts (not public)

**Operational Proof (Reference Only):**

Early validation of STOP as an executable outcome was conducted via two minimal automation pilots (Pilot 001, Pilot 002). These pilots demonstrated that stopping is conditional, not a failure mode.

These pilots are maintained as a separate sealed operational record:
→ **stop-first-operational-proof** (access restricted)

This proof demonstrates **how** stopping works, not **when** stopping should occur.

---

## Who This Is For

* Platform / infrastructure engineers
* AI governance, audit, and compliance teams
* Agent and orchestration framework designers

### Not Intended For

* Prompt engineering
* End-user AI tooling
* Content filtering use cases

---

## What This Is Not

* ❌ A filter
* ❌ Alignment or RLHF
* ❌ Content moderation
* ❌ "AI safety" by blocking outputs

This work exists to preserve **human responsibility** by making it provable when AI systems **did not decide**.

---

## Status

* **Public conceptual anchor**
* **Documentation-only repository**
* **No code execution required to understand the system**
* **All private links removed** (2026-02-15)

---

## About

**Judgment-first RAG**: Optimize the cost of being wrong, not answer rate.

**STOP is a first-class outcome.**

---

## License

MIT — See [LICENSE](LICENSE) file for details.
