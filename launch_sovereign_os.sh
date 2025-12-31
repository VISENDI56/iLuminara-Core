#!/bin/bash
echo "🚀 STARTING ILUMINARA-CORE SOVEREIGN STACK..."

# Launch Main Dashboard (Home)
nohup streamlit run Home.py --server.port 8501 --server.address 0.0.0.0 --server.headless true > home.log 2>&1 &
echo "[+] Home Dashboard Live on Port 8501"

# Launch Bio-Foundry (IP #03)
nohup streamlit run pages/1_🧬_Bio_Foundry.py --server.port 8502 --server.address 0.0.0.0 --server.headless true > bio.log 2>&1 &
echo "[+] Bio-Foundry Live on Port 8502"

# Launch Auth Demo (IP #06)
nohup streamlit run pages/authentication_demo.py --server.port 8503 --server.address 0.0.0.0 --server.headless true > auth.log 2>&1 &
echo "[+] Auth Demo Live on Port 8503"

echo "===================================================="
echo "   ✅ ALL SYSTEMS OPERATIONAL"
echo "   Check logs (home.log, bio.log, auth.log) for details."
echo "===================================================="