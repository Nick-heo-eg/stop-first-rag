# CLI Usage

Stop-first RAG can be used directly from the command line.

## Quick Test

```bash
# Test with no evidence (STOP)
python gate.py --query "What is the CEO's salary?" --chunks-empty
```

Output:
```
Query: What is the CEO's salary?
Chunks: 0
Decision: STOP
Reason: EVIDENCE_MISSING
Explanation: No chunks retrieved for query: '...'. Generation skipped.

🚫 LLM generation should be SKIPPED
```

Exit code: `1` (STOP = failure, useful for shell scripts)

---

## Real Usage

### 1. From JSON file

```bash
# Your retriever saves chunks to file
echo '[{"text": "relevant chunk"}]' > chunks.json

# Check evidence
python gate.py --query "What is quantum computing?" --chunks chunks.json
```

### 2. From JSONL file

```bash
# JSONL format (one chunk per line)
python gate.py --query "..." --chunks chunks.jsonl
```

### 3. From stdin (pipe)

```bash
# Pipe from your retriever
your-retriever query "..." | python gate.py --query "..." --chunks-stdin
```

### 4. JSON output (for scripts)

```bash
python gate.py --query "..." --chunks-empty --output json
```

Output:
```json
{
  "status": "STOP",
  "reason": "EVIDENCE_MISSING",
  "explanation": "No chunks retrieved for query: '...'. Generation skipped."
}
```

---

## Integration with RAG Pipeline

### Shell script example

```bash
#!/bin/bash

QUERY="What is the CEO's salary?"

# Step 1: Retrieve chunks
chunks=$(your-retriever "$QUERY")

# Step 2: Check evidence
echo "$chunks" | python gate.py --query "$QUERY" --chunks-stdin --output json > decision.json

# Step 3: Check exit code
if [ $? -eq 0 ]; then
    echo "Evidence verified, calling LLM..."
    your-llm generate "$QUERY" "$chunks"
else
    echo "No evidence found, skipping LLM call"
    cat decision.json
fi
```

### Python subprocess example

```python
import subprocess
import json

query = "What is the CEO's salary?"
chunks = retriever.retrieve(query)

# Check evidence via CLI
result = subprocess.run(
    ["python", "gate.py", "--query", query, "--chunks-stdin", "--output", "json"],
    input=json.dumps(chunks),
    capture_output=True,
    text=True
)

decision = json.loads(result.stdout)

if decision["status"] == "STOP":
    print(f"Generation skipped: {decision['reason']}")
else:
    answer = llm.generate(query, chunks)
    print(answer)
```

---

## Exit Codes

- `0`: ALLOW (evidence verified, proceed to LLM)
- `1`: STOP (evidence missing, skip LLM call)

Useful for shell scripts:

```bash
python gate.py --query "..." --chunks chunks.json && \
    echo "Calling LLM..." || \
    echo "Skipping LLM"
```

---

## Help

```bash
python gate.py --help
```

Shows all options and examples.
