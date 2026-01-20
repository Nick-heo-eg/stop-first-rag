# Responsibility Boundary

**Philosophy vs. Implementation: Clear Separation**

---

## Purpose of This Document

This document defines the responsibility boundary between:
- **stop-first-rag** (this repository) – Philosophy and constitutional framework
- **stopfirst-rag-adapter** – Experimental implementation

---

## What This Repository Is Responsible For

**stop-first-rag defines:**

### 1. Core Philosophy
- What "evidence sufficiency" means
- When AI should NOT generate answers
- What constitutes a "judgment-impossible state"
- Why STOP is a valid outcome (not an error)

### 2. Constitutional Framework
- ALLOW / REVIEW / STOP decision logic
- Evidence verification requirements
- Negative proof log requirements
- Judgment boundary principles

### 3. Conceptual Reference
- What judgment-first systems should do
- How to think about evidence in high-risk domains
- Where standard RAG assumptions break
- Why retrieval ≠ permission to answer

**These definitions are immutable.**

They form the constitutional basis for all judgment-first implementations.

---

## What This Repository Is NOT Responsible For

**stop-first-rag does NOT provide:**

- ❌ Installation guides
- ❌ Production-ready code
- ❌ Framework-specific adapters
- ❌ Integration examples
- ❌ Deployment instructions

**For implementation:**
→ See [stopfirst-rag-adapter](https://github.com/Nick-heo-eg/stopfirst-rag-adapter)

---

## Repository Separation

| Aspect | stop-first-rag (this repo) | stopfirst-rag-adapter |
|--------|---------------------------|----------------------|
| **Purpose** | Constitutional reference | Experimental implementation |
| **Contains** | Philosophy, logic, principles | Code, examples, guides |
| **Status** | Stable framework | Unstable, evolving |
| **Changes** | Rare, carefully considered | Frequent, breaking changes OK |
| **Audience** | Researchers, policy makers | Developers, PoC teams |
| **Lifespan** | Permanent reference | May be deprecated/replaced |

---

## Dependency Direction

```
stopfirst-rag-adapter (implementation)
        ↓
   depends on (for philosophy)
        ↓
   stop-first-rag (this repo)
```

**Philosophy does NOT depend on implementation.**

---

## If You Want To...

**Understand the concept:**
→ Read this repository

**Experiment with your RAG system:**
→ Use [stopfirst-rag-adapter](https://github.com/Nick-heo-eg/stopfirst-rag-adapter)

**Build a production system:**
→ Use this repo as constitutional reference, build your own implementation

**Write a research paper:**
→ Cite this repository (philosophy and principles)

**Fork and modify:**
→ Fork stopfirst-rag-adapter (implementation), not this repo

---

## What Can Change (and What Cannot)

### In This Repository (stop-first-rag)

**Can change:**
- ✅ Clarifications of existing principles
- ✅ Additional examples
- ✅ Improved explanations
- ✅ More detailed documentation

**Cannot change:**
- ❌ Core ALLOW/REVIEW/STOP semantics
- ❌ Principle that "STOP is valid outcome"
- ❌ Requirement for negative proof logs
- ❌ Definition of evidence sufficiency

### In stopfirst-rag-adapter

**Can change:**
- ✅ Everything (it's experimental)

**Must align with this repo:**
- ✅ ALLOW/REVIEW/STOP semantics
- ✅ Negative proof log generation
- ✅ Treatment of STOP as valid outcome

---

## If Logic Conflicts Between Repositories

**If stopfirst-rag-adapter logic conflicts with this repository:**

→ **This repository (stop-first-rag) is correct**
→ The adapter should be fixed, forked, or discarded

**Example conflict:**
- This repo says: "STOP is a valid outcome, not an error"
- Adapter treats: STOP as an error condition

**Resolution:**
- Fix the adapter
- OR: Document as "non-compliant variant"
- OR: Discard the adapter

---

## For Contributors

**Contributing to this repository:**
- Changes must maintain constitutional integrity
- Core principles are immutable
- Discussions required before major changes
- Focus on clarity, not implementation

**Contributing to stopfirst-rag-adapter:**
- Experimental changes welcome
- Breaking changes acceptable
- Fork and customize freely
- Focus on usability, not philosophy

---

## Summary

**This repository (stop-first-rag):**
- Defines the "what" and "why"
- Provides constitutional framework
- Stable, immutable reference
- For understanding and research

**stopfirst-rag-adapter:**
- Defines the "how"
- Provides experimental code
- Unstable, evolving
- For experimentation and prototyping

**Boundary:**
- Philosophy here, implementation there
- If conflict → Philosophy wins
- Adapter can be replaced, philosophy cannot

---

**Constitutional reference:** This repository

**Practical implementation:** [stopfirst-rag-adapter](https://github.com/Nick-heo-eg/stopfirst-rag-adapter)

---
