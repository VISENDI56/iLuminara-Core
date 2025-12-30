import streamlit as st
import random
from infrastructure.logistics.cuopt_agent import AgenticDispatcher

st.set_page_config(page_title="Logistics Command", layout="wide")
st.title("🚁 Autonomous Logistics Command")

col1, col2 = st.columns([3, 1])

with col1:
    # Placeholder for ESRI Map Component
    st.markdown("""
    <div style="background-color:#262730; padding:20px; border-radius:10px; height:400px; text-align:center;">
        <h3 style="color:white; padding-top:150px;">🗺️ GeoGhost Live Map (Simulated)</h3>
        <p>Rendering .vtpk Vector Tiles...</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("Fleet Status")
    st.metric("Active Drones", "12/15")
    st.metric("Battery Avg", "84%")

    st.divider()

    st.subheader("Agentic Dispatch")
    cmd = st.text_input("Voice Command", placeholder="e.g., 'Reroute Fleet Alpha to Sector 4'")
    if cmd:
        agent = AgenticDispatcher()
        response = agent.parse_command(cmd)
        st.success(f"Action: {response['route_update']}")
        st.info(f"Solver: {response['solver_backend']}")