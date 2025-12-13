import streamlit as st

# --- CONFIGURATION: MOBILE AESTHETIC ---
st.set_page_config(
    page_title="Field Validation",
    page_icon="📱",
    layout="centered",  # Optimized for mobile/smaller screens
)

# Custom CSS for high-contrast mobile look
st.markdown("""
    <style>
        .stApp {
            background-color: #f0f2f6; /* Light background for field use */
            color: #1e2430;
        }
        .stButton>button {
            background-color: #008000; /* Green for GO */
            color: white;
            font-weight: bold;
            padding: 10px;
            border-radius: 8px;
            width: 100%;
            margin-top: 20px;
        }
        .alert-box {
            border: 2px solid #FF0000;
            background-color: #ffe0e0;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-weight: bold;
            color: #FF0000;
        }
    </style>
    """, unsafe_allow_html=True)

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
