# Stop-First RAG

Judgment-first RAG implementation with minimal dependencies.

**STOP is a first-class outcome** — not a failure mode, but an intentional decision when evidence is insufficient.

---

## Quickstart

```bash
git clone https://github.com/Nick-heo-eg/stop-first-rag.git
cd stop-first-rag
python3 demo_minimal.py
```

Outputs STOP / ACCEPT / DEFER decisions with judgment reasoning.

**No external dependencies required** — runs on Python stdlib.

---

## What This Does

Traditional RAG systems retrieve evidence and generate answers by default.

Stop-First RAG adds a **judgment layer** that evaluates evidence quality before allowing answer generation:

1. **Retrieve** evidence candidates
2. **Judge** each piece of evidence (ACCEPT / REJECT / DEFER)
3. **Stop** if no acceptable evidence exists
4. **Answer** only when evidence meets quality thresholds

---

## Example Output

```
Query: What is our return policy for opened software?

Retrieved 3 evidence candidates

[E1] Decision: REJECT
     Reason: Evidence covers physical products, not software

[E2] Decision: DEFER
     Reason: Evidence mentions topic but provides no concrete answer

[E3] Decision: REJECT
     Reason: Confidence 0.43 below threshold 0.5

Final Decision: STOP
No acceptable evidence found. Cannot generate answer.
```

---

## Key Files

- `demo_minimal.py` — Self-contained demonstration (no dependencies)
- `demo.py` — Extended demo with mock retrieval
- `gate.py` — Core judgment logic implementation
- `eval/` — Evaluation scripts
- `demos/` — Additional examples

---

## Design Principles

- **Judgment before generation**: Decide if answer should exist before generating it
- **Explicit non-execution**: STOP is logged and auditable, not silent
- **Evidence-level decisions**: Each piece of evidence is judged independently
- **Observable outcomes**: All decisions include structured reasoning

---

## Repository Map

This repository contains working code for stop-first judgment logic.

Related specifications and concepts:

* **[ai-execution-boundary-spec](https://github.com/Nick-heo-eg/ai-execution-boundary-spec)** — Pre-incident execution boundaries
* **[agent-judgment-spec](https://github.com/Nick-heo-eg/agent-judgment-spec)** — Judgment authority transfer in autonomous agents
* **[ai-judgment-trail-spec](https://github.com/Nick-heo-eg/ai-judgment-trail-spec)** — Structured log schema for AI decision accountability
* **[decision-only-observability](https://github.com/Nick-heo-eg/decision-only-observability)** — Observing non-executed operations

---

## Who This Is For

* RAG system developers
* Platform / infrastructure engineers
* AI governance and audit teams
* Agent framework designers

---

## What This Is Not

* ❌ A content filter
* ❌ Alignment or RLHF
* ❌ Prompt engineering
* ❌ Output moderation

This work preserves **human responsibility** by making it provable when the system chose not to answer.

---

## Historical Context

This repository was the strategic hub for judgment boundary work (2024-2025). It remains as a working reference implementation demonstrating stop-first logic in RAG systems.

---

## License

MIT — See [LICENSE](LICENSE) file for details.
