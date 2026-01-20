# Standard RAG Architecture and Its Broken Assumptions

**Understanding what typical RAG systems assume — and where those assumptions break**

---

## The Standard RAG Pipeline

Most RAG (Retrieval-Augmented Generation) systems follow this structure:

```
1. Document Collection
   ↓
2. Preprocessing & Chunking
   ↓
3. Vectorization (embeddings)
   ↓
4. Vector Database Storage
   ↓
5. Query Processing
   ↓
6. Retrieval (similarity search)
   ↓
7. LLM Response Generation
   ↓
8. Return Answer
```

This architecture is widely adopted in:
- Enterprise chatbots
- Internal knowledge bases
- Customer support systems
- Document Q&A tools
- Compliance assistants

---

## The Core Assumption

**Standard RAG systems assume:**

> **"Retrieved documents = sufficient evidence"**

In other words:
- If the vector search returns documents with high similarity scores
- Then those documents are treated as valid evidence
- Therefore, generating an answer is always appropriate

**This assumption breaks in every high-risk domain.**

---

## Where This Assumption Breaks: Real-World Cases

### Case 1: HR / Employment Law

**Scenario:** Employee asks about parental leave policy

**What Standard RAG Does:**
```
Query: "How many days of parental leave do I get?"
Retrieved: [Policy v2.3 (2022), Policy v3.1 (2024), Email thread about proposed changes]
Generated Answer: "You are entitled to 12 weeks of parental leave."
```

**What's Wrong:**
- ❌ Policy v2.3 is outdated
- ❌ Email thread contains proposals, not approved policy
- ❌ Different chunks conflict on eligibility criteria
- ❌ No verification that the policy applies to the employee's contract type

**Real Risk:**
Employee takes leave based on wrong policy → legal liability

---

### Case 2: Finance / Compliance

**Scenario:** Trader asks if a transaction is compliant

**What Standard RAG Does:**
```
Query: "Can I execute this trade in market X?"
Retrieved: [General trading guidelines, Market X overview, Compliance memo 2023]
Generated Answer: "Yes, this trade is permitted under current guidelines."
```

**What's Wrong:**
- ❌ Guidelines exist but regulatory approval is pending
- ❌ Market X overview doesn't mention recent sanctions
- ❌ Compliance memo is a draft, not final policy
- ❌ No check for jurisdiction-specific restrictions

**Real Risk:**
Regulatory violation → fines, license suspension

---

### Case 3: Medical / Clinical Decision Support

**Scenario:** Clinician asks about drug interaction

**What Standard RAG Does:**
```
Query: "Is Drug A safe with Drug B?"
Retrieved: [Drug A monograph, Drug B contraindications, Case study 2021]
Generated Answer: "Drug A is generally safe with Drug B when monitored."
```

**What's Wrong:**
- ❌ Monographs don't mention patient-specific factors (age, kidney function)
- ❌ Case study is observational, not clinical trial evidence
- ❌ No check for updated FDA warnings
- ❌ "Generally safe when monitored" requires clinical judgment, not automated advice

**Real Risk:**
Adverse drug reaction → patient harm

---

### Case 4: Legal Research

**Scenario:** Junior attorney researches case precedent

**What Standard RAG Does:**
```
Query: "What is the statute of limitations for this claim?"
Retrieved: [State Code Section 12.34, Legal blog post, Court opinion 1998]
Generated Answer: "The statute of limitations is 3 years from date of injury."
```

**What's Wrong:**
- ❌ Code section may have been amended
- ❌ Blog post is not authoritative
- ❌ 1998 opinion may have been overturned
- ❌ No jurisdiction verification

**Real Risk:**
Case dismissed due to missed deadline → malpractice claim

---

## The Structural Problem

Standard RAG systems produce answers even when:

1. **Evidence doesn't exist**
   - No approved policy on the topic
   - Regulation hasn't been published yet
   - Documentation is incomplete

2. **Evidence conflicts**
   - Old policy vs. new policy
   - Draft vs. final version
   - General rule vs. exception

3. **Query requires discretion**
   - "Should I approve this request?"
   - "Is this situation compliant?"
   - "What is the right decision here?"

4. **Evidence status is unclear**
   - Is this the current version?
   - Has this been approved?
   - Does this apply to this case?

**In all these cases, standard RAG generates an answer anyway.**

Because the system is optimized to:
- Maximize answer coverage
- Minimize user friction
- Avoid "I don't know" responses

**Not to:**
- Verify evidence sufficiency
- Detect conflicting information
- Refuse answers when judgment is required

---

## Why This Happens: Market Incentives

Standard RAG systems are built to optimize:

- ✅ User engagement (more answers = better UX)
- ✅ Coverage metrics (% of questions answered)
- ✅ Retrieval accuracy (better similarity scores)
- ✅ Response speed (faster = better)

**They are NOT built to optimize:**

- ❌ Evidence sufficiency verification
- ❌ Conflict detection
- ❌ Refusal when judgment is needed
- ❌ Accountability for wrong answers

---

## The Evidence Existence Problem

**Standard RAG checks:**
- "Do we have documents similar to this query?"

**It does NOT check:**
- "Do we have *sufficient* evidence to answer this query?"
- "Does this evidence *apply* to this case?"
- "Are we *permitted* to make this decision?"

This is not a hallucination problem.
This is not a retrieval accuracy problem.

**This is a judgment gate problem.**

---

## Real-World Incident Patterns

Analysis of AI system failures in high-risk domains shows:

| Failure Type | Standard RAG Behavior | Real Cause |
|-------------|----------------------|------------|
| Wrong policy version cited | Generated answer from outdated doc | No version verification |
| Conflicting guidance | Generated answer averaging both | No conflict detection |
| Draft treated as final | Generated answer from unapproved doc | No approval status check |
| Jurisdiction error | Generated answer from wrong region | No applicability verification |
| Discretionary question auto-answered | Generated answer to judgment question | No discretion detection |

**Common pattern:** RAG retrieved documents, so RAG generated an answer.

**Missing step:** Check whether generating an answer is *permissible*.

---

## What Standard RAG Cannot Detect

1. **Evidence gaps**
   - Policy doesn't exist yet
   - Documentation is incomplete
   - Regulation pending publication

2. **Evidence conflicts**
   - Old vs. new policy
   - General rule vs. exception
   - Different jurisdictions

3. **Evidence status**
   - Draft vs. approved
   - Active vs. superseded
   - Proposed vs. enacted

4. **Judgment boundaries**
   - Question requires discretion
   - Multiple valid interpretations
   - Case-by-case determination needed

**These are not edge cases.**
**These are the majority of high-risk queries.**

---

## The Missing Layer: Judgment Before Generation

Standard RAG:
```
Query → Retrieve → Generate → Return
```

What's needed:
```
Query → Retrieve → **Judge if answer is permissible** → Generate (if ALLOW) → Return
                                                      ↓
                                                   STOP (if prohibited)
```

**This is not a safety feature.**
**This is a prerequisite for accountability.**

---

## Summary

Standard RAG systems assume:
- Retrieved documents = sufficient evidence
- High similarity score = permission to answer
- Generating answers = always better than refusing

**In high-risk domains:**
- Evidence sufficiency must be verified, not assumed
- Permission to answer must be checked, not implied
- Refusal is a valid outcome, not a system failure

**stop-first-rag exists to address this gap.**

It does NOT improve RAG retrieval.
It checks whether RAG evidence permits generating an answer.

---

**This system does not automate decisions.**
**It detects when decisions should not be automated.**

---
