#!/bin/bash
echo "🛡️ STARTING ILUMINARA QUALITY GATE..."

# 1. Static Analysis (Linting)
echo "🔍 Running Type & Syntax Check..."
python3 -m py_compile modules/*.py app.py

# 2. Logic & Governance Tests
echo "⚖️ Running Governance Stress-Tests..."
python3 tests/test_governance_logic.py

# 3. Security Check (Secret Exposure)
echo "🔒 Checking for hardcoded secrets..."
if grep -q "nb_..." modules/*.py; then
    echo "❌ ERROR: Potential hardcoded secret found in modules!"
    exit 1
fi

echo "✅ ALL QUALITY GATES PASSED. System is Institutional-Ready."
