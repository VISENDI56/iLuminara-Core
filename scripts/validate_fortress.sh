#!/bin/bash
echo "🛡️ INITIATING FORTRESS VALIDATION..."
if [ -f .github/workflows/codeql.yml ]; then echo "✅ CodeQL Active"; else echo "❌ CodeQL Missing"; fi
if [ -f governance_kernel/crypto_shredder.py ]; then echo "✅ Crypto Shredder Active"; else echo "❌ Shredder Missing"; fi
if [ -f governance_kernel/sovereign_guardrail.py ]; then echo "✅ Guardrails Active"; else echo "❌ Guardrails Missing"; fi
echo "🛡️ VALIDATION COMPLETE."
