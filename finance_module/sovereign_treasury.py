import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sovereign Fund", page_icon="🪙")
st.markdown("<style>.stApp { background-color: #1a1a1a; color: #FFD700; }</style>", unsafe_allow_html=True)

st.title("🪙 Sovereign Treasury")
st.markdown("### Decentralized Health Finance (DeHi)")

# TREASURY BALANCES
c1, c2, c3 = st.columns(3)
c1.metric("Global Liquidity", "$45,200,000", "+12%")
c2.metric("Emergency Reserve", "2,000 BTC", "Immutable")
c3.metric("Deployment Cost", "$0.04 / node", "Optimized")

st.markdown("---")
st.subheader("💸 Smart Contract Streams")

data = {
    "Project": ["Vaccine Procurement", "Edge Node Hardware", "R&D: FRENASA v2", "Community Bounties"],
    "Allocation": [40, 30, 20, 10],
    "Status": ["LOCKED", "DISBURSING", "VOTING", "OPEN"]
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

if st.button("MINT GOVERNANCE TOKENS"):
    st.balloons()
    st.success("1,000,000 $LUMI minted to contributing health workers.")
