import streamlit as st
import time

st.set_page_config(page_title="iLuminara Bridge", page_icon="🌉")
st.markdown("<style>.stApp { background-color: #000000; color: #FFFFFF; }</style>", unsafe_allow_html=True)

st.title("🌉 The Viral Bridge")
st.markdown("### Anonymous Public Reporting Node")
st.info("Your identity is cryptographically shredded. Only the data remains.")

# SYMPTOM CHECKER
st.markdown("---")
st.subheader("How are you feeling?")

symptoms = st.multiselect(
    "Select all that apply:",
    ["High Fever", "Unexplained Bleeding", "Red Eyes", "Severe Headache", "Vomiting"]
)

location = st.selectbox("Nearest Town", ["Nairobi", "Kisumu", "Mombasa", "Eldoret", "Remote Village"])

if st.button("BROADCAST ANONYMOUS SIGNAL"):
    with st.status("Encrypting Signal...", expanded=True) as status:
        time.sleep(1)
        st.write("Shredding Metadata (IP-02)...")
        time.sleep(1)
        st.write("Injecting into Golden Thread...")
        status.update(label="Signal Received. Stay Calm.", state="complete")
    if "Bleeding" in str(symptoms):
        st.error("🚨 **URGENT:** An autonomous drone has been dispatched to your sector.")
    else:
        st.success("Data added to predictive model. Thank you.")
