import streamlit as st
from core.state.sovereign_bus import bus

APP_NAME = "iLuminara"
TAGLINE = "Sovereign Intelligence for Human Systems"


def apply_layout():
    st.set_page_config(
        page_title=APP_NAME,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        f"""
        <style>
        .app-title {{
            font-size: 2rem;
            font-weight: 700;
        }}
        .app-tagline {{
            color: #666;
            margin-bottom: 1rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f"<div class='app-title'>{APP_NAME}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='app-tagline'>{TAGLINE}</div>", unsafe_allow_html=True)


def sidebar_status():
    state = bus.snapshot()
    st.sidebar.markdown("### System Status")

    status = state.get("status", "UNKNOWN")
    mode = state.get("mode", "UNKNOWN")

    if status in ("BOOT", "INITIALIZING"):
        st.sidebar.info(f"🟡 {status}")
    elif status == "ACTIVE":
        st.sidebar.success(f"🟢 {status}")
    elif status == "DEGRADED":
        st.sidebar.warning(f"🔴 {status}")
    else:
        st.sidebar.error("⚠️ UNKNOWN STATE")

    st.sidebar.caption(f"Mode: {mode}")
