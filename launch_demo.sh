#!/bin/bash
# Launch iLuminara Interactive Demo Dashboard

echo "🏛️ Launching iLuminara Sovereign Health Interface Demo..."
echo "=============================================="
echo ""
echo "Starting Streamlit dashboard..."
echo "Access URL will be displayed below"
echo ""

# Run Streamlit
cd "$(dirname "$0")"
streamlit run demo_dashboard.py --server.port 8501 --server.address 0.0.0.0
