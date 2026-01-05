import streamlit as st
from core.state.sovereign_bus import bus

def sidebar_status():
    st.sidebar.success(f"Global Status: {bus.get('status')}")
