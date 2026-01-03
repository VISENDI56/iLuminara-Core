#!/bin/bash
# Quick fix for iLuminara dashboard
pkill -f streamlit 2>/dev/null
cd /workspace 2>/dev/null || cd ~ 2>/dev/null
export PYTHONPATH="$(pwd):$PYTHONPATH"
streamlit run dashboards/sovereign_control.py --server.port=8501
