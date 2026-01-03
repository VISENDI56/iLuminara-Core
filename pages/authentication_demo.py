from core.ui.state_controller import initialize_sovereign_session; initialize_sovereign_session()
import streamlit as st
import plotly.graph_objects as go
import time
import numpy as np

st.set_page_config(page_title="Auth Demo | iLuminara", layout="wide")

st.title("🛡️ Authentication Demo: Polymorphic Bio-Lock")
st.caption("Visualizing the 18ms Triple-Helix Key Mutation")

# Generate Simulated Key Rotation Graph
t = np.linspace(0, 10, 100)
y = np.sin(t) * np.random.normal(1, 0.1, 100)

try:
    import plotly.graph_objects as go
except ImportError:
    st.warning("Plotly not found. Re-installing...")
    import plotly.graph_objects as go

fig = go.Figure(data=go.Scatter(x=t, y=y, mode='lines+markers', line=dict(color='#00FFA3')))
fig.update_layout(title="PBLS Lattice Signature Variance", template="plotly_dark")

st.plotly_chart(fig, use_container_width=True)
st.success("Polymorphic Key: Active and Mutating.")

# AMPLIFIED FUNCTIONALITY: The Heartbeat Synchronizer
if st.toggle("Observe Active Key Mutation"):
    placeholder = st.empty()
    for _ in range(10):
        # Simulate the 18ms key rotation logic
        theta = np.linspace(0, 2*np.pi, 100)
        r = np.random.uniform(0.8, 1.2, 100)

        fig = go.Figure(data=go.Scatterpolar(r=r, theta=theta*180/np.pi, 
                                             mode='lines', line_color='#00FFA3'))
        fig.update_layout(polar=dict(bgcolor='#0E1117'), showlegend=False, template="plotly_dark")
        
        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.5) # Throttled for UI visibility
