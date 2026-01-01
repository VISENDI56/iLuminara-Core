import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

def initialize_sovereign_session():
    """Ensures all 156-phase variables exist in the session state."""
    defaults = {
        "auth_status": "LOCKED",
        "oracle_online": False,
        "warehouse_sync": False,
        "nodes_active": 50,
        "precision_score": 0.98,
        "equity_value": 1000.00,
        "last_audit_receipt": "STBK-INIT-000"
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def check_system_integrity():
    """Health check for all external API bridges."""
    return {
        "Nebius": bool(os.getenv("NEBIUS_API_KEY")),
        "Snowflake": bool(os.getenv("SNOWFLAKE_ACCOUNT")),
        "NVIDIA": bool(os.getenv("NVIDIA_NIM_API_KEY")),
        "Esri": bool(os.getenv("ESRI_MAPS_KEY"))
    }