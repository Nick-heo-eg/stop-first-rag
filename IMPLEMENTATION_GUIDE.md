# Implementation Guide

**How to implement the boundary specification in your system**

> **"Retrieved documents ≠ permission to answer"**
> **"This system does not automate decisions"**

---

## Critical Requirements

### 1. Non-Bypassable Gate Structure

**The gate MUST be positioned:**
```
Query → Retrieve → [BOUNDARY GATE] → Generate → Return
                        ↑
                  NO EXCEPTIONS
            ALL paths pass through here
```

**Prohibited architectures:**
```
❌ Query → Retrieve → Generate → [Filter] → Return
   (Gate after generation = too late)

❌ Query → Retrieve → [Optional Gate] → Generate → Return
   (Optional = bypassable)

❌ Query → Retrieve → [Gate for some queries] → Generate → Return
   (Conditional = bypassable)
```

**Correct architecture:**
```
✅ Query → Retrieve → [MANDATORY GATE] → Generate (if ALLOW) → Return
                                      ↓
                                   STOP (if blocked)
```

---

## Code Structure (Sealed)

### Python Implementation

```python
def answer_query(query: str) -> Response:
    """
    Main query handler.

    The boundary gate CANNOT be skipped.
    No conditional logic. No bypass paths.
    """
    # Step 1: Retrieval
    docs = retrieve_documents(query)

    # Step 2: BOUNDARY GATE (MANDATORY)
    decision = boundary_gate(
        retrieved_docs=bool(docs),
        permission_to_answer=check_permission(query, docs),
        is_decision_request=detect_decision_request(query)
    )

    # Step 3: Conditional execution based on decision
    if decision.decision == "STOP":
        return create_stop_response(decision)
    elif decision.decision == "REVIEW":
        return route_to_human_review(decision)
    else:  # ALLOW
        return generate_answer(query, docs)


def boundary_gate(
    retrieved_docs: bool,
    permission_to_answer: bool,
    is_decision_request: bool
) -> BoundaryDecision:
    """
    Non-bypassable judgment boundary gate.

    Philosophy (enforced):
    - "Retrieved documents ≠ permission to answer"
    - "This system does not automate decisions"
    """
    # Rule 1: Decision automation blocked
    if is_decision_request:
        return BoundaryDecision(
            decision="STOP",
            reason="STOP.DECISION_AUTOMATION_BLOCKED",
            explanation="This system does not automate decisions"
        )

    # Rule 2: Permission required
    if not permission_to_answer:
        return BoundaryDecision(
            decision="STOP",
            reason="STOP.PERMISSION_MISSING",
            explanation="Retrieved documents ≠ permission to answer"
        )

    # Rule 3: Evidence required
    if not retrieved_docs:
        return BoundaryDecision(
            decision="STOP",
            reason="STOP.EVIDENCE_MISSING",
            explanation="No evidence retrieved"
        )

    # All checks passed
    return BoundaryDecision(
        decision="ALLOW",
        reason="Answer permitted"
    )
```

---

## Prohibited Patterns

### ❌ Pattern 1: Conditional Gate
```python
# WRONG: Gate only applied sometimes
def answer_query(query: str) -> Response:
    docs = retrieve_documents(query)

    if user.role == "admin":
        # Admin bypasses gate ← PROHIBITED
        return generate_answer(query, docs)
    else:
        decision = boundary_gate(...)
        # ...
```

**Why prohibited:** Gate MUST be non-bypassable for all users/roles.

---

### ❌ Pattern 2: Fallback Bypass
```python
# WRONG: Fallback bypasses gate
def answer_query(query: str) -> Response:
    docs = retrieve_documents(query)
    decision = boundary_gate(...)

    if decision.decision == "STOP":
        # Try to answer anyway ← PROHIBITED
        try:
            return generate_answer_with_lower_confidence(query, docs)
        except:
            return stop_response(decision)
```

**Why prohibited:** STOP means STOP. No fallbacks.

---

### ❌ Pattern 3: Adapter Override
```python
# WRONG: Adapter can force ANSWER
def boundary_gate(..., adapter_suggestion):
    if adapter_suggestion == "FORCE_ANSWER":
        return BoundaryDecision(decision="ALLOW")  # ← PROHIBITED

    # Normal checks...
```

**Why prohibited:** Philosophy > Adapter. No force mechanisms.

---

## Allowed Expansion Patterns

### ✅ Pattern 1: Enhanced Permission Check
```python
def check_permission(query: str, docs: List[Doc]) -> bool:
    """
    Expand permission calculation logic.
    This is an allowed expansion (gate input).
    """
    # Check document-level permissions
    has_doc_permission = all(doc.allows_answer for doc in docs)

    # Check role-based permissions
    has_role_permission = user.role in ["analyst", "manager"]

    # Check time-based permissions
    permission_not_expired = all(
        doc.permission_expires > now()
        for doc in docs
    )

    return (
        has_doc_permission and
        has_role_permission and
        permission_not_expired
    )
```

**Why allowed:** Enhances gate INPUT without bypassing gate.

---

### ✅ Pattern 2: Evidence Grading
```python
def grade_evidence(docs: List[Doc]) -> EvidenceGrade:
    """
    Add evidence quality assessment.
    This is an allowed expansion (gate input).
    """
    if any(doc.status == "draft" for doc in docs):
        return EvidenceGrade.INVALID

    if any(doc.superseded for doc in docs):
        return EvidenceGrade.INVALID

    if len(docs) < 2:
        return EvidenceGrade.INSUFFICIENT

    if has_conflicts(docs):
        return EvidenceGrade.CONFLICTING

    return EvidenceGrade.SUFFICIENT


def boundary_gate(...):
    # Use evidence grade in decision
    evidence_grade = grade_evidence(docs)

    if evidence_grade == EvidenceGrade.INVALID:
        return BoundaryDecision(
            decision="STOP",
            reason="STOP.EVIDENCE_INVALID"
        )

    # ... rest of checks
```

**Why allowed:** Adds sophistication to evidence check without bypassing gate.

---

### ✅ Pattern 3: New STOP Reason Codes
```python
class StopReason(Enum):
    # Existing codes
    PERMISSION_MISSING = "STOP.PERMISSION_MISSING"
    DECISION_AUTOMATION_BLOCKED = "STOP.DECISION_AUTOMATION_BLOCKED"

    # NEW: Domain-specific codes
    REGULATORY_APPROVAL_PENDING = "STOP.REGULATORY_APPROVAL_PENDING"
    JURISDICTION_MISMATCH = "STOP.JURISDICTION_MISMATCH"
    CONFIDENTIALITY_VIOLATION = "STOP.CONFIDENTIALITY_VIOLATION"


def boundary_gate(...):
    # Use new codes in decisions
    if query_violates_jurisdiction(query, docs):
        return BoundaryDecision(
            decision="STOP",
            reason=StopReason.JURISDICTION_MISMATCH.value,
            explanation="Query jurisdiction does not match document permissions"
        )

    # ... rest of checks
```

**Why allowed:** Expands reason code taxonomy without changing gate structure.

---

## Prohibited Expansion Patterns

### ❌ Expansion 1: RAG Optimization
```python
# PROHIBITED: Do not optimize RAG internals
def better_retrieve(query: str) -> List[Doc]:
    # Improved embeddings
    # Better chunking
    # Reranking
    # ← None of this belongs in this specification
```

**Why prohibited:** This specification defines boundaries, not RAG quality.

---

### ❌ Expansion 2: Answer Generation
```python
# PROHIBITED: Do not add generation improvements
def generate_better_answer(query: str, docs: List[Doc]) -> str:
    # Improved prompts
    # Few-shot examples
    # Model fine-tuning
    # ← None of this belongs in this specification
```

**Why prohibited:** This specification defines WHEN to answer, not WHAT to answer.

---

### ❌ Expansion 3: Force Mechanisms
```python
# PROHIBITED: Do not add override mechanisms
def boundary_gate_with_override(
    ...,
    force_allow: bool = False  # ← PROHIBITED
):
    if force_allow:
        return BoundaryDecision(decision="ALLOW")

    # Normal checks...
```

**Why prohibited:** Gate must be non-bypassable. No exceptions.

---

## Testing Requirements

### Required Tests (Before Every Release)

**5 Core Scenarios:**

```python
def test_1_docs_retrieved_no_permission():
    decision = boundary_gate(
        retrieved_docs=True,
        permission_to_answer=False,
        is_decision_request=False
    )
    assert decision.decision == "STOP"
    assert decision.reason == "STOP.PERMISSION_MISSING"


def test_2_no_docs_has_permission():
    decision = boundary_gate(
        retrieved_docs=False,
        permission_to_answer=True,
        is_decision_request=False
    )
    assert decision.decision == "STOP"
    assert decision.reason == "STOP.EVIDENCE_MISSING"


def test_3_decision_request():
    decision = boundary_gate(
        retrieved_docs=True,
        permission_to_answer=True,
        is_decision_request=True
    )
    assert decision.decision == "STOP"
    assert decision.reason == "STOP.DECISION_AUTOMATION_BLOCKED"


def test_4_adapter_forces_answer():
    decision = boundary_gate(
        retrieved_docs=True,
        permission_to_answer=False,
        is_decision_request=False,
        adapter_suggestion="ALLOW"  # Adapter wants to allow
    )
    # Philosophy overrides adapter
    assert decision.decision == "STOP"
    assert decision.reason == "STOP.PERMISSION_MISSING"


def test_5_adapter_suggests_stop():
    decision = boundary_gate(
        retrieved_docs=True,
        permission_to_answer=True,
        is_decision_request=False,
        adapter_suggestion="STOP"  # Adapter suggests stop
    )
    # Conditions allow, adapter is advisory only
    assert decision.decision == "ALLOW"
```

**All 5 MUST pass. No exceptions.**

---

## CI Configuration

**GitHub Actions example:**

```yaml
name: Boundary Specification Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Run boundary spec tests
        run: python test_boundary_spec.py

      - name: Archive test report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-report
          path: test_report.json
```

**Build MUST fail if any test fails.**

---

## Architecture Layers

**This specification is the TOP layer:**

```
┌────────────────────────────────────────┐
│  BOUNDARY SPECIFICATION (this doc)     │ ← TOP (immutable)
├────────────────────────────────────────┤
│  Adapter Layer (LangChain, custom)     │
├────────────────────────────────────────┤
│  Prompt Layer                          │
├────────────────────────────────────────┤
│  Model Layer (GPT-4, Claude, etc.)     │
└────────────────────────────────────────┘
```

**The specification can:**
- Override any lower layer
- Block any response path
- Enforce STOP regardless of model output

**Lower layers CANNOT:**
- Override the specification
- Bypass the gate
- Convert STOP to ALLOW

---

## Summary

**Required:**
- ✅ Gate positioned after retrieval, before generation
- ✅ Gate is non-bypassable (all paths go through)
- ✅ STOP includes structured reason code
- ✅ UX guidance provided (without automation)
- ✅ 5 core scenarios pass in CI
- ✅ Philosophy enforced: "Retrieved ≠ permission", "No decision automation"

**Prohibited:**
- ❌ Conditional gate execution
- ❌ Bypass mechanisms
- ❌ Adapter override capabilities
- ❌ RAG optimization in this spec
- ❌ Answer generation improvements

**Allowed expansions:**
- ✅ Permission calculation rules
- ✅ Evidence grading logic
- ✅ New STOP reason codes
- ✅ Role scope models

**Core Philosophy:**
> **"Retrieved documents ≠ permission to answer"**
> **"This system does not automate decisions"**

**Positioning:**
> **"This is not a system that answers questions well.**
> **This is a system that distinguishes when answering is permitted."**

---
