import streamlit as st
from core.state.sovereign_bus import bus


def offline_banner():
    status = bus.get("status")
    if status in ("OFFLINE", "DEGRADED"):
        st.warning("📴 Offline mode active — local intelligence only.")
