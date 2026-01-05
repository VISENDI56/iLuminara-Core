import streamlit as st

PAGES = {
    "Bio Foundry": "1_🧬_Bio_Foundry.py",
    "Technical Specs": "2_Technical_Specs.py",
}


def render_navigation():
    st.sidebar.markdown("### Navigation")
    choice = st.sidebar.radio(
        "Go to",
        list(PAGES.keys()),
        label_visibility="collapsed",
    )
    return PAGES[choice]
