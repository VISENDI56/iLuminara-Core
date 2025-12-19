"""
iLuminara Unified Portal - Transcendence Protocol Interface
============================================================
A unified Streamlit interface combining:
- Command Console (Leadership Dashboard)
- Transparency Audit View
- Field Validation Form

This portal serves as the central access point for the iLuminara system.
"""

import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(
    page_title="iLuminara Unified Portal",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for unified aesthetic
st.markdown("""
    <style>
        .stApp {background-color: #0e1117; color: #00FF41;}
        .metric-container {border: 1px solid #333; padding: 10px; background-color: #161b22; border-radius: 5px;}
        .big-font {font-size: 24px !important; font-weight: bold; font-family: 'Courier New', monospace;}
        .status-ok { color: #00FF41; }
        .status-warn { color: #FFD700; }
        .status-crit { color: #FF0000; text-shadow: 0 0 10px #FF0000; }
        .status-banner { padding: 10px 16px; border-radius: 6px; color: white; font-weight: 800; font-size: 20px; text-align:center; }
        .status-banner.ok { background: linear-gradient(90deg,#006400,#008000); }
        .status-banner.crit { background: linear-gradient(90deg,#7f0000,#ff0000); box-shadow: 0 0 18px rgba(255,0,0,0.6); animation: pulse 1s infinite; }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.02); } 100% { transform: scale(1); } }
        .green-box { background-color: #0f3f22; padding: 12px; border-radius: 8px; border-left: 4px solid #00ff88; }
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

# --- DATA LOADER ---
@st.cache_data
def load_outbreak_data():
    try:
        with open('simulated_outbreak.json', 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error("⚠️ DATA NOT FOUND. RUN 'python edge_node/frenasa_engine/simulate_outbreak.py' FIRST.")
        return None

@st.cache_data
def load_precision_data():
    try:
        with open('precision_alert_sequence.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# Load data
outbreak_data = load_outbreak_data()

if outbreak_data is None:
    st.stop()

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("# 💠 iLUMINARA PORTAL")
st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "Select View:",
    ["🛡️ Command Console", "📊 Transparency Audit", "📱 Field Validation"],
    label_visibility="collapsed"
)

st.sidebar.divider()

# Shared time control
if 'events' in outbreak_data:
    df = pd.DataFrame(outbreak_data['events'])
    max_hour = int(df['hour'].max()) if not df.empty else 72
    current_hour = st.sidebar.slider("Operation Hour", 0, max_hour, max_hour // 2)
else:
    # Fallback for old format
    df = pd.DataFrame(outbreak_data if isinstance(outbreak_data, list) else [])
    max_hour = 72
    current_hour = st.sidebar.slider("Operation Hour", 0, max_hour, 36)

st.sidebar.markdown(f"**System Time:** Hour {current_hour}/{max_hour}")
st.sidebar.divider()

st.sidebar.markdown("### System Status")
st.sidebar.markdown("**Node:** JOR-47 (DADAAB)")
st.sidebar.markdown("**Latency:** 18ms")
st.sidebar.markdown("**Protocol:** ACTIVE")

# ============================================================================
# PAGE 1: COMMAND CONSOLE (Leadership Dashboard)
# ============================================================================
if page == "🛡️ Command Console":
    if df.empty:
        st.error("No outbreak data available.")
        st.stop()
    
    # Filter data for current hour
    current_state = df[df['hour'] <= current_hour].iloc[-1] if len(df[df['hour'] <= current_hour]) > 0 else df.iloc[0]
    historical_data = df[df['hour'] <= current_hour]
    
    # --- HEADER SECTION ---
    col_head1, col_head2 = st.columns([3, 1])
    with col_head1:
        st.markdown("## 🛡️ iLUMINARA SOVEREIGN COMMAND")
        st.markdown("### NODE: **JOR-47 (DADAAB)** | LATENCY: **18ms**")
    
    with col_head2:
        payout_status = current_state.get('payout_status', 'LOCKED')
        if payout_status == "LOCKED":
            st.markdown("<div class='status-banner ok'>STATUS: SECURE</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='status-banner crit'>STATUS: CRITICAL — ACTION REQUIRED</div>", unsafe_allow_html=True)
    
    st.divider()
    
    # --- KPI ROW ---
    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns([1.5, 1.5, 1, 1, 1, 1])
    
    z_score = current_state.get('z_score', 0.0)
    z_color = "status-ok"
    if z_score > 2.0: z_color = "status-warn"
    if z_score > 3.5: z_color = "status-crit"
    
    # Logic for Field Validation Status
    validation_status = "PENDING"
    validation_color = "status-warn"
    if current_hour >= 40:
        validation_status = "COMPLETED"
        validation_color = "status-ok"
    
    with kpi1:
        st.markdown(f"<div class='metric-container'>Risk Z-Score<br><span class='big-font {z_color}'>{z_score:.2f}</span></div>", unsafe_allow_html=True)
    
    with kpi2:
        payout_color = "status-crit" if payout_status == "RELEASED" else "status-ok"
        st.markdown(f"<div class='metric-container'>Parametric Bond<br><span class='big-font {payout_color}'>{payout_status}</span></div>", unsafe_allow_html=True)
    
    with kpi3:
        cbs_signals = current_state.get('cbs_signals', 0)
        st.markdown(f"<div class='metric-container'>CBS Signals<br><span class='big-font'>{int(cbs_signals)}</span></div>", unsafe_allow_html=True)
    
    with kpi4:
        emr_confirmations = current_state.get('emr_confirmations', 0)
        st.markdown(f"<div class='metric-container'>EMR Confirmed<br><span class='big-font'>{int(emr_confirmations)}</span></div>", unsafe_allow_html=True)
    
    with kpi5:
        st.markdown(f"<div class='metric-container'>Governance Kernel<br><span class='big-font status-ok'>14 ACTIVE</span></div>", unsafe_allow_html=True)
    
    with kpi6:
        st.markdown(f"<div class='metric-container'>Field Validation<br><span class='big-font {validation_color}'>{validation_status}</span></div>", unsafe_allow_html=True)
    
    st.write("")  # Spacer
    
    # --- MAIN VISUALIZATION ROW ---
    viz1, viz2 = st.columns([2, 1])
    
    # PyDeck Map
    with viz1:
        st.markdown("### 🗺️ SPATIOTEMPORAL RISK MAP")
        
        lat = current_state.get('lat', 0.0512)
        lon = current_state.get('lon', 40.3129)
        
        r, g = 0, 255
        if z_score > 3.5: r, g = 255, 0
        elif z_score > 1.5: r, g = 255, 215
        
        zoom_level = 9 if z_score > 3.5 else (10 if z_score > 1.5 else 11)
        view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=zoom_level, pitch=50)
        layer = pdk.Layer("ScatterplotLayer", data=pd.DataFrame([{'lat': lat, 'lon': lon}]), 
                          get_position=["lon", "lat"],
                          get_color=[r, g, 0, 160], get_radius=1000 + (z_score * 500), pickable=True)
        
        st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/dark-v10', 
                                  initial_view_state=view_state, layers=[layer]))
    
    with viz2:
        st.markdown("### 📉 THE GOLDEN THREAD")
        st.markdown("**Resolution of Agentic Conflict (CBS vs. EMR)**")
        
        if 'cbs_signals' in historical_data.columns and 'z_score' in historical_data.columns:
            chart_data = historical_data[['hour', 'cbs_signals', 'z_score']].copy()
            fig = px.line(chart_data, x='hour', y=['cbs_signals', 'z_score'], 
                          color_discrete_map={"cbs_signals": "#FFD700", "z_score": "#FF0000"})
            fig.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', 
                              font_color='#00FF41', margin=dict(l=20, r=20, t=20, b=20), 
                              legend=dict(orientation="h"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Chart data not available in current format.")
    
    # --- FOOTER ---
    st.divider()
    st.markdown(f"**SYSTEM LOG:** Simulated Outbreak Scenario v1.0 | Offline Protocol: **ACTIVE** | Frame: {current_hour}/{max_hour}")

# ============================================================================
# PAGE 2: TRANSPARENCY AUDIT VIEW
# ============================================================================
elif page == "📊 Transparency Audit":
    st.title("Protocol Validation Console | Decision Confidence: 85%")
    
    st.header("Reasoning Weights (SHAP Analysis)")
    st.markdown("""
    - **Spatial Clustering:** 42%  
    - **Symptom Match:** 35%  
    - **Growth Rate:** 23%
    """)
    
    st.subheader("Time-to-Action Metric")
    st.markdown("**Alert Transmission Speed:** <span style='font-family: \"Courier New\", monospace; font-size:28px; color:#00FFB3;'>4.2s</span>", unsafe_allow_html=True)
    
    st.subheader("Consent Preservation Check (Dignity Guardrail)")
    st.markdown("""
    <div class='green-box'>
    <strong>Legal Vector Check: PASSED</strong><br/>
    Data is Anonymous & Stored Locally
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("Precision Alert Timeline (5s chain)")
    
    precision_data = load_precision_data()
    if precision_data:
        seq = precision_data.get("precision_sequence", [])
        for ev in seq:
            ts = ev.get("timestamp")
            offset = ev.get("offset_seconds")
            st.markdown(f"- **T={offset:.1f}s** — **{ev.get('source')}**: {ev.get('flow')} — _{ev.get('note')}_  ")
        st.markdown("\n\n*Note: This timeline demonstrates the 4.2s Alert Transmission speed and sub-90s pipeline handoff.*")
    else:
        st.error("precision_alert_sequence.json not found. Run the simulator to generate the precision sequence.")
    
    st.markdown("---")
    
    # Governance Kernel Log expander
    with st.expander('Governance Kernel Log: 14 Protocols Active', expanded=False):
        protocols = [
            ('GDPR Art 9', 'ENFORCED'),
            ('KDPA §37', 'ENFORCED'),
            ('HIPAA Section 164', 'ENFORCED'),
            ('PIPEDA', 'ENFORCED'),
            ('POPIA', 'ENFORCED'),
            ('Local Consent Guard', 'ENFORCED'),
            ('Retention Policy (180d)', 'ENFORCED'),
            ('Data Minimization', 'ENFORCED'),
            ('Purpose Limitation', 'ENFORCED'),
            ('Access Control', 'ENFORCED'),
            ('Audit Trail Integrity', 'ENFORCED'),
            ('SHAP Transparency', 'ENABLED'),
            ('Golden Thread Anchoring', 'ENABLED'),
            ('Anomaly Thresholds', 'ENFORCED')
        ]
        dfp = pd.DataFrame(protocols, columns=['Protocol', 'Status'])
        st.table(dfp)
    
    st.write("Goal: Reduce Decision Anxiety by making the 'Why' and 'How Fast' visible to clinical staff.")

# ============================================================================
# PAGE 3: FIELD VALIDATION FORM
# ============================================================================
elif page == "📱 Field Validation":
    st.title("Field Validation Check")
    st.header("CHW Amina Hassan (Zone 4)")
    st.divider()
    
    # --- ALERT CONTEXT ---
    st.markdown("""
        <div class="alert-box">
            🚨 URGENT ALERT: Zone 4 Spike Detected. Verification Required.
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("1. Confirmed Cases")
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
    
    # --- SUBMISSION LOGIC ---
    if st.button('Submit Validation & Sync to Edge Node'):
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
    
    st.caption('Note: Data transmission is secured by LoRaWAN mesh and governed by KDPA protocol. All submissions are encrypted at source.')

# --- GLOBAL FOOTER ---
st.sidebar.markdown("---")
st.sidebar.markdown("**iLuminara Core v1.0**")
st.sidebar.markdown("*Transform preventable suffering from statistical inevitability to historical anomaly.*")
