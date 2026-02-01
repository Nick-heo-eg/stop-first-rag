# Stop-First RAG → Regulated Write Firewall

AI가 이메일을 보냈을 때
누가 승인했는지 증명할 수 없는 시스템은
기술 문제가 아니라 책임 문제다.

When an AI sends an email,
a system that cannot prove who approved it
has a responsibility problem, not a technical one.

---

## Position

This repository is part of the **Judgment Boundary** work:
a set of experiments and specifications focused on
*when AI systems must stop or not execute*.

See the overarching map:
→ [JUDGMENT_BOUNDARY_MANIFEST.md](JUDGMENT_BOUNDARY_MANIFEST.md)

---

**Repository Evolution**: This repository originated as a reference implementation for RAG evidence gating. It has evolved to include execution governance for production AI agents.

---

## Quick Navigation

### Core Documents (New)

- **[MISSION.md](MISSION.md)** — Why we exist ("조직 생존 구조")
- **[INTERNAL_STANDARDS.md](INTERNAL_STANDARDS.md)** — Foundation principles (immutable)
- **[Product Pitch](docs/REGULATED_WRITE_FIREWALL_PITCH.md)** — Go-to-market positioning
- **[Technical Implementation](examples/halt_v01_skeleton.py)** — HALT v0.1 skeleton (production-ready)

### Strategic Documents

- **[Positioning Strategy](examples/POSITIONING_STRATEGY.md)** — Market positioning analysis
- **[Hybrid Interface Spec](examples/HYBRID_INTERFACE_SPEC.md)** — CrewAI ↔ LangGraph integration
- **[Guard Integration](examples/GUARD_INTEGRATION.md)** — Bash guard + HALT pipeline

---

## What This Repository Contains

### 1. Stop-First RAG (Original)

**Purpose**: Evidence presence gate for RAG pipelines

**Core principle**: "Don't answer" is a first-class system outcome, not an accident or fallback.

**Status**: Reference implementation (see below for original documentation)

---

### 2. HALT Loop (Human-Approved Lifecycle for Tasks)

**Purpose**: Execution governance for AI agents

**Core principle**: AI cannot execute external writes without human approval and cryptographic proof.

**Architecture**:
```
planner → risk_extract → det_judge
            ↓ HOLD         ↓ ALLOW         ↓ STOP
      human_interrupt   write_barrier    end_stop
            ↓                 ↓
      release_gate      tool_executor
            ↓                 ↓
      det_judge (re-eval)   END
```

**Key files**:
- `examples/halt_v01_skeleton.py` — Production-ready reference
- `examples/langgraph_halt_loop.py` — Original (deprecated, use v0.1)
- `examples/guard_integrated_halt.py` — Bash guard integration

---

### 3. Regulated Write Firewall (Core Product)

**Position**: Accountability infrastructure for production AI agents

**Value proposition**:
> "No write without proof. AI stops before external execution. When released, cryptographic evidence survives."

**Target market**:
- Fintech (규제 강함, 돈 많음)
- Healthcare (개인정보보호법, HIPAA)
- Enterprise GRC (준법감시, 감사 대응)

**Differentiation**:
| Aspect | LangChain/CrewAI | Regulated Write Firewall |
|--------|------------------|--------------------------|
| Purpose | Agent orchestration | **Write governance** |
| Write control | Agent executes directly | **Firewall blocks** |
| Enforcement | Prompt-dependent | **Code-level gates** |
| Audit trail | Conversation logs | **Proof Capsule (불변)** |
| Accountability | Vague | **Owner-of-Record 명시** |

**Status**: Product positioning locked, PoC ready

---

## Repository Mission

> **우리는 지능을 높이는 회사를 만드는 게 아니다.**
>
> **사고가 났을 때 조직이 살아남게 만드는 구조를 만든다.**

See [MISSION.md](MISSION.md) for full context.

---

## From Concept to Structure

**stop-first-rag** (this repository):
- Problem framing: "AI가 멈춰야 하는 이유"
- Philosophical foundation
- "STOP is cheaper than scaling"

**Implementation**:
- Production runtime: In development (private)
- Open-source release: TBD
- Early access: Contact via GitHub issues or repository discussions

**Relationship**: This repository defines the problem and philosophy. The production implementation (HALT loop, Proof Capsule, Write Barrier) is being developed separately as a regulated write firewall system.

---

## For New Contributors

**Read in this order**:

1. **[MISSION.md](MISSION.md)** — Identity (5 min)
2. **[INTERNAL_STANDARDS.md](INTERNAL_STANDARDS.md)** — Principles (15 min)
3. **[examples/halt_v01_skeleton.py](examples/halt_v01_skeleton.py)** — Implementation (30 min)
4. **[Product Pitch](docs/REGULATED_WRITE_FIREWALL_PITCH.md)** — Market context (20 min)

**If you disagree with the mission**, this project may not be the right fit. We optimize for organizational survival, not AI intelligence.

---

# Original: Stop-First RAG Documentation

**Layer:** Execution / Mechanism

**Reference implementation** of pre-generation gating applied to RAG systems.

> **For benchmark results and empirical validation**, see:
> → [llm-gating-bench](https://github.com/Nick-heo-eg/llm-gating-bench)

---

## Governance

**Constitutional Conformity**: This project conforms to an internal judgment-boundary constitutional specification (private).

> **Public repos argue. Private repos decide.**

---

## What This Repo Is

This repository demonstrates **RAG-specific patterns** for deciding whether to call an LLM before generation:

- Evidence presence checks (`if not chunks: return None`)
- Document conflict detection (when retrieved chunks disagree)
- Retrieval score thresholds (BM25 filtering)
- Typed stop reasons (`no_data`, `conflict`, `low_confidence`)

**Core principle**: "Don't answer" is a first-class system outcome, not an accident or fallback.

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

## Failure Modes Explicitly Modeled

This project treats *not answering* as a first-class system outcome.

| Scenario | Typical RAG Behavior | Stop-First RAG Outcome |
|--------|----------------------|------------------------|
| No relevant data exists | Hallucinates an answer | STOP (NoEvidence) |
| Data is partial or outdated | Fills gaps implicitly | STOP (InsufficientEvidence) |
| Retriever returns plausible but wrong chunks | Blends into response | STOP (ConflictDetected) |
| Model confidence is low | Hidden from user | STOP (LowConfidence) |
| Query is out of system scope | Attempts anyway | STOP (OutOfScope) |

**STOP is not a fallback. It is an explicit, typed system outcome.**

See `gate.py::StopReason` (lines 115-142) for the complete enumeration of stop reasons used in production scenarios.

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

## Intended Use Cases

- Local LLM deployments where incorrect answers are worse than silence
- Systems that must explicitly represent retrieval failure
- Pipelines that require auditability of non-answers
- Regulated or safety-sensitive domains

## Non-Goals

- Maximizing answer rate
- Convenience-first "answer anyway" UX
- Hiding uncertainty for smoother demos

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
