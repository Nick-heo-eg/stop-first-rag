# Stop-First RAG

**One line**: Check evidence before calling LLM → skip generation when chunks are empty → prevent hallucinations and save costs.

---

## The Problem

You're using RAG, but even when no relevant chunks are retrieved, your LLM still generates an answer—hallucinating and wasting money.

```python
chunks = retriever.retrieve(query)  # Returns []
answer = llm.generate(query, chunks)  # Generates anyway → hallucination
```

**Every time your retriever fails, you pay for a hallucinated answer.**

---

## The Solution

This repo provides a **stop-first filter** that runs before your LLM call.

**Not** a better RAG. **Not** a better LLM. Just a filter that **skips generation when evidence is missing**.

```python
chunks = retriever.retrieve(query)

# NEW: Check evidence first
if len(chunks) == 0:
    return None  # LLM not called, generation skipped

answer = llm.generate(query, chunks)
```

**What happens**: When `chunks = []`, LLM never gets called. No hallucination. Cost saved. Reason logged.

---

## Quick Start (30 seconds)

### Option 1: Run the demo

```bash
git clone https://github.com/yourusername/stop-first-rag.git
cd stop-first-rag/demos/local/hallucination_prevention
./demo_cli.sh
```

**What you'll see**:
```
Query: What is the CEO's salary?
  Retrieved chunks: 0
  Decision: STOP
  🚫 LLM generation: SKIPPED (not called)
  ✅ Hallucination prevented
```

### Option 2: Copy-paste this code

```python
# Add to your existing RAG pipeline
from gate import check_evidence

query = "What is the CEO's salary?"
chunks = retriever.retrieve(query)

# Check evidence before LLM
decision = check_evidence(query, chunks)

if decision["status"] == "STOP":
    print(f"Generation skipped: {decision['reason']}")
    # LLM not called, no cost, no hallucination
else:
    answer = llm.generate(query, chunks)
```

**File**: `gate.py` (included in this repo)

---

## How to Plug Into Your Existing RAG

### Your Current Pipeline (Any Framework)

**LangChain**:
```python
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
answer = qa_chain.run(query)  # Always calls LLM
```

**LlamaIndex**:
```python
from llama_index import VectorStoreIndex

index = VectorStoreIndex.from_documents(docs)
answer = index.as_query_engine().query(query)  # Always calls LLM
```

**Custom Pipeline**:
```python
chunks = retriever.retrieve(query)
answer = llm.generate(query, chunks)  # Always calls LLM
```

---

### Add Stop-First Filter (Same Pattern for All)

**LangChain**:
```python
from gate import check_evidence

# Wrap your chain
chunks = retriever.get_relevant_documents(query)
decision = check_evidence(query, chunks)

if decision["status"] == "STOP":
    return {"answer": None, "reason": decision["reason"]}

answer = qa_chain.run(query)  # Only called if evidence verified
```

**LlamaIndex**:
```python
from gate import check_evidence

# Wrap your query
nodes = retriever.retrieve(query)
chunks = [{"text": n.text} for n in nodes]
decision = check_evidence(query, chunks)

if decision["status"] == "STOP":
    return {"answer": None, "reason": decision["reason"]}

answer = query_engine.query(query)  # Only called if evidence verified
```

**Custom Pipeline**:
```python
from gate import check_evidence

chunks = retriever.retrieve(query)
decision = check_evidence(query, chunks)

if decision["status"] == "STOP":
    return {"answer": None, "reason": decision["reason"]}

answer = llm.generate(query, chunks)  # Only called if evidence verified
```

**Pattern**: Same 4 lines for any RAG framework.

---

## What This Is NOT

| System | What It Does | What Stop-First Does |
|--------|--------------|---------------------|
| **Self-RAG** | Decides when to retrieve during generation | Decides if generation should happen at all |
| **Adaptive-RAG** | Routes queries to different retrieval strategies | Blocks generation when evidence is missing |
| **Corrective-RAG** | Refines retrieved chunks during generation | Stops before generation if chunks are empty |

**This does NOT**:
- ❌ Improve retrieval quality (use better embeddings for that)
- ❌ Improve generation quality (use better prompts for that)
- ❌ Learn or adapt (it's a static check)
- ❌ Replace your RAG system

**This DOES**:
- ✅ Skip LLM calls when evidence is missing
- ✅ Return structured reasons (`EVIDENCE_MISSING`, `EVIDENCE_CONFLICT`)
- ✅ Log generation decisions for audit

**Position**: Runs **before** your RAG generates. Compatible with Self-RAG, Adaptive-RAG, etc.

---

## When to Use

**Use this if**:
- ✅ Your RAG sometimes retrieves no relevant chunks (closed knowledge base, out-of-scope queries)
- ✅ You're running local LLMs (every call costs time/compute)
- ✅ You see hallucinations in your logs from queries with no evidence

**Don't use this if**:
- ❌ Your retriever always finds relevant chunks (open domain Q&A with massive corpus)
- ❌ You want hallucinations (creative writing, brainstorming)
- ❌ You don't have a RAG pipeline yet (build that first)

---

## Demo: Hallucination Prevention

See stop-first filtering in action:

```bash
cd demos/local/hallucination_prevention
./demo_cli.sh
```

**Output**:
```
Query: What is the CEO's salary?
  Retrieved chunks: 0
  Decision: STOP
  Reason: EVIDENCE_MISSING
  🚫 LLM generation: SKIPPED (not called)

Query: Who won the 2025 Super Bowl?
  Retrieved chunks: 0
  Decision: STOP
  🚫 LLM generation: SKIPPED (not called)

Query: What is quantum computing?
  Retrieved chunks: 3
  Decision: ALLOW
  ✅ LLM generation: ALLOWED (proceeds to LLM)

Results:
  LLM calls: 1 (out of 3 queries)
  LLM calls skipped: 2
  Hallucinations prevented: 2
```

**Key insight**: 2 out of 3 queries had no evidence. Standard RAG would call LLM 3 times (2 hallucinations). Stop-first called LLM 1 time (0 hallucinations).

---

## Implementation Files

- **`gate.py`** - Core evidence checking logic (when to stop vs allow)
- **`demos/local/hallucination_prevention/`** - Working demo with test queries
- **`COMPLIANCE.md`** - Enterprise compliance features (audit trails, regulatory use)

---

## Enterprise & Compliance

For organizations requiring audit trails, regulatory compliance (EU AI Act, GDPR, HIPAA), or enterprise deployment patterns:

→ **See [COMPLIANCE.md](COMPLIANCE.md)**

---

## The Value

**Standard RAG**: Calls LLM on every query → some hallucinate → you log failures after the fact

**Stop-first RAG**: Checks evidence first → skips LLM when missing → logs refusal with reason

**Result**: LLM not called = cost saved + no hallucination generated + reason logged

**The fact that generation did not happen is itself the value.**

---

## Getting Started

1. **See it work**: Run `./demos/local/hallucination_prevention/demo_cli.sh`
2. **Understand the pattern**: Check evidence → STOP if missing → Only call LLM if verified
3. **Plug into your RAG**: Add 4 lines (see "How to Plug In" above)
4. **Check your logs**: Look for `generation_skipped: true` entries

---

## License

MIT License - See LICENSE file

**No claims regarding production readiness or legal sufficiency.** Use this to prevent hallucinations and reduce wasted LLM calls in your RAG pipeline.

---

**Remember**: The system works when it says STOP. That's when it prevented a hallucination and saved you money.
