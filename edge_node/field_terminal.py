import streamlit as st
import time

st.set_page_config(page_title="Field Unit 7", page_icon="💊")

st.title("💊 Field Unit Terminal")
st.caption("ID: VISENDI-NODE-Alpha | Status: OFFLINE-CAPABLE")

# BIOMETRIC AUTH SIMULATOR
st.markdown("### 🔐 Identity Verification (Somatic Auth)")
col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://img.icons8.com/ios/100/0D9488/fingerprint.png", width=100)

with col2:
    pin = st.text_input("Enter Node PIN", type="password")
    if st.button("INITIATE SOMATIC HANDSHAKE"):
        if pin == "1234": # Mock PIN
            with st.spinner("Analyzing micro-tremors..."):
                time.sleep(2)
            st.success("IDENTITY CONFIRMED: Dr. Amani")
            st.session_state['auth'] = True
        else:
            st.error("BIOMETRIC MISMATCH. Access Denied.")

if st.session_state.get('auth'):
    st.markdown("---")
    st.subheader("📝 Patient Intake (Viral Bridge)")
    with st.form("patient_data"):
        name = st.text_input("Patient Hash / Name")
        symptoms = st.multiselect("Symptoms", ["Fever", "Cough", "Hemorrhage", "Fatigue"])
        submitted = st.form_submit_button("SYNC TO MESH")
        if submitted:
            st.warning("☁️ Cloud Unreachable. Switching to **Sovereign Bridge**...")
            time.sleep(1)
            st.info("💾 Data encrypted with Kyber-1024.")
            time.sleep(1)
            st.success("✅ Saved to Local Ledger. Will sync when peer detected.")
