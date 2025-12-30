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
Internal Auditor Agent
Autonomous Non-Conformity Detection and Remediation System

This module implements an intelligent agent that continuously monitors
ISO compliance, detects non-conformities, and triggers automated remediation.
"""

import asyncio
import json
import datetime
import hashlib
import uuid
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import re
from pathlib import Path
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuditSeverity(Enum):
    """Audit finding severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class AuditStatus(Enum):
    """Audit status states."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class RemediationStatus(Enum):
    """Remediation status states."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    DEFERRED = "deferred"

@dataclass
class AuditFinding:
    """Represents an audit finding."""
    finding_id: str
    title: str
    description: str
    severity: AuditSeverity
    category: str
    iso_standard: str
    evidence_location: str
    detection_timestamp: datetime.datetime
    remediation_deadline: Optional[datetime.datetime]
    remediation_status: RemediationStatus
    remediation_actions: List[str]
    risk_impact: str
    compliance_impact: str
    assigned_owner: Optional[str]
    verification_status: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['severity'] = self.severity.value
        data['remediation_status'] = self.remediation_status.value
        data['detection_timestamp'] = self.detection_timestamp.isoformat()
        if self.remediation_deadline:
            data['remediation_deadline'] = self.remediation_deadline.isoformat()
        return data

@dataclass
class AuditReport:
    """Represents a complete audit report."""
    audit_id: str
    audit_type: str
    scope: List[str]
    start_timestamp: datetime.datetime
    end_timestamp: Optional[datetime.datetime]
    status: AuditStatus
    compliance_score: float
    findings_count: int
    findings: List[AuditFinding]
    recommendations: List[str]
    next_audit_date: Optional[datetime.datetime]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['status'] = self.status.value
        data['start_timestamp'] = self.start_timestamp.isoformat()
        if self.end_timestamp:
            data['end_timestamp'] = self.end_timestamp.isoformat()
        if self.next_audit_date:
            data['next_audit_date'] = self.next_audit_date.isoformat()
        data['findings'] = [finding.to_dict() for finding in self.findings]
        return data

class InternalAuditorAgent:
    """
    Autonomous internal auditor that continuously monitors compliance
    and triggers remediation for non-conformities.
    """

    def __init__(self, repository_root: Path):
        self.repository_root = repository_root
        self.audit_reports_dir = repository_root / "certification" / "audit_reports"
        self.audit_reports_dir.mkdir(exist_ok=True)

        self.findings_db: Dict[str, AuditFinding] = {}
        self.active_audits: Dict[str, AuditReport] = {}

        # Compliance rules database
        self.compliance_rules = self._load_compliance_rules()

        # Audit schedule
        self.audit_schedule = {
            "daily": ["evidence_integrity", "access_controls"],
            "weekly": ["iso_27001_compliance", "iso_42001_compliance"],
            "monthly": ["full_compliance_audit", "risk_assessment_review"],
            "quarterly": ["iso_13485_validation", "iso_14971_review"]
        }

        # Start background monitoring
        self.monitoring_active = False
        self.monitoring_thread = None

    def _load_compliance_rules(self) -> Dict[str, Dict]:
        """Load compliance rules for automated checking."""
        return {
            "evidence_integrity": {
                "description": "Verify evidence artifact integrity",
                "check_function": self._check_evidence_integrity,
                "frequency": "daily",
                "severity": AuditSeverity.HIGH
            },
            "access_controls": {
                "description": "Verify access control implementation",
                "check_function": self._check_access_controls,
                "frequency": "daily",
                "severity": AuditSeverity.CRITICAL
            },
            "iso_27001_compliance": {
                "description": "Check ISO 27001 control implementation",
                "check_function": self._check_iso_27001_compliance,
                "frequency": "weekly",
                "severity": AuditSeverity.HIGH
            },
            "iso_42001_compliance": {
                "description": "Check ISO 42001 AI ethics compliance",
                "check_function": self._check_iso_42001_compliance,
                "frequency": "weekly",
                "severity": AuditSeverity.HIGH
            },
            "iso_13485_validation": {
                "description": "Validate ISO 13485 medical device compliance",
                "check_function": self._check_iso_13485_compliance,
                "frequency": "monthly",
                "severity": AuditSeverity.CRITICAL
            },
            "iso_14971_review": {
                "description": "Review ISO 14971 risk management",
                "check_function": self._check_iso_14971_compliance,
                "frequency": "monthly",
                "severity": AuditSeverity.HIGH
            },
            "full_compliance_audit": {
                "description": "Comprehensive compliance audit",
                "check_function": self._run_full_compliance_audit,
                "frequency": "monthly",
                "severity": AuditSeverity.CRITICAL
            }
        }

    async def start_monitoring(self):
        """Start continuous compliance monitoring."""
        self.monitoring_active = True
        logger.info("Starting Internal Auditor Agent monitoring...")

        # Start background monitoring thread
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

    def stop_monitoring(self):
        """Stop continuous monitoring."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
        logger.info("Internal Auditor Agent monitoring stopped.")

    def _monitoring_loop(self):
        """Background monitoring loop."""
        while self.monitoring_active:
            try:
                # Run scheduled audits
                current_time = datetime.datetime.now()

                # Daily checks at 6 AM
                if current_time.hour == 6 and current_time.minute < 5:
                    asyncio.run(self._run_scheduled_audit("daily"))

                # Weekly checks on Monday at 7 AM
                elif (current_time.weekday() == 0 and current_time.hour == 7
                      and current_time.minute < 5):
                    asyncio.run(self._run_scheduled_audit("weekly"))

                # Monthly checks on 1st at 8 AM
                elif (current_time.day == 1 and current_time.hour == 8
                      and current_time.minute < 5):
                    asyncio.run(self._run_scheduled_audit("monthly"))

                # Quarterly checks on 1st of Jan/Apr/Jul/Oct at 9 AM
                elif (current_time.day == 1 and current_time.month in [1, 4, 7, 10]
                      and current_time.hour == 9 and current_time.minute < 5):
                    asyncio.run(self._run_scheduled_audit("quarterly"))

                # Continuous monitoring every 5 minutes
                asyncio.run(self._run_continuous_monitoring())

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")

            time.sleep(300)  # Sleep for 5 minutes

    async def _run_scheduled_audit(self, frequency: str):
        """Run scheduled audit for given frequency."""
        if frequency not in self.audit_schedule:
            return

        audit_id = f"scheduled-{frequency}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        logger.info(f"Running scheduled {frequency} audit: {audit_id}")

        audit_report = await self.run_audit(
            audit_type=f"Scheduled {frequency.capitalize()} Audit",
            scope=self.audit_schedule[frequency],
            audit_id=audit_id
        )

        # Save audit report
        self._save_audit_report(audit_report)

        # Trigger remediation for critical findings
        await self._trigger_remediation(audit_report)

    async def _run_continuous_monitoring(self):
        """Run continuous compliance monitoring."""
        # Check for new evidence files
        await self._check_new_evidence()

        # Monitor system health
        await self._check_system_health()

        # Check for configuration changes
        await self._check_configuration_changes()

    async def run_audit(self, audit_type: str, scope: List[str], audit_id: Optional[str] = None) -> AuditReport:
        """Run a comprehensive audit."""
        if not audit_id:
            audit_id = f"audit-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

        logger.info(f"Starting audit: {audit_id} - {audit_type}")

        audit_report = AuditReport(
            audit_id=audit_id,
            audit_type=audit_type,
            scope=scope,
            start_timestamp=datetime.datetime.now(),
            end_timestamp=None,
            status=AuditStatus.IN_PROGRESS,
            compliance_score=0.0,
            findings_count=0,
            findings=[],
            recommendations=[],
            next_audit_date=None
        )

        self.active_audits[audit_id] = audit_report

        findings = []

        # Run checks for each scope item
        for check_name in scope:
            if check_name in self.compliance_rules:
                rule = self.compliance_rules[check_name]
                try:
                    check_findings = await rule["check_function"]()
                    findings.extend(check_findings)
                    logger.info(f"Completed check: {check_name} - {len(check_findings)} findings")
                except Exception as e:
                    logger.error(f"Error running check {check_name}: {e}")
                    # Create error finding
                    error_finding = AuditFinding(
                        finding_id=f"ERROR-{uuid.uuid4().hex[:8]}",
                        title=f"Check Execution Error: {check_name}",
                        description=f"Failed to execute compliance check: {str(e)}",
                        severity=AuditSeverity.HIGH,
                        category="System Error",
                        iso_standard="N/A",
                        evidence_location="internal_auditor_agent.py",
                        detection_timestamp=datetime.datetime.now(),
                        remediation_deadline=datetime.datetime.now() + datetime.timedelta(days=1),
                        remediation_status=RemediationStatus.NOT_STARTED,
                        remediation_actions=["Investigate error", "Fix check implementation"],
                        risk_impact="Audit reliability compromised",
                        compliance_impact="Unable to verify compliance",
                        assigned_owner="System Administrator",
                        verification_status="pending"
                    )
                    findings.append(error_finding)

        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(findings)

        # Generate recommendations
        recommendations = self._generate_recommendations(findings)

        # Complete audit
        audit_report.end_timestamp = datetime.datetime.now()
        audit_report.status = AuditStatus.COMPLETED
        audit_report.compliance_score = compliance_score
        audit_report.findings_count = len(findings)
        audit_report.findings = findings
        audit_report.recommendations = recommendations
        audit_report.next_audit_date = datetime.datetime.now() + datetime.timedelta(days=30)

        logger.info(f"Audit completed: {audit_id} - Score: {compliance_score:.1f}% - Findings: {len(findings)}")

        return audit_report

    async def _check_evidence_integrity(self) -> List[AuditFinding]:
        """Check evidence artifact integrity."""
        findings = []

        # Check for evidence files
        evidence_dir = self.repository_root / "certification"
        if not evidence_dir.exists():
            findings.append(AuditFinding(
                finding_id=f"INT-{uuid.uuid4().hex[:8]}",
                title="Evidence Directory Missing",
                description="Certification evidence directory does not exist",
                severity=AuditSeverity.CRITICAL,
                category="Evidence Integrity",
                iso_standard="ISO 27001",
                evidence_location="certification/",
                detection_timestamp=datetime.datetime.now(),
                remediation_deadline=datetime.datetime.now() + datetime.timedelta(hours=4),
                remediation_status=RemediationStatus.NOT_STARTED,
                remediation_actions=["Create certification directory", "Initialize evidence collection"],
                risk_impact="Complete loss of compliance evidence",
                compliance_impact="Unable to demonstrate compliance",
                assigned_owner="Compliance Officer",
                verification_status="pending"
            ))
            return findings

        # Check for required evidence files
        required_files = [
            "AI_Ethics_Policy.md",
            "SoA.csv",
            "PIA_template.md",
            "Risk_Treatment_Plan.md",
            "living_evidence.py",
            "standard_extensions.py"
        ]

        for filename in required_files:
            file_path = evidence_dir / filename
            if not file_path.exists():
                findings.append(AuditFinding(
                    finding_id=f"INT-{uuid.uuid4().hex[:8]}",
                    title=f"Required Evidence Missing: {filename}",
                    description=f"Critical compliance evidence file is missing: {filename}",
                    severity=AuditSeverity.HIGH,
                    category="Evidence Integrity",
                    iso_standard="Multiple",
                    evidence_location=str(file_path),
                    detection_timestamp=datetime.datetime.now(),
                    remediation_deadline=datetime.datetime.now() + datetime.timedelta(days=1),
                    remediation_status=RemediationStatus.NOT_STARTED,
                    remediation_actions=[f"Create or restore {filename}", "Verify file integrity"],
                    risk_impact="Compliance gap in evidence collection",
                    compliance_impact="Incomplete audit trail",
                    assigned_owner="Compliance Officer",
                    verification_status="pending"
                ))

        return findings

    async def _check_access_controls(self) -> List[AuditFinding]:
        """Check access control implementation."""
        findings = []

        # Check for access control files
        access_files = [
            "security.txt",
            "SECURITY.md"
        ]

        for filename in access_files:
            file_path = self.repository_root / filename
            if not file_path.exists():
                findings.append(AuditFinding(
                    finding_id=f"ACC-{uuid.uuid4().hex[:8]}",
                    title=f"Access Control Documentation Missing: {filename}",
                    description=f"Access control documentation is missing: {filename}",
                    severity=AuditSeverity.MEDIUM,
                    category="Access Controls",
                    iso_standard="ISO 27001",
                    evidence_location=str(file_path),
                    detection_timestamp=datetime.datetime.now(),
                    remediation_deadline=datetime.datetime.now() + datetime.timedelta(days=7),
                    remediation_status=RemediationStatus.NOT_STARTED,
                    remediation_actions=[f"Create {filename}", "Document access control procedures"],
                    risk_impact="Potential unauthorized access",
                    compliance_impact="Incomplete security controls",
                    assigned_owner="Security Officer",
                    verification_status="pending"
                ))

        return findings

    async def _check_iso_27001_compliance(self) -> List[AuditFinding]:
        """Check ISO 27001 compliance."""
        findings = []

        # Check SoA file
        soa_file = self.repository_root / "certification" / "SoA.csv"
        if soa_file.exists():
            try:
                with open(soa_file, 'r') as f:
                    lines = f.readlines()
                    if len(lines) < 95:  # Should have 93 controls + header
                        findings.append(AuditFinding(
                            finding_id=f"27001-{uuid.uuid4().hex[:8]}",
                            title="Incomplete ISO 27001 Statement of Applicability",
                            description=f"SoA file has {len(lines)} lines, expected ~94 for complete Annex A coverage",
                            severity=AuditSeverity.HIGH,
                            category="ISO 27001 Compliance",
                            iso_standard="ISO 27001",
                            evidence_location=str(soa_file),
                            detection_timestamp=datetime.datetime.now(),
                            remediation_deadline=datetime.datetime.now() + datetime.timedelta(days=14),
                            remediation_status=RemediationStatus.NOT_STARTED,
                            remediation_actions=["Complete SoA mapping", "Verify all 93 Annex A controls"],
                            risk_impact="Incomplete ISMS coverage",
                            compliance_impact="Partial ISO 27001 compliance",
                            assigned_owner="Compliance Officer",
                            verification_status="pending"
                        ))
            except Exception as e:
                findings.append(AuditFinding(
                    finding_id=f"27001-{uuid.uuid4().hex[:8]}",
                    title="SoA File Read Error",
                    description=f"Unable to read SoA file: {str(e)}",
                    severity=AuditSeverity.MEDIUM,
                    category="ISO 27001 Compliance",
                    iso_standard="ISO 27001",
                    evidence_location=str(soa_file),
                    detection_timestamp=datetime.datetime.now(),
                    remediation_deadline=datetime.datetime.now() + datetime.timedelta(days=3),
                    remediation_status=RemediationStatus.NOT_STARTED,
                    remediation_actions=["Fix file permissions", "Verify file integrity"],
                    risk_impact="Unable to verify ISMS compliance",
                    compliance_impact="Audit evidence unavailable",
                    assigned_owner="System Administrator",
                    verification_status="pending"
                ))

        return findings

    async def _check_iso_42001_compliance(self) -> List[AuditFinding]:
        """Check ISO 42001 AI ethics compliance."""
        findings = []

        # Check AI ethics policy
        ethics_file = self.repository_root / "certification" / "AI_Ethics_Policy.md"
        if ethics_file.exists():
            try:
                with open(ethics_file, 'r') as f:
                    content = f.read().lower()

                    required_sections = [
                        "ethical principles",
                        "governance structure",
                        "risk management",
                        "transparency",
                        "accountability"
                    ]

                    missing_sections = []
                    for section in required_sections:
                        if section not in content:
                            missing_sections.append(section)

                    if missing_sections:
                        findings.append(AuditFinding(
                            finding_id=f"42001-{uuid.uuid4().hex[:8]}",
                            title="Incomplete AI Ethics Policy",
                            description=f"AI Ethics Policy missing sections: {', '.join(missing_sections)}",
                            severity=AuditSeverity.MEDIUM,
                            category="AI Ethics Compliance",
                            iso_standard="ISO 42001",
                            evidence_location=str(ethics_file),
                            detection_timestamp=datetime.datetime.now(),
                            remediation_deadline=datetime.datetime.now() + datetime.timedelta(days=7),
                            remediation_status=RemediationStatus.NOT_STARTED,
                            remediation_actions=[f"Add {section} section" for section in missing_sections],
                            risk_impact="Incomplete AI governance",
                            compliance_impact="Partial ISO 42001 compliance",
                            assigned_owner="AI Ethics Committee",
                            verification_status="pending"
                        ))

            except Exception as e:
                findings.append(AuditFinding(
                    finding_id=f"42001-{uuid.uuid4().hex[:8]}",
                    title="AI Ethics Policy Read Error",
                    description=f"Unable to read AI Ethics Policy: {str(e)}",
                    severity=AuditSeverity.MEDIUM,
                    category="AI Ethics Compliance",
                    iso_standard="ISO 42001",
                    evidence_location=str(ethics_file),
                    detection_timestamp=datetime.datetime.now(),
                    remediation_deadline=datetime.datetime.now() + datetime.timedelta(days=3),
                    remediation_status=RemediationStatus.NOT_STARTED,
                    remediation_actions=["Fix file permissions", "Verify file integrity"],
                    risk_impact="Unable to verify AI ethics compliance",
                    compliance_impact="Audit evidence unavailable",
                    assigned_owner="System Administrator",
                    verification_status="pending"
                ))

        return findings

    async def _check_iso_13485_compliance(self) -> List[AuditFinding]:
        """Check ISO 13485 medical device compliance."""
        findings = []

        # Check for medical device specific files
        medical_files = [
            "fhir_bundle.json",
            "simulated_outbreak.json"
        ]

        for filename in medical_files:
            file_path = self.repository_root / filename
            if not file_path.exists():
                findings.append(AuditFinding(
                    finding_id=f"13485-{uuid.uuid4().hex[:8]}",
                    title=f"Medical Device Evidence Missing: {filename}",
                    description=f"Required medical device compliance evidence missing: {filename}",
                    severity=AuditSeverity.HIGH,
                    category="Medical Device Compliance",
                    iso_standard="ISO 13485",
                    evidence_location=str(file_path),
                    detection_timestamp=datetime.datetime.now(),
                    remediation_deadline=datetime.datetime.now() + datetime.timedelta(days=14),
                    remediation_status=RemediationStatus.NOT_STARTED,
                    remediation_actions=[f"Create {filename}", "Validate medical device processes"],
                    risk_impact="Patient safety compliance gap",
                    compliance_impact="Incomplete medical device certification",
                    assigned_owner="Quality Manager",
                    verification_status="pending"
                ))

        return findings

    async def _check_iso_14971_compliance(self) -> List[AuditFinding]:
        """Check ISO 14971 risk management compliance."""
        findings = []

        # Check risk treatment plan
        risk_file = self.repository_root / "certification" / "Risk_Treatment_Plan.md"
        if risk_file.exists():
            try:
                with open(risk_file, 'r') as f:
                    content = f.read().lower()

                    if "residual risk" not in content:
                        findings.append(AuditFinding(
                            finding_id=f"14971-{uuid.uuid4().hex[:8]}",
                            title="Missing Residual Risk Analysis",
                            description="Risk Treatment Plan does not address residual risk management",
                            severity=AuditSeverity.MEDIUM,
                            category="Risk Management",
                            iso_standard="ISO 14971",
                            evidence_location=str(risk_file),
                            detection_timestamp=datetime.datetime.now(),
                            remediation_deadline=datetime.datetime.now() + datetime.timedelta(days=7),
                            remediation_status=RemediationStatus.NOT_STARTED,
                            remediation_actions=["Add residual risk analysis", "Document risk acceptance criteria"],
                            risk_impact="Incomplete risk management",
                            compliance_impact="Partial ISO 14971 compliance",
                            assigned_owner="Risk Manager",
                            verification_status="pending"
                        ))

            except Exception as e:
                findings.append(AuditFinding(
                    finding_id=f"14971-{uuid.uuid4().hex[:8]}",
                    title="Risk Treatment Plan Read Error",
                    description=f"Unable to read Risk Treatment Plan: {str(e)}",
                    severity=AuditSeverity.MEDIUM,
                    category="Risk Management",
                    iso_standard="ISO 14971",
                    evidence_location=str(risk_file),
                    detection_timestamp=datetime.datetime.now(),
                    remediation_deadline=datetime.datetime.now() + datetime.timedelta(days=3),
                    remediation_status=RemediationStatus.NOT_STARTED,
                    remediation_actions=["Fix file permissions", "Verify file integrity"],
                    risk_impact="Unable to verify risk management compliance",
                    compliance_impact="Audit evidence unavailable",
                    assigned_owner="System Administrator",
                    verification_status="pending"
                ))

        return findings

    async def _run_full_compliance_audit(self) -> List[AuditFinding]:
        """Run comprehensive compliance audit."""
        findings = []

        # Combine findings from all checks
        all_checks = [
            self._check_evidence_integrity(),
            self._check_access_controls(),
            self._check_iso_27001_compliance(),
            self._check_iso_42001_compliance(),
            self._check_iso_13485_compliance(),
            self._check_iso_14971_compliance()
        ]

        for check_coro in all_checks:
            check_findings = await check_coro
            findings.extend(check_findings)

        return findings

    async def _check_new_evidence(self):
        """Check for new evidence files."""
        # This would monitor for new evidence collection
        pass

    async def _check_system_health(self):
        """Check system health indicators."""
        # This would monitor system performance and health
        pass

    async def _check_configuration_changes(self):
        """Check for configuration changes that might affect compliance."""
        # This would monitor configuration files for changes
        pass

    def _calculate_compliance_score(self, findings: List[AuditFinding]) -> float:
        """Calculate compliance score based on findings."""
        if not findings:
            return 100.0

        # Weight findings by severity
        severity_weights = {
            AuditSeverity.CRITICAL: 10,
            AuditSeverity.HIGH: 5,
            AuditSeverity.MEDIUM: 2,
            AuditSeverity.LOW: 1,
            AuditSeverity.INFO: 0.5
        }

        total_weight = len(findings) * 10  # Assume max weight per finding
        actual_weight = sum(severity_weights[finding.severity] for finding in findings)

        score = max(0, 100 - (actual_weight / total_weight * 100))
        return round(score, 1)

    def _generate_recommendations(self, findings: List[AuditFinding]) -> List[str]:
        """Generate recommendations based on findings."""
        recommendations = []

        # Group findings by category
        categories = {}
        for finding in findings:
            if finding.category not in categories:
                categories[finding.category] = []
            categories[finding.category].append(finding)

        # Generate category-specific recommendations
        for category, category_findings in categories.items():
            if category == "Evidence Integrity":
                recommendations.append("Implement automated evidence integrity monitoring")
            elif category == "Access Controls":
                recommendations.append("Strengthen access control documentation and procedures")
            elif category == "ISO 27001 Compliance":
                recommendations.append("Complete ISMS implementation and SoA documentation")
            elif category == "AI Ethics Compliance":
                recommendations.append("Enhance AI ethics governance framework")
            elif category == "Medical Device Compliance":
                recommendations.append("Implement comprehensive medical device QMS")
            elif category == "Risk Management":
                recommendations.append("Strengthen risk management processes and documentation")

        # Add general recommendations
        if len(findings) > 10:
            recommendations.append("Implement corrective action tracking system")
        if any(f.severity == AuditSeverity.CRITICAL for f in findings):
            recommendations.append("Immediate attention required for critical findings")

        return recommendations

    async def _trigger_remediation(self, audit_report: AuditReport):
        """Trigger remediation for critical findings."""
        critical_findings = [f for f in audit_report.findings if f.severity == AuditSeverity.CRITICAL]

        for finding in critical_findings:
            logger.info(f"Triggering remediation for critical finding: {finding.finding_id}")
            # In a real implementation, this would trigger automated remediation workflows
            # For now, just log the finding
            self.findings_db[finding.finding_id] = finding

    def _save_audit_report(self, audit_report: AuditReport):
        """Save audit report to file."""
        report_file = self.audit_reports_dir / f"audit_report_{audit_report.audit_id}.json"

        with open(report_file, 'w') as f:
            json.dump(audit_report.to_dict(), f, indent=2)

        logger.info(f"Audit report saved: {report_file}")

    def get_audit_history(self) -> List[Dict]:
        """Get audit history."""
        audit_files = list(self.audit_reports_dir.glob("audit_report_*.json"))
        audit_history = []

        for audit_file in audit_files:
            try:
                with open(audit_file, 'r') as f:
                    audit_data = json.load(f)
                    audit_history.append(audit_data)
            except Exception as e:
                logger.error(f"Error reading audit file {audit_file}: {e}")

        # Sort by start timestamp, most recent first
        audit_history.sort(key=lambda x: x.get('start_timestamp', ''), reverse=True)
        return audit_history

    def get_active_findings(self) -> List[AuditFinding]:
        """Get active findings that need remediation."""
        active_findings = []

        for finding_id, finding in self.findings_db.items():
            if finding.remediation_status in [RemediationStatus.NOT_STARTED, RemediationStatus.IN_PROGRESS]:
                active_findings.append(finding)

        return active_findings

    async def run_manual_audit(self, audit_type: str, scope: List[str]) -> str:
        """Run a manual audit and return the audit ID."""
        audit_report = await self.run_audit(audit_type, scope)
        self._save_audit_report(audit_report)
        await self._trigger_remediation(audit_report)
        return audit_report.audit_id

# Global auditor instance
_auditor_instance = None

def get_internal_auditor(repository_root: Path = None) -> InternalAuditorAgent:
    """Get the global internal auditor instance."""
    global _auditor_instance

    if _auditor_instance is None:
        if repository_root is None:
            repository_root = Path("/workspaces/iLuminara-Core")
        _auditor_instance = InternalAuditorAgent(repository_root)

    return _auditor_instance

# Convenience functions for external use
async def start_auditor_monitoring():
    """Start the internal auditor monitoring."""
    auditor = get_internal_auditor()
    await auditor.start_monitoring()

def stop_auditor_monitoring():
    """Stop the internal auditor monitoring."""
    auditor = get_internal_auditor()
    auditor.stop_monitoring()

async def run_compliance_audit(audit_type: str = "Manual Compliance Audit",
                              scope: List[str] = None) -> str:
    """Run a compliance audit."""
    if scope is None:
        scope = ["evidence_integrity", "iso_27001_compliance", "iso_42001_compliance"]

    auditor = get_internal_auditor()
    return await auditor.run_manual_audit(audit_type, scope)

def get_audit_history() -> List[Dict]:
    """Get audit history."""
    auditor = get_internal_auditor()
    return auditor.get_audit_history()

def get_active_findings() -> List[AuditFinding]:
    """Get active findings."""
    auditor = get_internal_auditor()
    return auditor.get_active_findings()

if __name__ == "__main__":
    # Example usage
    async def main():
        auditor = get_internal_auditor()

        # Start monitoring
        await start_auditor_monitoring()

        # Run a manual audit
        audit_id = await run_compliance_audit()
        print(f"Manual audit completed: {audit_id}")

        # Get audit history
        history = get_audit_history()
        print(f"Total audits: {len(history)}")

        # Get active findings
        findings = get_active_findings()
        print(f"Active findings: {len(findings)}")

        # Stop monitoring
        stop_auditor_monitoring()

    asyncio.run(main())