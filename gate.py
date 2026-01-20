"""
stop-first-rag: Early Exit Guard Implementation

Reference implementation of evidence presence check before LLM generation.

Core functions:
- should_generate(chunks) → bool (minimal framework-agnostic interface)
- check_evidence(query, chunks) → dict (structured interface with reason codes)

Single responsibility: Decide if retrieved_chunks is empty before calling LLM.
This is intentionally trivial (if not chunks). Value is in naming, boundary
enforcement, and observability.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Dict, Any


# ============================================================================
# MINIMAL FRAMEWORK-AGNOSTIC INTERFACE
# ============================================================================

def should_generate(chunks: List[Dict[str, Any]]) -> bool:
    """
    Framework-agnostic early exit guard.

    Single responsibility: Decide if LLM generation should proceed based on
    evidence presence.

    This is intentionally trivial (if not chunks). The value is not in the
    condition itself, but in naming it, enforcing it as an execution boundary,
    and logging the decision.

    Args:
        chunks: Retrieved evidence chunks

    Returns:
        True if generation should proceed, False if it should be skipped

    Example:
        chunks = retriever.retrieve(query)
        if not should_generate(chunks):
            return None  # Early exit, LLM not called
        return llm.generate(query, chunks)
    """
    return bool(chunks and len(chunks) > 0)


# ============================================================================
# STRUCTURED DECISION INTERFACE (with reason codes)
# ============================================================================

def check_evidence(query: str, chunks: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Simple evidence check for use in RAG pipelines.

    This is the function shown in README examples.

    Args:
        query: User query string
        chunks: List of retrieved chunks (may be empty)

    Returns:
        Dict with:
        - "status": "STOP" or "ALLOW"
        - "reason": Reason code (e.g., "EVIDENCE_MISSING")
        - "explanation": Human-readable explanation

    Example:
        chunks = retriever.retrieve(query)
        decision = check_evidence(query, chunks)

        if decision["status"] == "STOP":
            return None  # Skip LLM call

        answer = llm.generate(query, chunks)
    """
    # Check if chunks list is empty
    if not chunks or len(chunks) == 0:
        return {
            "status": "STOP",
            "reason": "EVIDENCE_MISSING",
            "explanation": f"No chunks retrieved for query: '{query}'. Generation skipped."
        }

    # In a production system, you'd check:
    # - Relevance scores
    # - Semantic similarity
    # - Chunk quality
    # - Conflicts between chunks

    # For this demo: having ANY chunks = evidence exists
    return {
        "status": "ALLOW",
        "reason": "EVIDENCE_SUFFICIENT",
        "explanation": f"Found {len(chunks)} chunk(s). Generation allowed."
    }


# --- Advanced implementation below (for compliance/enterprise use) ---


class DecisionType(Enum):
    """
    Decision outcomes from boundary gate.

    STOP is a valid, first-class outcome (not an error).
    """
    ALLOW = "ALLOW"
    REVIEW = "REVIEW"
    STOP = "STOP"


class StopReason(Enum):
    """
    Structured reason codes for STOP outcomes.

    Every STOP MUST include one of these codes.
    These codes are for logging, audit, and post-hoc explanation.
    """
    # Category 1: Permission
    PERMISSION_MISSING = "STOP.PERMISSION_MISSING"
    PERMISSION_EXPIRED = "STOP.PERMISSION_EXPIRED"
    PERMISSION_SCOPE_VIOLATED = "STOP.PERMISSION_SCOPE_VIOLATED"

    # Category 2: Decision Automation
    DECISION_AUTOMATION_BLOCKED = "STOP.DECISION_AUTOMATION_BLOCKED"
    APPROVAL_REQUEST_BLOCKED = "STOP.APPROVAL_REQUEST_BLOCKED"
    JUDGMENT_REQUIRED = "STOP.JUDGMENT_REQUIRED"

    # Category 3: Evidence
    EVIDENCE_INSUFFICIENT = "STOP.EVIDENCE_INSUFFICIENT"
    EVIDENCE_MISSING = "STOP.EVIDENCE_MISSING"
    EVIDENCE_INVALID = "STOP.EVIDENCE_INVALID"
    EVIDENCE_CONFLICT = "STOP.EVIDENCE_CONFLICT"

    # Category 4: Boundary
    OUT_OF_SCOPE = "STOP.OUT_OF_SCOPE"
    UNSAFE_QUERY = "STOP.UNSAFE_QUERY"
    DISCRETION_REQUIRED = "STOP.DISCRETION_REQUIRED"


class ReviewReason(Enum):
    """Structured reason codes for REVIEW outcomes."""
    EVIDENCE_CONFLICT = "REVIEW.EVIDENCE_CONFLICT"
    MULTIPLE_INTERPRETATIONS = "REVIEW.MULTIPLE_INTERPRETATIONS"
    DISCRETION_ADVISED = "REVIEW.DISCRETION_ADVISED"


@dataclass
class NextAction:
    """Suggested next action for user (NOT automated)."""
    action: str
    description: str


@dataclass
class BoundaryDecision:
    """
    Output of boundary gate.

    This structure is the contract between gate and caller.
    """
    decision: DecisionType
    reason: str  # StopReason.value or ReviewReason.value or explanation
    explanation: str
    guidance: Optional[dict] = None
    next_actions: Optional[List[NextAction]] = None

    def is_allowed(self) -> bool:
        """Returns True if answer generation is permitted."""
        return self.decision == DecisionType.ALLOW

    def is_review(self) -> bool:
        """Returns True if human review is required."""
        return self.decision == DecisionType.REVIEW

    def is_stopped(self) -> bool:
        """Returns True if answer generation is prohibited."""
        return self.decision == DecisionType.STOP


def boundary_gate(
    retrieved_docs: bool,
    permission_to_answer: bool,
    is_decision_request: bool,
    adapter_suggestion: Optional[DecisionType] = None
) -> BoundaryDecision:
    """
    Non-bypassable judgment boundary gate.

    This function enforces the top-level contract:
    - "Retrieved documents ≠ permission to answer"
    - "This system does not automate decisions"

    Position in architecture:
        Query → Retrieve → [THIS GATE] → Generate → Return

    This gate CANNOT be skipped. No code path bypasses it.

    Args:
        retrieved_docs: Whether documents were retrieved
        permission_to_answer: Whether permission exists to generate answer
        is_decision_request: Whether query is requesting a decision
        adapter_suggestion: Adapter's suggestion (advisory only, non-binding)

    Returns:
        BoundaryDecision with status (ALLOW/REVIEW/STOP) and guidance
    """

    # ========================================================================
    # CORE PHILOSOPHY ENFORCEMENT
    # Philosophy always takes precedence over adapter suggestions
    # ========================================================================

    # Rule 1: "This system does not automate decisions"
    if is_decision_request:
        return BoundaryDecision(
            decision=DecisionType.STOP,
            reason=StopReason.DECISION_AUTOMATION_BLOCKED.value,
            explanation="This system does not automate decisions",
            guidance={
                "primary_message": "Decision automation is blocked by design",
                "philosophy": "This system does not automate decisions"
            },
            next_actions=[
                NextAction(
                    action="route_to_human",
                    description="Route decision request to human decision-maker"
                ),
                NextAction(
                    action="reframe_as_information",
                    description="Reframe as information request instead of decision request"
                )
            ]
        )

    # Rule 2: "Retrieved documents ≠ permission to answer"
    if not permission_to_answer:
        return BoundaryDecision(
            decision=DecisionType.STOP,
            reason=StopReason.PERMISSION_MISSING.value,
            explanation="Retrieved documents do not include permission to generate answers",
            guidance={
                "primary_message": "Retrieved documents ≠ permission to answer",
                "philosophy": "Retrieval does not imply permission"
            },
            next_actions=[
                NextAction(
                    action="request_permission",
                    description="Request permission from document owner or administrator"
                ),
                NextAction(
                    action="add_evidence",
                    description="Add documents that explicitly grant answer permission"
                ),
                NextAction(
                    action="reframe_question",
                    description="Reframe question to match available permissions"
                )
            ]
        )

    # Rule 3: Evidence existence check
    if not retrieved_docs:
        return BoundaryDecision(
            decision=DecisionType.STOP,
            reason=StopReason.EVIDENCE_MISSING.value,
            explanation="No evidence retrieved for this query",
            guidance={
                "primary_message": "Evidence required before answering",
                "philosophy": "Cannot answer without evidence"
            },
            next_actions=[
                NextAction(
                    action="add_documents",
                    description="Add relevant documents to knowledge base"
                ),
                NextAction(
                    action="reframe_question",
                    description="Reframe question to match available documentation"
                ),
                NextAction(
                    action="acknowledge_gap",
                    description="Acknowledge evidence gap and defer to human expert"
                )
            ]
        )

    # ========================================================================
    # ADAPTER SUGGESTION (Advisory only, non-binding)
    # ========================================================================

    # Adapter can suggest STOP, but if conditions allow ANSWER, we proceed
    # This demonstrates that philosophy > adapter logic
    if adapter_suggestion == DecisionType.STOP:
        # Conditions allow answering, adapter suggestion is overridden
        return BoundaryDecision(
            decision=DecisionType.ALLOW,
            reason="Answer permitted",
            explanation="Adapter suggested STOP, but boundary conditions allow answer generation",
            guidance={
                "note": "Adapter suggestion is advisory only. Philosophy takes precedence."
            }
        )

    # If adapter suggests ANSWER but we haven't hit STOP yet, that's fine
    # (We already checked all STOP conditions above)

    # ========================================================================
    # ALL CHECKS PASSED - ALLOW
    # ========================================================================

    return BoundaryDecision(
        decision=DecisionType.ALLOW,
        reason="Answer permitted",
        explanation="All boundary conditions satisfied. Answer generation permitted.",
        guidance={
            "note": "Permission verified. Evidence exists. Not a decision request."
        }
    )


# ============================================================================
# PUBLIC API (matches specification)
# ============================================================================

def check_boundary(
    retrieved_docs: bool,
    permission_to_answer: bool,
    is_decision_request: bool,
    adapter_suggestion: Optional[str] = None
) -> dict:
    """
    Public API for boundary checking.

    This is the function external systems should call.
    Returns a dictionary for easy serialization.
    """
    adapter_enum = None
    if adapter_suggestion:
        adapter_enum = DecisionType[adapter_suggestion]

    decision = boundary_gate(
        retrieved_docs=retrieved_docs,
        permission_to_answer=permission_to_answer,
        is_decision_request=is_decision_request,
        adapter_suggestion=adapter_enum
    )

    return {
        "decision": decision.decision.value,
        "reason": decision.reason,
        "explanation": decision.explanation,
        "guidance": decision.guidance,
        "next_actions": [
            {"action": a.action, "description": a.description}
            for a in (decision.next_actions or [])
        ]
    }


# ============================================================================
# CLI INTERFACE
# ============================================================================

if __name__ == "__main__":
    import sys
    import json
    import argparse

    parser = argparse.ArgumentParser(
        description="Stop-first RAG evidence checker (CLI)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check with JSON chunks file
  python gate.py --query "What is the CEO's salary?" --chunks chunks.json

  # Check with empty chunks (will STOP)
  python gate.py --query "What is the CEO's salary?" --chunks-empty

  # Pipe chunks via stdin
  echo '[]' | python gate.py --query "What is the CEO's salary?" --chunks-stdin

  # Quick test
  python gate.py --query "test query" --chunks-empty
        """
    )

    parser.add_argument("--query", required=True, help="Query string")

    chunks_group = parser.add_mutually_exclusive_group(required=True)
    chunks_group.add_argument("--chunks", help="Path to JSON/JSONL file with chunks")
    chunks_group.add_argument("--chunks-stdin", action="store_true", help="Read chunks from stdin")
    chunks_group.add_argument("--chunks-empty", action="store_true", help="Use empty chunks (test STOP)")

    parser.add_argument("--output", choices=["json", "text"], default="text", help="Output format")

    args = parser.parse_args()

    # Load chunks
    chunks = []
    if args.chunks_empty:
        chunks = []
    elif args.chunks_stdin:
        try:
            chunks = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON from stdin: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            with open(args.chunks, 'r') as f:
                # Try JSONL format first
                if args.chunks.endswith('.jsonl'):
                    chunks = []
                    for line in f:
                        line = line.strip()
                        if line:
                            chunks.append(json.loads(line))
                else:
                    # JSON format
                    chunks = json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found: {args.chunks}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in file: {e}", file=sys.stderr)
            sys.exit(1)

    # Run check
    decision = check_evidence(args.query, chunks)

    # Output
    if args.output == "json":
        print(json.dumps(decision, indent=2))
    else:
        # Human-readable text
        print(f"Query: {args.query}")
        print(f"Chunks: {len(chunks)}")
        print(f"Decision: {decision['status']}")
        print(f"Reason: {decision['reason']}")
        print(f"Explanation: {decision['explanation']}")

        if decision['status'] == 'STOP':
            print("\n🚫 LLM generation should be SKIPPED")
            sys.exit(1)  # Exit code 1 for STOP (useful in scripts)
        else:
            print("\n✅ LLM generation can PROCEED")
            sys.exit(0)
