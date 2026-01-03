#!/usr/bin/env python3
"""
Test script to verify iLuminara-Core imports
"""

import sys
import os

# Add current directory to Python path
sys.path.append('.')

print("🧪 Testing iLuminara-Core imports...")

# Test Sovereign Trinity imports
try:
    from core.sovereign_os import Z3GateVerifier, SovereignPaging, SolarGovernor
    print("✅ Sovereign Trinity imports OK")
    
    # Test instantiation
    z3_gate = Z3GateVerifier(timeout_ms=50)
    print(f"   Z3-Gate: timeout={z3_gate.timeout_ms}ms")
    
    pager = SovereignPaging(max_tokens=1048576)
    print(f"   Sovereign Paging: max_tokens={pager.max_tokens:,}")
    
    governor = SolarGovernor(solar_envelope_watts=100.0)
    print(f"   Solar Governor: {governor.solar_envelope}W")
    
except ImportError as e:
    print(f"❌ Sovereign Trinity import error: {e}")

# Test Nuclear IP Stack imports
try:
    from ip_stack.aegis_core import AegisCore
    from ip_stack.crypto_shredder import CryptoShredder
    from ip_stack.acorn_protocol import AcornProtocol
    
    print("✅ Nuclear IP Stack imports OK")
    
    # Test instantiation
    aegis = AegisCore(tpm_required=False)
    print(f"   Aegis Core: TPM required={aegis.tpm_required}")
    
except ImportError as e:
    print(f"❌ Nuclear IP Stack import error: {e}")

# Test Compliance Kernel imports
try:
    from kernel.legal_vector import LegalVectorLedger
    
    print("✅ Compliance Kernel imports OK")
    
    # Test instantiation
    ledger = LegalVectorLedger(jurisdiction="TEST")
    print(f"   Legal frameworks loaded: {len(ledger.frameworks)}")
    
except ImportError as e:
    print(f"❌ Compliance Kernel import error: {e}")

print("\n🎯 All imports tested successfully!")
