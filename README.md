# STOP-First RAG: Judgment-Centered Retrieval

Most RAG systems optimize for answer quality. This system optimizes for **judgment integrity**.

## What is STOP-First / Judgment-First RAG?

Traditional RAG follows: `Query → Retrieve → Generate → Answer`

STOP-First RAG follows: `Query → Retrieve → **Judge Evidence** → (Conditional) Generate → **Final Judge** → ANSWER or STOP`

The critical difference: **judgment happens before and after generation, not just at the end.**

### Core Principle

> **Retrieval is optional. Judgment is not.**

This system treats "I cannot answer this" as a **first-class outcome**, not a failure. When evidence is weak, conflicting, or absent, the system returns:

```
STOP
Reason: CONFLICTING_EVIDENCE
```

This is a **compliant result**, fully logged and traceable.

## How It Differs from Traditional RAG

| Traditional RAG | STOP-First RAG |
|----------------|----------------|
| Retrieve → Generate | Retrieve → **Evidence Judge** → Generate |
| Answer or hallucinate | Answer or **STOP with reason** |
| Failures attributed to "hallucination" | Structured reason codes (NO_ACCEPTABLE_EVIDENCE, CONFLICTING_EVIDENCE, LOW_CONFIDENCE) |
| Model owns the decision | **Judge owns the decision** (model only proposes) |
| Optimize answer rate | **Optimize cost of being wrong** |

## STOP is a Valid Outcome

In compliance, legal, and safety-critical domains, saying "I don't know" is often the correct answer. This system:

- **Does not penalize STOP** as failure
- **Logs every STOP** with a structured reason code
- **Tracks wrong-but-answered** as the primary risk metric

Traditional RAG: "How many questions did we answer?" (answer_rate)
STOP-First RAG: **"How many wrong answers did we emit?"** (wrong_but_answered)

## Trace & Reason Code Philosophy

Every query—whether answered or stopped—produces an **append-only trace**:

```
RUN_START → RETRIEVE → EVIDENCE_JUDGE → ANSWER_CANDIDATES → FINAL_DECISION → RUN_END
```

Reason codes are **not free-form excuses**. They are:

- Enumerated (e.g., `LOW_CONFIDENCE`, `CONFLICTING_EVIDENCE`, `NO_ACCEPTABLE_EVIDENCE`)
- Structured for audit and metrics
- Used to prove **why the system stopped**

This is **negative proof**: we can demonstrate what judgment was required and why it wasn't met.

## CPU-Only Demo Possible

This system runs **without GPUs** because responsibility doesn't need high-performance hardware. CPU-only execution:

- Forces explicit judgment rules
- Reveals STOP behavior clearly
- Proves the judgment layer is independent of model complexity

You can run the demo with **Ollama on CPU** and still see the full judgment flow.

## Evaluation: Precision vs STOP Trade-off

The `eval/` directory compares traditional RAG vs STOP-first RAG on:

- **answer_rate**: How many questions get answered
- **precision**: Of the answers given, how many are correct
- **hallucination_rate**: Unsupported claims per answer
- **wrong_but_answered**: The danger zone (answered incorrectly)
- **stop_rate**: How often the system stops (with reason distribution)

**Key insight**: Traditional RAG has higher answer_rate but also higher wrong_but_answered. STOP-first RAG trades answer coverage for **safety**.

See `eval/README.md` for full methodology.

## One-Line Summary

> **Traditional RAG answers questions. This RAG proves why it didn't.**

Or equivalently:

> **Traditional RAG optimizes answer rate. This system optimizes the cost of being wrong.**

## Where It Matters

- **Compliance & audit tools**: Every decision must be traceable
- **Legal/enterprise decision support**: Wrong answers are expensive
- **Safety-critical internal systems**: Silence is better than incorrect guidance

We aren't chasing flashy answers. We're ensuring the system knows when to remain silent—and can prove why.

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

## Getting Started

1. **Install dependencies** (Ollama recommended for CPU demo):
   ```bash
   # Install Ollama (see https://ollama.ai)
   ollama pull qwen2.5
   ```

2. **Run the demo**:
   ```bash
   python demo.py
   ```

3. **Check the trace**:
   - Every run creates a `.jsonl` trace file
   - Look for `STOP` entries with `reason_code`
   - Compare `EVIDENCE_JUDGE` vs `FINAL_DECISION` outcomes

4. **Run evaluation** (optional):
   ```bash
   cd eval
   python compare.py \
     --traditional traditional_outputs.jsonl \
     --judgment judgment_outputs.jsonl \
     --out report.csv
   ```

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

## Core Philosophy

This system embodies three principles:

1. **Judgment existence, not correctness**: We detect if a judgment happened, not if it's "right"
2. **Negative as first-class**: STOP is a legitimate output, not a fallback
3. **Trace before trust**: Every decision is logged in append-only format

These aren't aspirational values—they're **enforced by code**.

## License

MIT

## Contact

For questions about the judgment architecture or STOP-first design philosophy, open an issue.

---

**Final Statement:**

> **RAG is not a new safety add-on. It supplies evidence to the judgment system we already built.**

The model proposes. The judgment layer decides. RAG never owns the decision to speak.
