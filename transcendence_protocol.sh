#!/bin/bash

echo "💠 INITIATING iLUMINARA TRANSCENDENCE PROTOCOL..."

# 1. Kill zombies
pkill -f streamlit

# 2. Regenerate the Quantum Entangled Data
echo "   > Running Active Inference Simulation..."
python3 edge_node/frenasa_engine/simulate_outbreak.py

# 3. Launch the Unified Portal
echo "   > Opening The Portal..."
# Note: Ensure portal.py is created from the previous turn
streamlit run portal.py --server.port 8501 --server.address 0.0.0.0
