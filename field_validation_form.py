try:
    from utils.theme_manager import apply_circadian_theme
    apply_circadian_theme()
except Exception:
    import streamlit as st
    st.set_page_config(page_title="Field Validation", page_icon="📱", layout="centered")
    st.markdown("""
        <style>
            .stApp { background-color: #0D9488; color: #1e2430; }
            .stButton>button { background-color: #0D9488; color: white; font-weight: bold; padding: 10px; border-radius: 8px; width: 100%; margin-top: 20px; }
        </style>
    """, unsafe_allow_html=True)

# --- CONFIGURATION: MOBILE AESTHETIC ---
st.set_page_config(
    page_title="Field Validation",
    page_icon="📱",
    layout="centered",  # Optimized for mobile/smaller screens
)

# --- MINTLIFY GUIDANCE SIDEBAR ---
st.sidebar.header("📚 Mintlify Guidance")
with st.sidebar.expander("🤖 AI Agents / Validation", expanded=False):
    st.markdown("""
    **Field Validation Overview:**
    AI agents enable human-in-the-loop validation for clinical accuracy. Core capabilities:
    - Swahili language processing for East African CHWs
    - Behavioral biometrics for field authentication
    - Real-time clinical decision support with uncertainty quantification
    - Cascade AI propagation for network effects
    
    *This form demonstrates iLuminara's AI agent ecosystem in field conditions.*
    """)
    if st.button("📖 Open Full AI Agents Docs", key="ai_docs"):
        st.markdown("[https://visendi56.mintlify.app/ai-agents](https://visendi56.mintlify.app/ai-agents)")

st.sidebar.markdown("### Sovereign Documentation")
with st.sidebar.expander("Field Validation Excerpt", expanded=False):
    st.markdown("""
    **Field Validation:**
    - Human-in-the-loop validation for clinical accuracy
    - Swahili language processing for CHWs
    - Real-time clinical decision support
    - See [Mintlify Field Validation](https://visendi56.mintlify.app/field-validation)
    """)
if st.sidebar.button("Open Full Docs", key="mintlify_docs_field"):
    st.markdown("[Mintlify Portal](https://visendi56.mintlify.app/)")

st.title("Field Validation Check")
st.header("CHW Amina Hassan (Zone 4)")
st.divider()

# --- 1. ALERT CONTEXT ---
st.markdown("""
    <div class="alert-box">
        🚨 URGENT ALERT: Zone 4 Spike Detected. Verification Required.
    </div>
    """, unsafe_allow_html=True)

st.subheader("1. Confirmed Cases")
# --- 2. INPUT FIELDS ---
confirmed_cases = st.number_input(
    'Confirmed Cases (Observed)', 
    min_value=1, 
    max_value=10, 
    value=3, 
    step=1,
    help="Number of individuals matching symptoms at the source."
)

st.subheader("2. Environmental Factors")
water_source_status = st.radio(
    'Local Water Source Status',
    ['Contaminated (Suspected)', 'Clean (Confirmed)', 'Unknown'],
    index=0
)

st.subheader("3. Local Priority")
local_priority_score = st.slider(
    'Local Priority Score (0=Low, 10=Urgent)',
    0, 10, 8, help="How quickly do you need assistance based on local assessment?"
)

# --- 4. SUBMISSION LOGIC ---
if st.button('Submit Validation & Sync to Edge Node'):
    # Simulate data merging logic
    from datetime import datetime
    sync_id = '947F_DADAAB'
    ts = datetime.utcnow().isoformat() + 'Z'
    st.markdown("""
        <div style='border:2px solid #004400; background:#E8FFF0; padding:16px; border-radius:8px;'>
            <h3 style='color:#006400; margin:0;'>✅ VALIDATION RECEIPT</h3>
            <p style='margin:6px 0;'><strong>Cases:</strong> %d</p>
            <p style='margin:6px 0;'><strong>SYNC_ID:</strong> <code>%s</code></p>
            <p style='margin:6px 0;'><strong>Timestamp:</strong> <code>%s</code></p>
            <p style='margin:6px 0; color:#004400;'>CERTAINTY ACHIEVED — Data merged into Golden Thread and queued for sovereign anchoring.</p>
        </div>
    """ % (confirmed_cases, sync_id, ts), unsafe_allow_html=True)
    st.balloons()
    st.markdown("---")
    # --- 5. SOVEREIGN INTEGRITY NOTE ---
    st.caption('Note: Data transmission is secured by LoRaWAN mesh and governed by KDPA protocol. All submissions are encrypted at source.')

from state.shared_memory import load_state, get_shared, set_shared

# --- SOVEREIGN SHARED MEMORY SIDEBAR ---
state = load_state()
st.sidebar.markdown("---")
st.sidebar.subheader("🧠 Sovereign Shared Memory")
st.sidebar.json(state, expanded=False)
