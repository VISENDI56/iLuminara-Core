#!/bin/bash

# ══════════════════════════════════════════════════════════════════════════
# iLuminara Local Demo Launcher
# ══════════════════════════════════════════════════════════════════════════
# Starts the backend API and frontend dashboard for local testing

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   iLuminara Local Demo${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv .venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo -e "${GREEN}✓ Environment ready${NC}"
echo ""

# Check if backend is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠ Backend already running on port 8000${NC}"
else
    # Start backend in background
    echo -e "${BLUE}Starting backend API on http://localhost:8000${NC}"
    uvicorn app.backend.main:app --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    
    # Wait for backend to be ready
    echo -e "${YELLOW}Waiting for backend to initialize...${NC}"
    sleep 3
fi

# Check if frontend is already running
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠ Frontend already running on port 8501${NC}"
else
    # Start frontend
    echo -e "${BLUE}Starting frontend dashboard on http://localhost:8501${NC}"
    sleep 2
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   iLuminara is running!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Access Points:${NC}"
echo "  📊 Dashboard: ${BLUE}http://localhost:8501${NC}"
echo "  🔌 API:       ${BLUE}http://localhost:8000${NC}"
echo "  📚 API Docs:  ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}Mode:${NC} Local Demo (Mock GCP Services)"
echo ""
echo -e "${YELLOW}To launch the dashboard, run:${NC}"
echo "  streamlit run app/frontend/main.py"
echo ""
echo "Press Ctrl+C to stop services"

# Start Streamlit (this will run in foreground)
streamlit run app/frontend/main.py
