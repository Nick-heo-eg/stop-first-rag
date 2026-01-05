# STOP/Branch Judgment vs. RAG

## TL;DR
- STOP/branch judgment was never a bolt-on safety feature.
- It always asked “can we proceed?” before the next action.
- RAG simply became the evidence supply channel for that same judgment core.
- RAG retrieves evidence; the STOP/AJT core decides whether answering is permissible and logs the decision.

## What STOP/Branch originally did
- Halt when conditions weren’t satisfied.
- Branch when uncertainty required manual decisions.
- Stop when risk thresholds were exceeded.
- Record WHY it stopped (AJT/trace).
- Crucially: this happened **before** model execution, not after.

## What classic RAG lacks
```
Query → Retrieve → Generate → Return
```
- No check on whether generation should happen.
- Weak/contradictory evidence still leads to generation.
- Failures get attributed to “hallucination” with no structured reason.

## Mapping STOP rules to RAG language
| STOP rule                    | RAG judgment code          |
|-----------------------------|----------------------------|
| Condition unmet → STOP      | `NO_ACCEPTABLE_EVIDENCE`   |
| Conflicting signals          | `CONFLICTING_EVIDENCE`     |
| Insufficient context         | `INSUFFICIENT_CONTEXT`     |
| Risk threshold breached      | `LOW_CONFIDENCE`           |
| Logged reason                | `TRACE / NEGATIVE PROOF`   |

This shows we already built “Judgment-first RAG”; we were just missing retrieval.

## Correct relationship
```
[Judgment Core (STOP/AJT)] ← evidence from RAG
```
- STOP/AJT is the heart; RAG is the evidence supply.
- Decision rights never leave the system layer.

## Why it matters
1. RAG cannot “own” a decision; it only proposes evidence.
2. STOP policies get reused—A/B accept/reject logic stays identical pre/post RAG.
3. RAG failures are quarantined: if evidence is garbage, STOP fires, and the system behaves correctly.

## Key statement
> **We didn’t bolt STOP onto RAG; STOP existed first, so RAG finally found the right place.**

Or equivalently:
> **RAG fetches evidence; STOP decides if that evidence is good enough to speak.**

And in this system:
> **Retrieval is optional. Judgment is not.**
