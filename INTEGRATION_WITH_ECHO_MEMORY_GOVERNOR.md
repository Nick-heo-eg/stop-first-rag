# Integration with Echo Memory Governor

**RAG does not strengthen answers. It exposes evidence snapshots.**

---

## What Changed

### Removed (Intentionally)

❌ **Vector similarity scores** — RAG results no longer ranked by similarity score
❌ **Confidence-based ranking** — Context not selected by confidence threshold
❌ **Automatic context augmentation** — No hidden context injection based on scores
❌ **Pending item inclusion** — Pending layer NEVER exposed in RAG context

### Added

✅ **Snapshot ID in every RAG result** — All context traced to specific snapshot
✅ **Lineage metadata** — RAG results include parent chain information
✅ **Approval provenance** — Context shows how memory was approved
✅ **Pending exclusion enforcement** — Snapshots filter pending items automatically

---

## What This Integration Prevents

### 1. RAG without Evidence Snapshot

**Before:**
```python
rag_result = {
    "answer": "User prefers UTC timestamps",
    "context": [
        {"text": "..."},
        {"text": "..."}
    ],
    "similarity_score": 0.92  # Hidden scoring
}
```

**After:**
```python
rag_result = {
    "answer": "User prefers UTC timestamps",
    "context": [
        {
            "text": "...",
            "snapshot_id": "snap_123",  # REQUIRED
            "memory_id": "mem_456",
            "approved_by": "human",
            "approved_at": "2026-01-10T12:00:00Z"
        }
    ],
    "snapshot_lineage": {
        "snapshot_id": "snap_123",
        "parent_snapshot_id": "snap_122",
        "depth": 5
    }
}
```

Every RAG result **points to a snapshot**. No hidden context.

---

### 2. Vector Score-Based Ranking GONE

**Before:**
```python
# Select top K by similarity score
context = sorted(results, key=lambda x: x['score'], reverse=True)[:5]
```

**After:**
```python
# Select ALL approved memory from snapshot (no scoring)
context = snapshot["memory"]["approved_items"]

# OR: Filter by memory type (still no scoring)
context = [
    item for item in snapshot["memory"]["approved_items"]
    if item["type"] == "user_preference"
]
```

Context selection based on **snapshot membership**, not scores.

---

### 3. Pending Items NEVER in RAG Context

**Before:**
```python
# Context might include pending items (HIGH RISK)
context = get_all_items(entity_id="user_001")  # Includes pending
```

**After:**
```python
# Context ONLY from snapshot (pending automatically excluded)
snapshot = governor_client.get_snapshot_view(snapshot_id="snap_123")
context = snapshot["memory"]["approved_items"]  # Pending filtered

# If pending detected → raises PendingLeakError
```

Snapshots **constitutionally exclude** pending items.

---

## How Automation Disappeared (Intentionally)

### Similarity-based context injection: GONE

**Before:** Top K documents by similarity score automatically added to context
**After:** Context = snapshot approved memory. No similarity ranking.

### Confidence-based filtering: GONE

**Before:** Only include context items with confidence > 0.8
**After:** NO confidence field. All approved memory is equal.

### Dynamic context expansion: GONE

**Before:** Automatically fetch related documents based on embeddings
**After:** Context = single snapshot. No automatic expansion.

---

## Where Auditability Emerged

### 1. Every RAG call cites a snapshot

```python
rag_response = {
    "answer": "...",
    "evidence_snapshot": {
        "snapshot_id": "snap_123",
        "audit_url": "GET /audit/snapshot/snap_123",
        "memory_count": 5,
        "lineage_depth": 3
    }
}
```

External observer can verify:
- Which memory influenced the answer
- How that memory was approved
- What the lineage chain is

---

### 2. Lineage shows memory origin

```python
lineage_audit = governor_client.get_lineage_view(snapshot_id="snap_123")

# Shows:
# - Genesis → current snapshot chain
# - Memory deltas (what was added when)
# - Approval events for each memory item
```

Every piece of context is **traceable to its approval event**.

---

### 3. Rejection history auditable

```python
# If RAG attempted to use forbidden content (rejected)
rejection_audit = governor_client.get_rejection_view(
    from_timestamp="2026-01-10T00:00:00Z",
    to_timestamp="2026-01-10T23:59:59Z"
)

# Shows:
# - Negative memory violations
# - Rejection reason codes
# - What was attempted but refused
```

---

## Integration Files

```
integration/
├── GOVERNOR_INTEGRATION.md         # Integration overview
├── snapshot_context_builder.py     # Build RAG context from snapshot
├── rag_evidence_formatter.py       # Format RAG output with snapshot reference
└── pending_exclusion_test.py       # Verify pending never in context
```

---

## Example: RAG with Snapshot Evidence

```python
from integration.snapshot_context_builder import build_rag_context_from_snapshot
from integration.rag_evidence_formatter import format_rag_response_with_evidence

# 1. Get snapshot (NOT raw database query)
snapshot_id = "snap_123"
snapshot = governor_client.get_snapshot_view(snapshot_id)

# 2. Build context from approved memory ONLY
context = build_rag_context_from_snapshot(snapshot)

# 3. Run RAG (no scoring, just approved memory)
answer = rag_model.generate(
    query="What are user's preferences?",
    context=context
)

# 4. Format response with evidence
rag_response = format_rag_response_with_evidence(
    answer=answer,
    snapshot_id=snapshot_id,
    snapshot_lineage=snapshot["lineage"]
)

# Output:
# {
#   "answer": "User prefers UTC timestamps",
#   "evidence_snapshot": {
#     "snapshot_id": "snap_123",
#     "audit_url": "GET /audit/snapshot/snap_123",
#     "memory_count": 5,
#     "lineage_depth": 3,
#     "parent_snapshot_id": "snap_122"
#   },
#   "context_items": [
#     {
#       "memory_id": "mem_456",
#       "content": {...},
#       "approved_by": "human",
#       "approved_at": "2026-01-10T12:00:00Z"
#     }
#   ]
# }
```

---

## What This Proves

1. **RAG can cite evidence** — Every answer references a snapshot
2. **Scoring can be refused** — Context not ranked by similarity
3. **Pending cannot leak** — Snapshots constitutionally exclude pending
4. **Lineage is auditable** — All context traces to approval events

---

**This integration proves RAG can be grounded without hidden scoring or automatic context expansion.**

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
