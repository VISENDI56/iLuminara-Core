#!/bin/bash
# ═════════════════════════════════════════════════════════════════════════════
# iLuminara System Status Checker
# ═════════════════════════════════════════════════════════════════════════════
# This script checks the status of all iLuminara services
# ═════════════════════════════════════════════════════════════════════════════

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "════════════════════════════════════════════════════════════════"
echo -e "${BLUE}🛡️  iLUMINARA SYSTEM STATUS CHECK${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Function to check if a process is running
check_process() {
    local pattern=$1
    local name=$2
    if pgrep -f "$pattern" > /dev/null; then
        local pid=$(pgrep -f "$pattern" | head -1)
        echo -e "${GREEN}✅ $name (PID: $pid)${NC}"
        return 0
    else
        echo -e "${RED}❌ $name${NC}"
        return 1
    fi
}

# Function to check if a port is listening
check_port() {
    local port=$1
    local service=$2
    if lsof -i :$port -t >/dev/null 2>&1 || netstat -tuln 2>/dev/null | grep -q ":$port "; then
        echo -e "${GREEN}✅ $service listening on port $port${NC}"
        return 0
    else
        echo -e "${RED}❌ $service not listening on port $port${NC}"
        return 1
    fi
}

# Check Streamlit processes
echo -e "${YELLOW}STREAMLIT DASHBOARDS:${NC}"
check_process "streamlit run dashboard.py" "Command Console"
check_process "streamlit run transparency_view.py" "Transparency Audit"
check_process "streamlit run field_validation_form.py" "Field Validation"
echo ""

# Check ports
echo -e "${YELLOW}PORT STATUS:${NC}"
check_port 8501 "Command Console"
check_port 8502 "Transparency Audit"
check_port 8503 "Field Validation"
echo ""

# Check Docker services
echo -e "${YELLOW}DOCKER SERVICES:${NC}"
if command -v docker-compose &> /dev/null; then
    if [ -f "docker-compose.yml" ]; then
        if docker-compose ps 2>/dev/null | grep -q "Up"; then
            docker-compose ps 2>/dev/null | grep "Up" | while read line; do
                echo -e "${GREEN}✅ $line${NC}"
            done
            echo ""
            echo -e "${YELLOW}DOCKER PORTS:${NC}"
            check_port 8080 "Core API"
            check_port 8443 "Core HTTPS"
            check_port 5000 "Governance Service"
            check_port 5001 "Data Fusion Service"
            check_port 9091 "Prometheus"
            check_port 3000 "Grafana"
            check_port 80 "Nginx HTTP"
        else
            echo -e "${RED}❌ No Docker services running${NC}"
        fi
    else
        echo -e "${BLUE}ℹ️  docker-compose.yml not found${NC}"
    fi
else
    echo -e "${BLUE}ℹ️  Docker Compose not installed${NC}"
fi
echo ""

# Check port forwarder
echo -e "${YELLOW}SUPPORT SERVICES:${NC}"
check_process "port_forwarder.py" "Port Forwarder"
echo ""

# Check data files
echo -e "${YELLOW}DATA FILES:${NC}"
if [ -f "simulated_outbreak.json" ] && [ -s "simulated_outbreak.json" ]; then
    size=$(du -h simulated_outbreak.json | cut -f1)
    echo -e "${GREEN}✅ simulated_outbreak.json ($size)${NC}"
else
    echo -e "${RED}❌ simulated_outbreak.json missing or empty${NC}"
fi

if [ -f "precision_alert_sequence.json" ] && [ -s "precision_alert_sequence.json" ]; then
    size=$(du -h precision_alert_sequence.json | cut -f1)
    echo -e "${GREEN}✅ precision_alert_sequence.json ($size)${NC}"
else
    echo -e "${YELLOW}⚠️  precision_alert_sequence.json missing or empty${NC}"
fi
echo ""

# System resources
echo -e "${YELLOW}SYSTEM RESOURCES:${NC}"
echo -e "CPU Load: $(uptime | awk -F'load average:' '{print $2}')"
echo -e "Memory: $(free -h | awk '/^Mem:/ {printf "%s / %s (%.1f%%)", $3, $2, ($3/$2)*100}')"
echo -e "Disk: $(df -h . | awk 'NR==2 {printf "%s / %s (%s)", $3, $2, $5}')"
echo ""

echo "════════════════════════════════════════════════════════════════"
echo -e "${BLUE}Status check complete${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo -e "${BLUE}Commands:${NC}"
echo "   - Start services:  ./launch_all_services.sh"
echo "   - Stop services:   ./stop_all_services.sh"
echo "   - View logs:       tail -f logs/*.log"
echo ""
