# Stop-First RAG

**Early exit guard for RAG pipelines**: Check evidence presence before LLM generation → skip generation when chunks are empty.

---

## What This Project Is / Is Not

### This Project Is

A **reference implementation** of a single-responsibility gate that decides whether LLM generation should proceed based on evidence presence.

**Core principle**: This project does not optimize answer quality. It decides whether generation itself should be allowed or prohibited.

- **Single responsibility**: Decide if `retrieved_chunks` is empty before calling LLM
- **Core logic**: `if not chunks: return None` — intentionally trivial
- **Value proposition**: Not the condition itself, but naming it, enforcing it as an execution boundary, and making the decision observable through logs and demos
- **Output philosophy**: Silence is a valid output. This optimizes silence, not answers.
- **Positioning**: Deterministic gate, lightweight integrity check, hard stop on missing evidence
- **Also known as**: `early_exit_guard`, `evidence_presence_check`, `generation_gate`

**This is not a new algorithm.** It is an intentionally simple execution boundary definition.

**This is a boundary enforcement example, not a complete library.**

### This Project Is Not

**Out of scope** (intentionally):
- ❌ Relevance scoring or semantic similarity checks
- ❌ Reranking retrieved chunks
- ❌ Fallback UX or error message generation
- ❌ Answer generation or prompt engineering
- ❌ A drop-in solution or framework extension

**Note**: "Gate" here means an early exit guard, not a state machine or circuit breaker pattern.

---

## Generate-Anyway vs Hard Stop

Most RAG systems follow a **Generate-Anyway** philosophy:
- Retrieved nothing? Generate anyway (hallucinate or hedge)
- Retrieved irrelevant chunks? Generate anyway (confabulate from context)
- Low confidence? Generate anyway (add disclaimers in output)

This project follows a **Hard Stop** philosophy:
- No evidence retrieved → **Immediate stop** → LLM not called
- Generation prohibited at execution boundary, not softened through prompts
- Silence is chosen over speculation

**Why choose silence when evidence is missing?**

| Dimension | Generate-Anyway | Hard Stop (This Project) |
|-----------|----------------|-------------------------|
| **Security** | Hallucinations may leak training data or fabricate sensitive info | No generation = no hallucination surface |
| **Cost** | Pay for every LLM call, even when doomed to fail | LLM call skipped = cost saved |
| **Reliability** | Inconsistent output quality (sometimes good, sometimes hallucinated) | Deterministic: evidence exists → generate; no evidence → stop |
| **Observability** | Failures hidden in generated text, hard to detect | Explicit STOP decision logged with reason code |
| **User trust** | Confident-sounding wrong answers erode trust faster | "I don't have that information" preserves integrity |

**This is not a quality optimization.** Choosing silence does not make answers better. It prevents answers from existing when they should not exist.

---

## Why This Is Not Self-RAG / Adaptive-RAG

This project is often compared to Self-RAG, Adaptive-RAG, and CRAG. **These are not competitors.** This is a **precondition** that runs before those systems.

### Responsibility Scope

| System | What It Optimizes | When It Runs |
|--------|------------------|-------------|
| **Stop-First (this)** | Decides if generation should happen at all | **Before** RAG generation |
| **Self-RAG** | Decides when to retrieve during generation | **During** generation (multi-step) |
| **Adaptive-RAG** | Routes queries to different retrieval strategies | **During** retrieval (query classification) |
| **CRAG** | Refines and validates retrieved chunks | **During** generation (chunk filtering) |

### Key Difference

- **Self-RAG / Adaptive-RAG / CRAG**: "How do we generate better answers given some evidence?"
- **Stop-First**: "Should we generate at all, or enforce silence?"

**Example**:
```python
# Stop-First runs first (precondition)
if not should_generate(chunks):
    return None  # Hard stop, execution ends here

# If we reach this line, chunks exist
# Now Self-RAG / Adaptive-RAG / CRAG can optimize generation
answer = self_rag.generate(query, chunks)  # Uses reflection, retrieval
```

**This does not compete with or replace those systems.** You can use Stop-First as a precondition check, then pass allowed queries to Self-RAG / Adaptive-RAG downstream.

**What Stop-First does NOT do**:
- Does not decide which retrieval strategy to use (that's Adaptive-RAG's job)
- Does not validate chunk relevance during generation (that's Self-RAG's job)
- Does not refine or rerank chunks (that's CRAG's job)

**What Stop-First does**:
- Enforces `if chunks.length == 0 → STOP` as a non-bypassable execution boundary
- Logs the decision for observability
- Prevents LLM call when evidence is absent

---

## The Problem

Standard RAG pipelines call the LLM even when retrieval returns empty chunks, leading to hallucinations and wasted compute.

```python
chunks = retriever.retrieve(query)  # Returns []
answer = llm.generate(query, chunks)  # Generates anyway → hallucination
```

**Result**: Every failed retrieval costs money for a hallucinated answer.

---

## The Solution

Check evidence presence **before** calling LLM. Skip generation when chunks are empty.

```python
chunks = retriever.retrieve(query)

# Early exit guard
if not chunks:
    return None  # LLM not called, generation skipped

answer = llm.generate(query, chunks)
```

**Result**: When `chunks = []`, LLM is never called. No hallucination. Cost saved. Decision logged.

---

## Quick Demo (30 seconds)

**Core logic**: `gate.py::should_generate(chunks)` — single `if not chunks` check
**Minimal demo**: `demos/local/hallucination_prevention/demo_cli.sh`
**Prerequisites**: Python 3 stdlib only, zero dependencies

```bash
git clone https://github.com/Nick-heo-eg/stop-first-rag.git
cd stop-first-rag/demos/local/hallucination_prevention
./demo_cli.sh
```

**What you'll see**:
- Query with 0 chunks → Decision: **STOP** → LLM generation **SKIPPED**
- Query with 3 chunks → Decision: **ALLOW** → LLM generation **ALLOWED**
- Result: 2/3 queries had no evidence → 2 LLM calls skipped

**Execution time**: < 1 second

---

## Core Logic

The entire decision logic is intentionally trivial:

```python
def should_generate(chunks: List[Dict[str, Any]]) -> bool:
    """
    Framework-agnostic early exit guard.

    This is intentionally trivial (if not chunks). The value is not in the
    condition itself, but in naming it, enforcing it as an execution boundary,
    and logging the decision.
    """
    return bool(chunks and len(chunks) > 0)
```

**File**: `gate.py` lines 18-40

**Why this is useful despite being trivial**:
1. **Naming**: Gives the condition a semantic name (`should_generate`)
2. **Boundary enforcement**: Makes the check non-bypassable at the execution layer
3. **Observability**: Decision is logged with structured reason codes
4. **Consistency**: Same check applied uniformly across all queries

---

## Decision Boundary Table

This project only handles **evidence presence**. All other concerns are downstream responsibilities.

| Concern | Handled By This Project | Downstream Responsibility |
|---------|------------------------|---------------------------|
| **Evidence presence** | ✅ Yes — `if not chunks` | - |
| **Evidence relevance** | ❌ No | Your retrieval system (embeddings, reranking) |
| **Evidence quality** | ❌ No | Your retrieval system (scoring, filtering) |
| **Answer generation** | ❌ No | Your LLM + prompt engineering |
| **Fallback UX** | ❌ No | Your application layer |
| **Error messages** | ❌ No | Your application layer |

**Example**: If retrieval returns 3 irrelevant chunks, this gate returns `ALLOW` (chunks exist). Detecting irrelevance is your retrieval system's job.

---

## Framework Integration

The `should_generate()` function is framework-agnostic and can be wrapped in any execution model.

### Standalone Usage

```python
from gate import should_generate

chunks = retriever.retrieve(query)

if not should_generate(chunks):
    return {"answer": None, "reason": "No evidence found"}

answer = llm.generate(query, chunks)
```

### LangGraph Conditional Edge

```python
from gate import should_generate
from langgraph.graph import StateGraph

def evidence_check(state):
    return "generate" if should_generate(state["chunks"]) else "stop"

graph = StateGraph()
graph.add_conditional_edges("retrieve", evidence_check, {
    "generate": "llm_node",
    "stop": "end_node"
})
```

### FastAPI Dependency

```python
from gate import should_generate
from fastapi import Depends, HTTPException

def check_chunks(chunks: List[Dict]) -> List[Dict]:
    if not should_generate(chunks):
        raise HTTPException(status_code=404, detail="No evidence found")
    return chunks

@app.post("/query")
def query_endpoint(chunks: List[Dict] = Depends(check_chunks)):
    return llm.generate(query, chunks)
```

### LangChain Runnable

```python
from gate import should_generate
from langchain.schema.runnable import RunnableLambda

def gate_runnable(inputs):
    if not should_generate(inputs["chunks"]):
        return {"answer": None, "reason": "Evidence missing"}
    return inputs

chain = RunnableLambda(gate_runnable) | llm_chain
```

**Pattern**: Same core function (`should_generate`), different execution wrappers.

---

## Silence Is a Valid Output

Many production systems use fallback responses like "I don't have enough information to answer that question." This seems safe, but it hides the execution decision.

**The problem with fallback-first**:
- **Conceals hallucination risk**: Polite fallback masks that LLM was called with empty context
- **Loses observability**: No structured log of when/why retrieval failed
- **Prevents diagnosis**: Cannot measure retrieval failure rate or identify coverage gaps
- **False comfort**: Users see consistent UX, operators miss systemic retrieval problems

**This project's approach: Hard stop, then log, then optionally fallback**

```python
# Step 1: Hard stop (execution boundary)
if not should_generate(chunks):
    # Step 2: Log decision (observability)
    logger.info("STOP", reason="EVIDENCE_MISSING", query_id=...)

    # Step 3: Fallback (application layer, optional)
    return {"answer": None, "message": "No evidence found"}
```

**Silence (None/null) is the primary output.** Fallback messages are application-layer concerns, not generation decisions.

**Why this matters**:
- In production, fallback-only systems often generate answers with empty chunks, then hide failures in politeness
- Logs show "200 OK" even when retrieval failed → hallucination risk invisible
- Stop-first logs show "STOP" decision → retrieval failure measurable → coverage gaps identifiable

---

## Using the Structured Interface

If you need reason codes for logging or audit:

```python
from gate import check_evidence

chunks = retriever.retrieve(query)
decision = check_evidence(query, chunks)

if decision["status"] == "STOP":
    logger.info(f"Generation skipped: {decision['reason']}")
    return None

answer = llm.generate(query, chunks)
```

**Returns**:
```python
{
    "status": "STOP" | "ALLOW",
    "reason": "EVIDENCE_MISSING" | "EVIDENCE_SUFFICIENT",
    "explanation": "Human-readable explanation"
}
```

---

## Implementation Files

- **`gate.py`** — `should_generate()` function (lines 18-40, ~23 lines including docstring)
- **`gate.py`** — `check_evidence()` function (lines 48-90, ~43 lines) for structured reason codes
- **`demos/local/hallucination_prevention/`** — Working demo (< 1 second execution)
- **`COMPLIANCE.md`** — Enterprise audit trail features (for regulated environments)
- **`CLI_USAGE.md`** — Command-line interface

---

## When to Use This

**Use this pattern if**:
- ✅ Your retrieval sometimes returns empty results (closed domain, out-of-scope queries)
- ✅ You want to measure how often generation is skipped
- ✅ You're running local LLMs (every call costs compute)
- ✅ You need audit trails of generation decisions

**Don't use this if**:
- ❌ Your retrieval always returns results (open domain with massive corpus)
- ❌ You want creative/speculative answers without evidence
- ❌ You need relevance checking (use reranking instead)

---

## Getting Started

1. **See it work**: Run `./demos/local/hallucination_prevention/demo_cli.sh`
2. **Read the core logic**: Check `gate.py` lines 18-40 — the `should_generate()` function
3. **Understand the pattern**: Evidence presence check → Early exit if empty → Log decision
4. **Copy the function**: Paste `should_generate()` into your codebase
5. **Wrap for your framework**: See "Framework Integration" examples above

---

## License

MIT License - See LICENSE file

**This is a reference implementation, not a production-ready library.** Use this pattern to enforce evidence presence checks in your RAG pipeline.

---

**Remember**:
- The value is not in the `if not chunks` condition itself
- The value is in naming it, enforcing it as an execution boundary, and making the decision observable
- Silence is a valid output—this optimizes silence, not answers
- This is not a new algorithm—it is an intentionally simple execution boundary definition
