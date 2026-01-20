#!/usr/bin/env python3
"""
Hallucination Prevention Demo

Shows how stop-first RAG prevents hallucinations by checking evidence
BEFORE calling LLM generation.

Core principle: No evidence → No LLM call → No generation
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple


def load_query(query_file: Path) -> Dict:
    """Load query candidate from JSON file."""
    with open(query_file, 'r') as f:
        return json.load(f)


def load_chunks(chunks_file: Path) -> List[Dict]:
    """
    Load evidence chunks from JSONL file.

    This simulates your retriever's output (retriever.retrieve(query)).
    In your real system, this would be the list of chunks returned by your retriever.
    """
    if not chunks_file.exists():
        return []

    chunks = []
    with open(chunks_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                chunks.append(json.loads(line))
    return chunks


def check_evidence(query: str, chunks: List[Dict]) -> Tuple[str, str, str, bool]:
    """
    Evidence gate: Check if we have sufficient evidence to generate.

    This is the stop-first layer that sits between your retriever and LLM.

    Returns: (decision, reason, explanation, generation_skipped)
    - decision: "STOP" or "ALLOW"
    - reason: Structured reason code
    - explanation: Human-readable explanation
    - generation_skipped: True if LLM call should be skipped
    """
    if len(chunks) == 0:
        return (
            "STOP",
            "EVIDENCE_MISSING",
            f"No relevant chunks retrieved for query: '{query}'. Cannot generate without evidence.",
            True  # LLM generation will be skipped
        )

    # In a real system, you'd check relevance scores, semantic similarity, etc.
    # For this demo, having ANY chunks = evidence exists
    return (
        "ALLOW",
        "EVIDENCE_SUFFICIENT",
        f"Found {len(chunks)} relevant chunk(s). Safe to generate answer.",
        False  # LLM generation will proceed
    )


def run_demo():
    """Run hallucination prevention demo."""
    print("=" * 60)
    print("  Hallucination Prevention Demo")
    print("=" * 60)
    print()
    print("Testing stop-first RAG evidence checking...")
    print()

    # Get demo directory
    demo_dir = Path(__file__).parent
    candidates_dir = demo_dir / "data" / "candidates"
    chunks_dir = demo_dir / "data" / "chunks"

    # Find all query files
    query_files = sorted(candidates_dir.glob("*.json"))

    results = {
        "ALLOW": 0,
        "STOP": 0,
        "hallucinations_prevented": 0
    }

    for query_file in query_files:
        # Load query
        query_data = load_query(query_file)
        query_id = query_data["query_id"]
        query = query_data["query"]
        expected_decision = query_data.get("expected_decision", "UNKNOWN")

        # Load corresponding chunks
        chunks_file = chunks_dir / f"{query_file.stem}.jsonl"
        chunks = load_chunks(chunks_file)

        # Check evidence (stop-first gate)
        decision, reason, explanation, generation_skipped = check_evidence(query, chunks)

        # Display result
        print(f"Query: {query}")
        print(f"  Retrieved chunks: {len(chunks)}")
        print(f"  Decision: {decision}")
        print(f"  Reason: {reason}")
        print(f"  Explanation: {explanation}")
        if generation_skipped:
            print(f"  🚫 LLM generation: SKIPPED (not called)")
        else:
            print(f"  ✅ LLM generation: ALLOWED (would proceed to LLM)")

        # Verify against expected
        if decision == expected_decision:
            print(f"  ✅ Correct (expected {expected_decision})")
        else:
            print(f"  ❌ Unexpected (expected {expected_decision}, got {decision})")

        # Track results
        results[decision] += 1
        if decision == "STOP" and expected_decision == "STOP":
            results["hallucinations_prevented"] += 1

        print()

    # Summary
    print("=" * 60)
    print("  Results")
    print("=" * 60)
    total = results["ALLOW"] + results["STOP"]
    print(f"Total queries tested: {total}")
    print(f"  ALLOW: {results['ALLOW']} ({results['ALLOW']/total*100:.0f}%)")
    print(f"  STOP:  {results['STOP']} ({results['STOP']/total*100:.0f}%)")
    print()
    print(f"Hallucinations prevented: {results['hallucinations_prevented']}")
    print()
    print("=" * 60)
    print("  Key Insight")
    print("=" * 60)
    print(f"{results['STOP']/total*100:.0f}% STOP rate is not a failure.")
    print("It means:")
    print(f"  - {results['STOP']} queries had no evidence → LLM generation skipped → No hallucination")
    print(f"  - {results['ALLOW']} query had evidence → LLM generation allowed → Safe to generate")
    print()
    print("Standard RAG would:")
    print(f"  - Call LLM {total} times (generate ALL answers, some hallucinated)")
    print()
    print("Stop-first RAG does:")
    print(f"  - Call LLM only {results['ALLOW']} time (when evidence verified)")
    print(f"  - Skip LLM {results['STOP']} times (when evidence missing)")
    print(f"  - Save {results['STOP']} unnecessary LLM calls")
    print()


if __name__ == "__main__":
    run_demo()
