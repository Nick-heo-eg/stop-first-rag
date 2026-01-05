# RAG Evaluation Template

This folder compares a traditional “answer-first” RAG and the STOP-first judgment RAG. Both runners must log their outputs to JSON to be scored with the script below.

## Comparison Metrics

For each query we capture:
- `answered`: did the system produce an answer (vs. STOP)?
- `correct`: human/ground-truth verdict (1/0)
- `hallucination`: 1 if the answer made unsupported claims
- `stop_reason`: optional reason if it stopped

Derived metrics:
- `answer_rate`: fraction of queries that produced answers
- `precision_at_answer`: `correct_answers / answers_emitted`
- `hallucination_rate`: `hallucinations / answers_emitted`
- `wrong_but_answered`: answers emitted that were wrong (`answered=1 & correct=0`)
- `stop_rate`: fraction of queries stopped, with reason distribution

## Files

- `sample_questions.jsonl` – example query set with known ground truth
- `traditional_outputs.jsonl` – placeholder format for a typical RAG runner
- `judgment_outputs.jsonl` – placeholder for STOP-first results
- `compare.py` – reads the two JSONL logs, prints the metrics above, and writes a per-query CSV.
- `plot_metrics.py` – optional matplotlib script that generates a bar chart comparing answer rate / precision / hallucination / stop rate / wrong-but-answered.

## Workflow

1. Run both RAG pipelines against the same query set (e.g., `sample_questions.jsonl`), producing JSONL outputs with the schema described above. Each line should include: `query`, `answered`, optional `answer`, optional `correct`, optional `hallucination`, and optional `stop_reason`.
2. Populate `correct` / `hallucination` fields via manual review or automated grading.
3. Run:
   ```bash
   python rag_judgment_trace/eval/compare.py \
     --traditional rag_judgment_trace/eval/traditional_outputs.jsonl \
     --judgment rag_judgment_trace/eval/judgment_outputs.jsonl \
     --out rag_judgment_trace/eval/report.csv
   ```
4. (Optional) Install matplotlib (`pip install matplotlib`) and run:
   ```bash
   python rag_judgment_trace/eval/plot_metrics.py \
     --traditional rag_judgment_trace/eval/traditional_outputs.jsonl \
     --judgment rag_judgment_trace/eval/judgment_outputs.jsonl \
     --out rag_judgment_trace/eval/metrics.png
   ```
5. Attach the CSV/PNG when presenting the trade-off between “answer rate” and “cost of being wrong.”

## Hooking in real runners

- Traditional RAG runner: log outputs with the schema above right after generation (before any UI formatting). Ensure hallucinations are marked.
- STOP-first runner: reuse the existing trace data to populate the JSONL (answered flag = `FinalDecision == "ANSWER"`; stop reason from `reason_code` when `STOP`).
- Multiple query batches can be concatenated; the scripts aggregate automatically.
