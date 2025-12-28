import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Serenity Flow", page_icon="🧘")
st.markdown("<style>.stApp { background-color: #0F172A; color: #E2E8F0; }</style>", unsafe_allow_html=True)

st.title("🧘 Serenity Flow")
st.markdown("### Neuro-Linguistic Panic Dampener")

# PANIC METRICS
col1, col2 = st.columns(2)
col1.metric("Community Anxiety Score", "84/100", "CRITICAL", delta_color="inverse")
col2.metric("Misinformation Velocity", "High", "Rumors Spreading")

st.markdown("---")
st.subheader("📉 Narrative Control Interventions")

# INTERACTIVE GUIDANCE
scenario = st.selectbox("Select Active Crisis Narrative",
    ["'The government is hiding the cure'", "'It spreads through 5G'", "'Water supply is poisoned'"])

st.write(f"**Recommended Counter-Script for:** {scenario}")
st.code(f"""
1. Acknowledge fear (Validate).
2. Present 'Video Proof' from local leader (Trust Anchor).
3. deploy_bot_swarm(target='{scenario}', sentiment='calm')
""", language="python")

if st.button("DEPLOY CALMING AGENTS"):
    st.toast("🕊️ 5,000 AI Agents deployed to Twitter/WhatsApp with calming narratives.")
    st.metric("Projected Anxiety Score", "42/100", "-50% (stabilized)")
