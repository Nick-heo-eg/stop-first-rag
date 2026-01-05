from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class Result:
    query: str
    answered: bool
    answer: Optional[str]
    correct: Optional[int]
    hallucination: Optional[int]
    stop_reason: Optional[str]

    @classmethod
    def from_line(cls, line: str) -> "Result":
        obj = json.loads(line)
        return cls(
            query=obj["query"],
            answered=bool(obj.get("answered", False)),
            answer=obj.get("answer"),
            correct=obj.get("correct"),
            hallucination=obj.get("hallucination"),
            stop_reason=obj.get("stop_reason"),
        )


def load_results(path: Path) -> List[Result]:
    results: List[Result] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            results.append(Result.from_line(line))
    return results


def compute_metrics(results: List[Result]) -> dict:
    total = len(results)
    answered = [r for r in results if r.answered]
    stops = [r for r in results if not r.answered]

    correct_answers = sum(1 for r in answered if r.correct)
    wrong_answers = sum(1 for r in answered if r.correct == 0)
    hallucinations = sum(1 for r in answered if r.hallucination)

    answer_rate = len(answered) / total if total else 0.0
    precision_at_answer = correct_answers / len(answered) if answered else 0.0
    hallucination_rate = hallucinations / len(answered) if answered else 0.0
    wrong_but_answered = wrong_answers
    stop_rate = len(stops) / total if total else 0.0
    stop_reasons = Counter(r.stop_reason or "UNKNOWN" for r in stops)

    return {
        "total": total,
        "answer_rate": answer_rate,
        "precision_at_answer": precision_at_answer,
        "hallucination_rate": hallucination_rate,
        "wrong_but_answered": wrong_but_answered,
        "stop_rate": stop_rate,
        "stop_reasons": dict(stop_reasons),
    }


def write_csv(path: Path, traditional: List[Result], judgment: List[Result]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "query",
                "trad_answered",
                "trad_correct",
                "trad_hallucination",
                "judg_answered",
                "judg_correct",
                "judg_stop_reason",
            ]
        )
        for t, j in zip(traditional, judgment):
            writer.writerow(
                [
                    t.query,
                    int(t.answered),
                    t.correct if t.correct is not None else "",
                    t.hallucination if t.hallucination is not None else "",
                    int(j.answered),
                    j.correct if j.correct is not None else "",
                    j.stop_reason or "",
                ]
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare RAG outputs.")
    parser.add_argument("--traditional", required=True, help="Path to traditional RAG outputs JSONL")
    parser.add_argument("--judgment", required=True, help="Path to judgment-first outputs JSONL")
    parser.add_argument("--out", type=str, default="eval_report.csv", help="CSV output path")
    args = parser.parse_args()

    traditional_results = load_results(Path(args.traditional))
    judgment_results = load_results(Path(args.judgment))

    if len(traditional_results) != len(judgment_results):
        raise SystemExit("Mismatch in number of queries between runs.")

    trad_metrics = compute_metrics(traditional_results)
    judg_metrics = compute_metrics(judgment_results)

    print("=== Traditional RAG ===")
    for k, v in trad_metrics.items():
        print(f"{k}: {v}")

    print("\n=== Judgment-first RAG ===")
    for k, v in judg_metrics.items():
        print(f"{k}: {v}")

    write_csv(Path(args.out), traditional_results, judgment_results)
    print(f"\nCSV summary written to {args.out}")


if __name__ == "__main__":
    main()
