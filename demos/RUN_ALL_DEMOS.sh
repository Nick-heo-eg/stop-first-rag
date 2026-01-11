#!/bin/bash
set -e

echo "=== STOP-first RAG Gate Demos ==="
echo ""

echo ">>> HR Domain"
cd multidomain
python3 ajt_gate_multidomain_jd.py hr/data/candidates hr/data/chunks hr/policy/jd_policy.yaml hr/out_demo
echo ""

echo ">>> Finance Domain"
python3 ajt_gate_multidomain_jd.py finance/data/candidates finance/data/chunks finance/policy/jd_policy.yaml finance/out_demo
echo ""

echo ">>> Medical Domain"
cd ../medical
python3 ajt_gate_med.py data/candidates data/chunks policy/jd_policy.yaml out_demo
echo ""

echo "=== All demos completed ==="
echo "Output files created:"
echo "  - multidomain/hr/out_demo/"
echo "  - multidomain/finance/out_demo/"
echo "  - medical/out_demo/"
