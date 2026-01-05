# STOP-First RAG: Judgment-Centered Retrieval

> Traditional RAG answers everything. Even when it shouldn't.

**The Problem**: Most RAG systems optimize for answer rate. They retrieve, generate, and return—whether the evidence is solid or sketchy. The cost of a wrong answer? Not their problem.

**This System**: Optimizes for **judgment integrity**. If evidence is weak, conflicting, or absent, it returns `STOP` with a structured reason. No hallucination. No hand-waving. Just honest refusal.

---

## The Difference in 30 Seconds

**Traditional RAG**:
```
Query: "What's our return policy for opened software?"
[Weak evidence retrieved]
Answer: "Based on the documents, software can be returned within 14 days." ❌
```

**STOP-First RAG**:
```
Query: "What's our return policy for opened software?"
[Weak evidence retrieved]
STOP: NO_ACCEPTABLE_EVIDENCE
Reason: E1 covers physical products only, E2 mentions software but no concrete policy
Trace: examples/stop_trace.jsonl ✅
```

One system guessed. The other **proved why it didn't**.

**See the actual trace**: [`examples/stop_trace.jsonl`](examples/stop_trace.jsonl)
- Shows every evidence judgment (ACCEPT/REJECT/DEFER)
- Final decision with structured reason code
- Complete audit trail from query to STOP

---

## One-Line Thesis

> **Traditional RAG optimizes answer rate. This system optimizes the cost of being wrong.**

---

## Where This Matters

If you're building for:
- **Compliance & audit tools** (every decision must be traceable)
- **Legal/enterprise decision support** (wrong answers are expensive)
- **Safety-critical internal systems** (silence is better than incorrect guidance)

...then "I don't know" is often the **correct answer**, not a failure.

---

## Quick Start (1 Command)

```bash
# Run the minimal demo (no dependencies)
python demo_minimal.py
```

You'll see:
- Evidence judge decisions (ACCEPT/REJECT/DEFER) in real-time
- Final judgment (ANSWER or STOP) with reason code
- Complete trace output (JSON format)
- **Live STOP behavior** - system refuses to hallucinate

**No dependencies.** Just Python 3.7+. No GPU, no Ollama, no external libs.

---

<details>
<summary><strong>📖 Core Concepts (click to expand)</strong></summary>

## What is STOP-First / Judgment-First RAG?

Traditional RAG: `Query → Retrieve → Generate → Answer`

STOP-First RAG: `Query → Retrieve → **Judge Evidence** → (Conditional) Generate → **Final Judge** → ANSWER or STOP`

### Core Principle

> **Retrieval is optional. Judgment is not.**

The system treats "I cannot answer this" as a **first-class outcome**, not a failure.

### STOP is a Valid Outcome

When evidence is weak, conflicting, or absent, the system returns:

```json
{
  "decision": "STOP",
  "reason_code": "CONFLICTING_EVIDENCE",
  "explanation": "Found 3 sources: 2 say 14 days, 1 says 30 days",
  "trace_id": "run_abc123"
}
```

This is a **compliant result**, fully logged and traceable.

### Trace & Reason Code Philosophy

Every query—whether answered or stopped—produces an **append-only trace**:

```
RUN_START → RETRIEVE → EVIDENCE_JUDGE → ANSWER_CANDIDATES → FINAL_DECISION → RUN_END
```

Reason codes are **not free-form excuses**. They are:
- Enumerated (e.g., `LOW_CONFIDENCE`, `CONFLICTING_EVIDENCE`, `NO_ACCEPTABLE_EVIDENCE`)
- Structured for audit and metrics
- Used to prove **why the system stopped**

This is **negative proof**: we can demonstrate what judgment was required and why it wasn't met.

</details>

---

## How It Differs from Traditional RAG

**Architecture Diagram**:

```
Traditional RAG:
  Query → Retrieve → Generate → Answer
                                  ↓
                            (hallucinate when weak)

STOP-First RAG:
  Query → Retrieve → Evidence Judge ──→ Generate → Final Judge → ANSWER
                          ↓                             ↓
                        REJECT                        STOP
                          ↓                             ↓
                    (with reason code)          (with trace)
```

**Key Differences**:

| Traditional RAG | STOP-First RAG |
|----------------|----------------|
| Retrieve → Generate | Retrieve → **Evidence Judge** → Generate |
| Answer or hallucinate | Answer or **STOP with reason** |
| Failures attributed to "hallucination" | Structured reason codes |
| Model owns the decision | **Judge owns the decision** (model only proposes) |
| Optimize answer rate | **Optimize cost of being wrong** |

---

## Evaluation: Precision vs STOP Trade-off

The `eval/` directory compares traditional RAG vs STOP-first RAG on:

- **answer_rate**: How many questions get answered
- **precision**: Of the answers given, how many are correct
- **hallucination_rate**: Unsupported claims per answer
- **wrong_but_answered**: The danger zone (answered incorrectly) ⚠️
- **stop_rate**: How often the system stops (with reason distribution)

**Key insight**: Traditional RAG has higher answer_rate but also higher wrong_but_answered. STOP-first RAG trades answer coverage for **safety**.

**Run the comparison**:
```bash
cd eval
python compare.py \
  --traditional traditional_outputs.jsonl \
  --judgment judgment_outputs.jsonl \
  --out report.csv
```

See `eval/README.md` for full methodology.

---

## Project Structure

```
.
├── README.md                       # This file
├── demo.py                         # CPU-friendly demo script
├── ollama_call.py                  # Ollama integration
├── prompts/
│   └── epl_evidence_prompt.txt    # Evidence evaluation prompt
├── eval/
│   ├── README.md                  # Evaluation methodology
│   ├── compare.py                 # Metric comparison script
│   └── sample_questions.jsonl     # Example queries
└── docs/
    └── STOP_RAG_RELATIONSHIP.md   # Architectural explanation
```

---

<details>
<summary><strong>🏗️ Architecture: Relationship to STOP/Branch Judgment (click to expand)</strong></summary>

## Relationship to STOP/Branch Judgment

This is not a new safety feature bolted onto RAG. The **STOP/branch judgment core already existed**—it was used to halt execution when conditions weren't met, branch when uncertainty required manual decisions, and log the reason.

**RAG simply became the evidence supply channel** for that same judgment core:

```
[Judgment Core (STOP/AJT)] ← evidence from RAG
```

- STOP policies get reused (pre/post RAG logic stays identical)
- RAG retrieves evidence; the judgment layer decides if it's sufficient
- If evidence is weak/conflicting, STOP fires **before the model generates**

See `docs/STOP_RAG_RELATIONSHIP.md` for the full architectural explanation.

### Key Statement

> **RAG is not a new safety add-on. It supplies evidence to the judgment system we already built.**

The model proposes. The judgment layer decides. RAG never owns the decision to speak.

</details>

---

## Core Philosophy

This system embodies three principles:

1. **Judgment existence, not correctness**: We detect if a judgment happened, not if it's "right"
2. **Negative as first-class**: STOP is a legitimate output, not a fallback
3. **Trace before trust**: Every decision is logged in append-only format

These aren't aspirational values—they're **enforced by code**.

---

## CPU-Only Demo

Because responsibility doesn't need GPUs. CPU-only execution:
- Forces explicit judgment rules
- Reveals STOP behavior clearly
- Proves the judgment layer is independent of model complexity

Run with **Ollama on CPU** and see the full judgment flow.

---

## License

MIT

---

## Contact

For questions about the judgment architecture or STOP-first design philosophy, open an issue on GitHub.

---

**Final Statement:**

> **Traditional RAG answers questions. This RAG proves why it didn't.**
