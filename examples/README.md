# Example Traces

This directory contains real STOP-First RAG execution traces.

## stop_trace.jsonl

**Query**: "What is our return policy for opened software?"

**Result**: STOP with reason code `NO_ACCEPTABLE_EVIDENCE`

### What Happened

1. **Retrieved 3 evidence candidates**:
   - E1: "All physical products may be returned within 14 days" (physical products, not software)
   - E2: "Software has different policies - contact support" (no concrete answer)
   - E3: "Refunds processed in 5-7 days" (about timing, not eligibility)

2. **Evidence Judge decisions**:
   - E1: REJECT (relevance gap - physical vs software)
   - E2: DEFER (insufficient detail - no concrete policy stated)
   - E3: REJECT (off-topic - about processing, not eligibility)

3. **Final Decision**: STOP
   - Reason code: `NO_ACCEPTABLE_EVIDENCE`
   - Accepted evidence: 0
   - Query required concrete software return policy
   - No retrieved evidence provided that information

### Key Insight

**Traditional RAG** would likely have generated: "Software can be returned within 14 days with receipt" (hallucination combining E1 physical policy + E2 software mention).

**STOP-First RAG** correctly identified that **no evidence directly answers the question** and stopped with a structured reason.

### View the Raw Trace

```bash
cat examples/stop_trace.jsonl | jq .
```

Or step through each event:

```bash
jq -c 'select(.event == "EVIDENCE_JUDGE")' examples/stop_trace.jsonl
jq -c 'select(.event == "FINAL_DECISION")' examples/stop_trace.jsonl
```

### Trace Schema

Each line is a JSON event with:
- `event`: Event type (RUN_START, RETRIEVE, EVIDENCE_JUDGE, FINAL_DECISION, RUN_END)
- `timestamp`: ISO 8601 timestamp
- `data`: Event-specific payload

This append-only format enables:
- Complete audit trail
- Negative proof ("judgment was required but evidence was insufficient")
- Reproducible debugging
- Metrics extraction (e.g., STOP rate by reason code)
