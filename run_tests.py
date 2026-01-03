#!/usr/bin/env python3
"""
Working test script for iLuminara-Core
"""

import sys
sys.path.append('.')

print("🧪 iLuminara-Core Working Test")
print("=" * 40)

# Test 1: Import all modules
print("\n[1/5] Testing imports...")
try:
    from core.sovereign_os import Z3GateVerifier, SovereignPaging, SolarGovernor
    print("✓ Sovereign Trinity imported")
    
    from ip_stack.aegis_core import AegisCore
    print("✓ Nuclear IP Stack imported")
    
    from kernel.legal_vector import LegalVectorLedger
    print("✓ Compliance Kernel imported")
    
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Test 2: Test Z3-Gate
print("\n[2/5] Testing Z3-Gate...")
try:
    z3_gate = Z3GateVerifier(timeout_ms=50)
    
    # Create test data
    fp16_output = {'risk_level': 0.9}
    nvfp4_output = {'risk_level': 0.85}
    clinical_context = {'temperature': 41.5}
    
    result = z3_gate.verify_inference(fp16_output, nvfp4_output, clinical_context)
    print(f"✓ Z3-Gate result: {result['status']}")
    print(f"  Precision: {result['precision']}")
except Exception as e:
    print(f"❌ Z3-Gate test error: {e}")

# Test 3: Test Sovereign Paging
print("\n[3/5] Testing Sovereign Paging...")
try:
    pager = SovereignPaging(max_tokens=1048576)
    
    # Create test history
    test_history = [{'event': f'visit_{i}', 'data': f'data_{i}'} for i in range(100)]
    
    context = pager.load_patient_context('patient_001', test_history)
    print(f"✓ Paging context loaded: {context['page_count']} pages")
    print(f"  Total tokens: {context['total_tokens']}")
except Exception as e:
    print(f"❌ Sovereign Paging test error: {e}")

# Test 4: Test Solar Governor
print("\n[4/5] Testing Solar Governor...")
try:
    governor = SolarGovernor(solar_envelope_watts=100.0)
    
    z3_result = {'status': 'SAT'}
    mode = governor.optimize_precision('chest_xray', z3_result)
    
    print(f"✓ Solar Governor mode: {mode.value}")
except Exception as e:
    print(f"❌ Solar Governor test error: {e}")

# Test 5: Test Aegis Core
print("\n[5/5] Testing Aegis Core...")
try:
    aegis = AegisCore(tpm_required=False)
    integrity = aegis.verify_hardware_integrity()
    print(f"✓ Aegis Core integrity: {integrity}")
except Exception as e:
    print(f"❌ Aegis Core test error: {e}")

print("\n" + "=" * 40)
print("🎯 All tests completed!")
print("\nNext: Run 'make install' to install dependencies")
print("Then: Run './scripts/validation/validate_fortress.sh'")
