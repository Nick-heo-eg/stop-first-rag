#!/bin/bash
# Local Developer Demos Runner
# Runs all developer-focused demos showing stop-first RAG benefits

set -e

DEMOS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "  Stop-First RAG - Local Developer Demos"
echo "=========================================="
echo
echo "These demos show how stop-first RAG prevents low-quality outputs"
echo "by checking evidence BEFORE generation."
echo
echo "=========================================="
echo

# Demo 1: Hallucination Prevention
echo "Running Demo 1: Hallucination Prevention"
echo "------------------------------------------"
cd "$DEMOS_DIR/local/hallucination_prevention"
./demo_cli.sh
echo

# Future demos (not yet implemented)
echo "=========================================="
echo "  Coming Soon"
echo "=========================================="
echo "Demo 2: Duplicate Query Blocking"
echo "Demo 3: Low-Signal Filtering"
echo

echo "=========================================="
echo "  All Available Demos Completed!"
echo "=========================================="
echo
echo "Next Steps:"
echo "  - Check out demos/regulated/ for compliance-focused demos"
echo "  - Read COMPLIANCE.md for regulatory use cases"
echo "  - See README.md for implementation guide"
echo
