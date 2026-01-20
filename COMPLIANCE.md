# Compliance and Regulatory Use

This document covers stop-first RAG in regulated environments where audit trails, accountability, and governance frameworks are required.

**Audience**: Enterprise organizations, compliance officers, legal teams, auditors

---

## Table of Contents

1. [Core Philosophy](#core-philosophy)
2. [Regulatory Frameworks](#regulatory-frameworks)
3. [Judgment Boundary Contract](#judgment-boundary-contract)
4. [Regulated Demos](#regulated-demos)
5. [Audit and Accountability](#audit-and-accountability)
6. [Constitutional Framework](#constitutional-framework)
7. [Enterprise Deployment](#enterprise-deployment)
8. [Responsibility Boundaries](#responsibility-boundaries)

---

## Core Philosophy

> **"Retrieved documents ≠ permission to answer"**

> **"This system does not automate decisions"**

In regulated environments, stop-first RAG enforces a **judgment boundary** — a non-bypassable gate that determines when answering is permitted.

**Positioning:**
> "This is not a system that answers questions well.
> This is a system that distinguishes when answering is permitted."

**Key Principle:**
- AI should not be optimized to answer more questions
- It should be optimized to **refuse answers when judgment is not permitted**

---

## Regulatory Frameworks

### EU AI Act Compliance

**Article 14 - Human Oversight**

Stop-first RAG supports EU AI Act Article 14 requirements by:
- Enforcing non-bypassable checkpoints before automated decisions
- Generating STOP decisions when human oversight is required
- Maintaining audit trails of decision boundaries
- Preventing unauthorized decision automation

**High-Risk AI Systems (Annex III)**

The system addresses high-risk domains including:
- **Employment and Worker Management** (HR demos)
- **Access to Essential Services** (Finance demos)
- **Critical Infrastructure** (Medical demos)

### GDPR Article 22

**Automated Decision-Making**

GDPR Article 22 grants individuals the right not to be subject to solely automated decision-making with legal or similarly significant effects.

Stop-first RAG enforces this by:
- Detecting when a query is a **decision request** (not an information request)
- Blocking answer generation with reason code `DECISION_AUTOMATION_BLOCKED`
- Routing to human review when discretionary judgment is required
- Logging all decision boundary events for auditability

### HIPAA / Medical Compliance

**Clinical Consent and Evidence Requirements**

In healthcare contexts, stop-first RAG verifies:
- **Consent verification**: `consent_signed` must be True
- **Evidence sufficiency**: Required medical evidence tags present
- **Risk disclosure**: Acknowledgment of risk disclosures
- **No consent violations**: `no_consent` tag triggers immediate STOP

### Financial Regulations

**KYC (Know Your Customer) and AML (Anti-Money Laundering)**

Finance demos validate:
- Consent form signed
- Credit report available
- Income verification complete
- Debt summary present
- No consent violations

---

## Judgment Boundary Contract

### Three Outcomes (Immutable)

The judgment boundary returns one of three decisions:

**1. ALLOW** - Permission to answer verified
- Evidence sufficient
- Permission explicitly granted
- Not a decision request
- → Proceed to answer generation

**2. REVIEW** - Human judgment required
- Evidence exists but conflicts detected
- Multiple valid interpretations
- Discretionary judgment needed
- → Route to human review

**3. STOP** - Answer generation prohibited

> **STOP is not a failure. STOP is a valid outcome.**

STOP means:
- "Retrieved documents ≠ permission to answer"
- "This system does not automate decisions"
- "Evidence insufficient to answer responsibly"

### Structured Reason Codes

Every STOP includes a structured reason code for accountability:

**Permission Violations:**
- `STOP.PERMISSION_MISSING` - No permission to answer found
- `STOP.PERMISSION_EXPIRED` - Permission no longer valid
- `STOP.PERMISSION_SCOPE_VIOLATED` - Query outside permitted scope

**Decision Automation Blocks:**
- `STOP.DECISION_AUTOMATION_BLOCKED` - Query requires human decision
- `STOP.JUDGMENT_REQUIRED` - Discretionary judgment needed

**Evidence Issues:**
- `STOP.EVIDENCE_MISSING` - No relevant evidence retrieved
- `STOP.EVIDENCE_INSUFFICIENT` - Evidence doesn't fully support answer
- `STOP.EVIDENCE_INVALID` - Evidence quality/status unverified
- `STOP.EVIDENCE_CONFLICT` - Retrieved documents contradict

**Boundary Violations:**
- `STOP.OUT_OF_SCOPE` - Query outside system boundaries
- `STOP.DISCRETION_REQUIRED` - Requires case-by-case judgment

---

## Regulated Demos

### HR - Employment Compliance

**Location**: `demos/regulated/multidomain/hr/`

**Regulatory Context**: Employment law, anti-discrimination, portfolio verification

**Scenario**: Technical hiring with mandatory evidence requirements
- Backend Engineer
- ML Engineer
- Data Analyst

**Policy Requirements**:
- **Global must-links**: `portfolio_url`, `github_url` (required for all)
- **Role-specific evidence**: Code samples, model training logs, analysis reports
- **Verification**: Evidence tags checked before approval

**Results**:
- Total: 60 candidates
- ALLOW: 38 (63%) - Evidence complete
- STOP: 22 (37%) - Missing required evidence

**Top STOP Reasons**:
- `missing_must_evidence`: 12 cases (no code samples, no training logs)
- `missing_must_links`: 10 cases (no portfolio, no GitHub)

**Audit View**: Every rejection includes structured reason, timestamp, evidence gaps

---

### Finance - Loan Underwriting

**Location**: `demos/regulated/multidomain/finance/`

**Regulatory Context**: KYC, AML, credit verification

**Scenario**: Loan underwriting analyst decisions

**Policy Requirements**:
- **Consent**: `consent_form_signed` (global must-link)
- **Must-have evidence**: `credit_report`, `income_verification`, `debt_summary`, `policy_disclosure_ack`
- **Should-have evidence**: `bank_statement`, `employment_verification`
- **Must-not tags**: `no_consent` (immediate STOP)

**Results**:
- Total: 40 loan applications
- ALLOW: 17 (42.5%) - All evidence verified
- REVIEW: 5 (12.5%) - Missing should-have evidence (manual review required)
- STOP: 18 (45%) - Missing required evidence or no consent

**Audit Trail**: Complete evidence lineage, consent verification logs, decision timestamps

---

### Medical - Clinical Triage

**Location**: `demos/regulated/medical/`

**Regulatory Context**: HIPAA, FDA, clinical consent

**Scenario**: Clinical triage and consent compliance

**Policy Requirements**:
- **Global must-links**: `consent_signed` (True required)
- **Must-have evidence**: `symptom_report`, `vitals`, `risk_disclosure_ack`
- **Should-have evidence**: `lab_results`, `imaging_summary`
- **Must-not tags**: `no_consent`, `diagnosis_without_evidence`

**Results**:
- Total: 30 patients
- ALLOW: 15 (50%) - Consent + evidence complete
- REVIEW: 2 (7%) - Consent signed but evidence conflicts
- STOP: 13 (43%) - No consent or missing critical evidence

**Compliance Feature**: No clinical response generated without explicit consent

---

### Running Regulated Demos

```bash
cd demos/regulated
./RUN_REGULATED_DEMOS.sh
```

Executes all three regulated domain demos sequentially.

---

## Audit and Accountability

### Accountability Logs (Negative Proof)

Every STOP decision generates a structured accountability log:

```json
{
  "decision": "STOP",
  "reason_code": "STOP.PERMISSION_MISSING",
  "timestamp": "2024-01-20T10:30:00Z",
  "query": "What is the CEO's salary?",
  "retrieved_chunks": 0,
  "context": {
    "domain": "hr",
    "permission_status": "NOT_FOUND"
  },
  "explanation": "Retrieved documents do not include permission to answer salary queries"
}
```

**These logs are NOT errors. They are accountability artifacts.**

In high-risk domains:
> "Why we didn't answer" is as important as "what we answered"

### Audit Trail Requirements

For regulated environments, stop-first RAG provides:

1. **Decision Logs**: Every ALLOW/REVIEW/STOP decision recorded
2. **Evidence Lineage**: Which documents were retrieved and checked
3. **Reason Codes**: Structured, auditable refusal reasons
4. **Timestamps**: When each boundary check occurred
5. **Context Preservation**: Domain, role, permission status

### Audit Views

Auditors can verify:
- ✅ No answers generated without evidence
- ✅ No decision automation occurred
- ✅ All STOP decisions include structured reasons
- ✅ Human oversight maintained for discretionary cases
- ✅ Permission boundaries enforced

**What auditors DON'T need**:
- ❌ Model weights or training data
- ❌ Model accuracy metrics
- ❌ LLM prompt engineering details
- ❌ RAG retrieval algorithms

**Focus**: Decision boundary enforcement, not model performance

---

## Constitutional Framework

### Declaration of Dependence

Stop-first RAG depends on a constitutional memory system (Echo Memory Governor) for:

**1. Snapshot-Based Context**
- System operates on **snapshots**, not raw queries
- No pending/draft items leak into evidence checks
- Only approved, finalized documents count as evidence

**2. Pending Exclusion**
- Draft policies, unapproved documents excluded automatically
- Evidence status verified before permission granted

**3. Evidence Citation**
- Every ALLOW decision cites specific evidence sources
- Lineage tracking for audit compliance

**4. Accountability Claims**
- System makes NO claims it cannot prove
- "Evidence insufficient" preferred over "here's an answer"

**See**: [DECLARATION_OF_DEPENDENCE.md](DECLARATION_OF_DEPENDENCE.md) for constitutional relationship details

---

## Enterprise Deployment

### Deployment Patterns

**1. API Gateway Pattern**
```
User Request → API Gateway → [Boundary Gate] → RAG Pipeline → LLM
```
- Gate as first checkpoint
- Centralized enforcement
- All requests pass through

**2. Sidecar Pattern**
```
RAG Service + [Boundary Gate Sidecar]
```
- Gate deployed alongside RAG
- Service-level enforcement
- Portable across environments

**3. Library Integration Pattern**
```python
from judgment_boundary import BoundaryGate

gate = BoundaryGate()
result = gate.check(query, chunks, context)
if result.decision == "ALLOW":
    response = rag_pipeline.generate(query, chunks)
```
- Embedded in application code
- Framework-agnostic
- Custom integration logic

### Enterprise Requirements

**Governance**:
- Non-bypassable gate enforcement
- Audit trail generation
- Reason code standardization
- Human review routing

**Compliance**:
- Regulatory framework mapping (EU AI Act, GDPR, HIPAA)
- Evidence sufficiency verification
- Decision automation detection
- Permission boundary enforcement

**Accountability**:
- Negative proof logs (why we didn't answer)
- Evidence lineage tracking
- Timestamp and context preservation
- Structured refusal reasons

---

## Responsibility Boundaries

### What This System Does NOT Do

**This system does NOT automate decisions.**
**It detects when decisions should NOT be automated.**

**Domain-Specific Clarifications:**

**HR / Employment:**
- ❌ Does NOT rank candidates
- ❌ Does NOT approve/reject applications
- ❌ Does NOT determine eligibility
- ✅ Verifies whether evidence exists to support ranking/approval/eligibility decisions

**Finance / Compliance:**
- ❌ Does NOT approve loans or trades
- ❌ Does NOT assess credit risk
- ❌ Does NOT determine regulatory compliance
- ✅ Verifies whether evidence permits making loan/trade/compliance decisions

**Medical / Clinical:**
- ❌ Does NOT diagnose conditions
- ❌ Does NOT recommend treatments
- ❌ Does NOT prescribe medications
- ✅ Verifies whether evidence supports clinical decision-making

### Responsibility Separation

**This system does NOT:**
- Replace domain expertise
- Bypass regulatory requirements
- Substitute for professional judgment
- Reduce human accountability

**What it DOES:**
- Detect when evidence is missing
- Identify when policies conflict
- Recognize when discretion is required
- **Stop before irresponsible automation happens**

---

## Integration with Echo Memory Governor

Stop-first RAG's constitutional dependence on Echo Memory Governor ensures:

**1. Evidence Integrity**
- Only approved, finalized documents count as evidence
- Pending items excluded from evidence checks
- Version control and status verification

**2. Snapshot Consistency**
- Boundary checks operate on immutable snapshots
- No race conditions from document updates
- Deterministic evidence evaluation

**3. Audit Lineage**
- Every evidence claim traceable to source document
- Snapshot ID, timestamp, approval status preserved
- Full chain of custody for compliance

**See**: [INTEGRATION_WITH_ECHO_MEMORY_GOVERNOR.md](INTEGRATION_WITH_ECHO_MEMORY_GOVERNOR.md)

---

## Architecture (Governance View)

**System-Level Position (TOP Layer)**:

```
┌──────────────────────────────────────────────┐
│  JUDGMENT BOUNDARY (Constitutional Layer)   │ ← TOP LAYER
│  "Retrieved ≠ permission"                    │   Immutable
│  "No decision automation"                    │   Non-bypassable
├──────────────────────────────────────────────┤
│  Adapter Layer (LangChain, custom, etc.)    │
├──────────────────────────────────────────────┤
│  Prompt Layer                                │
├──────────────────────────────────────────────┤
│  Model Layer (GPT-4, Claude, Llama, etc.)   │
└──────────────────────────────────────────────┘
```

**Enforcement Point**:

```
Query → Retrieve → [JUDGMENT BOUNDARY] → Generate → Return
                          ↑
                    Non-bypassable
              ALL paths go through here
```

**Flow**:

```
User Query
  ↓
Retrieval (RAG)
  ↓
Retrieved Documents
  ↓
[JUDGMENT BOUNDARY] ← **CONSTITUTIONAL CONTRACT**
  │
  ├─ Check Permission
  ├─ Check Evidence Sufficiency
  ├─ Detect Decision Request
  │
  ├─→ ALLOW    → Generate answer
  ├─→ REVIEW   → Route to human
  └─→ STOP     → Log reason, refuse generation
```

**Core Principle:**
> "Retrieved documents ≠ permission to answer"
> "This system does not automate decisions"

---

## Supporting Documents

**Constitutional Framework**:
- [BOUNDARY_SPEC.md](BOUNDARY_SPEC.md) - Complete specification (immutable contract)
- [RESPONSIBILITY_BOUNDARY.md](RESPONSIBILITY_BOUNDARY.md) - Philosophy vs. implementation separation
- [DECLARATION_OF_DEPENDENCE.md](DECLARATION_OF_DEPENDENCE.md) - Echo Memory Governor relationship

**Analysis**:
- [STANDARD_RAG_AND_ITS_ASSUMPTIONS.md](docs/STANDARD_RAG_AND_ITS_ASSUMPTIONS.md) - Where RAG assumptions break in high-risk domains

**Implementation**:
- [gate.py](gate.py) - Reference implementation
- [test_boundary_spec.py](test_boundary_spec.py) - 5 core scenarios (CI validation)

---

## Verification

### CI Pipeline Validation

Every commit validates the judgment boundary contract:

```bash
python test_boundary_spec.py
```

**5 Core Scenarios**:
1. Documents Retrieved + Permission Missing → STOP
2. No Documents + Permission Granted → STOP
3. Decision Request → STOP
4. Adapter Forces ANSWER → STOP (philosophy overrides)
5. Adapter Suggests STOP → ALLOW (if conditions met)

Expected output:
```
✅ ALL TESTS PASSED - BOUNDARY SPEC VALIDATED

Philosophy enforced:
  ✅ "Retrieved documents ≠ permission to answer"
  ✅ "This system does not automate decisions"
```

**CI Integration**: Tests run automatically; build fails if any scenario fails

---

## License & Intent

This project is published for research, validation, and discussion.
It is intended to inform safer AI system design, not to bypass domain regulations.

**No claims are made regarding:**
- Production readiness for all environments
- Automatic regulatory compliance
- Legal sufficiency without expert review
- Enterprise deployment without customization

**Use this work to:**
- Understand where RAG assumptions break in regulated domains
- Design accountability into AI systems
- Inform governance and policy discussions
- Build evidence-based decision boundaries

**Do NOT use this work to:**
- Replace professional judgment
- Bypass regulatory review processes
- Claim automated compliance
- Avoid human accountability

---

## Final Note

> **"Retrieved documents ≠ permission to answer"**
> **"This system does not automate decisions"**

**In regulated domains:**
- The most dangerous answer is not the wrong answer
- It is the answer given without sufficient evidence or permission to answer at all

**This specification exists to detect that condition.**
**Not to fix it. Not to work around it. To detect it and stop.**

---

**For developer-focused documentation, see**: [README.md](README.md)
