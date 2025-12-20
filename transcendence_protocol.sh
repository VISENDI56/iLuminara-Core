#!/bin/bash

set -e  # Exit on error

echo "💠 INITIATING iLUMINARA TRANSCENDENCE PROTOCOL..."

# 1. Kill zombies
echo "   > Cleaning up existing processes..."
pkill -f streamlit || true  # Don't fail if no processes found

# 2. Regenerate the Quantum Entangled Data
echo "   > Running Active Inference Simulation..."
if ! python3 edge_node/frenasa_engine/simulate_outbreak.py; then
    echo "❌ ERROR: Simulation failed"
    exit 1
fi

echo "   > Simulation complete"

# 3. Launch the Unified Portal
echo "   > Opening The Portal..."
if [ ! -f portal.py ]; then
    echo "❌ ERROR: portal.py not found"
    exit 1
fi

streamlit run portal.py --server.port 8501 --server.address 0.0.0.0
