import streamlit as st
from core.state.sovereign_bus import bus


def loading_guard():
    status = bus.get("status")

    if status in ("BOOT", "INITIALIZING"):
        with st.spinner("System initializing…"):
            st.info(
                "iLuminara is preparing sovereign intelligence systems. "
                "This ensures compliance, integrity, and safety."
            )
        st.stop()


def explain(text: str):
    st.caption(f"ℹ️ {text}")


def tooltip(label: str, help_text: str):
    st.markdown(f"**{label}**")
    st.caption(help_text)
