#!/bin/bash
# Test All iLuminara Services
# ═════════════════════════════════════════════════════════════════════════════

set -e

echo "═════════════════════════════════════════════════════════════════════════════"
echo "iLuminara Multi-Service Test Suite"
echo "═════════════════════════════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TOTAL=0
PASSED=0
FAILED=0

test_endpoint() {
    local name=$1
    local url=$2
    local expected_status=${3:-200}
    
    TOTAL=$((TOTAL + 1))
    echo -n "Testing ${name}... "
    
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
    
    if [ "$status" -eq "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $status)"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (HTTP $status, expected $expected_status)"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

echo "Testing Health Endpoints"
echo "-------------------------------------"
test_endpoint "Main API (8080)" "http://localhost:8080/health"
test_endpoint "HTTPS API (8443)" "http://localhost:8443/health"
test_endpoint "Metrics (9090)" "http://localhost:9090/health"
test_endpoint "Governance (5000)" "http://localhost:5000/health"
test_endpoint "Data Fusion (5001)" "http://localhost:5001/health"
echo ""

echo "Testing Functional Endpoints"
echo "-------------------------------------"

# Test Metrics endpoint
test_endpoint "Metrics export" "http://localhost:9090/metrics"

# Test Governance frameworks
test_endpoint "Governance frameworks" "http://localhost:5000/frameworks"

# Test Data Fusion records
test_endpoint "Data Fusion records" "http://localhost:5001/records"

echo ""

# Test Main API voice processing with sample data
echo "Testing Voice Processing..."
TEMP_AUDIO=$(mktemp /tmp/test-audio-XXXXXX.wav)
python3 -c "
import wave, struct, random
w = wave.open('$TEMP_AUDIO', 'wb')
w.setnchannels(1)
w.setsampwidth(2)
w.setframerate(16000)
frames = [struct.pack('h', int(random.gauss(0, 3000))) for _ in range(16000)]
w.writeframes(b''.join(frames))
w.close()
" 2>/dev/null

if curl -s -X POST http://localhost:8080/process-voice \
    -H "Content-Type: audio/wav" \
    --data-binary @"$TEMP_AUDIO" \
    -o /dev/null -w "%{http_code}" | grep -q "200"; then
    echo -e "${GREEN}✓ PASS${NC} Voice Processing"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}✗ FAIL${NC} Voice Processing"
    FAILED=$((FAILED + 1))
fi
TOTAL=$((TOTAL + 1))

rm -f "$TEMP_AUDIO"

# Test Outbreak Prediction
echo "Testing Outbreak Prediction..."
if curl -s -X POST http://localhost:8080/predict \
    -H "Content-Type: application/json" \
    -d '{"location":{"lat":0.4221,"lng":40.2255},"symptoms":["diarrhea","vomiting"]}' \
    -o /dev/null -w "%{http_code}" | grep -q "200"; then
    echo -e "${GREEN}✓ PASS${NC} Outbreak Prediction"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}✗ FAIL${NC} Outbreak Prediction"
    FAILED=$((FAILED + 1))
fi
TOTAL=$((TOTAL + 1))

echo ""
echo "═════════════════════════════════════════════════════════════════════════════"
echo "Test Results"
echo "═════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Total Tests: $TOTAL"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    echo ""
    echo "All 5 services are running correctly:"
    echo "  ✓ Port 8080: Main API"
    echo "  ✓ Port 8443: HTTPS API"
    echo "  ✓ Port 9090: Metrics"
    echo "  ✓ Port 5000: Governance"
    echo "  ✓ Port 5001: Data Fusion"
    echo ""
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    echo ""
    echo "Please check that all services are running:"
    echo "  python start_all_services.py"
    echo ""
    exit 1
fi
