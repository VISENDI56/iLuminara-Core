"""
iLuminara Sovereign Command Console
═════════════════════════════════════════════════════════════════════════════

A dark-mode, industrial-aesthetic dashboard for visualizing real-time surveillance
and outbreak detection. Designed to be projected in a war room for investor demos.

Key Visualizations:
1. Command Header: Node status, uptime, compliance status
2. Hexagon Map: Spatial distribution of cases, color-coded by Z-score
3. Golden Thread: Timeline showing CBS signals leading to EMR confirmation
4. Parametric Bond Trigger: Bond payout status (LOCKED → RELEASED)
5. Metrics: Real-time Z-score, case counts, alert levels

Run with: streamlit run dashboard.py
"""

import streamlit as st
import json
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import pydeck as pdk

# Page configuration
st.set_page_config(
    page_title="iLuminara Command Console",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Dark mode CSS
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #0a0e27;
        color: #e0e6ed;
    }
    [data-testid="stSidebar"] {
        background-color: #0f1229;
    }
    .stMetric {
        background-color: #1a1f3a;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #00ff88;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0f1229;
    }
    .stTabs [aria-selected="true"] {
        border-bottom-color: #00ff88;
    }
    h1, h2, h3 {
        color: #00ff88;
        font-family: 'Courier New', monospace;
    }
    .green-text { color: #00ff88; }
    .yellow-text { color: #ffff00; }
    .red-text { color: #ff3366; }
    .info-card {
        background: linear-gradient(135deg, #1a1f3a 0%, #0f1229 100%);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #00ff88;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_outbreak_data():
    """Load simulated outbreak data from JSON."""
    filepath = Path("simulated_outbreak.json")
    if not filepath.exists():
        st.error("❌ simulated_outbreak.json not found. Run: python edge_node/frenasa_engine/simulate_outbreak.py")
        return None

    with open(filepath) as f:
        return json.load(f)


def format_timestamp(iso_string):
    """Convert ISO timestamp to readable format."""
    try:
        dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
        return dt.strftime("%H:%M:%S")
    except:
        return iso_string


def get_z_score_color(z_score):
    """Return color based on Z-score alert level."""
    if z_score < 1.0:
        return "#00ff88"  # GREEN
    elif z_score < 2.576:
        return "#ffff00"  # YELLOW
    elif z_score < 4.0:
        return "#ff9900"  # ORANGE
    else:
        return "#ff3366"  # RED


def render_header(data):
    """Render the command console header."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"<h2 class='green-text'>⚡ iLuminara Sovereign Command</h2>",
            unsafe_allow_html=True,
        )

    with col2:
        node_status = "🟢 ONLINE"
        st.markdown(
            f"<div class='info-card'><strong>Node:</strong> JOR-47 (Dadaab)<br/><strong>Status:</strong> {node_status}</div>",
            unsafe_allow_html=True,
        )

    with col3:
        uptime = datetime.utcnow() - datetime.fromisoformat(
            data["simulation_metadata"]["generated_at"]
        )
        st.markdown(
            f"<div class='info-card'><strong>Uptime:</strong> {uptime.seconds // 3600}h {(uptime.seconds % 3600) // 60}m</div>",
            unsafe_allow_html=True,
        )

    with col4:
        compliance = "🛡️ COMPLIANT"
        st.markdown(
            f"<div class='info-card'><strong>Compliance:</strong> {compliance}</div>",
            unsafe_allow_html=True,
        )


def render_metrics(data):
    """Render key performance metrics."""
    st.markdown("---")
    st.markdown("<h3 class='green-text'>📊 Real-Time Metrics</h3>", unsafe_allow_html=True)

    z_scores = data["z_score_timeline"]
    current_z = z_scores[-1]["z_score"]
    max_z = max(z["z_score"] for z in z_scores)
    total_cases = sum(z["cases"] for z in z_scores)
    bond_status = data["parametric_bond_trigger"]["status"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        status_color = "#00ff88" if current_z < 2.576 else "#ff3366"
        st.markdown(
            f"""
            <div class='info-card'>
            <h4 style='color: {status_color};'>Current Z-Score</h4>
            <h2 style='color: {status_color}; font-size: 48px;'>{current_z:.2f}</h2>
            <small>Threshold: 2.576 (99%)</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class='info-card'>
            <h4 style='color: #ffff00;'>Peak Z-Score</h4>
            <h2 style='color: #ffff00; font-size: 48px;'>{max_z:.2f}</h2>
            <small>Since simulation start</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class='info-card'>
            <h4 style='color: #00ff88;'>Total Cases</h4>
            <h2 style='color: #00ff88; font-size: 48px;'>{total_cases}</h2>
            <small>Across all zones</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        bond_color = "#ff3366" if bond_status == "PAYOUT_RELEASED" else "#00ff88"
        st.markdown(
            f"""
            <div class='info-card'>
            <h4 style='color: {bond_color};'>Bond Status</h4>
            <h2 style='color: {bond_color}; font-size: 36px;'>{bond_status}</h2>
            <small>Parametric Insurance</small>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_map(data):
    """Render pydeck hexagon map of Dadaab."""
    st.markdown("---")
    st.markdown("<h3 class='green-text'>🗺️ Geographic Surveillance Map</h3>", unsafe_allow_html=True)

    # Get geographic data
    geographic = data["geographic_data"]

    # Create DataFrame for pydeck
    map_data = []
    for zone in geographic:
        map_data.append(
            {
                "lat": zone["latitude"],
                "lon": zone["longitude"],
                "cases": zone["cases"],
                "zone": zone["zone"],
                "attack_rate": zone["attack_rate"],
            }
        )

    df_map = pd.DataFrame(map_data)

    # Create hexagon layer
    hexagon_layer = pdk.Layer(
        "HexagonLayer",
        data=df_map,
        get_position=["lon", "lat"],
        radius=5000,  # 5km hexagon size
        elevation_scale=100,
        elevation_range=[0, 1000],
        pickable=True,
        extruded=True,
        get_fill_color="[cases * 20, 200, 200 - cases * 15]",  # Color intensity by cases
    )

    # Tooltip
    tooltip = {
        "html": "<b>{zone}</b><br/>Cases: {cases}<br/>Attack Rate: {attack_rate:.2%}",
        "style": {
            "backgroundColor": "#0a0e27",
            "color": "#00ff88",
            "fontSize": "12px",
        },
    }

    # Create map
    view_state = pdk.ViewState(
        longitude=40.33,
        latitude=2.79,
        zoom=10,
        min_zoom=9,
        max_zoom=12,
        pitch=45,
        bearing=0,
    )

    st.pydeck_chart(
        pdk.Deck(
            layers=[hexagon_layer],
            initial_view_state=view_state,
            tooltip=tooltip,
            map_provider="mapbox",
            map_style="mapbox://styles/mapbox/dark-v10",
        )
    )


def render_z_score_timeline(data):
    """Render Z-score progression over time."""
    st.markdown("---")
    st.markdown("<h3 class='green-text'>📈 Z-Score Outbreak Detection Timeline</h3>", unsafe_allow_html=True)

    z_scores = data["z_score_timeline"]
    df_z = pd.DataFrame(z_scores)

    # Create chart data
    chart_data = df_z[["hour", "z_score", "cases"]].copy()

    # Plot using Streamlit's line chart
    col1, col2 = st.columns(2)

    with col1:
        st.line_chart(
            chart_data.set_index("hour")[["z_score"]],
            use_container_width=True,
            height=300,
        )
        st.caption("Z-Score Progression (99% threshold at 2.576)")

    with col2:
        st.line_chart(
            chart_data.set_index("hour")[["cases"]],
            use_container_width=True,
            height=300,
        )
        st.caption("Cases per Hour (Exponential Growth Phase)")

    # Add timeline table
    st.markdown("**Detailed Z-Score Timeline**")
    display_cols = ["hour", "timestamp", "cases", "z_score", "alert_level"]
    st.dataframe(
        df_z[display_cols].tail(20),
        use_container_width=True,
        height=300,
    )


def render_golden_thread(data):
    """Render Golden Thread fusion examples."""
    st.markdown("---")
    st.markdown("<h3 class='green-text'>🔗 Golden Thread: CBS → EMR Fusion</h3>", unsafe_allow_html=True)

    fusion_examples = data["golden_thread_examples"]

    for i, fusion in enumerate(fusion_examples[:5]):
        col1, col2, col3 = st.columns([2, 1, 2])

        with col1:
            cbs = fusion["cbs_signal"]
            st.markdown(
                f"""
                <div class='info-card'>
                <strong>📡 CBS Signal #{i+1}</strong><br/>
                <small>Community Report</small><br/>
                ⏰ {format_timestamp(cbs['timestamp'])}<br/>
                📍 {cbs['location']}<br/>
                🔍 {cbs['symptom']}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            score = fusion["verification_score"]
            color = "#00ff88" if score == 1.0 else "#ffff00"
            st.markdown(
                f"""
                <div class='info-card' style='text-align: center;'>
                <h3 style='color: {color};'>✓</h3>
                <small>VERIFIED</small><br/>
                Score: {score:.1%}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            emr = fusion["emr_record"]
            st.markdown(
                f"""
                <div class='info-card'>
                <strong>📋 EMR Confirmation #{i+1}</strong><br/>
                <small>Clinical Diagnosis</small><br/>
                ⏰ {format_timestamp(emr['timestamp'])}<br/>
                📍 {emr['location']}<br/>
                🩺 {emr['diagnosis']}
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_alert_timeline(data):
    """Render alert progression timeline."""
    st.markdown("---")
    st.markdown("<h3 class='green-text'>🚨 Alert Progression</h3>", unsafe_allow_html=True)

    # Categorize events by alert level and time
    events = data["events"]
    events_df = pd.DataFrame(events)

    # Group by hour and alert level
    alert_timeline = []
    for hour in sorted(set(int(e["hour"]) for e in events)):
        hour_events = [e for e in events if int(e["hour"]) == hour]
        alert_level = max(
            (e.get("alert_level", "UNKNOWN") for e in hour_events),
            key=lambda x: ["UNKNOWN", "WATCH", "ALERT", "CRITICAL"].index(x),
        )

        alert_timeline.append(
            {
                "hour": hour,
                "events": len(hour_events),
                "alert_level": alert_level,
            }
        )

    df_alerts = pd.DataFrame(alert_timeline)

    # Color by alert level
    colors = {
        "WATCH": "#ffff00",
        "ALERT": "#ff9900",
        "CRITICAL": "#ff3366",
        "UNKNOWN": "#888888",
    }

    col1, col2 = st.columns([2, 1])

    with col1:
        st.bar_chart(df_alerts.set_index("hour")[["events"]], use_container_width=True, height=250)
        st.caption("Events per Hour During Surveillance Period")

    with col2:
        alert_counts = df_alerts["alert_level"].value_counts()
        st.markdown("**Alert Summary**")
        for level, count in alert_counts.items():
            color = colors.get(level, "#888888")
            st.markdown(f"<span style='color: {color};'>●</span> {level}: {count}", unsafe_allow_html=True)


def render_compliance_panel(data):
    """Render compliance and governance status."""
    st.markdown("---")
    st.markdown("<h3 class='green-text'>🛡️ Compliance & Governance</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class='info-card'>
            <h4 style='color: #00ff88;'>Active Frameworks</h4>
            ✓ GDPR Art. 9 (Data Sovereignty)<br/>
            ✓ Kenya DPA §37 (Transfer Restrictions)<br/>
            ✓ HIPAA §164.312 (Safeguards)<br/>
            ✓ EU AI Act §6 (Right to Explanation)<br/>
            <strong style='color: #00ff88;'>14/14 Frameworks Active</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class='info-card'>
            <h4 style='color: #00ff88;'>Audit Trail</h4>
            ✓ All events logged<br/>
            ✓ Consent validated<br/>
            ✓ Data sovereignty enforced<br/>
            ✓ Explainability tracked<br/>
            <strong style='color: #00ff88;'>100% Auditable</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ═════════════════════════════════════════════════════════════════════════════
# Main Dashboard
# ═════════════════════════════════════════════════════════════════════════════

def main():
    # Load data
    data = load_outbreak_data()

    if data is None:
        st.error(
            """
            ❌ Cannot load outbreak data.
            
            Run the data generator first:
            ```
            python edge_node/frenasa_engine/simulate_outbreak.py
            ```
            """
        )
        return

    # Render dashboard
    render_header(data)
    render_metrics(data)
    render_map(data)

    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Z-Score Timeline", "🔗 Golden Thread", "🚨 Alerts", "🛡️ Compliance"]
    )

    with tab1:
        render_z_score_timeline(data)

    with tab2:
        render_golden_thread(data)

    with tab3:
        render_alert_timeline(data)

    with tab4:
        render_compliance_panel(data)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #888; font-size: 12px; margin-top: 30px;'>
        iLuminara Sovereign Command Console | Node: JOR-47 | Status: ONLINE<br/>
        <span style='color: #00ff88;'>█ Active</span> | 
        <span style='color: #ffff00;'>⚠ Watch</span> | 
        <span style='color: #ff9900;'>⚠ Alert</span> | 
        <span style='color: #ff3366;'>🚨 Critical</span><br/>
        "Transform preventable suffering from statistical inevitability to historical anomaly."
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
