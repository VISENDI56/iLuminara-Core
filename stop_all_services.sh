#!/bin/bash
# ═════════════════════════════════════════════════════════════════════════════
# iLuminara Complete System Shutdown Script
# ═════════════════════════════════════════════════════════════════════════════
# This script stops ALL iLuminara services safely
# ═════════════════════════════════════════════════════════════════════════════

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "════════════════════════════════════════════════════════════════"
echo -e "${YELLOW}🛡️  iLUMINARA SYSTEM SHUTDOWN${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Stop Streamlit applications
echo -e "${YELLOW}Stopping Streamlit Dashboards...${NC}"
pkill -f "streamlit run dashboard.py" && echo -e "${GREEN}✅ Command Console stopped${NC}" || echo -e "${BLUE}ℹ️  Command Console not running${NC}"
pkill -f "streamlit run transparency_view.py" && echo -e "${GREEN}✅ Transparency Audit stopped${NC}" || echo -e "${BLUE}ℹ️  Transparency Audit not running${NC}"
pkill -f "streamlit run field_validation_form.py" && echo -e "${GREEN}✅ Field Validation stopped${NC}" || echo -e "${BLUE}ℹ️  Field Validation not running${NC}"
echo ""

# Stop port forwarder
echo -e "${YELLOW}Stopping Port Forwarder...${NC}"
pkill -f "port_forwarder.py" && echo -e "${GREEN}✅ Port forwarder stopped${NC}" || echo -e "${BLUE}ℹ️  Port forwarder not running${NC}"
echo ""

# Stop Docker Compose services
echo -e "${YELLOW}Stopping Docker Services...${NC}"
if command -v docker-compose &> /dev/null; then
    if [ -f "docker-compose.yml" ]; then
        docker-compose down > /dev/null 2>&1 && echo -e "${GREEN}✅ Docker services stopped${NC}" || echo -e "${BLUE}ℹ️  Docker services not running${NC}"
    else
        echo -e "${BLUE}ℹ️  docker-compose.yml not found${NC}"
    fi
else
    echo -e "${BLUE}ℹ️  Docker Compose not installed${NC}"
fi
echo ""

echo "════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ ALL SERVICES STOPPED${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo -e "${BLUE}To restart services, run:${NC}"
echo "   ./launch_all_services.sh"
echo ""
