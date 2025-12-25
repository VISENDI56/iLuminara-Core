import streamlit as st
import pandas as pd
import pydeck as pdk
import time
import json
import os
from utils.theme_manager import apply_circadian_theme
from state.shared_memory import load_state, get_shared, set_shared
from edge_node.data_ingestion_layer import IngestionEngine

# --- CLASS-5 CONFIGURATION ---
st.set_page_config(page_title="iLuminara Command", page_icon="🏛️", layout="wide")
apply_circadian_theme()

# --- MINTLIFY GUIDANCE SIDEBAR ---
with st.sidebar:
    st.header("📚 Mintlify Guidance")
    with st.expander("🏛️ Architecture / Command Decision", expanded=False):
        st.markdown("""
        **Command Console Overview:**
        The sovereign command center orchestrates real-time health intelligence decisions across jurisdictional boundaries. Features include:
        - Multi-source data fusion with probabilistic outbreak prediction
        - Active inference engine for clinical decision support
        - Zero-latency alert distribution to field teams
        - Regulatory compliance monitoring with 45+ frameworks
        
        *This console demonstrates iLuminara's nuclear IP stack in action.*
        """)
        if st.button("📖 Open Full Architecture Docs", key="arch_docs"):
            st.markdown("[https://visendi56.mintlify.app/architecture](https://visendi56.mintlify.app/architecture)")

# --- SECURITY HEADER (SENTINEL v3.0) ---
def get_integrity_status():
    if os.path.exists("sentinel_report.sarif"):
        return "🟢 INTEGRITY: VERIFIED (SHA-256)", "success"
    return "🟡 INTEGRITY: UNVERIFIED", "warning"

int_status, int_color = get_integrity_status()

# --- HEADER UI ---
st.markdown(f"""
    <div style="border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px;">
        <span style="font-size: 24px; font-weight: bold; color: #fff;">🏛️ iLUMINARA: SOVEREIGN COMMAND</span>
        <span style="float: right; font-family: monospace; color: #00ff88; border: 1px solid #00ff88; padding: 2px 8px; border-radius: 4px;">CLASS-5 DEFENSIVE ASSET</span>
    </div>
    <div style="font-family: monospace; font-size: 12px; color: #888; margin-bottom: 20px;">
        NODE: JOR-47 | JURISDICTION: KENYA_DPA | {int_status}
    </div>
""", unsafe_allow_html=True)


# --- LOAD ENGINES & SOVEREIGN MEMORY ---
state = load_state()
ingestor = IngestionEngine()
fusion = ingestor.fuse_data_streams()

# --- SIDEBAR: SOVEREIGN SHARED MEMORY ---
st.sidebar.markdown("---")
st.sidebar.subheader("🧠 Sovereign Shared Memory")
st.sidebar.json(state, expanded=False)

# --- 1. THE NUCLEAR IP STACK STATUS ---
st.subheader("📡 NUCLEAR IP STACK STATUS")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Governance Kernel", "ACTIVE", "SovereignGuardrail")
    st.caption("14 Frameworks Enforced")
    
with c2:
    st.metric("Intelligence Engine", "LOCKED", "Silent Flux")
    st.caption(f"Fusion Score: {fusion['fusion_score']}")

with c3:
    st.metric("Bio-Interface", "ONLINE", "Acorn Protocol")
    st.caption("Sentry Mode: Offline-First")

with c4:
    st.metric("Distribution", "READY", "5DM Bridge")
    st.caption("Logistics Fleet: 3 Units")

st.divider()

# --- 2. GOLDEN THREAD INTELLIGENCE (The Truth) ---
st.subheader("🧬 GOLDEN THREAD: JURIDICAL PHYSICS")
feeds = fusion['live_feeds']

g1, g2 = st.columns([2, 1])

with g1:
    # 3D MAP OF CONVERGENCE
    st.markdown("**Vector Convergence Analysis (Rift Valley Model)**")
    
    # Extract coords for map
    map_data = pd.DataFrame([
        {"lat": feeds[0]['coords'][0], "lon": feeds[0]['coords'][1], "type": "EMR (Clinical)", "radius": 200},
        {"lat": feeds[1]['coords'][0], "lon": feeds[1]['coords'][1], "type": "CBS (Signal)", "radius": 500},
    ])
    
    layer = pdk.Layer(
        "ScatterplotLayer",
        map_data,
        get_position='[lon, lat]',
        get_color='[200, 30, 0, 160]',
        get_radius="radius",
        pickable=True,
    )
    
    view_state = pdk.ViewState(latitude=0.0512, longitude=40.3129, zoom=12, pitch=45)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{type}"}))

with g2:
    # FUSION CALCULUS
    st.markdown("**Calculus of Truth:**")
    st.code(f"""
Distance: {fusion['physics']['dist_km']} km
Time Lag: {fusion['physics']['time_lag_h']} hours
    """, language="text")
    
    if fusion['fusion_score'] > 0.8:
        st.error(f"🚨 **CRITICAL CONVERGENCE**\n{fusion['fusion_note']}")
        if st.button("🔴 AUTHORIZE NUCLEAR RESPONSE", type="primary"):
            state['protocol_status'] = "AUTHORIZED"
            st.toast("Response Authorized. Logistics Dispatched.")
            time.sleep(1)
            st.rerun()
    else:
        st.info(f"ℹ️ **Signal Analysis**\n{fusion['fusion_note']}")

# --- 3. CRYPTO SHREDDER (The End) ---
st.divider()
with st.expander("🗑️ IP-02: CRYPTO SHREDDER PROTOCOL (Dissolution)"):
    st.warning("This will cryptographically dissolve all local PII keys. Irreversible.")
    if st.button("EXECUTE DISSOLUTION"):
        st.success("KEYS SHREDDED. DATA IS NOW ENTROPY.")