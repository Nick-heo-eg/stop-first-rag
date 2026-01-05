#!/usr/bin/env python3
"""
Minimal STOP-First RAG Demo

This is a self-contained demonstration showing the core STOP-first logic.
No external dependencies beyond Python stdlib.

Run: python demo_minimal.py
"""

import json
from dataclasses import dataclass
from typing import List, Literal
from datetime import datetime, timezone


@dataclass
class Evidence:
    id: str
    source: str
    text: str
    confidence: float


@dataclass
class JudgmentResult:
    evidence_id: str
    decision: Literal["ACCEPT", "REJECT", "DEFER"]
    reason: str


def judge_evidence(evidence: Evidence, query: str) -> JudgmentResult:
    """
    Evidence Judge: Decides if evidence is acceptable.

    This is a simplified rule-based judge for demonstration.
    In production, this would use more sophisticated logic.
    """
    # Rule 1: Low confidence → REJECT
    if evidence.confidence < 0.5:
        return JudgmentResult(
            evidence_id=evidence.id,
            decision="REJECT",
            reason=f"Confidence {evidence.confidence:.2f} below threshold 0.5"
        )

    # Rule 2: Check if evidence actually addresses the query
    query_lower = query.lower()
    text_lower = evidence.text.lower()

    # For "software" query, reject "physical products" evidence
    if "software" in query_lower and "physical" in text_lower:
        return JudgmentResult(
            evidence_id=evidence.id,
            decision="REJECT",
            reason="Evidence covers physical products, not software"
        )

    # Rule 3: Vague references → DEFER
    if "contact support" in text_lower or "different polic" in text_lower:
        return JudgmentResult(
            evidence_id=evidence.id,
            decision="DEFER",
            reason="Evidence mentions topic but provides no concrete answer"
        )

    # Rule 4: Off-topic → REJECT
    keywords = ["return", "refund", "policy"]
    if not any(kw in text_lower for kw in keywords):
        return JudgmentResult(
            evidence_id=evidence.id,
            decision="REJECT",
            reason="Evidence does not address query topic"
        )

    # Default: ACCEPT if passed all filters
    return JudgmentResult(
        evidence_id=evidence.id,
        decision="ACCEPT",
        reason="Evidence is relevant and concrete"
    )


def final_judge(accepted_count: int, query: str) -> tuple[str, str]:
    """
    Final Judge: Decides whether to ANSWER or STOP.

    Returns: (decision, reason_code)
    """
    if accepted_count == 0:
        return ("STOP", "NO_ACCEPTABLE_EVIDENCE")

    if accepted_count < 2:
        return ("STOP", "INSUFFICIENT_EVIDENCE")

    return ("ANSWER", "SUFFICIENT_EVIDENCE")


def main():
    print("=" * 70)
    print("STOP-First RAG: Minimal Demo")
    print("=" * 70)
    print()

    # Query
    query = "What is our return policy for opened software?"
    print(f"Query: {query}")
    print()

    # Simulated retrieved evidence
    evidence_candidates = [
        Evidence(
            id="E1",
            source="policy_doc_2023.pdf",
            text="All physical products may be returned within 14 days with receipt.",
            confidence=0.72
        ),
        Evidence(
            id="E2",
            source="faq_page.html",
            text="Software and digital products have different return policies - contact support.",
            confidence=0.65
        ),
        Evidence(
            id="E3",
            source="terms_2022.pdf",
            text="Refunds are processed within 5-7 business days.",
            confidence=0.43
        ),
    ]

    print(f"Retrieved {len(evidence_candidates)} evidence candidates")
    print()

    # Evidence Judgment Phase
    print("=" * 70)
    print("Evidence Judgment Phase")
    print("=" * 70)

    judgments: List[JudgmentResult] = []
    accepted_evidence = []

    for evidence in evidence_candidates:
        judgment = judge_evidence(evidence, query)
        judgments.append(judgment)

        print(f"\n[{evidence.id}] {evidence.text[:60]}...")
        print(f"  Source: {evidence.source}")
        print(f"  Confidence: {evidence.confidence:.2f}")
        print(f"  ⚖️  Decision: {judgment.decision}")
        print(f"  📝 Reason: {judgment.reason}")

        if judgment.decision == "ACCEPT":
            accepted_evidence.append(evidence)

    print()
    print("=" * 70)
    print("Final Judgment Phase")
    print("=" * 70)
    print()

    # Final Decision
    decision, reason_code = final_judge(len(accepted_evidence), query)

    print(f"Accepted evidence count: {len(accepted_evidence)}")
    print(f"Decision: {decision}")
    print(f"Reason code: {reason_code}")
    print()

    if decision == "STOP":
        print("🛑 STOP")
        print(f"   Reason: {reason_code}")
        print()
        print("   Explanation:")
        print(f"   Query asked about opened software return policy.")
        print(f"   Retrieved {len(evidence_candidates)} evidence candidates.")
        print(f"   E1: Covers physical products, not software → REJECT")
        print(f"   E2: Mentions software but no concrete policy → DEFER")
        print(f"   E3: About refund timing, not eligibility → REJECT")
        print(f"   No evidence directly answers the question.")
        print()
        print("   ✅ System correctly refused to hallucinate an answer.")
    else:
        print("✅ ANSWER")
        print(f"   Generated answer from {len(accepted_evidence)} accepted evidence")

    print()
    print("=" * 70)
    print("Trace Summary")
    print("=" * 70)

    # Generate trace-like output
    trace = {
        "run_id": "demo_minimal",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "evidence_count": len(evidence_candidates),
        "judgments": [
            {
                "evidence_id": j.evidence_id,
                "decision": j.decision,
                "reason": j.reason
            }
            for j in judgments
        ],
        "final_decision": {
            "decision": decision,
            "reason_code": reason_code,
            "accepted_count": len(accepted_evidence)
        }
    }

    print(json.dumps(trace, indent=2))
    print()
    print("=" * 70)
    print("Demo Complete")
    print("=" * 70)
    print()
    print("Key Takeaways:")
    print("1. Evidence Judge filters BEFORE generation")
    print("2. STOP is a first-class outcome (not failure)")
    print("3. Structured reason codes (NO_ACCEPTABLE_EVIDENCE)")
    print("4. Complete audit trail in trace")
    print()
    print("See examples/stop_trace.jsonl for full production trace format")
    print()


if __name__ == "__main__":
    main()
