# Stop-First RAG

Judgment-first RAG implementation with minimal dependencies.

Adds a decision layer before answer generation.
STOP is a first-class outcome.

---

## Quickstart

```bash
git clone https://github.com/Nick-heo-eg/stop-first-rag.git
cd stop-first-rag
python3 demo_minimal.py
```

No external dependencies required (Python stdlib only).

---

## Example Output

```
Query: What is our return policy for opened software?

Retrieved 3 evidence candidates

[E1] Decision: REJECT
     Reason: Evidence covers physical products, not software

[E2] Decision: DEFER
     Reason: Mentions topic but provides no concrete answer

[E3] Decision: REJECT
     Reason: Confidence 0.43 below threshold 0.5

Final Decision: STOP
No acceptable evidence found. Cannot generate answer.
```

---

## Multi-Domain Benchmark

| Domain  | Cases | STOP Rate | Notes                     |
|---------|-------|-----------|---------------------------|
| HR      | 60    | Measured  | Policy ambiguity handling |
| Finance | 40    | Measured  | Risk-sensitive queries    |
| Medical | 30    | Measured  | Safety-critical responses |

Benchmark datasets available in `benchmarks/` and `datasets/` directories.

---

## How It Works

1. Retrieve evidence candidates
2. Judge each evidence item (ACCEPT / REJECT / DEFER)
3. If no ACCEPT → STOP
4. Generate answer only when threshold satisfied

---

## Key Files

- `demo_minimal.py` — Self-contained demonstration
- `demo.py` — Extended demo
- `gate.py` — Core judgment logic
- `eval/` — Evaluation scripts
- `demos/` — Additional examples

---

## License

MIT
