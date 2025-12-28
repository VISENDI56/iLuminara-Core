#!/bin/bash
echo "Starting the iLuminara-Core 20-Module Singularity..."

# Core Commands (Port 8501-8519)
streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0 &
streamlit run pages/frenasa_engine.py --server.port 8502 --server.address 0.0.0.0 &
streamlit run pages/network_map.py --server.port 8503 --server.address 0.0.0.0 &
streamlit run pages/guardrail_ui.py --server.port 8504 --server.address 0.0.0.0 &
streamlit run pages/ledger_explorer.py --server.port 8505 --server.address 0.0.0.0 &
streamlit run pages/risk_core.py --server.port 8506 --server.address 0.0.0.0 &
streamlit run pages/ml_health_ops.py --server.port 8507 --server.address 0.0.0.0 &
streamlit run pages/ai_robustness.py --server.port 8508 --server.address 0.0.0.0 &
streamlit run pages/audit_evidence.py --server.port 8509 --server.address 0.0.0.0 &
streamlit run pages/dhis2_adapter.py --server.port 8510 --server.address 0.0.0.0 &
streamlit run pages/sc_trace.py --server.port 8511 --server.address 0.0.0.0 &
streamlit run pages/epidemiology.py --server.port 8512 --server.address 0.0.0.0 &
streamlit run pages/clinical_voice.py --server.port 8513 --server.address 0.0.0.0 &
streamlit run pages/genomic_sim.py --server.port 8514 --server.address 0.0.0.0 &
streamlit run pages/sensor_mesh.py --server.port 8515 --server.address 0.0.0.0 &
streamlit run pages/zipline_nexus.py --server.port 8516 --server.address 0.0.0.0 &
streamlit run pages/regional_regs.py --server.port 8517 --server.address 0.0.0.0 &
streamlit run pages/agent_logs.py --server.port 8518 --server.address 0.0.0.0 &
streamlit run pages/global_sync.py --server.port 8519 --server.address 0.0.0.0 &
./launch_robustness.sh &
./launch_audit_evidence.sh &

# API & MLOps
uvicorn api.server:app --host 0.0.0.0 --port 8000 &
echo "✅ All 20 Modules Dispatched."