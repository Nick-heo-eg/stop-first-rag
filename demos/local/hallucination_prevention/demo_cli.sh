#!/bin/bash
# Hallucination Prevention Demo - CLI Runner

set -e

# Get script directory
DEMO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Running Hallucination Prevention Demo..."
echo

# Run Python demo
python3 "$DEMO_DIR/demo.py"

echo
echo "Demo complete!"
echo
echo "What you just saw:"
echo "  - Queries with NO evidence → STOP (hallucination prevented)"
echo "  - Queries WITH evidence → ALLOW (safe to generate)"
echo
echo "Key takeaway: STOP is not a failure, it's quality control."
