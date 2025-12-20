#!/bin/bash
# ═════════════════════════════════════════════════════════════════════════════
# iLuminara Complete System Launch Script
# ═════════════════════════════════════════════════════════════════════════════
# This script launches ALL iLuminara services, apps, platforms, and dashboards:
# - Streamlit Dashboards (3 apps on ports 8501-8503)
# - Docker Compose Services (Core API, Prometheus, Grafana, Nginx)
# - Port Forwarding Tools
# ═════════════════════════════════════════════════════════════════════════════

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "════════════════════════════════════════════════════════════════"
echo -e "${BLUE}🛡️  iLUMINARA COMPLETE SYSTEM LAUNCHER${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Create logs directory if it doesn't exist
mkdir -p logs

# ═══════════════════════════════════════════════════════════════════
# STEP 1: Check and Install Dependencies
# ═══════════════════════════════════════════════════════════════════
echo -e "${YELLOW}[1/7] Checking Python Dependencies...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Check if required packages are installed
python3 -c "import streamlit" 2>/dev/null || {
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    pip install -q streamlit pandas pydeck numpy plotly 2>&1 | tee logs/pip_install.log
}
echo -e "${GREEN}✅ Python dependencies ready${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEP 2: Generate Outbreak Simulation Data
# ═══════════════════════════════════════════════════════════════════
echo -e "${YELLOW}[2/7] Generating Outbreak Simulation Data...${NC}"
if [ ! -f "simulated_outbreak.json" ] || [ ! -s "simulated_outbreak.json" ]; then
    echo "Generating fresh outbreak data..."
    python3 edge_node/frenasa_engine/simulate_outbreak.py > logs/outbreak_generation.log 2>&1
    echo -e "${GREEN}✅ Outbreak data generated (simulated_outbreak.json)${NC}"
else
    echo -e "${GREEN}✅ Outbreak data already exists${NC}"
fi
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEP 3: Start Port Forwarder (if needed)
# ═══════════════════════════════════════════════════════════════════
echo -e "${YELLOW}[3/7] Starting Port Forwarder...${NC}"
if [ -f "tools/port_forwarder.py" ]; then
    if ! pgrep -f "port_forwarder.py" > /dev/null; then
        nohup python3 tools/port_forwarder.py > logs/port_forwarder.log 2>&1 &
        sleep 1
        echo -e "${GREEN}✅ Port forwarder started${NC}"
    else
        echo -e "${GREEN}✅ Port forwarder already running${NC}"
    fi
else
    echo -e "${BLUE}ℹ️  Port forwarder not found (optional)${NC}"
fi
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEP 4: Launch Streamlit Dashboards (3 Apps)
# ═══════════════════════════════════════════════════════════════════
echo -e "${YELLOW}[4/7] Launching Streamlit Dashboards...${NC}"

# Dashboard 1: Command Console (Port 8501)
if ! pgrep -f "streamlit run dashboard.py" > /dev/null; then
    echo "Starting Command Console (Port 8501)..."
    nohup streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0 --server.headless true > logs/dashboard.log 2>&1 &
    sleep 2
    echo -e "${GREEN}✅ Command Console: http://0.0.0.0:8501${NC}"
else
    echo -e "${GREEN}✅ Command Console already running on port 8501${NC}"
fi

# Dashboard 2: Transparency Audit View (Port 8502)
if ! pgrep -f "streamlit run transparency_view.py" > /dev/null; then
    echo "Starting Transparency Audit (Port 8502)..."
    nohup streamlit run transparency_view.py --server.port 8502 --server.address 0.0.0.0 --server.headless true > logs/transparency.log 2>&1 &
    sleep 2
    echo -e "${GREEN}✅ Transparency Audit: http://0.0.0.0:8502${NC}"
else
    echo -e "${GREEN}✅ Transparency Audit already running on port 8502${NC}"
fi

# Dashboard 3: Field Validation Form (Port 8503)
if ! pgrep -f "streamlit run field_validation_form.py" > /dev/null; then
    echo "Starting Field Validation (Port 8503)..."
    nohup streamlit run field_validation_form.py --server.port 8503 --server.address 0.0.0.0 --server.headless true > logs/field_validation.log 2>&1 &
    sleep 2
    echo -e "${GREEN}✅ Field Validation: http://0.0.0.0:8503${NC}"
else
    echo -e "${GREEN}✅ Field Validation already running on port 8503${NC}"
fi
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEP 5: Start Docker Compose Services (Optional)
# ═══════════════════════════════════════════════════════════════════
echo -e "${YELLOW}[5/7] Starting Docker Compose Services...${NC}"
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    # Check if Dockerfile exists
    if [ -f "Dockerfile.arm64" ] || [ -f "Dockerfile" ]; then
        echo "Docker detected. Starting services..."
        docker-compose up -d > logs/docker_compose.log 2>&1 || {
            echo -e "${YELLOW}⚠️  Docker services failed to start (may require build)${NC}"
            echo -e "${BLUE}ℹ️  Run 'docker-compose build' first if needed${NC}"
        }
        
        # Wait for services to initialize
        sleep 5
        
        # Check if services are running
        if docker-compose ps | grep -q "Up"; then
            echo -e "${GREEN}✅ Docker services started:${NC}"
            echo -e "   - Core API: http://0.0.0.0:8080"
            echo -e "   - Core HTTPS: https://0.0.0.0:8443"
            echo -e "   - Prometheus: http://0.0.0.0:9091"
            echo -e "   - Grafana: http://0.0.0.0:3000"
            echo -e "   - Nginx: http://0.0.0.0:80"
        else
            echo -e "${YELLOW}⚠️  Docker services may not be fully running${NC}"
        fi
    else
        echo -e "${BLUE}ℹ️  Dockerfile not found. Skipping Docker services.${NC}"
    fi
else
    echo -e "${BLUE}ℹ️  Docker not installed. Skipping Docker services.${NC}"
fi
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEP 6: Verify All Services
# ═══════════════════════════════════════════════════════════════════
echo -e "${YELLOW}[6/7] Verifying All Services...${NC}"
sleep 3

# Function to check if a port is listening
check_port() {
    local port=$1
    local service=$2
    if lsof -i :$port -t >/dev/null 2>&1 || netstat -tuln 2>/dev/null | grep -q ":$port "; then
        echo -e "${GREEN}✅ $service (Port $port)${NC}"
        return 0
    else
        echo -e "${RED}❌ $service (Port $port)${NC}"
        return 1
    fi
}

echo "Checking active services:"
check_port 8501 "Command Console"
check_port 8502 "Transparency Audit"
check_port 8503 "Field Validation"

# Check Docker services (optional)
if command -v docker &> /dev/null; then
    if docker-compose ps 2>/dev/null | grep -q "Up"; then
        check_port 8080 "Core API" || echo -e "${BLUE}ℹ️  Core API (Port 8080) - Docker may be starting${NC}"
        check_port 3000 "Grafana" || echo -e "${BLUE}ℹ️  Grafana (Port 3000) - Docker may be starting${NC}"
        check_port 9091 "Prometheus" || echo -e "${BLUE}ℹ️  Prometheus (Port 9091) - Docker may be starting${NC}"
    fi
fi
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEP 7: Display Summary
# ═══════════════════════════════════════════════════════════════════
echo "════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ LAUNCH COMPLETE${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo -e "${BLUE}📊 STREAMLIT DASHBOARDS:${NC}"
echo "   1. Command Console:      http://0.0.0.0:8501"
echo "   2. Transparency Audit:   http://0.0.0.0:8502"
echo "   3. Field Validation:     http://0.0.0.0:8503"
echo ""

if command -v docker &> /dev/null && docker-compose ps 2>/dev/null | grep -q "Up"; then
    echo -e "${BLUE}🐳 DOCKER SERVICES:${NC}"
    echo "   - Core API:             http://0.0.0.0:8080"
    echo "   - Core HTTPS:           https://0.0.0.0:8443"
    echo "   - Governance Service:   http://0.0.0.0:5000"
    echo "   - Data Fusion Service:  http://0.0.0.0:5001"
    echo "   - Prometheus:           http://0.0.0.0:9091"
    echo "   - Grafana:              http://0.0.0.0:3000 (admin/iluminara)"
    echo "   - Nginx:                http://0.0.0.0:80"
    echo ""
fi

echo -e "${BLUE}💡 USAGE:${NC}"
echo "   - View logs: tail -f logs/*.log"
echo "   - Stop all services: ./stop_all_services.sh"
echo "   - Check status: ./check_services_status.sh"
echo ""
echo -e "${BLUE}📁 LOG FILES:${NC}"
echo "   - Dashboard:        logs/dashboard.log"
echo "   - Transparency:     logs/transparency.log"
echo "   - Field Validation: logs/field_validation.log"
echo "   - Docker Services:  logs/docker_compose.log"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo -e "${GREEN}Quote: 'Transform preventable suffering from statistical${NC}"
echo -e "${GREEN}        inevitability to historical anomaly.'${NC}"
echo "════════════════════════════════════════════════════════════════"
