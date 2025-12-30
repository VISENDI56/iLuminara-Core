#!/usr/bin/env python3
"""
iLuminara Interactive Demo Dashboard
=====================================
Streamlit-based interactive demonstration of the iLuminara Sovereign Health Interface.

This dashboard showcases:
1. Regulatory Compliance Simulator (RCO)
2. Authentication Demo (STA)
3. Signal Fusion Interface (ECF)
4. 49-Law Audit Dashboard
5. Network Propagation Visualizer (VSAI)
"""

import streamlit as st
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure page
st.set_page_config(
    page_title="iLuminara Sovereign Health Interface",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for branding
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0D9488 0%, #14B8A6 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .metric-card {
        background: #f0fdfa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #0D9488;
        margin: 1rem 0;
    }
    .status-operational {
        color: #059669;
        font-weight: bold;
    }
    .status-warning {
        color: #d97706;
        font-weight: bold;
    }
    .status-critical {
        color: #dc2626;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🏛️ iLuminara Sovereign Health Interface</h1>
    <p>Self-Governing Compliance System | Quantum-Inspired Intelligence | Offline-First Architecture</p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Demo Module:",
    [
        "🏠 Overview",
        "⚖️ Compliance Simulator",
        "🔐 Authentication Demo",
        "🔮 Signal Fusion",
        "📊 49-Law Audit",
        "🌐 Network Propagation",
        "ℹ️ About This Demo"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### System Status")
st.sidebar.markdown("🟢 **RCO**: Operational")
st.sidebar.markdown("🟢 **Guardrail**: Active")
st.sidebar.markdown("🟢 **Quantum Nexus**: Synchronized")
st.sidebar.markdown("🟢 **Law Registry**: 7 Frameworks Live")

# Route to appropriate page
if page == "🏠 Overview":
    from pages import overview
    overview.render()
elif page == "⚖️ Compliance Simulator":
    from pages import compliance_simulator
    compliance_simulator.render()
elif page == "🔐 Authentication Demo":
    from pages import authentication_demo
    authentication_demo.render()
elif page == "🔮 Signal Fusion":
    from pages import signal_fusion
    signal_fusion.render()
elif page == "📊 49-Law Audit":
    from pages import law_audit
    law_audit.render()
elif page == "🌐 Network Propagation":
    from pages import network_propagation
    network_propagation.render()
elif page == "ℹ️ About This Demo":
    from pages import about
    about.render()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 2rem 0;">
    <p><strong>iLuminara-Core v3.0</strong> | The Fortress is Sealed | The Converged Architecture is Complete</p>
    <p>🛡️ 7 Legal Frameworks Active | ✅ 100% Compliance Health | 🔒 Zero Security Alerts</p>
</div>
""", unsafe_allow_html=True)
