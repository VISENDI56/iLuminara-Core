"""
Living Evidence Engine
Autonomous Evidence Collection and Audit Package Generation

This module implements the Living Evidence Engine that continuously collects,
validates, and packages evidence for ISO certification audits. It automatically
generates audit-ready packages with cryptographic integrity verification.
"""

import json
import os
import hashlib
import datetime
import uuid
import asyncio
import threading
import time
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
import glob
import re
from pathlib import Path
import pandas as pd
import numpy as np

# Import iLuminara compliance modules
try:
    from risk_management.ai_impact_assessment_log import json as ai_impact_data
    from privacy.controller_processor_matrix import json as controller_processor_data
    from training_pipeline.data_quality_report import generate_audit_bundle_report
    from governance_kernel.national_strategy_guard import NationalStrategyGuard
except ImportError:
    # Fallback for development
    ai_impact_data = {}
    controller_processor_data = {}
    NationalStrategyGuard = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EvidenceType(Enum):
    """Types of evidence collected for living bundles."""
    SYSTEM_LOG = "system_log"
    SECURITY_EVENT = "security_event"
    COMPLIANCE_CHECK = "compliance_check"
    CODE_REVIEW = "code_review"
    CONFIGURATION = "configuration"
    TEST_RESULT = "test_result"
    AUDIT_TRAIL = "audit_trail"
    POLICY_DOCUMENT = "policy_document"
    TRAINING_RECORD = "training_record"
    INCIDENT_REPORT = "incident_report"
    RISK_ASSESSMENT = "risk_assessment"
    PERFORMANCE_METRIC = "performance_metric"
    VALIDATION_REPORT = "validation_report"

class RiskLevel(Enum):
    """Risk severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    ACCEPTABLE = "acceptable"

@dataclass
class EvidenceArtifact:
    """Individual evidence artifact with metadata."""
    artifact_id: str
    evidence_type: EvidenceType
    source_file: str
    collection_timestamp: datetime.datetime
    content_hash: str
    content_summary: str
    relevance_score: float
    iso_standards: List[str]
    retention_period_days: int
    classification: str
    validation_status: str = "pending"
    risk_level: RiskLevel = RiskLevel.MEDIUM
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LivingEvidenceBundle:
    """Dynamic audit bundle that continuously updates."""
    bundle_id: str
    bundle_version: str
    creation_timestamp: datetime.datetime
    target_standards: List[str]
    status: str
    evidence_artifacts: List[EvidenceArtifact] = field(default_factory=list)
    compliance_summary: Dict[str, Any] = field(default_factory=dict)
    integrity_hash: Optional[str] = None
    blockchain_anchor: Optional[str] = None
    risk_summary: Dict[str, Any] = field(default_factory=dict)
    validation_results: Dict[str, Any] = field(default_factory=dict)
    last_updated: datetime.datetime = field(default_factory=datetime.datetime.utcnow)

@dataclass
class ResidualRisk:
    """Represents a residual risk after treatment."""
    risk_id: str
    description: str
    category: str
    initial_likelihood: RiskLevel
    initial_impact: RiskLevel
    residual_likelihood: RiskLevel
    residual_impact: RiskLevel
    treatment_measures: List[str]
    monitoring_frequency: str
    acceptance_rationale: Optional[str] = None
    last_assessed: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    next_review: datetime.datetime = field(default_factory=lambda: datetime.datetime.utcnow() + datetime.timedelta(days=90))

class LivingEvidenceEngine:
    """Autonomous evidence collection and risk resolution engine."""

    def __init__(self, repository_root: str = "/workspaces/iLuminara-Core"):
        self.repository_root = Path(repository_root)
        self.evidence_patterns = self._initialize_evidence_patterns()
        self.active_bundles: Dict[str, LivingEvidenceBundle] = {}
        self.residual_risks: List[ResidualRisk] = []
        self.evidence_cache: Dict[str, EvidenceArtifact] = {}
        self.collection_active = False
        self.national_guard = NationalStrategyGuard() if NationalStrategyGuard else None

    def _initialize_evidence_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive evidence collection patterns."""

        return {
            # ISO 42001 AI Management evidence
            "ai_impact_assessments": {
                "pattern": "**/risk_management/ai_impact_assessment_log.json",
                "evidence_type": EvidenceType.RISK_ASSESSMENT,
                "iso_standards": ["ISO 42001"],
                "relevance_score": 1.0,
                "retention_period_days": 2555,
                "risk_category": "AI Ethics"
            },
            "data_quality_reports": {
                "pattern": "**/training_pipeline/data_quality_report.py",
                "evidence_type": EvidenceType.VALIDATION_REPORT,
                "iso_standards": ["ISO 42001"],
                "relevance_score": 0.95,
                "retention_period_days": 2555,
                "risk_category": "AI Bias"
            },
            "aims_policy": {
                "pattern": "**/governance/aims_policy.md",
                "evidence_type": EvidenceType.POLICY_DOCUMENT,
                "iso_standards": ["ISO 42001"],
                "relevance_score": 1.0,
                "retention_period_days": 2555,
                "risk_category": "AI Governance"
            },

            # ISO 27001 Information Security evidence
            "isms_handbook": {
                "pattern": "**/governance/isms_handbook.md",
                "evidence_type": EvidenceType.POLICY_DOCUMENT,
                "iso_standards": ["ISO 27001"],
                "relevance_score": 1.0,
                "retention_period_days": 2555,
                "risk_category": "Security Governance"
            },
            "statement_of_applicability": {
                "pattern": "**/compliance/statement_of_applicability.csv",
                "evidence_type": EvidenceType.COMPLIANCE_CHECK,
                "iso_standards": ["ISO 27001"],
                "relevance_score": 0.95,
                "retention_period_days": 2555,
                "risk_category": "Security Controls"
            },
            "dspm_dashboard": {
                "pattern": "**/infrastructure/dspm/unified_dashboard.py",
                "evidence_type": EvidenceType.SECURITY_EVENT,
                "iso_standards": ["ISO 27001"],
                "relevance_score": 0.90,
                "retention_period_days": 1825,
                "risk_category": "Security Monitoring"
            },

            # ISO 27701 Privacy Management evidence
            "controller_processor_matrix": {
                "pattern": "**/privacy/controller_processor_matrix.json",
                "evidence_type": EvidenceType.POLICY_DOCUMENT,
                "iso_standards": ["ISO 27701"],
                "relevance_score": 0.95,
                "retention_period_days": 2555,
                "risk_category": "Privacy Governance"
            },
            "privacy_impact_assessments": {
                "pattern": "**/privacy/impact_assessment_template.md",
                "evidence_type": EvidenceType.COMPLIANCE_CHECK,
                "iso_standards": ["ISO 27701"],
                "relevance_score": 0.90,
                "retention_period_days": 2555,
                "risk_category": "Privacy Assessment"
            },
            "national_strategy_guard": {
                "pattern": "**/governance_kernel/national_strategy_guard.py",
                "evidence_type": EvidenceType.AUDIT_TRAIL,
                "iso_standards": ["ISO 27701"],
                "relevance_score": 0.85,
                "retention_period_days": 2555,
                "risk_category": "Data Residency"
            },

            # System and operational evidence
            "system_logs": {
                "pattern": "**/logs/*.log",
                "evidence_type": EvidenceType.SYSTEM_LOG,
                "iso_standards": ["ISO 27001", "ISO 27701"],
                "relevance_score": 0.70,
                "retention_period_days": 2555,
                "risk_category": "Operational Security"
            },
            "audit_trails": {
                "pattern": "**/*audit*.json",
                "evidence_type": EvidenceType.AUDIT_TRAIL,
                "iso_standards": ["ISO 27001", "ISO 27701", "ISO 42001"],
                "relevance_score": 0.80,
                "retention_period_days": 2555,
                "risk_category": "Audit Compliance"
            },
            "test_results": {
                "pattern": "**/test_results/*.json",
                "evidence_type": EvidenceType.TEST_RESULT,
                "iso_standards": ["ISO 42001", "ISO 27001"],
                "relevance_score": 0.75,
                "retention_period_days": 1825,
                "risk_category": "System Validation"
            },
            "performance_metrics": {
                "pattern": "**/metrics/*.json",
                "evidence_type": EvidenceType.PERFORMANCE_METRIC,
                "iso_standards": ["ISO 42001", "ISO 27001"],
                "relevance_score": 0.65,
                "retention_period_days": 1825,
                "risk_category": "System Performance"
            },

            # Risk and compliance evidence
            "risk_assessments": {
                "pattern": "**/risk_management/*.json",
                "evidence_type": EvidenceType.RISK_ASSESSMENT,
                "iso_standards": ["ISO 42001", "ISO 27001", "ISO 27701"],
                "relevance_score": 0.85,
                "retention_period_days": 2555,
                "risk_category": "Risk Management"
            },
            "incident_reports": {
                "pattern": "**/*incident*.json",
                "evidence_type": EvidenceType.INCIDENT_REPORT,
                "iso_standards": ["ISO 27001", "ISO 27701"],
                "relevance_score": 0.90,
                "retention_period_days": 2555,
                "risk_category": "Incident Management"
            }
        }

    async def start_living_collection(self):
        """Start continuous evidence collection and risk resolution."""
        self.collection_active = True
        logger.info("Starting Living Evidence Collection...")

        while self.collection_active:
            try:
                # Collect new evidence
                await self._collect_evidence_artifacts()

                # Update living bundles
                await self._update_living_bundles()

                # Resolve residual risks
                await self._resolve_residual_risks()

                # Validate evidence integrity
                await self._validate_evidence_integrity()

                # Generate compliance reports
                await self._generate_compliance_reports()

                # Wait before next collection cycle
                await asyncio.sleep(1800)  # 30 minutes

            except Exception as e:
                logger.error(f"Error in living collection: {e}")
                await asyncio.sleep(300)  # 5 minutes on error

    async def _collect_evidence_artifacts(self):
        """Collect evidence artifacts from repository."""
        logger.info("Collecting evidence artifacts...")

        for pattern_name, pattern_config in self.evidence_patterns.items():
            pattern = pattern_config["pattern"]

            # Find matching files
            matching_files = list(self.repository_root.glob(pattern))

            for file_path in matching_files:
                if file_path.is_file():
                    await self._process_evidence_file(file_path, pattern_config)

    async def _process_evidence_file(self, file_path: Path, pattern_config: Dict[str, Any]):
        """Process individual evidence file."""

        # Calculate file hash for change detection
        file_hash = self._calculate_file_hash(file_path)

        # Check if we've already processed this version
        cache_key = f"{file_path}:{file_hash}"
        if cache_key in self.evidence_cache:
            return  # Already processed

        # Read and analyze file content
        try:
            content = await self._read_file_content(file_path)

            # Create evidence artifact
            artifact = EvidenceArtifact(
                artifact_id=str(uuid.uuid4()),
                evidence_type=pattern_config["evidence_type"],
                source_file=str(file_path.relative_to(self.repository_root)),
                collection_timestamp=datetime.datetime.utcnow(),
                content_hash=file_hash,
                content_summary=self._generate_content_summary(content, file_path.suffix),
                relevance_score=pattern_config["relevance_score"],
                iso_standards=pattern_config["iso_standards"],
                retention_period_days=pattern_config["retention_period_days"],
                classification=self._determine_classification(file_path, content),
                risk_level=self._assess_risk_level(content, pattern_config),
                metadata=self._extract_metadata(content, file_path)
            )

            # Validate artifact
            artifact.validation_status = await self._validate_artifact(artifact, content)

            # Cache artifact
            self.evidence_cache[cache_key] = artifact

            logger.info(f"Processed evidence artifact: {file_path.name}")

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")

    async def _read_file_content(self, file_path: Path) -> str:
        """Read file content asynchronously."""
        try:
            if file_path.suffix.lower() in ['.json', '.py', '.md', '.csv', '.log']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return f"Binary file: {file_path.name}"
        except Exception:
            return f"Error reading file: {file_path.name}"

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file content."""
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
        except Exception:
            hash_sha256.update(str(file_path).encode())
        return hash_sha256.hexdigest()

    def _generate_content_summary(self, content: str, file_extension: str) -> str:
        """Generate summary of file content."""

        if file_extension == '.json':
            try:
                data = json.loads(content)
                if isinstance(data, dict):
                    keys = list(data.keys())[:5]
                    return f"JSON object with {len(data)} keys: {', '.join(keys)}"
                elif isinstance(data, list):
                    return f"JSON array with {len(data)} items"
            except:
                pass

        elif file_extension == '.py':
            classes = re.findall(r'class\s+(\w+)', content)
            functions = re.findall(r'def\s+(\w+)', content)
            return f"Python module with {len(classes)} classes and {len(functions)} functions"

        elif file_extension == '.md':
            lines = content.split('\n')[:3]
            return f"Markdown document: {' '.join(lines)}".strip()

        elif file_extension == '.log':
            lines = content.split('\n')[:5]
            return f"Log file with {len(content.split())} entries"

        return f"Text document with {len(content.split())} words"

    def _determine_classification(self, file_path: Path, content: str) -> str:
        """Determine information classification level."""

        path_str = str(file_path).lower()
        if any(keyword in path_str for keyword in ['secret', 'key', 'credential', 'private']):
            return "Restricted"

        if any(term in content.lower() for term in ['patient', 'medical', 'health', 'diagnosis']):
            return "Confidential"

        return "Internal"

    def _assess_risk_level(self, content: str, pattern_config: Dict[str, Any]) -> RiskLevel:
        """Assess risk level of evidence artifact."""

        risk_indicators = {
            RiskLevel.CRITICAL: ['breach', 'incident', 'critical', 'failure', 'violation'],
            RiskLevel.HIGH: ['high risk', 'vulnerability', 'threat', 'non-compliant'],
            RiskLevel.MEDIUM: ['medium risk', 'warning', 'issue', 'concern'],
            RiskLevel.LOW: ['low risk', 'info', 'normal', 'compliant']
        }

        content_lower = content.lower()
        for level, indicators in risk_indicators.items():
            if any(indicator in content_lower for indicator in indicators):
                return level

        return RiskLevel.LOW

    def _extract_metadata(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from file content."""

        metadata = {
            "file_size": file_path.stat().st_size,
            "last_modified": datetime.datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            "file_type": file_path.suffix
        }

        # Extract timestamps from logs
        if file_path.suffix == '.log':
            timestamps = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', content)
            if timestamps:
                metadata["log_start"] = min(timestamps)
                metadata["log_end"] = max(timestamps)

        # Extract version info
        version_match = re.search(r'version[:\s]+([\d.]+)', content, re.IGNORECASE)
        if version_match:
            metadata["version"] = version_match.group(1)

        return metadata

    async def _validate_artifact(self, artifact: EvidenceArtifact, content: str) -> str:
        """Validate evidence artifact integrity and relevance."""

        try:
            if not artifact.content_hash:
                return "invalid"

            # File existence check
            full_path = self.repository_root / artifact.source_file
            if not full_path.exists():
                return "missing"

            # ISO-specific validation
            validation_results = []
            for iso_standard in artifact.iso_standards:
                if iso_standard == "ISO 42001":
                    validation_results.append(self._validate_iso42001(content))
                elif iso_standard == "ISO 27001":
                    validation_results.append(self._validate_iso27001(content))
                elif iso_standard == "ISO 27701":
                    validation_results.append(self._validate_iso27701(content))

            if all(validation_results):
                return "verified"
            elif any(validation_results):
                return "partially_verified"
            else:
                return "non_compliant"

        except Exception as e:
            logger.error(f"Validation error for {artifact.artifact_id}: {e}")
            return "error"

    def _validate_iso42001(self, content: str) -> bool:
        """Validate ISO 42001 compliance indicators."""
        ai_indicators = [
            'bias', 'fairness', 'explainability', 'transparency',
            'accountability', 'ethical', 'impact assessment', 'ai',
            'machine learning', 'model', 'training', 'data quality'
        ]
        return any(indicator.lower() in content.lower() for indicator in ai_indicators)

    def _validate_iso27001(self, content: str) -> bool:
        """Validate ISO 27001 compliance indicators."""
        security_indicators = [
            'confidentiality', 'integrity', 'availability', 'security',
            'risk assessment', 'controls', 'audit', 'access', 'authentication',
            'encryption', 'monitoring', 'incident', 'policy', 'procedure'
        ]
        return any(indicator.lower() in content.lower() for indicator in security_indicators)

    def _validate_iso27701(self, content: str) -> bool:
        """Validate ISO 27701 compliance indicators."""
        privacy_indicators = [
            'privacy', 'data protection', 'consent', 'controller',
            'processor', 'data subject', 'rights', 'gdpr', 'ccpa',
            'personal data', 'processing', 'retention', 'breach'
        ]
        return any(indicator.lower() in content.lower() for indicator in privacy_indicators)

    async def _update_living_bundles(self):
        """Update all active living evidence bundles."""

        for bundle_id, bundle in self.active_bundles.items():
            # Add new evidence artifacts
            new_artifacts = [
                artifact for artifact in self.evidence_cache.values()
                if artifact.collection_timestamp > bundle.last_updated
            ]

            bundle.evidence_artifacts.extend(new_artifacts)
            bundle.last_updated = datetime.datetime.utcnow()

            # Update compliance and risk summaries
            bundle.compliance_summary = self._generate_compliance_summary(bundle)
            bundle.risk_summary = self._generate_risk_summary(bundle)

            # Validate bundle integrity
            await self._validate_bundle_integrity(bundle)

    def _generate_compliance_summary(self, bundle: LivingEvidenceBundle) -> Dict[str, Any]:
        """Generate compliance summary for the bundle."""

        summary = {
            "total_artifacts": len(bundle.evidence_artifacts),
            "standards_coverage": {},
            "evidence_types": {},
            "validation_status": {},
            "risk_distribution": {},
            "collection_date_range": {}
        }

        if bundle.evidence_artifacts:
            timestamps = [art.collection_timestamp for art in bundle.evidence_artifacts]
            summary["collection_date_range"] = {
                "earliest": min(timestamps).isoformat(),
                "latest": max(timestamps).isoformat()
            }

        # Analyze artifacts
        for artifact in bundle.evidence_artifacts:
            # Standards coverage
            for iso_standard in artifact.iso_standards:
                summary["standards_coverage"][iso_standard] = summary["standards_coverage"].get(iso_standard, 0) + 1

            # Evidence types
            evidence_type = artifact.evidence_type.value
            summary["evidence_types"][evidence_type] = summary["evidence_types"].get(evidence_type, 0) + 1

            # Validation status
            summary["validation_status"][artifact.validation_status] = summary["validation_status"].get(artifact.validation_status, 0) + 1

            # Risk distribution
            risk_level = artifact.risk_level.value
            summary["risk_distribution"][risk_level] = summary["risk_distribution"].get(risk_level, 0) + 1

        return summary

    def _generate_risk_summary(self, bundle: LivingEvidenceBundle) -> Dict[str, Any]:
        """Generate risk summary for the bundle."""

        risk_summary = {
            "total_artifacts": len(bundle.evidence_artifacts),
            "risk_levels": {},
            "risk_categories": {},
            "critical_findings": [],
            "high_risk_items": []
        }

        for artifact in bundle.evidence_artifacts:
            # Risk levels
            risk_level = artifact.risk_level.value
            risk_summary["risk_levels"][risk_level] = risk_summary["risk_levels"].get(risk_level, 0) + 1

            # Risk categories
            risk_category = artifact.metadata.get("risk_category", "Unknown")
            risk_summary["risk_categories"][risk_category] = risk_summary["risk_categories"].get(risk_category, 0) + 1

            # Critical and high-risk findings
            if artifact.risk_level in [RiskLevel.CRITICAL]:
                risk_summary["critical_findings"].append({
                    "artifact_id": artifact.artifact_id,
                    "description": artifact.content_summary,
                    "source": artifact.source_file
                })
            elif artifact.risk_level == RiskLevel.HIGH:
                risk_summary["high_risk_items"].append({
                    "artifact_id": artifact.artifact_id,
                    "description": artifact.content_summary,
                    "source": artifact.source_file
                })

        return risk_summary

    async def _validate_bundle_integrity(self, bundle: LivingEvidenceBundle):
        """Validate bundle integrity and generate hash."""

        try:
            # Calculate bundle integrity hash
            bundle_content = json.dumps({
                "bundle_id": bundle.bundle_id,
                "artifacts": [
                    {
                        "id": artifact.artifact_id,
                        "hash": artifact.content_hash,
                        "timestamp": artifact.collection_timestamp.isoformat()
                    }
                    for artifact in bundle.evidence_artifacts
                ]
            }, sort_keys=True)

            bundle.integrity_hash = hashlib.sha256(bundle_content.encode()).hexdigest()

        except Exception as e:
            logger.error(f"Bundle integrity validation error: {e}")

    async def _resolve_residual_risks(self):
        """Resolve and monitor residual risks."""

        # Analyze current evidence for new risks
        new_risks = await self._analyze_evidence_for_risks()

        # Update existing residual risks
        for risk in self.residual_risks:
            if risk.next_review <= datetime.datetime.utcnow():
                await self._review_residual_risk(risk)

        # Add new residual risks
        self.residual_risks.extend(new_risks)

        # Generate risk treatment recommendations
        await self._generate_risk_treatments()

    async def _analyze_evidence_for_risks(self) -> List[ResidualRisk]:
        """Analyze evidence artifacts for potential risks."""

        risks = []

        for artifact in self.evidence_cache.values():
            if artifact.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                # Create residual risk entry
                risk = ResidualRisk(
                    risk_id=f"RISK-{artifact.artifact_id[:8]}",
                    description=f"Risk identified in {artifact.source_file}: {artifact.content_summary}",
                    category=artifact.metadata.get("risk_category", "General"),
                    initial_likelihood=artifact.risk_level,
                    initial_impact=artifact.risk_level,
                    residual_likelihood=artifact.risk_level,
                    residual_impact=artifact.risk_level,
                    treatment_measures=self._generate_treatment_measures(artifact),
                    monitoring_frequency="weekly"
                )
                risks.append(risk)

        return risks

    def _generate_treatment_measures(self, artifact: EvidenceArtifact) -> List[str]:
        """Generate treatment measures for a risk."""

        measures = []

        if artifact.evidence_type == EvidenceType.SECURITY_EVENT:
            measures.extend([
                "Implement additional security controls",
                "Enhance monitoring and alerting",
                "Conduct security awareness training"
            ])
        elif artifact.evidence_type == EvidenceType.RISK_ASSESSMENT:
            measures.extend([
                "Review and update risk assessment",
                "Implement recommended controls",
                "Schedule follow-up assessment"
            ])
        elif artifact.evidence_type == EvidenceType.INCIDENT_REPORT:
            measures.extend([
                "Investigate root cause",
                "Implement corrective actions",
                "Update incident response procedures"
            ])

        return measures

    async def _review_residual_risk(self, risk: ResidualRisk):
        """Review and update residual risk status."""

        # Check if risk has been mitigated based on new evidence
        mitigating_evidence = [
            art for art in self.evidence_cache.values()
            if art.metadata.get("risk_category") == risk.category
            and art.collection_timestamp > risk.last_assessed
            and art.validation_status == "verified"
        ]

        if mitigating_evidence:
            # Potentially reduce risk level
            risk.residual_likelihood = RiskLevel.LOW
            risk.residual_impact = RiskLevel.LOW
            risk.last_assessed = datetime.datetime.utcnow()
            risk.next_review = datetime.datetime.utcnow() + datetime.timedelta(days=90)

    async def _generate_risk_treatments(self):
        """Generate risk treatment recommendations."""

        # Analyze risk patterns
        risk_patterns = {}
        for risk in self.residual_risks:
            category = risk.category
            if category not in risk_patterns:
                risk_patterns[category] = []
            risk_patterns[category].append(risk)

        # Generate treatment plans for high-risk categories
        for category, risks in risk_patterns.items():
            if len(risks) > 2:  # Multiple risks in same category
                logger.warning(f"Multiple risks in category {category}: {len(risks)} items")

    async def _validate_evidence_integrity(self):
        """Validate integrity of all cached evidence."""

        for cache_key, artifact in self.evidence_cache.items():
            # Re-validate file hash
            file_path = self.repository_root / artifact.source_file
            if file_path.exists():
                current_hash = self._calculate_file_hash(file_path)
                if current_hash != artifact.content_hash:
                    logger.warning(f"Evidence integrity violation: {artifact.source_file}")
                    artifact.validation_status = "integrity_violation"
            else:
                artifact.validation_status = "file_missing"

    async def _generate_compliance_reports(self):
        """Generate automated compliance reports."""

        # Generate reports for each active bundle
        for bundle_id, bundle in self.active_bundles.items():
            report_path = self.repository_root / "certification" / f"compliance_report_{bundle_id}.json"

            report = {
                "report_id": str(uuid.uuid4()),
                "bundle_id": bundle.bundle_id,
                "generation_timestamp": datetime.datetime.utcnow().isoformat(),
                "compliance_summary": bundle.compliance_summary,
                "risk_summary": bundle.risk_summary,
                "residual_risks": [
                    {
                        "risk_id": risk.risk_id,
                        "description": risk.description,
                        "category": risk.category,
                        "residual_likelihood": risk.residual_likelihood.value,
                        "residual_impact": risk.residual_impact.value,
                        "treatment_measures": risk.treatment_measures
                    }
                    for risk in self.residual_risks
                ],
                "recommendations": self._generate_recommendations(bundle)
            }

            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2, default=str)

    def _generate_recommendations(self, bundle: LivingEvidenceBundle) -> List[str]:
        """Generate compliance recommendations."""

        recommendations = []

        compliance = bundle.compliance_summary
        risk_summary = bundle.risk_summary

        # Check standards coverage
        required_standards = {"ISO 42001", "ISO 27001", "ISO 27701"}
        covered_standards = set(compliance.get("standards_coverage", {}).keys())

        missing_standards = required_standards - covered_standards
        if missing_standards:
            recommendations.append(f"Obtain evidence for missing standards: {missing_standards}")

        # Check validation status
        validation_status = compliance.get("validation_status", {})
        non_verified = validation_status.get("non_compliant", 0) + validation_status.get("error", 0)
        if non_verified > 0:
            recommendations.append(f"Address {non_verified} non-compliant or erroneous evidence items")

        # Check risk levels
        risk_levels = risk_summary.get("risk_levels", {})
        critical_count = risk_levels.get("critical", 0)
        high_count = risk_levels.get("high", 0)

        if critical_count > 0:
            recommendations.append(f"Immediately address {critical_count} critical risk items")
        if high_count > 0:
            recommendations.append(f"Prioritize treatment of {high_count} high-risk items")

        return recommendations

    async def create_living_bundle(self,
                                 target_standards: List[str],
                                 bundle_type: str = "comprehensive") -> str:
        """Create a new living evidence bundle."""

        bundle_id = f"LEB-{bundle_type}-{datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

        bundle = LivingEvidenceBundle(
            bundle_id=bundle_id,
            bundle_version="1.0",
            creation_timestamp=datetime.datetime.utcnow(),
            target_standards=target_standards,
            status="active"
        )

        self.active_bundles[bundle_id] = bundle
        logger.info(f"Created living evidence bundle: {bundle_id}")

        return bundle_id

    def export_audit_package(self, bundle_id: str, output_path: str):
        """Export bundle as audit-ready package."""

        if bundle_id not in self.active_bundles:
            raise ValueError(f"Bundle {bundle_id} not found")

        bundle = self.active_bundles[bundle_id]

        # Prepare export data
        export_data = {
            "audit_package": {
                "package_id": str(uuid.uuid4()),
                "bundle_id": bundle.bundle_id,
                "export_timestamp": datetime.datetime.utcnow().isoformat(),
                "target_standards": bundle.target_standards,
                "integrity_hash": bundle.integrity_hash
            },
            "evidence_inventory": [
                {
                    "artifact_id": artifact.artifact_id,
                    "evidence_type": artifact.evidence_type.value,
                    "source_file": artifact.source_file,
                    "collection_timestamp": artifact.collection_timestamp.isoformat(),
                    "content_hash": artifact.content_hash,
                    "relevance_score": artifact.relevance_score,
                    "iso_standards": artifact.iso_standards,
                    "validation_status": artifact.validation_status,
                    "risk_level": artifact.risk_level.value,
                    "classification": artifact.classification,
                    "metadata": artifact.metadata
                }
                for artifact in bundle.evidence_artifacts
            ],
            "compliance_summary": bundle.compliance_summary,
            "risk_summary": bundle.risk_summary,
            "residual_risks": [
                {
                    "risk_id": risk.risk_id,
                    "description": risk.description,
                    "category": risk.category,
                    "residual_likelihood": risk.residual_likelihood.value,
                    "residual_impact": risk.residual_impact.value,
                    "treatment_measures": risk.treatment_measures,
                    "last_assessed": risk.last_assessed.isoformat(),
                    "next_review": risk.next_review.isoformat()
                }
                for risk in self.residual_risks
            ],
            "validation_results": bundle.validation_results
        }

        # Calculate export integrity hash
        export_content = json.dumps(export_data, sort_keys=True, default=str)
        export_data["audit_package"]["export_integrity_hash"] = hashlib.sha256(export_content.encode()).hexdigest()

        # Write to file
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)

        logger.info(f"Exported audit package: {output_path}")

        return export_data["audit_package"]["export_integrity_hash"]

    def get_bundle_status(self, bundle_id: str) -> Dict[str, Any]:
        """Get status of a specific bundle."""

        if bundle_id not in self.active_bundles:
            return {"status": "not_found"}

        bundle = self.active_bundles[bundle_id]

        return {
            "bundle_id": bundle.bundle_id,
            "status": bundle.status,
            "creation_timestamp": bundle.creation_timestamp.isoformat(),
            "evidence_count": len(bundle.evidence_artifacts),
            "compliance_summary": bundle.compliance_summary,
            "risk_summary": bundle.risk_summary,
            "last_updated": bundle.last_updated.isoformat()
        }

# Global instance
living_evidence_engine = LivingEvidenceEngine()

async def start_living_evidence_engine():
    """Start the living evidence engine."""
    logger.info("Starting Living Evidence Engine...")

    # Create initial comprehensive bundle
    bundle_id = await living_evidence_engine.create_living_bundle(
        target_standards=["ISO 42001", "ISO 27001", "ISO 27701"],
        bundle_type="comprehensive"
    )

    # Start continuous collection
    await living_evidence_engine.start_living_collection()

def start_living_engine_thread():
    """Start living evidence engine in background thread."""
    def run_async_engine():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_living_evidence_engine())

    engine_thread = threading.Thread(target=run_async_engine, daemon=True)
    engine_thread.start()
    logger.info("Living Evidence Engine started in background")

if __name__ == "__main__":
    # Start the living evidence engine
    start_living_engine_thread()

    # Example: Create and export an audit package
    import time
    time.sleep(5)  # Wait for initial collection

    # Get status of active bundles
    bundles = list(living_evidence_engine.active_bundles.keys())
    print(f"Active bundles: {len(bundles)}")

    if bundles:
        bundle_id = bundles[0]
        print(f"Exporting audit package for bundle: {bundle_id}")

        # Export audit package
        integrity_hash = living_evidence_engine.export_audit_package(
            bundle_id,
            f"/tmp/audit_package_{datetime.datetime.utcnow().strftime('%Y%m%d')}.json"
        )

        print(f"Audit package exported with integrity hash: {integrity_hash[:16]}...")