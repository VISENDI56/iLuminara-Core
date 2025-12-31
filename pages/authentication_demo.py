import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Auth Demo | iLuminara", layout="wide")

st.title("🛡️ Authentication Demo: Polymorphic Bio-Lock")
st.caption("Visualizing the 18ms Triple-Helix Key Mutation")

# Generate Simulated Key Rotation Graph
t = np.linspace(0, 10, 100)
y = np.sin(t) * np.random.normal(1, 0.1, 100)

fig = go.Figure(data=go.Scatter(x=t, y=y, mode='lines+markers', line=dict(color='#00FFA3')))
fig.update_layout(title="PBLS Lattice Signature Variance", template="plotly_dark")

st.plotly_chart(fig, use_container_width=True)
st.success("Polymorphic Key: Active and Mutating.")
