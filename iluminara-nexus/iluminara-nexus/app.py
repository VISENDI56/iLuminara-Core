import streamlit as st
import time
import pandas as pd
from modules.state_manager import StateManager
from modules.governance import GovernanceKernel
from modules.security import SecurityGate
from modules.logger import log_audit
from modules.validator import validate_input
from modules.persistence import InstitutionalDatabase

st.set_page_config(page_title="iLuminara-Core | v1.0 Pilot", layout="wide")

try:
    SecurityGate.verify_role("OPERATOR")
    sm = StateManager()
    gov = GovernanceKernel()
    db = InstitutionalDatabase() # Phase 3.2 Persistence

    st.sidebar.title("🛡️ Institutional Status")
    st.sidebar.info(f"Mode: {sm.state['system_mode']}")
    
    # Persistent Record Count
    records = db.get_recent_signals(limit=100)
    st.sidebar.metric("Sovereign Records", len(records))

    if sm.state['system_mode'] == "BOOT":
        st.title("System Initialization")
        if st.button("Boot System"):
            log_audit("SYS_BOOT", "Initialization started")
            sm.update_mode("READY")
            st.rerun()

    elif sm.state['system_mode'] == "READY":
        st.title("🛡️ Operational Readiness")
        if st.button("Activate Predictive Framework"):
            sm.update_mode("ACTIVE")
            st.rerun()

    elif sm.state['system_mode'] == "ACTIVE":
        st.title("🚀 Active Command Center")
        
        tab1, tab2 = st.tabs(["📥 Ingestion", "📋 Local Ledger"])

        with tab1:
            with st.form("signal_form"):
                col1, col2 = st.columns(2)
                with col1:
                    loc = st.selectbox("Location", ["Ifo", "Dagahaley", "Hagadera", "Kalobeyei"])
                    symptom = st.text_input("Symptom Code", "CHOLERA-01")
                with col2:
                    severity = st.slider("Severity Score", 1, 5, 3)
                    reporter = st.text_input("Reporter ID", "KRCS-FIELD-01")
                
                if st.form_submit_button("Ingest Signal"):
                    raw_data = {"source_id": reporter, "location": loc, "symptom_code": symptom, "severity_score": severity}
                    is_valid, result = validate_input(raw_data)
                    
                    if is_valid:
                        # Commit to Database (Phase 3.2)
                        db.save_signal(result)
                        log_audit("DATA_INGEST_PERSISTENT", "Signal saved to SQLite", result.dict())
                        st.success("Signal Persisted to Sovereign Ledger.")
                    else:
                        st.error("Validation Failed.")

        with tab2:
            st.subheader("Sovereign Audit Ledger (Phase 3.2)")
            recent_data = db.get_recent_signals(10)
            if recent_data:
                df = pd.DataFrame(recent_data, columns=["ID", "Source", "Location", "Symptom", "Severity", "Timestamp", "Sync Status"])
                st.table(df)
            else:
                st.write("No local records found.")

        if st.button("Emergency Standby"):
            sm.update_mode("READY")
            st.rerun()

except Exception as e:
    log_audit("CRITICAL_ERROR", str(e))
    st.error(f"System Intercept: {e}")
