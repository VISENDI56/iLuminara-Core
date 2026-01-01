# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# COMPETITOR EXCLUSION: Commercial use by entities offering Sovereign/Health OS 
# solutions is STRICTLY PROHIBITED without a commercial license.
# 
# The Sovereign Immune System (Omni-Law) and JEPA-MPC Architecture are 
# proprietary inventions of iLuminara.
# ------------------------------------------------------------------------------

"""
iLuminara Unified DSPM (Data Security Posture Management) Dashboard
ISO 27001:2022 Continuous Security Monitoring and Consolidated Visibility

This module provides a single pane of glass for security posture management,
eliminating visibility gaps across hybrid environments through integrated
monitoring, alerting, and compliance reporting.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecuritySeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class AssetType(Enum):
    SERVER = "server"
    DATABASE = "database"
    NETWORK = "network"
    APPLICATION = "application"
    CONTAINER = "container"
    CLOUD_SERVICE = "cloud_service"
    ENDPOINT = "endpoint"
    DATA_STORE = "data_store"

@dataclass
class SecurityFinding:
    """Individual security finding with full context."""
    finding_id: str
    title: str
    description: str
    severity: SecuritySeverity
    asset_type: AssetType
    asset_name: str
    asset_location: str
    detection_time: datetime
    source_scanner: str
    cve_id: Optional[str] = None
    cvss_score: Optional[float] = None
    compliance_violation: Optional[str] = None
    remediation_steps: List[str] = None
    status: str = "open"
    assigned_to: Optional[str] = None
    resolution_eta: Optional[datetime] = None
    evidence: Dict[str, Any] = None

@dataclass
class ComplianceStatus:
    """Compliance status for various frameworks."""
    framework: str
    standard_version: str
    overall_score: float
    total_controls: int
    compliant_controls: int
    non_compliant_controls: int
    compensating_controls: int
    last_assessment: datetime
    next_assessment: datetime
    critical_findings: int

@dataclass
class SecurityMetrics:
    """Real-time security metrics dashboard."""
    total_findings: int
    critical_findings: int
    open_vulnerabilities: int
    compliance_score: float
    mean_time_to_remediate: float
    active_incidents: int
    monitored_assets: int
    scan_coverage: float

class UnifiedDSPMDashboard:
    """Unified DSPM Dashboard for consolidated security visibility."""

    def __init__(self):
        self.findings: List[SecurityFinding] = []
        self.compliance_status: Dict[str, ComplianceStatus] = {}
        self.metrics_history: List[Dict[str, Any]] = []
        self.asset_inventory: Dict[str, Dict[str, Any]] = {}
        self.scanners = {
            "cloud_security_scanner": self._scan_cloud_resources,
            "container_scanner": self._scan_containers,
            "network_scanner": self._scan_network,
            "endpoint_scanner": self._scan_endpoints,
            "data_scanner": self._scan_data_stores,
            "compliance_scanner": self._assess_compliance
        }
        self._load_initial_data()

    def _load_initial_data(self):
        """Load initial security data and compliance status."""
        # Initialize compliance status for key frameworks
        self.compliance_status = {
            "ISO27001": ComplianceStatus(
                framework="ISO/IEC 27001",
                standard_version="2022",
                overall_score=94.2,
                total_controls=93,
                compliant_controls=87,
                non_compliant_controls=4,
                compensating_controls=2,
                last_assessment=datetime.now(timezone.utc) - timedelta(days=7),
                next_assessment=datetime.now(timezone.utc) + timedelta(days=77),
                critical_findings=2
            ),
            "ISO27701": ComplianceStatus(
                framework="ISO/IEC 27701",
                standard_version="2019",
                overall_score=96.1,
                total_controls=37,
                compliant_controls=35,
                non_compliant_controls=1,
                compensating_controls=1,
                last_assessment=datetime.now(timezone.utc) - timedelta(days=5),
                next_assessment=datetime.now(timezone.utc) + timedelta(days=85),
                critical_findings=0
            ),
            "HIPAA": ComplianceStatus(
                framework="HIPAA Security Rule",
                standard_version="2013",
                overall_score=97.3,
                total_controls=45,
                compliant_controls=44,
                non_compliant_controls=1,
                compensating_controls=0,
                last_assessment=datetime.now(timezone.utc) - timedelta(days=3),
                next_assessment=datetime.now(timezone.utc) + timedelta(days=87),
                critical_findings=1
            )
        }

        # Generate sample findings
        self._generate_sample_findings()

    def _generate_sample_findings(self):
        """Generate realistic sample security findings."""
        findings_data = [
            {
                "finding_id": "DSPM-2025-001",
                "title": "Unencrypted Data at Rest in Cloud Storage",
                "description": "Patient health records stored without encryption in GCP Cloud Storage bucket",
                "severity": SecuritySeverity.CRITICAL,
                "asset_type": AssetType.CLOUD_SERVICE,
                "asset_name": "fhir-data-bucket-prod",
                "asset_location": "GCP us-central1",
                "source_scanner": "cloud_security_scanner",
                "compliance_violation": "ISO 27001 A.8.24",
                "remediation_steps": [
                    "Enable Customer-Managed Encryption Keys (CMEK)",
                    "Implement bucket-level encryption",
                    "Update data classification policy"
                ],
                "evidence": {"bucket_name": "fhir-data-bucket-prod", "encryption_status": "disabled"}
            },
            {
                "finding_id": "DSPM-2025-002",
                "title": "Privileged Access Without MFA",
                "description": "Administrative accounts accessing production databases without multi-factor authentication",
                "severity": SecuritySeverity.HIGH,
                "asset_type": AssetType.DATABASE,
                "asset_name": "postgres-prod-cluster",
                "asset_location": "AWS eu-west-1",
                "source_scanner": "database_scanner",
                "compliance_violation": "ISO 27001 A.5.15",
                "remediation_steps": [
                    "Enable MFA for all privileged accounts",
                    "Implement just-in-time access",
                    "Regular access review process"
                ]
            },
            {
                "finding_id": "DSPM-2025-003",
                "title": "Outdated SSL/TLS Configuration",
                "description": "API endpoints using deprecated TLS 1.1 protocol",
                "severity": SecuritySeverity.MEDIUM,
                "asset_type": AssetType.APPLICATION,
                "asset_name": "fhir-api-gateway",
                "asset_location": "Azure eastus2",
                "source_scanner": "network_scanner",
                "cve_id": "CVE-2018-734",
                "cvss_score": 5.3,
                "remediation_steps": [
                    "Upgrade to TLS 1.3",
                    "Disable deprecated cipher suites",
                    "Implement HSTS headers"
                ]
            }
        ]

        for finding_data in findings_data:
            finding = SecurityFinding(
                finding_id=finding_data["finding_id"],
                title=finding_data["title"],
                description=finding_data["description"],
                severity=finding_data["severity"],
                asset_type=finding_data["asset_type"],
                asset_name=finding_data["asset_name"],
                asset_location=finding_data["asset_location"],
                detection_time=datetime.now(timezone.utc) - timedelta(hours=np.random.randint(1, 24)),
                source_scanner=finding_data["source_scanner"],
                cve_id=finding_data.get("cve_id"),
                cvss_score=finding_data.get("cvss_score"),
                compliance_violation=finding_data.get("compliance_violation"),
                remediation_steps=finding_data.get("remediation_steps", []),
                evidence=finding_data.get("evidence", {})
            )
            self.findings.append(finding)

    async def run_continuous_scanning(self):
        """Run continuous security scanning across all environments."""
        while True:
            try:
                # Run all scanners concurrently
                tasks = []
                for scanner_name, scanner_func in self.scanners.items():
                    tasks.append(scanner_func())

                await asyncio.gather(*tasks)

                # Update metrics
                self._update_security_metrics()

                # Wait before next scan cycle
                await asyncio.sleep(300)  # 5 minutes

            except Exception as e:
                logger.error(f"Error in continuous scanning: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry

    def _scan_cloud_resources(self):
        """Scan cloud resources for security misconfigurations."""
        # Simulate cloud resource scanning
        logger.info("Scanning cloud resources...")
        # In real implementation, this would use AWS Config, GCP Security Command Center, etc.

    def _scan_containers(self):
        """Scan container images and runtime for vulnerabilities."""
        logger.info("Scanning containers...")
        # In real implementation, this would use Trivy, Clair, etc.

    def _scan_network(self):
        """Scan network infrastructure for security issues."""
        logger.info("Scanning network infrastructure...")
        # In real implementation, this would use Nmap, Nessus, etc.

    def _scan_endpoints(self):
        """Scan endpoints for security compliance."""
        logger.info("Scanning endpoints...")
        # In real implementation, this would use endpoint detection tools

    def _scan_data_stores(self):
        """Scan data stores for security and compliance issues."""
        logger.info("Scanning data stores...")
        # In real implementation, this would scan databases, file shares, etc.

    def _assess_compliance(self):
        """Assess compliance across all frameworks."""
        logger.info("Assessing compliance...")
        # Update compliance scores based on findings
        for framework, status in self.compliance_status.items():
            # Simulate compliance score updates
            status.overall_score = min(100.0, status.overall_score + np.random.uniform(-0.5, 0.5))
            status.last_assessment = datetime.now(timezone.utc)

    def _update_security_metrics(self):
        """Update real-time security metrics."""
        current_metrics = {
            "timestamp": datetime.now(timezone.utc),
            "total_findings": len(self.findings),
            "critical_findings": len([f for f in self.findings if f.severity == SecuritySeverity.CRITICAL]),
            "open_vulnerabilities": len([f for f in self.findings if f.status == "open"]),
            "compliance_score": np.mean([s.overall_score for s in self.compliance_status.values()]),
            "mean_time_to_remediate": np.random.uniform(24, 72),  # hours
            "active_incidents": np.random.randint(0, 3),
            "monitored_assets": 1247,
            "scan_coverage": 98.3
        }

        self.metrics_history.append(current_metrics)

        # Keep only last 1000 metrics points
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]

    def get_security_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive security dashboard data."""
        return {
            "current_metrics": self.metrics_history[-1] if self.metrics_history else {},
            "findings_summary": self._get_findings_summary(),
            "compliance_status": {k: asdict(v) for k, v in self.compliance_status.items()},
            "asset_inventory": self.asset_inventory,
            "trends": self._get_trends_data(),
            "risk_assessment": self._get_risk_assessment()
        }

    def _get_findings_summary(self) -> Dict[str, Any]:
        """Get summary of security findings."""
        severity_counts = {}
        for severity in SecuritySeverity:
            severity_counts[severity.value] = len([f for f in self.findings if f.severity == severity])

        asset_type_counts = {}
        for asset_type in AssetType:
            asset_type_counts[asset_type.value] = len([f for f in self.findings if f.asset_type == asset_type])

        return {
            "by_severity": severity_counts,
            "by_asset_type": asset_type_counts,
            "total_open": len([f for f in self.findings if f.status == "open"]),
            "recent_findings": len([f for f in self.findings if f.detection_time > datetime.now(timezone.utc) - timedelta(hours=24)])
        }

    def _get_trends_data(self) -> Dict[str, Any]:
        """Get security trends over time."""
        if len(self.metrics_history) < 2:
            return {}

        recent_metrics = self.metrics_history[-30:]  # Last 30 data points

        return {
            "compliance_trend": [m["compliance_score"] for m in recent_metrics],
            "findings_trend": [m["total_findings"] for m in recent_metrics],
            "timestamps": [m["timestamp"].isoformat() for m in recent_metrics]
        }

    def _get_risk_assessment(self) -> Dict[str, Any]:
        """Get overall risk assessment."""
        critical_findings = len([f for f in self.findings if f.severity == SecuritySeverity.CRITICAL])
        compliance_avg = np.mean([s.overall_score for s in self.compliance_status.values()])

        # Calculate risk score (simplified)
        risk_score = (critical_findings * 10) + (100 - compliance_avg)

        if risk_score < 20:
            risk_level = "Low"
            risk_color = "green"
        elif risk_score < 50:
            risk_level = "Medium"
            risk_color = "yellow"
        elif risk_score < 80:
            risk_level = "High"
            risk_color = "orange"
        else:
            risk_level = "Critical"
            risk_color = "red"

        return {
            "risk_score": round(risk_score, 1),
            "risk_level": risk_level,
            "risk_color": risk_color,
            "contributing_factors": [
                f"{critical_findings} critical findings",
                f"Compliance score: {compliance_avg:.1f}%",
                f"{len([f for f in self.findings if f.status == 'open'])} open vulnerabilities"
            ]
        }

# Global DSPM instance
dspm_dashboard = UnifiedDSPMDashboard()

def create_streamlit_dashboard():
    """Create the Streamlit DSPM dashboard."""
    st.set_page_config(
        page_title="iLuminara DSPM Dashboard",
        page_icon="🔒",
        layout="wide"
    )

    st.title("🔒 iLuminara Unified DSPM Dashboard")
    st.markdown("**Data Security Posture Management - Single Pane of Glass**")

    # Get dashboard data
    dashboard_data = dspm_dashboard.get_security_dashboard_data()

    if not dashboard_data["current_metrics"]:
        st.error("No security metrics available. Please check DSPM configuration.")
        return

    metrics = dashboard_data["current_metrics"]
    findings = dashboard_data["findings_summary"]
    compliance = dashboard_data["compliance_status"]
    risk = dashboard_data["risk_assessment"]

    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Overall Compliance",
            f"{metrics.get('compliance_score', 0):.1f}%",
            "↗️ +0.3%"
        )

    with col2:
        st.metric(
            "Critical Findings",
            metrics.get('critical_findings', 0),
            "🔴 Active"
        )

    with col3:
        st.metric(
            "Open Vulnerabilities",
            metrics.get('open_vulnerabilities', 0),
            "📋 Pending"
        )

    with col4:
        st.metric(
            "Risk Level",
            risk.get('risk_level', 'Unknown'),
            f"🎯 {risk.get('risk_score', 0)}"
        )

    # Risk Assessment
    st.subheader("🎯 Risk Assessment")
    risk_col1, risk_col2 = st.columns([1, 2])

    with risk_col1:
        # Risk score gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk.get('risk_score', 0),
            title={'text': "Security Risk Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': risk.get('risk_color', 'gray')},
                'steps': [
                    {'range': [0, 20], 'color': 'green'},
                    {'range': [20, 50], 'color': 'yellow'},
                    {'range': [50, 80], 'color': 'orange'},
                    {'range': [80, 100], 'color': 'red'}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

    with risk_col2:
        st.markdown("**Contributing Factors:**")
        for factor in risk.get('contributing_factors', []):
            st.markdown(f"• {factor}")

    # Findings Overview
    st.subheader("🔍 Security Findings Overview")

    col1, col2 = st.columns(2)

    with col1:
        # Findings by severity
        severity_data = findings.get('by_severity', {})
        fig = px.bar(
            x=list(severity_data.keys()),
            y=list(severity_data.values()),
            title="Findings by Severity",
            color=list(severity_data.keys()),
            color_discrete_map={
                'critical': 'red',
                'high': 'orange',
                'medium': 'yellow',
                'low': 'blue',
                'info': 'gray'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Findings by asset type
        asset_data = findings.get('by_asset_type', {})
        fig = px.pie(
            values=list(asset_data.values()),
            names=list(asset_data.keys()),
            title="Findings by Asset Type"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Compliance Status
    st.subheader("📋 Compliance Status")

    compliance_df = pd.DataFrame([
        {
            'Framework': status['framework'],
            'Version': status['standard_version'],
            'Score': f"{status['overall_score']:.1f}%",
            'Compliant': f"{status['compliant_controls']}/{status['total_controls']}",
            'Critical Issues': status['critical_findings']
        }
        for status in compliance.values()
    ])

    st.dataframe(compliance_df, use_container_width=True)

    # Recent Findings Table
    st.subheader("📋 Recent Critical Findings")

    recent_findings = sorted(dspm_dashboard.findings,
                           key=lambda x: x.detection_time, reverse=True)[:10]

    findings_df = pd.DataFrame([
        {
            'ID': f.finding_id,
            'Title': f.title,
            'Severity': f.severity.value.upper(),
            'Asset': f.asset_name,
            'Location': f.asset_location,
            'Detected': f.detection_time.strftime('%Y-%m-%d %H:%M'),
            'Status': f.status.title()
        }
        for f in recent_findings
    ])

    st.dataframe(findings_df, use_container_width=True)

    # Compliance Trends
    st.subheader("📈 Security Trends (Last 30 Data Points)")

    trends = dashboard_data.get('trends', {})
    if trends.get('compliance_trend'):
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Compliance trend
        fig.add_trace(
            go.Scatter(
                x=trends.get('timestamps', []),
                y=trends.get('compliance_trend', []),
                name="Compliance Score",
                line=dict(color='green')
            ),
            secondary_y=False
        )

        # Findings trend
        fig.add_trace(
            go.Scatter(
                x=trends.get('timestamps', []),
                y=trends.get('findings_trend', []),
                name="Total Findings",
                line=dict(color='red')
            ),
            secondary_y=True
        )

        fig.update_layout(title="Compliance vs Findings Trend")
        fig.update_xaxes(title="Time")
        fig.update_yaxes(title="Compliance Score (%)", secondary_y=False)
        fig.update_yaxes(title="Total Findings", secondary_y=True)

        st.plotly_chart(fig, use_container_width=True)

def start_continuous_monitoring():
    """Start the continuous monitoring thread."""
    def run_async_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(dspm_dashboard.run_continuous_scanning())

    monitoring_thread = threading.Thread(target=run_async_loop, daemon=True)
    monitoring_thread.start()
    logger.info("Continuous DSPM monitoring started")

if __name__ == "__main__":
    # Start continuous monitoring in background
    start_continuous_monitoring()

    # Create Streamlit dashboard
    create_streamlit_dashboard()