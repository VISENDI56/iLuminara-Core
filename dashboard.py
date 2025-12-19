import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import plotly.express as px

# --- CONFIGURATION: THE SOVEREIGN AESTHETIC ---
st.set_page_config(
    page_title="iLuminara Sovereign Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for industrial look
st.markdown("""
    <style>
        .stApp {background-color: #0e1117; color: #00FF41;}
        .metric-container {border: 1px solid #333; padding: 10px; background-color: #161b22; border-radius: 5px;}
        .big-font {font-size: 24px !important; font-weight: bold; font-family: 'Courier New', monospace;}
        .status-ok { color: #00FF41; }
        .status-warn { color: #FFD700; }
        .status-crit { color: #FF0000; text-shadow: 0 0 10px #FF0000; }
        /* Banner styling for immediate visual triage */
        .status-banner { padding: 10px 16px; border-radius: 6px; color: white; font-weight: 800; font-size: 20px; text-align:center; }
        .status-banner.ok { background: linear-gradient(90deg,#006400,#008000); }
        .status-banner.crit { background: linear-gradient(90deg,#7f0000,#ff0000); box-shadow: 0 0 18px rgba(255,0,0,0.6); animation: pulse 1s infinite; }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.02); } 100% { transform: scale(1); } }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADER ---
@st.cache_data
def load_data():
    try:
        with open('simulated_outbreak.json', 'r') as f:
            data = json.load(f)
        # Load z_score_timeline for hourly aggregated metrics
        df_timeline = pd.DataFrame(data['z_score_timeline'])
        
        # Add derived fields for compatibility
        df_timeline['cbs_signals'] = df_timeline['cases']  # CBS signals correlate with cases
        df_timeline['emr_confirmations'] = (df_timeline['cases'] * 0.3).astype(int)  # ~30% EMR confirmed
        df_timeline['payout_status'] = df_timeline['z_score'].apply(lambda z: "RELEASED" if z > 4.2 else "LOCKED")
        df_timeline['lat'] = 0.0512  # Dadaab coordinates
        df_timeline['lon'] = 40.3129
        
        return df_timeline
    except FileNotFoundError:
        st.error("⚠️ DATA NOT FOUND. RUN 'python edge_node/frenasa_engine/simulate_outbreak.py' FIRST.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# --- SIDEBAR CONTROL ---
st.sidebar.header("🕹️ TIME TRAVEL CONTROL")
current_hour = st.sidebar.slider("Operation Hour", 0, 72, 36)

# Filter data for current hour
current_state = df[df['hour'] == current_hour].iloc[0] if len(df[df['hour'] == current_hour]) > 0 else df.iloc[0]
historical_data = df[df['hour'] <= current_hour]

# Get z_score for threshold checks
z_score = current_state['z_score']

# --- ⛓️ PARAMETRIC ORACLE (SIDEBAR UPGRADE) ---
st.sidebar.markdown("---")
st.sidebar.header("⛓️ PARAMETRIC ORACLE")

# Smart Contract Simulation
contract_address = "0x7a23...F9"
oracle_status = "LISTENING"
gas_fee = "0.00 Gwei (Private Chain)"

if z_score > 4.2:
    oracle_status = "EXECUTING PAYOUT"
    tx_hash = f"0x{int(z_score*1000)}...9928"
    st.sidebar.success(f"💸 PAYOUT RELEASED")
    st.sidebar.code(f"TX: {tx_hash}\nVAL: $500,000.00 USDC\nBLK: 1928374", language="text")
else:
    st.sidebar.info(f"🛡️ CONTRACT SECURE")
    st.sidebar.markdown(f"""
    **Addr:** `{contract_address}`  
    **Oracle:** `{oracle_status}`  
    **Threshold:** `Z > 4.2`
    """)

# --- HEADER SECTION ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("## 🛡️ iLUMINARA SOVEREIGN COMMAND")
    st.markdown("### NODE: **JOR-47 (DADAAB)** | LATENCY: **18ms**")

with col_head2:
    # Prominent banner: surface immediate triage
    if current_state['payout_status'] == "LOCKED":
        st.markdown("<div class='status-banner ok'>STATUS: SECURE</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='status-banner crit'>STATUS: CRITICAL — ACTION REQUIRED</div>", unsafe_allow_html=True)

st.divider()

# --- 🚨 BOND TRIGGER EVENT ALARM ---
if z_score > 4.2:
    st.markdown("""
    <div style="padding: 20px; background-color: #3d0000; border: 2px solid #ff0000; text-align: center; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: #ff0000; margin:0;">🚨 BOND TRIGGER EVENT 🚨</h1>
        <p style="color: #ffffff; margin:0;">STATISTICAL THRESHOLD BREACHED (Z > 4.2). FUNDS RELEASED TO MSF WALLET.</p>
    </div>
    """, unsafe_allow_html=True)

# --- 📊 ENHANCED METRICS (REPLACES OLD METRIC ROW) ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("RISK Z-SCORE", f"{z_score:.2f}", delta=f"{z_score - 0.5:.2f} (24h)", delta_color="inverse")
col2.metric("CONFIRMED CASES", f"{current_state['emr_confirmations']}", "EMR VERIFIED")
col3.metric("ENTANGLEMENT", "94.7%", "+2.1% (AI Confidence)")
col4.metric("BOND STATUS", "RELEASED" if z_score > 4.2 else "LOCKED", "USDC POOL")

st.write("")  # Spacer

# --- MAIN VISUALIZATION ROW ---
viz1, viz2 = st.columns([2, 1])

# PyDeck Map
with viz1:
    st.markdown("### 🗺️ SPATIOTEMPORAL RISK MAP")
    
    r, g = 0, 255
    if z_score > 3.5: r, g = 255, 0
    elif z_score > 1.5: r, g = 255, 215

    # Zoom into the affected zone when severity is high
    zoom_level = 9 if z_score > 3.5 else (10 if z_score > 1.5 else 11)
    view_state = pdk.ViewState(latitude=0.0512, longitude=40.3129, zoom=zoom_level, pitch=50)
    layer = pdk.Layer("ScatterplotLayer", data=pd.DataFrame([current_state]), get_position=["lon", "lat"],
                      get_color=[r, g, 0, 160], get_radius=1000 + (z_score * 500), pickable=True)

    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/dark-v10', initial_view_state=view_state, layers=[layer]))

with viz2:
    st.markdown("### 📉 THE GOLDEN THREAD: Resolution of Agentic Conflict (CBS vs. EMR)")
    chart_data = historical_data[['hour', 'cbs_signals', 'z_score']]
    fig = px.line(chart_data, x='hour', y=['cbs_signals', 'z_score'], 
                  color_discrete_map={"cbs_signals": "#FFD700", "z_score": "#FF0000"})
    fig.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color='#00FF41', margin=dict(l=20, r=20, t=20, b=20), legend=dict(orientation="h"))
    st.plotly_chart(fig, use_container_width=True)

# --- FOOTER ---
st.divider()
st.markdown(f"**SYSTEM LOG:** Simulated Outbreak Scenario v1.0 | Offline Protocol: **ACTIVE** | Frame: {current_hour}/72")
