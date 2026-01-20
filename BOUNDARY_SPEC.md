# Boundary Specification

**System-level judgment boundary contract**

**Version:** 1.0
**Status:** Immutable specification
**Type:** Top-level boundary contract

---

## Core Principle

> **"Retrieved documents ≠ permission to answer"**

> **"This system does not automate decisions"**

---

## What This Specification Defines

This is **NOT**:
- ❌ A feature
- ❌ A library
- ❌ A framework component
- ❌ An optional safety layer

This **IS**:
- ✅ A system-level contract
- ✅ A non-bypassable judgment boundary
- ✅ A specification for "when NOT to answer"
- ✅ The top-most layer in any system architecture

---

## Architectural Position

**This specification defines the TOP layer:**

```
┌─────────────────────────────────────────────────┐
│         STOP-FIRST BOUNDARY (THIS SPEC)         │ ← TOP LAYER
│   Non-bypassable gate: "Can we answer?"         │   (Immutable)
├─────────────────────────────────────────────────┤
│              Adapter Layer                       │
│   (LangChain, LlamaIndex, custom, etc.)         │
├─────────────────────────────────────────────────┤
│              Prompt Layer                        │
│   (System prompts, few-shot examples)           │
├─────────────────────────────────────────────────┤
│              Model Layer                         │
│   (GPT-4, Claude, Llama, etc.)                  │
└─────────────────────────────────────────────────┘
```

**Boundary enforcement point:**
```
Query → Retrieve → [BOUNDARY GATE] → Generate → Return
                         ↑
                    THIS SPEC
              (non-bypassable)
```

**The gate MUST:**
- Be positioned after retrieval, before generation
- Be non-bypassable (no code path can skip it)
- Return structured decisions (ALLOW/REVIEW/STOP)
- Enforce judgment boundaries, not optimize answers

---

## Decision Types

### 1. ALLOW
**Meaning:** Evidence sufficient, answer generation permitted

**Conditions:**
- Permission to answer: TRUE
- Is decision request: FALSE
- Evidence status: Valid

**Output:**
```json
{
  "decision": "ALLOW",
  "reason": "Answer permitted",
  "proceed_to_generation": true
}
```

---

### 2. REVIEW
**Meaning:** Evidence exists but requires human judgment

**Conditions:**
- Evidence conflicts detected
- Multiple valid interpretations
- Discretionary judgment required

**Output:**
```json
{
  "decision": "REVIEW",
  "reason": "REVIEW.EVIDENCE_CONFLICT",
  "guidance": "Route to human review queue"
}
```

---

### 3. STOP
**Meaning:** Answer generation prohibited (NORMAL outcome, not error)

**STOP is a valid, first-class outcome.**

**Conditions:**
- Permission to answer: FALSE
- Is decision request: TRUE
- Evidence insufficient
- Evidence invalid

**Output:**
```json
{
  "decision": "STOP",
  "reason": "STOP.PERMISSION_MISSING",
  "guidance": "Request permission from document owner",
  "next_actions": ["request_permission", "add_evidence", "reframe_question"]
}
```

---

## STOP Reason Codes

**All STOP outcomes MUST include a structured reason code.**

### Category 1: Permission
- `STOP.PERMISSION_MISSING` – No permission to generate answer
- `STOP.PERMISSION_EXPIRED` – Permission revoked or expired
- `STOP.PERMISSION_SCOPE_VIOLATED` – Query outside permission scope

### Category 2: Decision Automation
- `STOP.DECISION_AUTOMATION_BLOCKED` – This system does not automate decisions
- `STOP.APPROVAL_REQUEST_BLOCKED` – Approval requests cannot be automated
- `STOP.JUDGMENT_REQUIRED` – Human judgment required

### Category 3: Evidence
- `STOP.EVIDENCE_INSUFFICIENT` – Not enough evidence to answer
- `STOP.EVIDENCE_MISSING` – No evidence found
- `STOP.EVIDENCE_INVALID` – Evidence status invalid (draft, superseded, etc.)
- `STOP.EVIDENCE_CONFLICT` – Evidence conflicts, cannot resolve

### Category 4: Boundary
- `STOP.OUT_OF_SCOPE` – Query outside system scope
- `STOP.UNSAFE_QUERY` – Query violates safety boundaries
- `STOP.DISCRETION_REQUIRED` – Query requires discretionary judgment

---

## Structural Requirements

### 1. Non-Bypassable Gate

**Every response path MUST pass through the gate:**

```python
def answer_query(query: str, docs: List[Doc]) -> Response:
    # Step 1: Retrieve (RAG layer)
    retrieved_docs = retrieve(query)

    # Step 2: Boundary Gate (THIS SPEC - CANNOT BE SKIPPED)
    decision = boundary_gate(
        query=query,
        docs=retrieved_docs,
        permission=check_permission(query),
        is_decision_request=detect_decision_request(query)
    )

    # Step 3: Conditional generation
    if decision.status == "ALLOW":
        return generate_answer(query, retrieved_docs)
    elif decision.status == "REVIEW":
        return route_to_human(decision)
    else:  # STOP
        return stop_response(decision)
```

**Prohibited:**
- Skipping the gate
- Bypassing with fallback logic
- Overriding STOP with adapter logic
- Conditional gate application

**The gate is ALWAYS executed. No exceptions.**

---

### 2. Code-Test-Doc 1:1 Correspondence

**Every specification statement MUST have:**

1. **Code implementation**
   ```python
   if not permission_to_answer:
       return Decision.STOP, "STOP.PERMISSION_MISSING"
   ```

2. **Test case**
   ```python
   def test_permission_missing():
       decision = gate(permission_to_answer=False)
       assert decision.status == "STOP"
       assert decision.reason == "STOP.PERMISSION_MISSING"
   ```

3. **Documentation**
   ```markdown
   ## STOP.PERMISSION_MISSING
   When permission to answer is missing, the gate returns STOP.
   ```

**No code without tests. No tests without docs. No docs without code.**

---

## 5 Core Scenarios (CI Validation Required)

**These scenarios MUST be validated in CI before every release:**

### Scenario 1: Documents Retrieved + Permission Missing
```python
Input:
  retrieved_docs: True
  permission_to_answer: False
  is_decision_request: False

Expected:
  decision: STOP
  reason: STOP.PERMISSION_MISSING
  guidance: "Request permission from document owner"
```

### Scenario 2: No Documents + Permission Granted
```python
Input:
  retrieved_docs: False
  permission_to_answer: True
  is_decision_request: False

Expected:
  decision: STOP
  reason: STOP.EVIDENCE_MISSING
  guidance: "Add relevant documents or reframe question"
```

### Scenario 3: Decision Request
```python
Input:
  retrieved_docs: True
  permission_to_answer: True
  is_decision_request: True

Expected:
  decision: STOP
  reason: STOP.DECISION_AUTOMATION_BLOCKED
  guidance: "This system does not automate decisions"
```

### Scenario 4: Adapter Attempts to Force ANSWER
```python
Input:
  retrieved_docs: True
  permission_to_answer: False
  adapter_suggestion: ANSWER

Expected:
  decision: STOP  # Philosophy overrides adapter
  reason: STOP.PERMISSION_MISSING
  note: "Adapter suggestion ignored (philosophy takes precedence)"
```

### Scenario 5: Adapter Suggests STOP (but conditions allow)
```python
Input:
  retrieved_docs: True
  permission_to_answer: True
  is_decision_request: False
  adapter_suggestion: STOP

Expected:
  decision: ALLOW  # Conditions satisfied
  reason: "Answer permitted"
  note: "Adapter suggestion is advisory only"
```

**CI MUST:**
- Run all 5 scenarios on every commit
- Fail build if any scenario fails
- Archive test results as artifacts
- Generate human-readable test report

---

## UX Guidance for STOP Outcomes

**When STOP occurs, the system MUST provide:**

1. **Clear reason code**
   - `STOP.PERMISSION_MISSING`

2. **Human-readable explanation**
   - "Answer generation blocked: No permission to answer based on these documents"

3. **Next action guidance** (NOT automated)
   - "You can: Request permission from document owner"
   - "You can: Add documents with explicit permission"
   - "You can: Reframe your question to match available permissions"

4. **No automated judgment**
   - ❌ Do NOT auto-request permission
   - ❌ Do NOT auto-select next action
   - ❌ Do NOT suggest "best" action

**Example STOP response:**

```json
{
  "decision": "STOP",
  "reason": "STOP.PERMISSION_MISSING",
  "explanation": "Retrieved documents do not include permission to generate answers",
  "guidance": {
    "primary_message": "This system does not automate decisions",
    "next_actions": [
      {
        "action": "request_permission",
        "description": "Request permission from document owner or administrator"
      },
      {
        "action": "add_evidence",
        "description": "Add documents that explicitly grant answer permission"
      },
      {
        "action": "reframe_question",
        "description": "Reframe your question to match available permissions"
      }
    ],
    "note": "The system will not automatically choose an action. You must decide."
  }
}
```

---

## Positioning Statement

**Use this exact wording in all external communication:**

> **"This is not a system that answers questions well.**
> **This is a system that distinguishes when answering is permitted."**

Alternative phrasings:
- "We don't optimize answers. We verify permission to answer."
- "Not better answers. Better judgment boundaries."
- "This system decides whether to answer, not what to answer."

**Prohibited phrasings:**
- ❌ "Safer RAG"
- ❌ "Better retrieval"
- ❌ "Reduced hallucination"
- ❌ "More accurate answers"

**This is NOT a safety feature.**
**This is a judgment boundary layer.**

---

## Expansion Policy

**Future expansion is ONLY permitted in these directions:**

### ✅ Allowed Expansions (Gate Inputs)

1. **Permission calculation rules**
   - More sophisticated permission models
   - Role-based permission scopes
   - Time-based permission expiry

2. **Evidence grading**
   - Evidence quality levels (draft, approved, final)
   - Evidence freshness checks
   - Evidence source verification

3. **Role scope calculation**
   - User role definitions
   - Query scope matching
   - Cross-role permission aggregation

4. **Additional STOP reason codes**
   - More granular STOP categories
   - Domain-specific reasons
   - Jurisdiction-specific blocks

### ❌ Prohibited Expansions

1. **RAG internals**
   - Do NOT optimize retrieval
   - Do NOT improve embeddings
   - Do NOT tune ranking algorithms

2. **Answer generation**
   - Do NOT improve answer quality
   - Do NOT add prompt engineering
   - Do NOT fine-tune models

3. **Bypass mechanisms**
   - Do NOT add "force answer" modes
   - Do NOT add "skip gate for admin" logic
   - Do NOT add conditional gate execution

**If it's not a gate input, it doesn't belong in this specification.**

---

## Implementation Checklist

**Before any release, verify:**

- [ ] Gate is positioned after retrieve, before generate
- [ ] Gate is non-bypassable (no code path skips it)
- [ ] All 5 core scenarios pass in CI
- [ ] Every STOP includes structured reason code
- [ ] Every STOP includes UX guidance
- [ ] Code-Test-Doc 1:1 correspondence verified
- [ ] Philosophy phrases present in all docs
- [ ] Positioning statement consistent across all materials
- [ ] No "safety feature" language used
- [ ] No "better answers" claims made

---

## Adapter/Prompt/Model Subordination

**This specification is the TOP layer.**

**Adapters, prompts, and models are LOWER layers:**

```
Boundary Spec (this document)
    ↓ enforces on
Adapter Layer (LangChain, custom, etc.)
    ↓ configures
Prompt Layer (system prompts)
    ↓ inputs to
Model Layer (LLM)
```

**Boundary spec can:**
- ✅ Override adapter suggestions
- ✅ Block any response path
- ✅ Enforce STOP regardless of model output

**Adapters/prompts/models CANNOT:**
- ❌ Override boundary decisions
- ❌ Bypass the gate
- ❌ Convert STOP to ALLOW

**Philosophy always wins.**

---

## Audit and Logging

**Every gate invocation MUST log:**

1. Input parameters
   - Query
   - Retrieved docs count
   - Permission status
   - Decision request detection

2. Decision outcome
   - ALLOW / REVIEW / STOP
   - Reason code
   - Timestamp

3. Context
   - User/role (if applicable)
   - Session ID
   - System version

**STOP outcomes MUST additionally log:**
- Full reason explanation
- Guidance provided
- Next action options

**Logs are NOT errors. They are accountability artifacts.**

---

## Version Control

**This specification is immutable.**

**Version 1.0 defines:**
- Core principles
- Decision types
- 5 core scenarios
- Structural requirements

**Future versions MAY:**
- Add new STOP reason codes
- Expand permission calculation rules
- Add evidence grading dimensions
- Clarify ambiguous statements

**Future versions MAY NOT:**
- Remove existing STOP codes
- Make gate bypassable
- Change core principles
- Allow decision automation

---

## Summary

**This specification defines a judgment boundary, not a feature.**

- Top-level system contract
- Non-bypassable gate structure
- STOP as normal outcome
- Code-Test-Doc 1:1 correspondence
- 5 core scenarios in CI
- Structured reason codes
- UX guidance without automation
- "When to answer" not "what to answer"

**Philosophy:**
> **"Retrieved documents ≠ permission to answer"**
> **"This system does not automate decisions"**

**These statements appear in:**
- This spec
- All README files
- All test output
- All UX messages

**Immutable. Non-negotiable. Top-layer contract.**

---
