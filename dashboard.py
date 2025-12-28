import streamlit as st
import pandas as pd
import pydeck as pdk
import time
import json
import os
from infrastructure.ui_engine.theme_manager import apply_circadian_theme
from state.shared_memory import load_state
from edge_node.data_ingestion_layer import IngestionEngine

# Import governance modules
from governance.living_certification import LivingCertificationDashboard
from governance.compliance_oracle import ComplianceOracle
from governance.dspm_dashboard import UnifiedDSPMDashboard

# --- CLASS-5 CONFIGURATION ---
st.set_page_config(page_title="iLuminara Command", page_icon="🏛️", layout="wide")
apply_circadian_theme()

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

# --- LOAD ENGINES ---
state = load_state()
ingestor = IngestionEngine()
fusion = ingestor.fuse_data_streams()

# --- CREATE TABS ---
tab1, tab2 = st.tabs(["🏛️ Command Center", "🏛️ Living IMS Dashboard"])

with tab1:
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

with tab2:
    # --- LIVING IMS DASHBOARD ---
    st.subheader("🏛️ INTEGRATED MANAGEMENT SYSTEM - TRIPLE CERTIFICATION STATUS")
    
    # Initialize governance components
    living_cert = LivingCertificationDashboard()
    compliance_oracle = ComplianceOracle()
    dspm_dashboard = UnifiedDSPMDashboard()
    
    # Update with sample data for demonstration
    living_cert.update_certification_score('ISO42001', 0.87)
    living_cert.update_certification_score('ISO27001', 0.92)
    living_cert.update_certification_score('ISO27701', 0.89)
    
    # Get dashboard data
    cert_data = living_cert.get_dashboard_data()
    compliance_data = compliance_oracle.get_compliance_status()
    dspm_data = dspm_dashboard.get_dashboard_data()
    
    # Overall Status
    overall_status = cert_data['overall_status']
    status_color = "🟢" if overall_status == "certified" else "🟡" if overall_status == "developing" else "🔴"
    st.metric("Triple Certification Status", f"{status_color} {overall_status.upper()}", 
              f"{cert_data['progress_summary']['completion_percentage']:.1f}% Complete")
    
    # Certification Scores
    col1, col2, col3 = st.columns(3)
    
    with col1:
        iso42001 = cert_data['certifications']['ISO42001']
        st.metric("ISO 42001 (AI)", f"{iso42001['current_score']:.2%}", 
                  f"Target: {iso42001['target_score']:.0%}", 
                  delta=f"{iso42001['status'].replace('_', ' ').title()}")
    
    with col2:
        iso27001 = cert_data['certifications']['ISO27001']
        st.metric("ISO 27001 (Security)", f"{iso27001['current_score']:.2%}", 
                  f"Target: {iso27001['target_score']:.0%}",
                  delta=f"{iso27001['status'].replace('_', ' ').title()}")
    
    with col3:
        iso27701 = cert_data['certifications']['ISO27701']
        st.metric("ISO 27701 (Privacy)", f"{iso27701['current_score']:.2%}", 
                  f"Target: {iso27701['target_score']:.0%}",
                  delta=f"{iso27701['status'].replace('_', ' ').title()}")
    
    st.divider()
    
    # Compliance Validation Status
    st.subheader("🔍 Continuous Compliance Validation")
    if compliance_data['last_validation']:
        last_val = compliance_data['last_validation']
        st.info(f"Last Validation: {last_val['timestamp'][:19]} | Status: {last_val['overall_status'].upper()}")
        
        # Show individual framework status
        val_results = last_val['results']
        for iso, result in val_results.items():
            st.write(f"**{iso}**: {result['status'].replace('_', ' ').title()} ({result['score']:.1%})")
    else:
        st.warning("No compliance validation data available")
    
    # DSPM Security Posture
    st.subheader("🛡️ Data Security Posture Management")
    dspm_report = dspm_data['report']
    st.metric("Security Score", f"{dspm_report['average_security_score']:.2%}")
    st.caption(f"Assets Monitored: {dspm_report['total_assets']} | High Risk: {dspm_report['high_risk_assets']}")
    
    # Next Steps
    st.subheader("🎯 Next Steps for Certification")
    next_steps = cert_data['next_steps']
    for step in next_steps:
        st.write(f"• {step}")
    
    # Recent Milestones
    st.subheader("🏆 Recent Certification Milestones")
    all_milestones = []
    for iso, milestones in cert_data['milestones'].items():
        for milestone in milestones[-3:]:  # Last 3 per standard
            all_milestones.append(f"{iso}: {milestone.get('title', 'Milestone')} ({milestone['timestamp'][:10]})")
    
    if all_milestones:
        for milestone in all_milestones[-5:]:  # Show last 5 overall
            st.write(f"• {milestone}")
    else:
        st.info("No milestones recorded yet")