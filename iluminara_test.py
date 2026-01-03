#!/usr/bin/env python3
import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_z3_gate():
    """Test Z3-Gate functionality"""
    try:
        from core.sovereign_os.z3_gate import Z3GateVerifier
        print("✓ Z3GateVerifier imported")
        
        verifier = Z3GateVerifier(timeout_ms=50)
        print(f"  Created with timeout: {verifier.timeout_ms}ms")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_sovereign_paging():
    """Test Sovereign Paging functionality"""
    try:
        from core.sovereign_os.sovereign_paging import SovereignPaging
        print("✓ SovereignPaging imported")
        
        pager = SovereignPaging(max_tokens=1048576)
        print(f"  Created with max_tokens: {pager.max_tokens:,}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_solar_governor():
    """Test Solar Governor functionality"""
    try:
        from core.sovereign_os.solar_governor import SolarGovernor, PrecisionMode
        print("✓ SolarGovernor imported")
        
        governor = SolarGovernor(solar_envelope_watts=100.0)
        print(f"  Created with envelope: {governor.solar_envelope}W")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 iLuminara-Core Module Test")
    print("=" * 40)
    
    tests = [
        ("Z3-Gate", test_z3_gate),
        ("Sovereign Paging", test_sovereign_paging),
        ("Solar Governor", test_solar_governor)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1
    
    print(f"\n" + "=" * 40)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed!")
    else:
        print("⚠️ Some tests failed")
        sys.exit(1)
