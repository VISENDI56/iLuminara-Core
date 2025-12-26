import streamlit as st
import random

st.set_page_config(page_title="Hammurabi-Zero", page_icon="⚖️")
st.title("⚖️ Hammurabi-Zero")
st.markdown("### Reinforcement Learning Governance Agent")
st.info("Training an AI to write laws that maximize Human Survival + Liberty.")

# THE REWARD FUNCTION
st.subheader("Objective Function")
st.latex(r'''
R_t = \alpha \cdot \text{SurvivalRate} - \beta \cdot \text{CivilUnrest} - \gamma \cdot \text{EconomicCost}
''')

st.markdown("---")
st.write("### Current Policy Proposal")

if st.button("ASK AGENT FOR POLICY"):
    # Simulated Inference
    policies = [
        "Protocol 7: Close borders but keep markets open (Reward: 0.85)",
        "Protocol 9: Total Shutdown + UBI Distribution (Reward: 0.92)",
        "Protocol 2: Do Nothing (Reward: -1.5)"
    ]
    choice = random.choice(policies)
    with st.chat_message("assistant"):
        st.write(f"Based on current entropy, I have drafted **{choice}**.")
        st.write("Reasoning: This path minimizes riot probability by 40% compared to Protocol 7.")
        st.button("Ratify into Smart Contract")
