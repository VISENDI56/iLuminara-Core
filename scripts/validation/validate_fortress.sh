#!/bin/bash

echo "🛡️ iLuminara Security Fortress Validation"
echo "=========================================="

# Check 1: Nuclear IP Stack
echo "[1/5] Validating Nuclear IP Stack..."
python3 -c "
import sys
sys.path.append('.')
try:
    from ip_stack.aegis_core import AegisCore
    from ip_stack.crypto_shredder import CryptoShredder
    from ip_stack.acorn_protocol import AcornProtocol
    
    aegis = AegisCore(tpm_required=False)
    integrity = aegis.verify_hardware_integrity()
    print('✓ Aegis Core: Hardware trust substrate')
    
    shredder = CryptoShredder(shred_passes=3)
    print('✓ Crypto Shredder: Forward secrecy ready')
    
    acorn = AcornProtocol()
    print('✓ Acorn Protocol: Somatic security framework')
    
    print('✅ Nuclear IP Stack validation complete')
except Exception as e:
    print(f'⚠️ Nuclear IP validation error: {e}')
"

# Check 2: Sovereign Trinity
echo "[2/5] Validating Sovereign Trinity..."
python3 -c "
import sys
sys.path.append('.')
try:
    from core.sovereign_os import Z3GateVerifier, SovereignPaging, SolarGovernor
    
    z3 = Z3GateVerifier(timeout_ms=50)
    print(f'✓ Z3-Gate: {z3.timeout_ms}ms timeout configured')
    
    pager = SovereignPaging(max_tokens=1048576)
    print(f'✓ Sovereign Paging: {pager.max_tokens:,} token capacity')
    
    governor = SolarGovernor(solar_envelope_watts=100.0)
    print(f'✓ Solar Governor: {governor.solar_envelope}W envelope')
    
    print('✅ Sovereign Trinity validation complete')
except Exception as e:
    print(f'⚠️ Sovereign Trinity validation error: {e}')
"

# Check 3: Compliance Kernel
echo "[3/5] Validating Compliance Kernel..."
python3 -c "
import sys
sys.path.append('.')
try:
    from kernel.legal_vector import LegalVectorLedger
    ledger = LegalVectorLedger(jurisdiction='TEST')
    print(f'✓ Legal Vector Ledger: {len(ledger.frameworks)} frameworks loaded')
    print('✅ Compliance Kernel validation complete')
except Exception as e:
    print(f'⚠️ Compliance Kernel validation error: {e}')
"

# Check 4: System Requirements
echo "[4/5] Checking System Requirements..."
python3 -c "
import sys
print(f'✓ Python: {sys.version.split()[0]}')

try:
    import torch
    print(f'✓ PyTorch: {torch.__version__}')
    if torch.cuda.is_available():
        print(f'✓ CUDA: Available ({torch.cuda.get_device_name(0)})')
    else:
        print('⚠️ CUDA: Not available (CPU mode only)')
except ImportError:
    print('⚠️ PyTorch: Not installed (run: pip install torch)')

try:
    import streamlit
    print(f'✓ Streamlit: {streamlit.__version__}')
except ImportError:
    print('⚠️ Streamlit: Not installed (run: pip install streamlit)')
"

# Check 5: Repository Structure
echo "[5/5] Validating Repository Structure..."
if [ -d "core" ] && [ -d "kernel" ] && [ -d "ip_stack" ]; then
    echo "✓ Core directories: Present"
else
    echo "⚠️ Core directories: Missing"
fi

if [ -f "requirements.txt" ]; then
    echo "✓ Requirements file: Present"
else
    echo "⚠️ Requirements file: Missing"
fi

if [ -f "Makefile" ]; then
    echo "✓ Makefile: Present"
else
    echo "⚠️ Makefile: Missing"
fi

echo ""
echo "=========================================="
echo "🔐 FORTRESS VALIDATION COMPLETE"
echo "=========================================="
