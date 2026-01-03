# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# COMPETITOR EXCLUSION: Commercial use by entities offering Sovereign/Health OS 
# solutions is STRICTLY PROHIBITED without a commercial license.
# 
# The Sovereign Immune System (Omni-Law) and JEPA-MPC Architecture are 
# proprietary inventions of iLuminara.
# ------------------------------------------------------------------------------

import streamlit as st
from datetime import datetime
import time

def get_circadian_mode():
    hour = datetime.now().hour
    if 5 <= hour < 9:
        return "dawn"    # Warm awakening (orange/teal)
    elif 9 <= hour < 17:
        return "day"  # Clear sovereignty (teal/white)
    elif 17 <= hour < 21:
        return "dusk" # Serene transition (deep teal/purple)
    else:
        return "night"               # Void protection (dark/black)

def apply_circadian_theme():
    mode = get_circadian_mode()
    
    themes = {
        "dawn": {
            "primaryColor": "#FF6B35",     # Warm sunrise
            "backgroundColor": "#FFF4E5",
            "secondaryBackgroundColor": "#FFE4C4",
            "textColor": "#3E2723"
        },
        "day": {
            "primaryColor": "#0D9488",     # iLuminara teal sovereignty
            "backgroundColor": "#FFFFFF",
            "secondaryBackgroundColor": "#E0F2F1",
            "textColor": "#00695C"
        },
        "dusk": {
            "primaryColor": "#4A148C",     # Deep serenity
            "backgroundColor": "#EDE7F6",
            "secondaryBackgroundColor": "#D1C4E9",
            "textColor": "#311B92"
        },
        "night": {
            "primaryColor": "#0D9488",
            "backgroundColor": "#121212",
            "secondaryBackgroundColor": "#1E1E1E",
            "textColor": "#B2DFDB"
        }
    }
    
    theme = themes[mode]
    st.set_page_config(page_title=f"iLuminara - {mode.capitalize()} Mode", layout="wide")
    
    # Custom CSS for sovereignty
    st.markdown(f"""
        <style>
            .stApp {{ background-color: {theme["backgroundColor"]}; color: {theme["textColor"]}; }}
            .css-1d391kg {{ background-color: {theme["secondaryBackgroundColor"]}; }}
            h1, h2, h3 {{ color: {theme["primaryColor"]}; }}
            .stButton>button {{ background-color: {theme["primaryColor"]}; }}
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.info(f"🌅 Circadian Mode: **{mode.capitalize()}** — Compassionate precision aligned with natural rhythm.")
