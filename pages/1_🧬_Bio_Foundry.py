import streamlit as st
from ml_health.bionemo_genomics.evo2_engine import Evo2FoundationEngine

st.set_page_config(page_title="Bio-Foundry | iLuminara", layout="wide")

st.title("🧬 Bio-Foundry: Evo2 Core")
st.caption("Substrate: NVIDIA B300 | Status: Structural Integrity Verified")

# Initialize Engine
engine = Evo2FoundationEngine()

target = st.text_input("Pathogen Target Sequence", "GATTACA...")
if st.button("Initialize Generative Synthesis"):
    with st.spinner("Synthesizing via System-2 Reasoning..."):
        result = engine.generate_binder(target, "SOVEREIGN_CONSTRAINTS")
        st.success("Binder Synthesized.")
        st.json(result)