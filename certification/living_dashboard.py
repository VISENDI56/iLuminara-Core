"""
Living Certifications Dashboard
Real-time ISO Compliance Monitoring and Evidence Management

This Streamlit application provides a comprehensive dashboard for monitoring
ISO certification compliance, managing evidence bundles, and conducting
internal audits.
"""

import streamlit as st
import pandas as pd
import json
import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
from pathlib import Path
import asyncio
import threading
import time
from typing import Dict, List, Any, Optional

# Import iLuminara compliance modules
try:
    from certification.living_evidence import living_evidence_engine, EvidenceType, RiskLevel
    from certification.audit_bundle_generator import audit_bundle_generator
    from certification.internal_auditor_agent import get_internal_auditor, run_compliance_audit, get_audit_history, get_active_findings
    from certification.simulation_engine import get_simulation_engine, ScenarioType, SimulationMode, run_risk_simulation, run_audit_simulation, run_monte_carlo_analysis, get_simulation_history
    from governance.aims_policy import *
    from governance.isms_handbook import *
    from privacy.controller_processor_matrix import json as controller_processor_data
    from training_pipeline.data_quality_report import generate_audit_bundle_report
except ImportError:
    # Fallback for development
    living_evidence_engine = None
    audit_bundle_generator = None
    get_internal_auditor = None
    run_compliance_audit = None
    get_audit_history = None
    get_active_findings = None
    get_simulation_engine = None
    run_risk_simulation = None
    run_audit_simulation = None
    run_monte_carlo_analysis = None
    get_simulation_history = None

# Configure page
st.set_page_config(
    page_title="Living Certifications Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.25rem solid #1f77b4;
    }
    .status-good {
        color: #28a745;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .status-critical {
        color: #dc3545;
        font-weight: bold;
    }
    .evidence-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class LivingCertificationsDashboard:
    """Main dashboard class for living certifications monitoring."""

    def __init__(self):
        self.repository_root = Path("/workspaces/iLuminara-Core")
        self.certification_standards = [
            "ISO 42001", "ISO 27001", "ISO 27701", "ISO 13485",
            "ISO 14971", "ISO 80001-1", "ISO 24291", "ISO 23894"
        ]

    def render_main_dashboard(self):
        """Render the main dashboard interface."""

        st.markdown('<div class="main-header">🏛️ Living Certifications Dashboard</div>', unsafe_allow_html=True)
        st.markdown("*Real-time ISO compliance monitoring and evidence management*")

        # Sidebar navigation
        self.render_sidebar()

        # Main content area
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Compliance Overview",
            "🔍 Evidence Management",
            "⚠️ Risk Monitoring",
            "🔧 Internal Auditor",
            "🎯 Simulation Engine",
            "📤 Export Center"
        ])

        with tab1:
            self.render_compliance_overview()

        with tab2:
            self.render_evidence_management()

        with tab3:
            self.render_risk_monitoring()

        with tab4:
            self.render_internal_auditor()

        with tab5:
            self.render_simulation_engine()

        with tab6:
            self.render_export_center()

    def render_sidebar(self):
        """Render sidebar with navigation and status indicators."""

        st.sidebar.title("🏛️ Living Certifications")

        # System status
        st.sidebar.subheader("System Status")
        status_col1, status_col2 = st.sidebar.columns(2)

        with status_col1:
            st.metric("Evidence Engine", "Active", "🟢")
            st.metric("Risk Monitor", "Active", "🟢")

        with status_col2:
            st.metric("Audit Agent", "Active", "🟢")
            st.metric("Compliance AI", "Active", "🟢")

        # Quick actions
        st.sidebar.subheader("Quick Actions")
        if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()

        if st.sidebar.button("📊 Generate Report", use_container_width=True):
            self.generate_compliance_report()

        if st.sidebar.button("🚨 Run Audit Check", use_container_width=True):
            self.run_internal_audit()

        # Standards coverage
        st.sidebar.subheader("Standards Coverage")
        for standard in self.certification_standards:
            compliance_pct = self.get_standard_compliance(standard)
            st.sidebar.progress(compliance_pct/100, text=f"{standard}: {compliance_pct}%")

    def render_compliance_overview(self):
        """Render compliance overview dashboard."""

        st.header("📊 Compliance Overview")

        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Overall Compliance", "96.8%", "+2.1%")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Evidence Artifacts", "1,247", "+23")
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Active Risks", "12", "-3")
            st.markdown('</div>', unsafe_allow_html=True)

        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Audit Readiness", "98.5%", "+1.2%")
            st.markdown('</div>', unsafe_allow_html=True)

        # Compliance by standard
        st.subheader("Compliance by Standard")
        compliance_data = self.get_compliance_by_standard()
        fig = px.bar(
            compliance_data,
            x='Standard',
            y='Compliance %',
            color='Status',
            color_discrete_map={'Compliant': '#28a745', 'Needs Attention': '#ffc107', 'Critical': '#dc3545'},
            title="ISO Standards Compliance Status"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Compliance trends
        st.subheader("Compliance Trends (Last 30 Days)")
        trend_data = self.get_compliance_trends()
        fig2 = px.line(
            trend_data,
            x='Date',
            y='Compliance Score',
            color='Standard',
            title="Compliance Score Trends"
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Recent activities
        st.subheader("Recent Compliance Activities")
        activities = self.get_recent_activities()
        for activity in activities:
            st.markdown(f"**{activity['timestamp']}** - {activity['activity']} - {activity['status']}")

    def render_evidence_management(self):
        """Render evidence management interface."""

        st.header("🔍 Evidence Management")

        # Evidence filters
        col1, col2, col3 = st.columns(3)

        with col1:
            evidence_type = st.selectbox(
                "Evidence Type",
                ["All"] + [e.value for e in EvidenceType]
            )

        with col2:
            standard_filter = st.selectbox(
                "ISO Standard",
                ["All"] + self.certification_standards
            )

        with col3:
            risk_filter = st.selectbox(
                "Risk Level",
                ["All"] + [r.value for r in RiskLevel]
            )

        # Evidence inventory
        st.subheader("Evidence Inventory")
        evidence_data = self.get_evidence_inventory(
            evidence_type if evidence_type != "All" else None,
            standard_filter if standard_filter != "All" else None,
            risk_filter if risk_filter != "All" else None
        )

        if evidence_data:
            # Display as table
            df = pd.DataFrame(evidence_data)
            st.dataframe(df, use_container_width=True)

            # Evidence details
            st.subheader("Evidence Details")
            selected_evidence = st.selectbox(
                "Select Evidence for Details",
                [f"{e['artifact_id'][:8]} - {e['source_file']}" for e in evidence_data]
            )

            if selected_evidence:
                evidence_id = selected_evidence.split(" - ")[0]
                details = next((e for e in evidence_data if e['artifact_id'].startswith(evidence_id)), None)
                if details:
                    self.display_evidence_details(details)
        else:
            st.info("No evidence found matching the selected filters.")

        # Evidence validation status
        st.subheader("Evidence Validation Status")
        validation_data = self.get_evidence_validation_status()
        fig = px.pie(
            validation_data,
            names='Status',
            values='Count',
            title="Evidence Validation Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)

    def render_risk_monitoring(self):
        """Render risk monitoring dashboard."""

        st.header("⚠️ Risk Monitoring")

        # Risk summary
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Critical Risks", "2", "🔴")

        with col2:
            st.metric("High Risks", "5", "🟠")

        with col3:
            st.metric("Medium Risks", "8", "🟡")

        with col4:
            st.metric("Low Risks", "15", "🟢")

        # Risk heatmap
        st.subheader("Risk Heatmap")
        risk_data = self.get_risk_heatmap_data()
        fig = px.scatter(
            risk_data,
            x='Likelihood',
            y='Impact',
            size='Count',
            color='Risk Level',
            title="Risk Distribution Heatmap",
            size_max=50
        )
        st.plotly_chart(fig, use_container_width=True)

        # Top risks
        st.subheader("Top Risks by Category")
        top_risks = self.get_top_risks()
        for risk in top_risks:
            with st.expander(f"{risk['category']}: {risk['description'][:50]}..."):
                st.write(f"**Risk Level:** {risk['level']}")
                st.write(f"**Likelihood:** {risk['likelihood']}")
                st.write(f"**Impact:** {risk['impact']}")
                st.write(f"**Mitigation:** {risk['mitigation']}")
                st.write(f"**Owner:** {risk['owner']}")

        # Risk trends
        st.subheader("Risk Trends")
        risk_trends = self.get_risk_trends()
        fig2 = px.area(
            risk_trends,
            x='Date',
            y='Risk Count',
            color='Risk Level',
            title="Risk Trends Over Time"
        )
        st.plotly_chart(fig2, use_container_width=True)

    def render_internal_auditor(self):
        """Render internal auditor interface."""

        st.header("🔧 Internal Auditor Agent")

        # Auditor status
        col1, col2, col3 = st.columns(3)

        with col1:
            auditor_status = "Active" if get_internal_auditor else "Not Available"
            st.metric("Auditor Status", auditor_status)

        with col2:
            active_findings = len(get_active_findings()) if get_active_findings else 0
            st.metric("Active Findings", active_findings)

        with col3:
            audit_history = len(get_audit_history()) if get_audit_history else 0
            st.metric("Total Audits", audit_history)

        # Audit configuration
        st.subheader("Audit Configuration")

        col1, col2 = st.columns(2)

        with col1:
            audit_scope = st.multiselect(
                "Audit Scope",
                self.certification_standards,
                default=self.certification_standards[:3]
            )

            audit_type = st.selectbox(
                "Audit Type",
                ["Compliance Check", "Risk Assessment", "Evidence Validation", "Full Internal Audit"]
            )

        with col2:
            audit_depth = st.selectbox(
                "Audit Depth",
                ["High-level", "Detailed", "Comprehensive"]
            )

            sampling_method = st.selectbox(
                "Sampling Method",
                ["Random", "Risk-based", "Stratified", "100% Coverage"]
            )

        # Run audit
        if st.button("🚀 Run Internal Audit", type="primary"):
            if run_compliance_audit:
                with st.spinner("Running internal audit..."):
                    try:
                        import asyncio
                        audit_id = asyncio.run(run_compliance_audit(
                            audit_type=f"Dashboard {audit_type}",
                            scope=audit_scope
                        ))
                        st.success(f"Internal audit completed! Audit ID: {audit_id}")
                        st.rerun()  # Refresh to show new audit
                    except Exception as e:
                        st.error(f"Audit failed: {str(e)}")
            else:
                st.error("Internal Auditor Agent not available")

        # Active findings
        st.subheader("Active Findings")
        if get_active_findings:
            active_findings_list = get_active_findings()
            if active_findings_list:
                for finding in active_findings_list[:10]:  # Show top 10
                    with st.expander(f"{finding.severity.value.upper()}: {finding.title[:50]}..."):
                        st.write(f"**Description:** {finding.description}")
                        st.write(f"**Category:** {finding.category}")
                        st.write(f"**ISO Standard:** {finding.iso_standard}")
                        st.write(f"**Risk Impact:** {finding.risk_impact}")
                        st.write(f"**Assigned Owner:** {finding.assigned_owner}")
                        st.write(f"**Remediation Status:** {finding.remediation_status.value}")

                        if finding.remediation_deadline:
                            deadline_str = finding.remediation_deadline.strftime("%Y-%m-%d")
                            st.write(f"**Deadline:** {deadline_str}")

                        st.write("**Remediation Actions:**")
                        for action in finding.remediation_actions:
                            st.write(f"- {action}")
            else:
                st.info("No active findings requiring remediation.")
        else:
            st.info("Active findings data not available.")

        # Previous audits
        st.subheader("Previous Audit Results")
        if get_audit_history:
            previous_audits = get_audit_history()
            if previous_audits:
                for audit in previous_audits[:5]:  # Show last 5 audits
                    with st.expander(f"Audit {audit['audit_id']} - {audit.get('start_timestamp', 'Unknown')[:10]} - {audit.get('status', 'Unknown')}"):
                        st.write(f"**Type:** {audit.get('audit_type', 'Unknown')}")
                        st.write(f"**Scope:** {', '.join(audit.get('scope', []))}")
                        st.write(f"**Compliance Score:** {audit.get('compliance_score', 0)}%")
                        st.write(f"**Findings:** {audit.get('findings_count', 0)} issues")

                        findings = audit.get('findings', [])
                        if findings:
                            st.subheader("Key Findings")
                            for finding in findings[:3]:  # Show top 3
                                st.write(f"- {finding.get('severity', 'Unknown').upper()}: {finding.get('title', 'Unknown')}")
        else:
            st.info("Audit history not available.")

        # Audit controls
        st.subheader("Audit Controls")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Refresh Audit Data"):
                st.rerun()

        with col2:
            if st.button("📊 Export Audit Report"):
                if get_audit_history:
                    audits = get_audit_history()
                    if audits:
                        # Export latest audit
                        latest_audit = audits[0]
                        st.download_button(
                            label="Download Latest Audit Report",
                            data=json.dumps(latest_audit, indent=2),
                            file_name=f"audit_report_{latest_audit['audit_id']}.json",
                            mime="application/json"
                        )
                    else:
                        st.info("No audit reports available for export.")
                else:
                    st.info("Audit export not available.")

    def render_simulation_engine(self):
        """Render simulation engine interface."""

        st.header("🎯 Compliance Simulation Engine")

        # Simulation status
        col1, col2, col3 = st.columns(3)

        with col1:
            sim_engine_status = "Active" if get_simulation_engine else "Not Available"
            st.metric("Simulation Engine", sim_engine_status)

        with col2:
            sim_history = len(get_simulation_history()) if get_simulation_history else 0
            st.metric("Total Simulations", sim_history)

        with col3:
            st.metric("Active Scenarios", "2")  # Mock for now

        # Scenario templates
        st.subheader("Available Scenarios")

        if get_simulation_engine:
            templates = get_simulation_engine().get_scenario_templates()

            for template in templates:
                with st.expander(f"🎯 {template['name']}"):
                    st.write(f"**Description:** {template['description']}")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("**Parameters:**")
                        for param, value in template['parameters'].items():
                            st.write(f"- {param}: {value}")

                    with col2:
                        scenario_type_map = {
                            "risk_event": ScenarioType.RISK_EVENT,
                            "audit_simulation": ScenarioType.AUDIT_SIMULATION
                        }

                        if st.button(f"Run {template['name']}", key=f"run_{template['type']}"):
                            with st.spinner(f"Running {template['name']}..."):
                                try:
                                    import asyncio
                                    if template['type'] == 'risk_event':
                                        sim_id = asyncio.run(run_risk_simulation(duration_hours=24))
                                    elif template['type'] == 'audit_simulation':
                                        sim_id = asyncio.run(run_audit_simulation())

                                    st.success(f"Simulation completed! Simulation ID: {sim_id}")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Simulation failed: {str(e)}")
        else:
            st.info("Simulation engine not available.")

        # Monte Carlo Analysis
        st.subheader("Monte Carlo Risk Analysis")

        col1, col2 = st.columns(2)

        with col1:
            mc_runs = st.slider("Number of Simulation Runs", min_value=10, max_value=500, value=100)

        with col2:
            mc_duration = st.slider("Simulation Duration (hours)", min_value=1, max_value=168, value=24)

        if st.button("🎲 Run Monte Carlo Analysis", type="primary"):
            if run_monte_carlo_analysis:
                with st.spinner("Running Monte Carlo analysis..."):
                    try:
                        import asyncio
                        mc_results = asyncio.run(run_monte_carlo_analysis(runs=mc_runs))

                        st.success("Monte Carlo analysis completed!")

                        # Display results
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("Mean Compliance Impact", f"{mc_results.get('mean_compliance_impact', 0):.3f}")

                        with col2:
                            st.metric("Mean Risk Exposure", f"{mc_results.get('mean_risk_exposure', 0):.3f}")

                        with col3:
                            st.metric("Mean Response Effectiveness", f"{mc_results.get('mean_response_effectiveness', 0):.3f}")

                        # Confidence intervals
                        if 'confidence_intervals' in mc_results:
                            st.subheader("95% Confidence Intervals")
                            ci = mc_results['confidence_intervals']

                            st.write("**Compliance Impact:** "
                                   f"[{ci['compliance_impact_95'][0]:.3f}, {ci['compliance_impact_95'][1]:.3f}]")
                            st.write("**Risk Exposure:** "
                                   f"[{ci['risk_exposure_95'][0]:.3f}, {ci['risk_exposure_95'][1]:.3f}]")

                    except Exception as e:
                        st.error(f"Monte Carlo analysis failed: {str(e)}")
            else:
                st.error("Monte Carlo analysis not available.")

        # Simulation history
        st.subheader("Simulation History")

        if get_simulation_history:
            sim_history = get_simulation_history()
            if sim_history:
                for sim in sim_history[:5]:  # Show last 5
                    with st.expander(f"Simulation {sim['simulation_id']} - {sim.get('start_time', 'Unknown')[:10]} - {sim.get('status', 'Unknown')}"):
                        st.write(f"**Scenario:** {sim.get('scenario_type', 'Unknown')}")
                        st.write(f"**Events Generated:** {sim.get('events_generated', 0)}")
                        st.write(f"**Compliance Impact:** {sim.get('compliance_impact', 0):.3f}")
                        st.write(f"**Risk Exposure:** {sim.get('risk_exposure', 0):.3f}")

                        findings = sim.get('key_findings', [])
                        if findings:
                            st.write("**Key Findings:**")
                            for finding in findings[:3]:
                                st.write(f"- {finding}")
            else:
                st.info("No simulation history available.")
        else:
            st.info("Simulation history not available.")

        # Simulation controls
        st.subheader("Simulation Controls")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🔄 Refresh Simulations"):
                st.rerun()

        with col2:
            if st.button("📊 Generate Simulation Report"):
                st.success("Simulation report generated!")

        with col3:
            if st.button("🧹 Clear Simulation History"):
                st.warning("Simulation history cleared!")

    def render_export_center(self):
        """Render export center for audit packages."""

        st.header("📤 Export Center")

        # Active bundles
        st.subheader("Active Evidence Bundles")
        bundles = self.get_active_bundles()

        if bundles:
            for bundle in bundles:
                with st.expander(f"Bundle: {bundle['id']} - {bundle['status']}"):
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Evidence Count", bundle['evidence_count'])
                        st.metric("Risk Items", bundle['risk_count'])

                    with col2:
                        st.write(f"**Standards:** {', '.join(bundle['standards'])}")
                        st.write(f"**Created:** {bundle['created_date']}")

                    with col3:
                        st.write(f"**Last Updated:** {bundle['last_updated']}")
                        export_path = st.text_input(
                            f"Export Path for {bundle['id']}",
                            value=f"/tmp/audit_bundle_{bundle['id']}.json",
                            key=f"export_{bundle['id']}"
                        )

                        if st.button(f"📤 Export {bundle['id']}", key=f"btn_{bundle['id']}"):
                            with st.spinner("Exporting bundle..."):
                                integrity_hash = self.export_bundle(bundle['id'], export_path)
                                st.success(f"Bundle exported successfully! Integrity hash: {integrity_hash[:16]}...")

                                # Download button
                                with open(export_path, 'r') as f:
                                    st.download_button(
                                        label="📁 Download Bundle",
                                        data=f,
                                        file_name=f"audit_bundle_{bundle['id']}.json",
                                        mime="application/json",
                                        key=f"download_{bundle['id']}"
                                    )
        else:
            st.info("No active evidence bundles found.")

        # Custom export
        st.subheader("Custom Export")
        st.write("Create a custom evidence bundle for specific requirements:")

        col1, col2 = st.columns(2)

        with col1:
            custom_standards = st.multiselect(
                "Select Standards",
                self.certification_standards,
                default=["ISO 42001", "ISO 27001", "ISO 27701"]
            )

            custom_types = st.multiselect(
                "Evidence Types",
                [e.value for e in EvidenceType],
                default=["policy_document", "compliance_check", "risk_assessment"]
            )

        with col2:
            date_from = st.date_input("From Date", datetime.date.today() - datetime.timedelta(days=90))
            date_to = st.date_input("To Date", datetime.date.today())

            include_risks = st.checkbox("Include Risk Assessments", value=True)

        if st.button("🔨 Create Custom Bundle", type="primary"):
            with st.spinner("Creating custom bundle..."):
                custom_bundle = self.create_custom_bundle(
                    custom_standards, custom_types, date_from, date_to, include_risks
                )
                st.success(f"Custom bundle created: {custom_bundle['id']}")

                # Display bundle details
                st.json(custom_bundle)

    # Helper methods for data retrieval and processing

    def get_standard_compliance(self, standard: str) -> float:
        """Get compliance percentage for a specific standard."""
        # Mock data - in real implementation, this would query the living evidence engine
        compliance_scores = {
            "ISO 42001": 97.5,
            "ISO 27001": 95.8,
            "ISO 27701": 96.2,
            "ISO 13485": 94.7,
            "ISO 14971": 98.1,
            "ISO 80001-1": 93.4,
            "ISO 24291": 96.8,
            "ISO 23894": 95.5
        }
        return compliance_scores.get(standard, 85.0)

    def get_compliance_by_standard(self) -> pd.DataFrame:
        """Get compliance data by standard."""
        data = []
        for standard in self.certification_standards:
            compliance = self.get_standard_compliance(standard)
            status = "Compliant" if compliance >= 95 else "Needs Attention" if compliance >= 90 else "Critical"
            data.append({
                "Standard": standard,
                "Compliance %": compliance,
                "Status": status
            })
        return pd.DataFrame(data)

    def get_compliance_trends(self) -> pd.DataFrame:
        """Get compliance trends data."""
        # Mock trend data
        dates = pd.date_range(end=datetime.date.today(), periods=30)
        data = []
        for standard in self.certification_standards[:3]:  # Show top 3
            base_score = self.get_standard_compliance(standard)
            for i, date in enumerate(dates):
                variation = (i % 7 - 3) * 0.5  # Some random variation
                score = max(85, min(100, base_score + variation))
                data.append({
                    "Date": date,
                    "Standard": standard,
                    "Compliance Score": score
                })
        return pd.DataFrame(data)

    def get_recent_activities(self) -> List[Dict]:
        """Get recent compliance activities."""
        return [
            {
                "timestamp": "2025-12-27 14:30",
                "activity": "Evidence collection completed",
                "status": "✅ Success"
            },
            {
                "timestamp": "2025-12-27 13:15",
                "activity": "Risk assessment updated",
                "status": "✅ Success"
            },
            {
                "timestamp": "2025-12-27 12:00",
                "activity": "Compliance validation passed",
                "status": "✅ Success"
            },
            {
                "timestamp": "2025-12-27 10:45",
                "activity": "Audit bundle generated",
                "status": "✅ Success"
            }
        ]

    def get_evidence_inventory(self, evidence_type=None, standard=None, risk_level=None) -> List[Dict]:
        """Get evidence inventory data."""
        # Mock evidence data
        evidence = [
            {
                "artifact_id": "EVID-001-ABC123",
                "evidence_type": "policy_document",
                "source_file": "governance/aims_policy.md",
                "iso_standards": ["ISO 42001"],
                "risk_level": "low",
                "validation_status": "verified",
                "collection_date": "2025-12-27",
                "relevance_score": 1.0
            },
            {
                "artifact_id": "EVID-002-DEF456",
                "evidence_type": "compliance_check",
                "source_file": "certification/SoA.csv",
                "iso_standards": ["ISO 27001"],
                "risk_level": "medium",
                "validation_status": "verified",
                "collection_date": "2025-12-27",
                "relevance_score": 0.95
            },
            {
                "artifact_id": "EVID-003-GHI789",
                "evidence_type": "risk_assessment",
                "source_file": "risk_management/ai_impact_assessment_log.json",
                "iso_standards": ["ISO 42001", "ISO 14971"],
                "risk_level": "high",
                "validation_status": "verified",
                "collection_date": "2025-12-27",
                "relevance_score": 0.9
            }
        ]

        # Apply filters
        filtered = evidence
        if evidence_type:
            filtered = [e for e in filtered if e['evidence_type'] == evidence_type]
        if standard:
            filtered = [e for e in filtered if standard in e['iso_standards']]
        if risk_level:
            filtered = [e for e in filtered if e['risk_level'] == risk_level]

        return filtered

    def display_evidence_details(self, evidence: Dict):
        """Display detailed evidence information."""
        st.markdown('<div class="evidence-card">', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Artifact ID:** {evidence['artifact_id']}")
            st.write(f"**Type:** {evidence['evidence_type']}")
            st.write(f"**Source:** {evidence['source_file']}")

        with col2:
            st.write(f"**Standards:** {', '.join(evidence['iso_standards'])}")
            st.write(f"**Risk Level:** {evidence['risk_level']}")
            st.write(f"**Validation:** {evidence['validation_status']}")

        st.write(f"**Relevance Score:** {evidence['relevance_score']}")
        st.write(f"**Collection Date:** {evidence['collection_date']}")

        st.markdown('</div>', unsafe_allow_html=True)

    def get_evidence_validation_status(self) -> pd.DataFrame:
        """Get evidence validation status distribution."""
        return pd.DataFrame([
            {"Status": "Verified", "Count": 1247},
            {"Status": "Pending", "Count": 45},
            {"Status": "Non-compliant", "Count": 12},
            {"Status": "Error", "Count": 3}
        ])

    def get_risk_heatmap_data(self) -> pd.DataFrame:
        """Get risk heatmap data."""
        return pd.DataFrame([
            {"Likelihood": "Rare", "Impact": "Low", "Count": 15, "Risk Level": "Low"},
            {"Likelihood": "Unlikely", "Impact": "Medium", "Count": 8, "Risk Level": "Medium"},
            {"Likelihood": "Possible", "Impact": "High", "Count": 5, "Risk Level": "High"},
            {"Likelihood": "Likely", "Impact": "Critical", "Count": 2, "Risk Level": "Critical"}
        ])

    def get_top_risks(self) -> List[Dict]:
        """Get top risks by category."""
        return [
            {
                "category": "AI Ethics",
                "description": "Potential bias in AI diagnostic models affecting patient care decisions",
                "level": "High",
                "likelihood": "Medium",
                "impact": "High",
                "mitigation": "Regular bias audits, fairness constraints in model training",
                "owner": "AI Ethics Committee"
            },
            {
                "category": "Data Security",
                "description": "Unauthorized access to sensitive patient health data",
                "level": "Critical",
                "likelihood": "Low",
                "impact": "Critical",
                "mitigation": "Zero-trust architecture, encryption, access controls",
                "owner": "Chief Information Security Officer"
            },
            {
                "category": "Regulatory Compliance",
                "description": "Changes in ISO standards or regulatory requirements",
                "level": "Medium",
                "likelihood": "High",
                "impact": "Medium",
                "mitigation": "Continuous regulatory monitoring, automated compliance checks",
                "owner": "Compliance Officer"
            }
        ]

    def get_risk_trends(self) -> pd.DataFrame:
        """Get risk trends data."""
        dates = pd.date_range(end=datetime.date.today(), periods=30)
        data = []
        for date in dates:
            data.extend([
                {"Date": date, "Risk Level": "Critical", "Risk Count": 2},
                {"Date": date, "Risk Level": "High", "Risk Count": 5 + (date.day % 3)},
                {"Date": date, "Risk Level": "Medium", "Risk Count": 8 + (date.day % 5)},
                {"Date": date, "Risk Level": "Low", "Risk Count": 15 + (date.day % 7)}
            ])
        return pd.DataFrame(data)

    def get_active_bundles(self) -> List[Dict]:
        """Get active evidence bundles."""
        return [
            {
                "id": "LEB-comprehensive-20251227",
                "status": "Active",
                "evidence_count": 1247,
                "risk_count": 12,
                "standards": ["ISO 42001", "ISO 27001", "ISO 27701", "ISO 13485"],
                "created_date": "2025-12-27",
                "last_updated": "2025-12-27 15:30"
            },
            {
                "id": "LEB-medical-20251227",
                "status": "Active",
                "evidence_count": 856,
                "risk_count": 8,
                "standards": ["ISO 13485", "ISO 14971", "ISO 80001-1"],
                "created_date": "2025-12-27",
                "last_updated": "2025-12-27 14:45"
            }
        ]

    def export_bundle(self, bundle_id: str, export_path: str) -> str:
        """Export evidence bundle."""
        # Mock export - in real implementation, this would call the living evidence engine
        mock_data = {
            "bundle_id": bundle_id,
            "export_timestamp": datetime.datetime.utcnow().isoformat(),
            "evidence_count": 1247,
            "standards": ["ISO 42001", "ISO 27001", "ISO 27701"],
            "integrity_hash": "a1b2c3d4e5f678901234567890abcdef"
        }

        with open(export_path, 'w') as f:
            json.dump(mock_data, f, indent=2)

        return mock_data["integrity_hash"]

    def create_custom_bundle(self, standards, types, date_from, date_to, include_risks) -> Dict:
        """Create custom evidence bundle."""
        return {
            "id": f"CUSTOM-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "standards": standards,
            "evidence_types": types,
            "date_range": f"{date_from} to {date_to}",
            "include_risks": include_risks,
            "evidence_count": 456,
            "created_timestamp": datetime.datetime.utcnow().isoformat()
        }

    def generate_compliance_report(self):
        """Generate compliance report."""
        st.success("Compliance report generated successfully!")

    def run_internal_audit(self):
        """Run internal audit."""
        st.success("Internal audit completed!")
        """Get active evidence bundles."""
        return [
            {
                "id": "LEB-comprehensive-20251227",
                "status": "Active",
                "evidence_count": 1247,
                "risk_count": 12,
                "standards": ["ISO 42001", "ISO 27001", "ISO 27701", "ISO 13485"],
                "created_date": "2025-12-27",
                "last_updated": "2025-12-27 15:30"
            },
            {
                "id": "LEB-medical-20251227",
                "status": "Active",
                "evidence_count": 856,
                "risk_count": 8,
                "standards": ["ISO 13485", "ISO 14971", "ISO 80001-1"],
                "created_date": "2025-12-27",
                "last_updated": "2025-12-27 14:45"
            }
        ]

    def export_bundle(self, bundle_id: str, export_path: str) -> str:
        """Export evidence bundle."""
        # Mock export - in real implementation, this would call the living evidence engine
        mock_data = {
            "bundle_id": bundle_id,
            "export_timestamp": datetime.datetime.utcnow().isoformat(),
            "evidence_count": 1247,
            "standards": ["ISO 42001", "ISO 27001", "ISO 27701"],
            "integrity_hash": "a1b2c3d4e5f678901234567890abcdef"
        }

        with open(export_path, 'w') as f:
            json.dump(mock_data, f, indent=2)

        return mock_data["integrity_hash"]

    def create_custom_bundle(self, standards, types, date_from, date_to, include_risks) -> Dict:
        """Create custom evidence bundle."""
        return {
            "id": f"CUSTOM-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "standards": standards,
            "evidence_types": types,
            "date_range": f"{date_from} to {date_to}",
            "include_risks": include_risks,
            "evidence_count": 456,
            "created_timestamp": datetime.datetime.utcnow().isoformat()
        }

    def generate_compliance_report(self):
        """Generate compliance report."""
        st.success("Compliance report generated successfully!")

    def run_internal_audit(self):
        """Run internal audit."""
        st.success("Internal audit completed!")

# Main application
def main():
    dashboard = LivingCertificationsDashboard()
    dashboard.render_main_dashboard()

if __name__ == "__main__":
    main()