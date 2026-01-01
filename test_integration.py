# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# COMPETITOR EXCLUSION: Commercial use by entities offering Sovereign/Health OS 
# solutions is STRICTLY PROHIBITED without a commercial license.
# 
# The Sovereign Immune System (Omni-Law) and JEPA-MPC Architecture are 
# proprietary inventions of iLuminara.
# ------------------------------------------------------------------------------

#!/usr/bin/env python3
"""
Integration Test Script for iLuminara GCP Prototype
Tests all backend services and endpoints
"""

import sys
import requests
import json

# Colors for terminal output
GREEN = '\33[0;32m'
RED = '\33[0;31m'
YELLOW = '\33[1;33m'
NC = '\33[0m'

API_URL = "http://127.0.0.1:8000"

def test_endpoint(name, method, endpoint, data=None):
    """Test a single API endpoint."""
    try:
        url = f"{API_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success", True):
                print(f"{GREEN}✓{NC} {name}")
                return True
            else:
                print(f"{RED}✗{NC} {name}: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"{RED}✗{NC} {name}: HTTP {response.status_code}")
            return False
    
    except requests.exceptions.ConnectionError:
        print(f"{RED}✗{NC} {name}: Backend not running")
        return False
    except Exception as e:
        print(f"{RED}✗{NC} {name}: {str(e)}")
        return False

def main():
    print(f"{YELLOW}═══════════════════════════════════════════════════════════════{NC}")
        print(f"{YELLOW}# --- Integration Test Start ---{NC}")
    print(f"{YELLOW}   iLuminara GCP Prototype - Integration Tests{NC}")
    print(f"{YELLOW}═══════════════════════════════════════════════════════════════{NC}\n")
    
    tests_passed = 0
    tests_total = 0
    
    # Test Health Endpoints
    print(f"{YELLOW}Testing Health Endpoints...{NC}")
    tests_total += 1
    if test_endpoint("Health Check", "GET", "/health"):
        tests_passed += 1
    
    tests_total += 1
    if test_endpoint("Root Endpoint", "GET", "/"):
        tests_passed += 1
    
    print()
    
    # Test Voice Processing
    print(f"{YELLOW}Testing Voice Processing...{NC}")
    tests_total += 1
    if test_endpoint("Voice Simulate", "POST", "/voice/simulate"):
        tests_passed += 1
    
    print()
    
    # Test HSTPU Forecasting
    print(f"{YELLOW}Testing HSTPU Forecasting...{NC}")
    tests_total += 1
    if test_endpoint("HSTPU Map", "GET", "/hstpu/map"):
        tests_passed += 1
    
    tests_total += 1
    if test_endpoint("HSTPU Hotspots", "GET", "/hstpu/hotspots?threshold=2.0"):
        tests_passed += 1
    
    tests_total += 1
    forecast_data = {
        "lat": -1.2921,
        "lon": 36.8219,
        "region": "Nairobi"
    }
    if test_endpoint("HSTPU Forecast", "POST", "/hstpu/forecast", forecast_data):
        tests_passed += 1
    
    print()
    
    # Test Ethical Engine
    print(f"{YELLOW}Testing Ethical Engine...{NC}")
    tests_total += 1
    if test_endpoint("Ethics Statistics", "GET", "/ethics/stats"):
        tests_passed += 1
    
    tests_total += 1
    if test_endpoint("Ethics Log", "GET", "/ethics/log?limit=10"):
        tests_passed += 1
    
    tests_total += 1
    eval_data = {
        "action_type": "outbreak_alert",
        "payload": {
            "risk_level": "high",
            "explanation": "Test action"
        }
    }
    if test_endpoint("Ethics Evaluate", "POST", "/ethics/evaluate", eval_data):
        tests_passed += 1
    
    print()
    
    # Summary
    print(f"{YELLOW}═══════════════════════════════════════════════════════════════{NC}")
        print(f"{YELLOW}# --- Test Summary ---{NC}")
    print(f"{YELLOW}   Test Summary{NC}")
    print(f"{YELLOW}═══════════════════════════════════════════════════════════════{NC}")
    
    pass_rate = (tests_passed / tests_total * 100) if tests_total > 0 else 0
    
    if tests_passed == tests_total:
        print(f"{GREEN}All tests passed! ({tests_passed}/{tests_total}){NC}")
        return 0
    else:
        print(f"{RED}Some tests failed: {tests_passed}/{tests_total} passed ({pass_rate:.1f}%){NC}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
