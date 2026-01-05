from __future__ import annotations

from schema import new_run_id
from trace import TraceLogger
from retrieve import load_sample_evidence, retrieve_top_k
from judge import judge_evidence, judge_final
from respond import build_answer_candidates


def main():
    run_id = new_run_id()
    t = TraceLogger(run_id=run_id)

    query = open("samples/sample_query.txt", "r", encoding="utf-8").read().strip()

    t.emit("RUN_START", {"query": query, "version": "mvp-judge-trace-0.1"})

    all_evidence = load_sample_evidence()
    topk = retrieve_top_k(all_evidence, query=query, k=5)

    t.emit("RETRIEVE", {"top_k": len(topk), "candidates": [e.to_dict() for e in topk]})

    judgments = []
    accepted = []
    for e in topk:
        j = judge_evidence(e)
        judgments.append(j)
        if j.decision == "ACCEPT":
            accepted.append(e)
        t.emit("EVIDENCE_JUDGE", j.to_dict())

    candidates = build_answer_candidates(query=query, accepted=accepted)
    t.emit("ANSWER_CANDIDATES", {"count": len(candidates), "candidates": [c.to_dict() for c in candidates]})

    final_decision, reason_code, extra = judge_final(accepted=accepted, candidates=candidates)
    t.emit("FINAL_DECISION", {"decision": final_decision, "reason_code": reason_code, "extra": extra})

    if final_decision == "STOP":
        final_answer = f"STOP: {reason_code}\nExtra: {extra}\nNo answer was produced due to policy."
        citations = []
    else:
        best = max(candidates, key=lambda c: c.estimated_coverage)
        final_answer = best.text
        citations = best.cited_evidence_ids

    t.emit("RUN_END", {"final_answer": final_answer, "citations": citations})

    print("=== FINAL ===")
    print(final_answer)
    print("\nCITATIONS:", citations)
    print("\nTRACE:", t.file_path())


if __name__ == "__main__":
    main()
