"""
iLuminara Unified Sovereign Health Platform
Multi-page Streamlit application with all core functionalities
Deployed on Streamlit Community Cloud for global access
"""
import streamlit as st

# Page configurations
st.set_page_config(
    page_title="iLuminara Sovereign Health",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MINTLIFY GUIDANCE SIDEBAR ---
with st.sidebar:
    st.header("📚 Mintlify Guidance")
    st.markdown("**Unified Platform Overview:**")
    st.markdown("""
    iLuminara-Core provides sovereign health intelligence through:
    - **Quickstart:** War Room launch for immediate demonstration
    - **Architecture:** Command orchestration and decision support
    - **Governance Kernel:** Regulatory compliance and security
    - **AI Agents:** Field validation and human-in-the-loop
    - **Security:** Class-5 defensive protocols
    - **Deployment:** Global accessibility via Streamlit Cloud
    - **API:** RESTful integrations for external systems
    """)
    if st.button("📖 Open Full Documentation", key="full_docs"):
        st.markdown("[https://visendi56.mintlify.app/](https://visendi56.mintlify.app/)")

# Navigation
pages = {
    "🏛️ Command Console": "command_console",
    "🔍 Transparency Audit": "transparency_audit",
    "📱 Field Validation": "field_validation"
}

selected_page = st.sidebar.radio("Navigate to:", list(pages.keys()))

# Page routing
if selected_page == "🏛️ Command Console":
    st.title("🏛️ iLuminara Command Console")
    st.markdown("**Architecture Overview:** Real-time decision orchestration and health intelligence command center.")
    # Import and run dashboard logic here, or embed simplified version
    st.info("Full Command Console functionality available at individual app deployment.")

elif selected_page == "🔍 Transparency Audit":
    st.title("🔍 Transparency Audit Console")
    st.markdown("**Governance Kernel Overview:** Complete audit trails and regulatory compliance monitoring.")
    # Import and run transparency_view logic
    st.info("Full Transparency Audit functionality available at individual app deployment.")

elif selected_page == "📱 Field Validation":
    st.title("📱 Field Validation Form")
    st.markdown("**AI Agents Overview:** Human-in-the-loop validation for clinical accuracy in field conditions.")
    # Import and run field_validation_form logic
    st.info("Full Field Validation functionality available at individual app deployment.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("🩺 **iLuminara-Core v2.1**")
st.sidebar.markdown("*Sovereign Health Intelligence Platform*")