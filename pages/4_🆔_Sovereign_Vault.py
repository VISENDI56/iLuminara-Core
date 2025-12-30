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
from core.privacy_zkp.eligibility_circuit import ZKPCircom

st.set_page_config(page_title="Sovereign Vault", layout="centered")
st.title("🆔 My Sovereign Identity")

col1, col2 = st.columns(2)

with col1:
    st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=iLuminara-ZKP-Identity", caption="ZKP Credential")

with col2:
    st.metric("Bio-Credit Balance", "450 Credits", delta="+50 (Sanitation)")
    st.metric("Health Status", "Verified", delta="Vaccinated")

st.divider()

st.subheader("Proof of Eligibility")
criteria = st.selectbox("Select Criteria to Prove", ["Age > 60", "Resident: Kalobeyei", "Vaccinated: Cholera"])

if st.button("Generate Zero-Knowledge Proof"):
    zkp = ZKPCircom()
    proof = zkp.prove_eligibility("PRIVATE_KEY")
    st.success("Proof Generated Successfully!")
    st.json({"Proof": proof, "Data_Revealed": "NONE"})