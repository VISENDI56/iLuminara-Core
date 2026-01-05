import streamlit as st
import json
import time
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="Blackwell B300 Live", layout="wide")
st.title("⚡ Live Blackwell B300 Simulation - Nairobi-Nexus")
st.markdown("**Real-Time Telemetry | Rev-217-OMEGA | January 05, 2026**")

# Auto-refresh
placeholder = st.empty()
refresh = st.sidebar.selectbox("Refresh Rate", [5, 10, 30], index=0)

while True:
    try:
        with open("telemetry/latest.json") as f:
            data = json.load(f)
    except:
        data = {"system_status": "INITIALIZING"}
    
    with placeholder.container():
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Trust Index", f"{data.get('sovereign_trust_index', 0)}%", "Stable")
        col2.metric("Battery", f"{data.get('battery_reserve_percent', 0)}%", f"{data.get('solar_input_w', 0)}W solar")
        col3.metric("GPU Temp", f"{data.get('gpu_temperature_c', 0)}°C")
        col4.metric("Inference Load", f"{data.get('inference_utilization_percent', 0)}%")
        
        # Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=data.get('battery_reserve_percent', 50),
            title={'text': "Battery Reserve"},
            gauge={'axis': {'range': [None, 100]},
                   'steps': [{'range': [0, 30], 'color': "red"},
                             {'range': [30, 70], 'color': "yellow"},
                             {'range': [70, 100], 'color': "green"}]}
        ))
        st.plotly_chart(fig, use_container_width=True)
        
        st.json(data, expanded=False)
        st.success(f"🟢 {data.get('system_status', 'NOMINAL')} - Blackwell B300 Operational")
    
    time.sleep(refresh)
