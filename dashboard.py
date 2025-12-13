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
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADER ---
@st.cache_data
def load_data():
    try:
        with open('simulated_outbreak.json', 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data['events'])
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

# --- HEADER SECTION ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("## 🛡️ iLUMINARA SOVEREIGN COMMAND")
    st.markdown("### NODE: **JOR-47 (DADAAB)** | LATENCY: **18ms**")

with col_head2:
    if current_state['payout_status'] == "LOCKED":
        st.markdown("## STATUS: <span class='status-ok'>SECURE</span>", unsafe_allow_html=True)
    else:
        st.markdown("## STATUS: <span class='status-crit'>CRITICAL</span>", unsafe_allow_html=True)

st.divider()

# --- KPI ROW (6 Columns) ---
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

z_score = current_state['z_score']
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
    payout_color = "status-crit" if current_state['payout_status'] == "RELEASED" else "status-ok"
    st.markdown(f"<div class='metric-container'>Parametric Bond<br><span class='big-font {payout_color}'>{current_state['payout_status']}</span></div>", unsafe_allow_html=True)

with kpi3:
    st.markdown(f"<div class='metric-container'>CBS Signals<br><span class='big-font'>{int(current_state['cbs_signals'])}</span></div>", unsafe_allow_html=True)

with kpi4:
    st.markdown(f"<div class='metric-container'>EMR Confirmed<br><span class='big-font'>{int(current_state['emr_confirmations'])}</span></div>", unsafe_allow_html=True)

with kpi5:
    st.markdown(f"<div class='metric-container'>Governance Kernel<br><span class='big-font status-ok'>14 ACTIVE</span></div>", unsafe_allow_html=True)
    if st.button("VIEW LEGAL LEDGER"):
        st.info("💡 Concept: This would navigate to the Transparency View.")

# NEW Field Validation KPI
with kpi6:
    st.markdown(f"<div class='metric-container'>Field Validation<br><span class='big-font {validation_color}'>{validation_status}</span></div>", unsafe_allow_html=True)

st.write("")  # Spacer

# --- MAIN VISUALIZATION ROW ---
viz1, viz2 = st.columns([2, 1])

# PyDeck Map
with viz1:
    st.markdown("### 🗺️ SPATIOTEMPORAL RISK MAP")
    
    r, g = 0, 255
    if z_score > 3.5: r, g = 255, 0
    elif z_score > 1.5: r, g = 255, 215
    
    view_state = pdk.ViewState(latitude=0.0512, longitude=40.3129, zoom=11, pitch=50)
    layer = pdk.Layer("ScatterplotLayer", data=pd.DataFrame([current_state]), get_position=["lon", "lat"],
                      get_color=[r, g, 0, 160], get_radius=1000 + (z_score * 500), pickable=True)

    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/dark-v10', initial_view_state=view_state, layers=[layer]))

with viz2:
    st.markdown("### 📉 THE GOLDEN THREAD")
    chart_data = historical_data[['hour', 'cbs_signals', 'z_score']]
    fig = px.line(chart_data, x='hour', y=['cbs_signals', 'z_score'], 
                  color_discrete_map={"cbs_signals": "#FFD700", "z_score": "#FF0000"})
    fig.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color='#00FF41', margin=dict(l=20, r=20, t=20, b=20), legend=dict(orientation="h"))
    st.plotly_chart(fig, use_container_width=True)

# --- FOOTER ---
st.divider()
st.markdown(f"**SYSTEM LOG:** Simulated Outbreak Scenario v1.0 | Offline Protocol: **ACTIVE** | Frame: {current_hour}/72")
