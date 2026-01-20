# Hallucination Prevention Demo

This demo shows how stop-first RAG prevents hallucinations by **skipping LLM generation** when no evidence exists.

## What This Demo Shows

**Core principle**: No evidence → No generation → Logged reason

Instead of letting the LLM hallucinate an answer when no relevant chunks are retrieved, stop-first RAG:
1. Checks evidence before calling your LLM
2. Skips generation if evidence is missing
3. Returns a structured STOP decision with a clear reason
4. Logs the fact that generation was not attempted

## Test Scenarios

### Scenario 1: Missing Evidence (CEO Salary)
**Query**: "What is the CEO's salary?"
**Retrieved Chunks**: Empty (no salary information in knowledge base)
**Expected Decision**: **STOP**
**Reason**: `EVIDENCE_MISSING`

**Standard RAG behavior**:
- Calls LLM with empty chunks
- LLM hallucinates a plausible but wrong answer

**Stop-first behavior**:
- Detects no evidence exists
- **LLM generation skipped** (not called at all)
- Returns "Cannot answer - no evidence found" with structured reason
- Logs: `{"decision": "STOP", "reason": "EVIDENCE_MISSING", "generation_skipped": true}`

---

### Scenario 2: Out-of-Scope Query (Future Event)
**Query**: "Who won the 2025 Super Bowl?"
**Retrieved Chunks**: Empty (event hasn't happened yet)
**Expected Decision**: **STOP**
**Reason**: `EVIDENCE_MISSING`

**Standard RAG behavior**:
- Calls LLM with empty chunks
- LLM either hallucinates a winner or gives confused response

**Stop-first behavior**:
- Detects no evidence available
- **LLM generation skipped**
- Returns "Cannot answer - no evidence available"
- Logs: Decision made, generation not attempted

---

### Scenario 3: Evidence Found (Quantum Computing)
**Query**: "What is quantum computing?"
**Retrieved Chunks**: 3 relevant chunks from knowledge base
**Expected Decision**: **ALLOW**
**Reason**: Evidence sufficient

**Standard RAG behavior**:
- Calls LLM with chunks
- Generates answer

**Stop-first behavior**:
- Verifies evidence exists (3 chunks found)
- **Allows LLM generation to proceed**
- LLM generates answer (same as standard RAG)
- Logs: `{"decision": "ALLOW", "reason": "EVIDENCE_SUFFICIENT", "chunks": 3}`

---

## Running the Demo

### CLI Version (Quick)

```bash
./demo_cli.sh
```

Expected output:
```
=== Hallucination Prevention Demo ===

Query 1: What is the CEO's salary?
Decision: STOP
Reason: EVIDENCE_MISSING
Explanation: No relevant chunks retrieved. Cannot generate answer without evidence.
✅ Hallucination prevented

Query 2: Who won the 2025 Super Bowl?
Decision: STOP
Reason: EVIDENCE_MISSING
Explanation: No chunks retrieved for future event. Cannot answer.
✅ Hallucination prevented

Query 3: What is quantum computing?
Decision: ALLOW
Reason: Evidence sufficient (3 chunks retrieved)
Explanation: Relevant evidence found. Safe to generate.
✅ Generation permitted

=== Results ===
Total queries: 3
ALLOW: 1 (33%)
STOP: 2 (67%)

Hallucinations prevented: 2
```

### Python Version (Detailed)

```bash
python demo.py
```

Shows full decision details including evidence status, chunk count, and structured reasons.

---

## Key Takeaway

**67% STOP rate is not a failure.**

It means:
- 2 queries had no evidence → **LLM generation skipped** → No hallucination generated
- 1 query had evidence → **LLM generation allowed** → Safe to generate

**Standard RAG would**:
- Call LLM 3 times
- Generate 3 answers (2 hallucinated, 1 correct)

**Stop-first RAG does**:
- Check evidence first
- Call LLM only 1 time (when evidence verified)
- Generate 1 answer (0 hallucinated)
- Save 2 LLM calls (cost saved)

**The value**: Your LLM never gets called on queries with no evidence. Generation is skipped, and you get a log explaining why.

---

## Files

- `demo_cli.sh` - Quick demo runner
- `demo.py` - Full Python implementation
- `data/candidates/` - Test queries (JSON)
- `data/chunks/` - Evidence chunks (JSONL, some empty)
- `policy.yaml` - Evidence checking policy

---

## Extending This Demo

Add your own test cases:

1. Create `data/candidates/query4_yourtest.json`:
```json
{
  "query_id": "query4",
  "query": "Your question here",
  "expected_decision": "STOP",
  "expected_reason": "EVIDENCE_MISSING"
}
```

2. Create `data/chunks/query4_yourtest.jsonl`:
```jsonl
{"chunk_id": "1", "text": "Relevant evidence if any"}
```

3. Run demo - it will automatically test your new case

---

**Remember**: STOP is a feature, not a bug. It prevents your LLM from making things up.
