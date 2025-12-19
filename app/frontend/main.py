"""
iLuminara Compassionate UI Dashboard
══════════════════════════════════════════════════════════════════════════════

High-fidelity Streamlit dashboard for the iLuminara GCP prototype.
Industrial Cyberpunk aesthetic with dark mode.

Tabs:
1. Sentry Mode - Voice-to-JSON processing and visualization
2. HSTPU Map - Hierarchical spatiotemporal outbreak visualization
3. Ethical Audit - Active Inference decision log
"""

import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from datetime import datetime
import random

# ══════════════════════════════════════════════════════════════════════════
# CONFIGURATION: THE SOVEREIGN AESTHETIC (Industrial Cyberpunk)
# ══════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="iLuminara • Compassionate Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS: Dark Mode Industrial Cyberpunk
st.markdown("""
    <style>
        /* Core Theme */
        .stApp {
            background-color: #0a0e1a;
            color: #00FF41;
            font-family: 'Courier New', monospace;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #00FF41 !important;
            text-shadow: 0 0 10px rgba(0, 255, 65, 0.3);
            font-weight: 800;
            letter-spacing: 1px;
        }
        
        /* Metrics & Cards */
        .metric-container {
            border: 2px solid #1a1f2e;
            padding: 16px;
            background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            margin: 8px 0;
        }
        
        .metric-label {
            font-size: 12px;
            color: #7a8599;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 8px;
        }
        
        .metric-value {
            font-size: 32px;
            font-weight: 900;
            color: #00FF41;
            text-shadow: 0 0 15px rgba(0, 255, 65, 0.5);
        }
        
        /* Status Indicators */
        .status-ok { color: #00FF41; }
        .status-warn { color: #FFD700; text-shadow: 0 0 10px rgba(255, 215, 0, 0.5); }
        .status-crit { 
            color: #FF0000; 
            text-shadow: 0 0 15px rgba(255, 0, 0, 0.7);
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        /* Banners */
        .status-banner {
            padding: 16px 24px;
            border-radius: 8px;
            color: white;
            font-weight: 800;
            font-size: 18px;
            text-align: center;
            margin: 16px 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        }
        
        .status-banner.secure {
            background: linear-gradient(90deg, #004d00, #008000);
            border: 2px solid #00FF41;
        }
        
        .status-banner.active {
            background: linear-gradient(90deg, #1a4d80, #2d7ab8);
            border: 2px solid #4da6ff;
        }
        
        .status-banner.critical {
            background: linear-gradient(90deg, #7f0000, #ff0000);
            border: 2px solid #ff4444;
            animation: pulse-banner 1s infinite;
        }
        
        @keyframes pulse-banner {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #1a4d80, #2d7ab8);
            color: white;
            border: 2px solid #4da6ff;
            border-radius: 6px;
            padding: 10px 24px;
            font-weight: 700;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #2d7ab8, #4da6ff);
            box-shadow: 0 0 20px rgba(77, 166, 255, 0.5);
        }
        
        /* Dividers */
        hr {
            border: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, #1a4d80, transparent);
            margin: 24px 0;
        }
        
        /* JSON Display */
        .json-display {
            background: #0f1419;
            border: 1px solid #1a4d80;
            border-radius: 6px;
            padding: 16px;
            font-family: 'Courier New', monospace;
            color: #00FF41;
            overflow-x: auto;
            max-height: 400px;
            overflow-y: auto;
        }
        
        /* Table Styling */
        .dataframe {
            background: #0f1419 !important;
            color: #00FF41 !important;
        }
    </style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════

API_BASE_URL = "http://localhost:8000"

def call_api(endpoint: str, method: str = "GET", data: dict = None):
    """Call backend API with error handling."""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "error": f"API returned {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Backend not running. Start with: uvicorn app.backend.main:app"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ══════════════════════════════════════════════════════════════════════════
# HEADER SECTION
# ══════════════════════════════════════════════════════════════════════════

col_header1, col_header2 = st.columns([3, 1])

with col_header1:
    st.markdown("# 🛡️ iLUMINARA")
    st.markdown("### Compassionate Intelligence • Sovereign Health Platform")

with col_header2:
    st.markdown("<div class='status-banner active'>PROTOTYPE MODE</div>", unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════
# TAB NAVIGATION
# ══════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3 = st.tabs([
    "🎤 SENTRY MODE",
    "🗺️ HSTPU MAP",
    "⚖️ ETHICAL AUDIT"
])

# ══════════════════════════════════════════════════════════════════════════
# TAB 1: SENTRY MODE (Voice-to-JSON)
# ══════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("## 🎤 Sentry Mode: Voice Intelligence")
    st.markdown("*Convert field voice reports to structured JSON intelligence.*")
    
    st.markdown("---")
    
    col_voice1, col_voice2 = st.columns([1, 1])
    
    with col_voice1:
        st.markdown("### 📡 Voice Input")
        
        # Audio file upload
        audio_file = st.file_uploader(
            "Upload Audio Report (MP3, WAV)",
            type=["mp3", "wav", "m4a"],
            help="Field worker voice report"
        )
        
        # Metadata inputs
        with st.expander("📋 Optional Metadata"):
            worker_id = st.text_input("Worker ID", placeholder="e.g., FW-12345")
            location = st.text_input("Location", placeholder="e.g., Dadaab Camp")
        
        # Process button
        if st.button("🔍 Process Voice Report", type="primary"):
            with st.spinner("Processing audio..."):
                # For demo, simulate voice report
                result = call_api("/voice/simulate", method="POST")
                
                if result.get("success"):
                    st.session_state['voice_result'] = result['data']
                    st.success("✅ Voice report processed successfully!")
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    with col_voice2:
        st.markdown("### 📊 Structured Output")
        
        if 'voice_result' in st.session_state:
            result = st.session_state['voice_result']
            
            # Display key metrics
            metrics_cols = st.columns(3)
            with metrics_cols[0]:
                st.markdown(f"""
                    <div class='metric-container'>
                        <div class='metric-label'>Confidence</div>
                        <div class='metric-value'>{result['transcription']['confidence']:.1%}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with metrics_cols[1]:
                urgency = result['entities']['urgency']
                urgency_class = "status-crit" if urgency == "HIGH" else "status-ok"
                st.markdown(f"""
                    <div class='metric-container'>
                        <div class='metric-label'>Urgency</div>
                        <div class='metric-value {urgency_class}'>{urgency}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with metrics_cols[2]:
                case_count = result['entities'].get('case_count', 0)
                st.markdown(f"""
                    <div class='metric-container'>
                        <div class='metric-label'>Cases</div>
                        <div class='metric-value'>{case_count or 'N/A'}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Transcription
            st.markdown("#### 📝 Transcription")
            st.info(result['transcription']['text'])
            
            # Extracted entities
            st.markdown("#### 🔍 Extracted Entities")
            entities_df = pd.DataFrame([
                {"Entity": "Symptoms", "Value": ", ".join(result['entities']['symptoms']) or "None detected"},
                {"Entity": "Location", "Value": result['entities']['location_mentioned'] or "Not specified"},
                {"Entity": "Case Count", "Value": result['entities']['case_count'] or "Not mentioned"},
                {"Entity": "Urgency", "Value": result['entities']['urgency']}
            ])
            st.table(entities_df)
            
            # Full JSON
            with st.expander("🔧 View Full JSON"):
                st.markdown(f"<div class='json-display'><pre>{json.dumps(result, indent=2)}</pre></div>", 
                          unsafe_allow_html=True)
        else:
            st.info("👆 Process a voice report to see structured output")

# ══════════════════════════════════════════════════════════════════════════
# TAB 2: HSTPU MAP
# ══════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("## 🗺️ HSTPU: Hierarchical Spatiotemporal Map")
    st.markdown("*Real-time outbreak intelligence across spatial and temporal hierarchies.*")
    
    st.markdown("---")
    
    # Controls
    col_map1, col_map2, col_map3 = st.columns([2, 1, 1])
    
    with col_map1:
        region_select = st.selectbox("📍 Region", ["Kenya", "East Africa", "Global"])
    
    with col_map2:
        threshold = st.slider("🎯 Risk Threshold", 0.0, 5.0, 2.0, 0.1)
    
    with col_map3:
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    # Fetch HSTPU data
    hstpu_data = call_api("/hstpu/map", method="GET")
    hotspots_data = call_api(f"/hstpu/hotspots?threshold={threshold}", method="GET")
    
    if hstpu_data.get("success"):
        map_info = hstpu_data['data']
        points = map_info['points']
        
        # Convert to DataFrame
        df_map = pd.DataFrame(points)
        
        # KPIs
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        with kpi1:
            total_hotspots = len(df_map[df_map['z_score'] > threshold])
            st.markdown(f"""
                <div class='metric-container'>
                    <div class='metric-label'>Active Hotspots</div>
                    <div class='metric-value status-crit'>{total_hotspots}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with kpi2:
            max_z = df_map['z_score'].max()
            z_class = "status-crit" if max_z > 3.5 else "status-warn" if max_z > 2.0 else "status-ok"
            st.markdown(f"""
                <div class='metric-container'>
                    <div class='metric-label'>Max Z-Score</div>
                    <div class='metric-value {z_class}'>{max_z:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with kpi3:
            total_at_risk = df_map['population_at_risk'].sum()
            st.markdown(f"""
                <div class='metric-container'>
                    <div class='metric-label'>Population at Risk</div>
                    <div class='metric-value'>{total_at_risk:,}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with kpi4:
            total_confirmed = df_map['cases_confirmed'].sum()
            st.markdown(f"""
                <div class='metric-container'>
                    <div class='metric-label'>Confirmed Cases</div>
                    <div class='metric-value'>{int(total_confirmed)}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Map visualization
        col_mapviz1, col_mapviz2 = st.columns([2, 1])
        
        with col_mapviz1:
            st.markdown("### 🌍 Outbreak Geospatial Visualization")
            
            # PyDeck map
            view_state = pdk.ViewState(
                latitude=map_info['center']['lat'],
                longitude=map_info['center']['lon'],
                zoom=map_info['zoom'],
                pitch=45
            )
            
            layer = pdk.Layer(
                "ScatterplotLayer",
                data=df_map,
                get_position=["lon", "lat"],
                get_color="color",
                get_radius="z_score * 5000",
                pickable=True,
                opacity=0.7
            )
            
            deck = pdk.Deck(
                map_style='mapbox://styles/mapbox/dark-v10',
                initial_view_state=view_state,
                layers=[layer],
                tooltip={
                    "text": "{region}\nZ-Score: {z_score}\nCases: {cases_confirmed}"
                }
            )
            
            st.pydeck_chart(deck)
        
        with col_mapviz2:
            st.markdown("### 📈 Risk Trend")
            
            # Generate time series
            hours = list(range(24))
            risk_trend = [random.uniform(1.5, 4.0) for _ in hours]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=hours,
                y=risk_trend,
                mode='lines+markers',
                line=dict(color='#FF0000', width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(255, 0, 0, 0.2)'
            ))
            
            fig.update_layout(
                plot_bgcolor='#0f1419',
                paper_bgcolor='#0f1419',
                font_color='#00FF41',
                xaxis_title="Hours",
                yaxis_title="Z-Score",
                height=300,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(gridcolor='#1a1f2e'),
                yaxis=dict(gridcolor='#1a1f2e')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Hotspots table
            st.markdown("### 🔥 Priority Hotspots")
            hotspot_df = df_map.nlargest(3, 'z_score')[['region', 'z_score', 'cases_confirmed']]
            hotspot_df.columns = ['Region', 'Z-Score', 'Cases']
            st.dataframe(hotspot_df, use_container_width=True, hide_index=True)
    else:
        st.error(f"❌ {hstpu_data.get('error', 'Failed to load map data')}")

# ══════════════════════════════════════════════════════════════════════════
# TAB 3: ETHICAL AUDIT
# ══════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("## ⚖️ Ethical Audit: Active Inference Log")
    st.markdown("*Every high-stakes decision validated through humanitarian constraints.*")
    
    st.markdown("---")
    
    # Test action section
    col_eth1, col_eth2 = st.columns([1, 1])
    
    with col_eth1:
        st.markdown("### 🧪 Test Ethical Decision")
        
        action_type = st.selectbox(
            "Action Type",
            ["Resource Allocation", "Outbreak Alert", "Data Transfer", "Intervention", "Prediction"]
        )
        
        # Action-specific inputs
        if action_type == "Resource Allocation":
            equity_based = st.checkbox("Equity-Based Allocation", value=True)
            payload = {
                "allocation_criteria": {"equity_based": equity_based},
                "resources": ["vaccines", "medical_supplies"]
            }
        
        elif action_type == "Data Transfer":
            data_type = st.selectbox("Data Type", ["PHI", "Aggregated", "Anonymous"])
            destination = st.selectbox("Destination", ["Local", "Foreign_Cloud"])
            has_consent = st.checkbox("Has Consent Token", value=False)
            
            payload = {
                "data_type": data_type,
                "destination": destination,
                "destination_jurisdiction": "FOREIGN" if destination == "Foreign_Cloud" else "LOCAL",
                "consent_token": "CONSENT_123" if has_consent else None
            }
        
        else:
            has_explanation = st.checkbox("Include Explanation", value=False)
            payload = {
                "action": f"Test {action_type}",
                "risk_level": "high"
            }
            if has_explanation:
                payload["explanation"] = "SHAP values: [0.3, 0.5, 0.2]"
        
        if st.button("⚖️ Evaluate Action", type="primary"):
            with st.spinner("Evaluating through ethical engine..."):
                result = call_api(
                    "/ethics/evaluate",
                    method="POST",
                    data={
                        "action_type": action_type.lower().replace(" ", "_"),
                        "payload": payload
                    }
                )
                
                if result.get("success"):
                    st.session_state['eval_result'] = result['data']
                    st.rerun()
    
    with col_eth2:
        st.markdown("### 📋 Evaluation Result")
        
        if 'eval_result' in st.session_state:
            eval_data = st.session_state['eval_result']
            
            # Status banner
            if eval_data['approved']:
                st.markdown("<div class='status-banner secure'>✅ ACTION APPROVED</div>", 
                          unsafe_allow_html=True)
            else:
                st.markdown("<div class='status-banner critical'>❌ ACTION REJECTED</div>", 
                          unsafe_allow_html=True)
            
            # Reasoning
            st.markdown("#### 💭 Reasoning")
            st.info(eval_data['reasoning'])
            
            # Violations (if any)
            if eval_data['violations']:
                st.markdown("#### ⚠️ Violations Detected")
                for violation in eval_data['violations']:
                    st.error(violation)
            
            # Checks detail
            with st.expander("🔍 View Detailed Checks"):
                st.json(eval_data)
        else:
            st.info("👆 Test an action to see evaluation results")
    
    st.markdown("---")
    
    # Decision log
    st.markdown("### 📜 Recent Decision Log")
    
    log_data = call_api("/ethics/log?limit=20", method="GET")
    stats_data = call_api("/ethics/stats", method="GET")
    
    if log_data.get("success"):
        # Statistics
        if stats_data.get("success"):
            stats = stats_data['data']
            
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            
            with stat_col1:
                st.markdown(f"""
                    <div class='metric-container'>
                        <div class='metric-label'>Total Decisions</div>
                        <div class='metric-value'>{stats['total_decisions']}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with stat_col2:
                st.markdown(f"""
                    <div class='metric-container'>
                        <div class='metric-label'>Approved</div>
                        <div class='metric-value status-ok'>{stats['approved']}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with stat_col3:
                st.markdown(f"""
                    <div class='metric-container'>
                        <div class='metric-label'>Rejected</div>
                        <div class='metric-value status-crit'>{stats['rejected']}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with stat_col4:
                approval_rate = stats['approval_rate'] * 100
                rate_class = "status-ok" if approval_rate > 80 else "status-warn"
                st.markdown(f"""
                    <div class='metric-container'>
                        <div class='metric-label'>Approval Rate</div>
                        <div class='metric-value {rate_class}'>{approval_rate:.1f}%</div>
                    </div>
                """, unsafe_allow_html=True)
        
        # Log table
        log_entries = log_data['data']['log']
        
        if log_entries:
            df_log = pd.DataFrame(log_entries)
            df_log['timestamp'] = pd.to_datetime(df_log['timestamp']).dt.strftime('%H:%M:%S')
            
            st.dataframe(
                df_log[['timestamp', 'action', 'status', 'reasoning']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No decisions logged yet. Test an action above to generate logs.")
    else:
        st.warning("⚠️ Could not load decision log. Ensure backend is running.")

# ══════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7a8599; font-size: 12px;'>
        iLuminara-Core GCP Prototype v1.0 | Sovereign Health Intelligence Platform<br>
        <strong>Status:</strong> Local Demo Mode | Mock GCP Services Active
    </div>
""", unsafe_allow_html=True)
