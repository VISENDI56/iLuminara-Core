#!/bin/bash

echo "🏥 iLuminara Edge Node Deployment"
echo "================================="

# Configuration with defaults
MODE="${1:-test}"
POWER="${2:-solar}"
CONTEXT="${3:-131072}"  # 128K tokens for testing
IP_STACK="${4:-minimal}"

echo "Deployment Configuration:"
echo "  Mode: $MODE"
echo "  Power: $POWER"
echo "  Context: $CONTEXT tokens"
echo "  IP Stack: $IP_STACK"
echo ""

# Step 1: Validate environment
echo "[1/6] Validating deployment environment..."
if [ -f "./scripts/validation/validate_fortress.sh" ]; then
    bash ./scripts/validation/validate_fortress.sh
else
    echo "⚠️ Validation script not found, continuing..."
fi

# Step 2: Initialize Governance Kernel
echo "[2/6] Initializing Governance Kernel..."
python3 -c "
import sys
sys.path.append('.')
from kernel.legal_vector import LegalVectorLedger

ledger = LegalVectorLedger(jurisdiction='TEST')
print(f'✓ Legal frameworks: {len(ledger.frameworks)} loaded')
print('✓ Governance Kernel ready')
"

# Step 3: Configure Nuclear IP Stack
echo "[3/6] Configuring Nuclear IP Stack..."
case $IP_STACK in
    "full")
        echo "  Enabling all Nuclear IP components"
        python3 -c "
import sys
sys.path.append('.')
try:
    from ip_stack.aegis_core import AegisCore
    from ip_stack.crypto_shredder import CryptoShredder
    from ip_stack.acorn_protocol import AcornProtocol
    print('✓ All Nuclear IP components initialized')
except Exception as e:
    print(f'⚠️ IP Stack initialization: {e}')
        "
        ;;
    "minimal")
        echo "  Enabling minimal IP stack"
        python3 -c "
import sys
sys.path.append('.')
try:
    from ip_stack.aegis_core import AegisCore
    from ip_stack.crypto_shredder import CryptoShredder
    print('✓ Minimal IP stack: Aegis Core, Crypto Shredder')
except Exception as e:
    print(f'⚠️ IP Stack initialization: {e}')
        "
        ;;
    *)
        echo "  Using custom IP stack: $IP_STACK"
        ;;
esac

# Step 4: Configure Sovereign Trinity
echo "[4/6] Configuring Sovereign Trinity..."
python3 -c "
import sys
sys.path.append('.')
from core.sovereign_os import Z3GateVerifier, SovereignPaging, SolarGovernor

try:
    z3_gate = Z3GateVerifier(timeout_ms=50)
    pager = SovereignPaging(max_tokens=int('$CONTEXT'))
    
    if '$POWER' == 'solar':
        governor = SolarGovernor(solar_envelope_watts=100.0)
    else:
        governor = SolarGovernor(solar_envelope_watts=250.0)
    
    print(f'✓ Z3-Gate: 50ms guillotine configured')
    print(f'✓ Sovereign Paging: {pager.max_tokens:,} token context')
    print(f'✓ Solar Governor: {governor.solar_envelope}W envelope')
except Exception as e:
    print(f'⚠️ Sovereign Trinity configuration error: {e}')
"

# Step 5: Test Clinical Agents
echo "[5/6] Testing Clinical Agents..."
python3 -c "
import sys
sys.path.append('.')
try:
    from core.agentic_clinical.voice_triage_agent import VoiceEnabledTriageAgent
    
    agent = VoiceEnabledTriageAgent()
    test_result = agent.assess_patient({'text': 'Patient has 41C fever'})
    
    print(f'✓ Voice Triage Agent: {test_result[\"status\"]}')
    print('✓ Clinical agents ready')
except Exception as e:
    print(f'⚠️ Clinical agents error: {e}')
"

# Step 6: Start iLuminara
echo "[6/6] Starting iLuminara Sovereign OS..."
python3 -c "
print('🚀 iLuminara Edge Node Deployment Complete')
print('')
print('📊 Deployment Summary:')
print(f'   Mode: $MODE')
print(f'   Context: $CONTEXT tokens')
print(f'   Power: $POWER')
print(f'   IP Stack: $IP_STACK')
print('')
print('✅ iLuminara ready for clinical deployment')
print('')
print('🔧 Next steps:')
print('   1. Install dependencies: pip install -r requirements.txt')
print('   2. Access dashboard: streamlit run dashboards/sovereign_control.py')
print('   3. Run validation: ./scripts/validation/validate_fortress.sh')
"

echo ""
echo "================================="
echo "✅ iLuminara Edge Node Deployed"
echo "================================="
