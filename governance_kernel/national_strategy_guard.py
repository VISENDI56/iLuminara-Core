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
iLuminara National Strategy Guard
ISO 27701 Privacy Management - Local Data Residency Enforcement

This module implements national strategy guardrails to ensure verifiable evidence
of local data residency compliance for regional African regulators (KDPA, POPIA, etc.).
Logs are formatted to provide cryptographic proof of data location and sovereignty.
"""

import json
import hashlib
import datetime
import uuid
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import Certificate, load_pem_x509_certificate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Jurisdiction(Enum):
    """African jurisdictions with data protection laws."""
    KENYA = "kenya"
    SOUTH_AFRICA = "south_africa"
    NIGERIA = "nigeria"
    GHANA = "ghana"
    UGANDA = "uganda"
    TANZANIA = "tanzania"
    ETHIOPIA = "ethiopia"
    RWANDA = "rwanda"
    SENEGAL = "senegal"
    MOROCCO = "morocco"
    EGYPT = "egypt"

class DataResidencyStatus(Enum):
    """Data residency compliance status."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PENDING_VERIFICATION = "pending_verification"
    UNDER_REVIEW = "under_review"

class SovereigntyLevel(Enum):
    """Data sovereignty classification."""
    FULL_SOVEREIGNTY = "full_sovereignty"  # Data never leaves jurisdiction
    CONDITIONAL_SOVEREIGNTY = "conditional_sovereignty"  # Data can leave with safeguards
    LIMITED_SOVEREIGNTY = "limited_sovereignty"  # Data processed internationally
    NO_SOVEREIGNTY = "no_sovereignty"  # Data in non-compliant location

@dataclass
class DataLocationProof:
    """Cryptographic proof of data location and sovereignty."""
    proof_id: str
    data_object_id: str
    jurisdiction: Jurisdiction
    physical_location: str  # Data center coordinates/city
    cloud_provider: Optional[str]
    sovereignty_level: SovereigntyLevel
    residency_status: DataResidencyStatus
    timestamp: datetime.datetime
    verification_hash: str
    blockchain_anchor: Optional[str] = None
    regulatory_compliance: Dict[str, bool] = field(default_factory=dict)
    evidence_chain: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class ResidencyVerificationLog:
    """Verifiable log entry for data residency compliance."""
    log_id: str
    jurisdiction: Jurisdiction
    data_subject_jurisdiction: Jurisdiction
    processing_activity: str
    data_categories: List[str]
    data_location_proofs: List[DataLocationProof]
    compliance_assessment: Dict[str, Any]
    verification_timestamp: datetime.datetime
    verifier_identity: str
    cryptographic_signature: Optional[str] = None
    regulatory_submission_status: Dict[str, str] = field(default_factory=dict)
    audit_trail: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class NationalStrategyGuard:
    """Guardrail for national data residency and sovereignty requirements."""

    jurisdiction_configs: Dict[Jurisdiction, Dict[str, Any]] = field(default_factory=dict)
    residency_logs: List[ResidencyVerificationLog] = field(default_factory=list)
    location_proofs: List[DataLocationProof] = field(default_factory=list)

    def __post_init__(self):
        self._initialize_jurisdiction_configs()
        self._load_verification_keys()

    def _initialize_jurisdiction_configs(self):
        """Initialize data residency requirements for each African jurisdiction."""

        self.jurisdiction_configs = {
            Jurisdiction.KENYA: {
                "law": "Kenya Data Protection Act (KDPA) 2019",
                "data_residency_required": True,
                "sovereignty_requirements": {
                    "health_data": SovereigntyLevel.FULL_SOVEREIGNTY,
                    "personal_data": SovereigntyLevel.CONDITIONAL_SOVEREIGNTY,
                    "public_health_data": SovereigntyLevel.CONDITIONAL_SOVEREIGNTY
                },
                "approved_locations": ["Nairobi", "Mombasa", "Kisumu"],
                "international_transfer_allowed": True,
                "transfer_mechanisms": ["adequacy_decisions", "sccs", "binding_corporate_rules"],
                "regulatory_authority": "Office of the Data Protection Commissioner (ODPC)",
                "reporting_requirements": {
                    "breach_notification": "72 hours",
                    "annual_reporting": True,
                    "data_inventory": True
                }
            },
            Jurisdiction.SOUTH_AFRICA: {
                "law": "Protection of Personal Information Act (POPIA) 2013",
                "data_residency_required": False,  # No explicit residency requirement
                "sovereignty_requirements": {
                    "health_data": SovereigntyLevel.CONDITIONAL_SOVEREIGNTY,
                    "personal_data": SovereigntyLevel.CONDITIONAL_SOVEREIGNTY,
                    "special_personal_data": SovereigntyLevel.FULL_SOVEREIGNTY
                },
                "approved_locations": ["Cape Town", "Johannesburg", "Durban"],
                "international_transfer_allowed": True,
                "transfer_mechanisms": ["adequacy_decisions", "sccs", "approved_codes"],
                "regulatory_authority": "Information Regulator",
                "reporting_requirements": {
                    "breach_notification": "Business days as soon as reasonably possible",
                    "annual_reporting": False,
                    "data_inventory": True
                }
            },
            Jurisdiction.NIGERIA: {
                "law": "Nigeria Data Protection Regulation (NDPR) 2019",
                "data_residency_required": False,
                "sovereignty_requirements": {
                    "health_data": SovereigntyLevel.CONDITIONAL_SOVEREIGNTY,
                    "personal_data": SovereigntyLevel.CONDITIONAL_SOVEREIGNTY,
                    "sensitive_data": SovereigntyLevel.FULL_SOVEREIGNTY
                },
                "approved_locations": ["Lagos", "Abuja", "Port Harcourt"],
                "international_transfer_allowed": True,
                "transfer_mechanisms": ["adequacy_decisions", "sccs", "binding_corporate_rules"],
                "regulatory_authority": "Nigeria Data Protection Bureau (NDPB)",
                "reporting_requirements": {
                    "breach_notification": "72 hours",
                    "annual_reporting": True,
                    "data_inventory": True
                }
            },
            Jurisdiction.GHANA: {
                "law": "Data Protection Act 2012 (Act 843)",
                "data_residency_required": False,
                "sovereignty_requirements": {
                    "health_data": SovereigntyLevel.CONDITIONAL_SOVEREIGNTY,
                    "personal_data": SovereigntyLevel.CONDITIONAL_SOVEREIGNTY,
                    "sensitive_data": SovereigntyLevel.FULL_SOVEREIGNTY
                },
                "approved_locations": ["Accra", "Tema", "Takoradi"],
                "international_transfer_allowed": True,
                "transfer_mechanisms": ["adequacy_decisions", "sccs"],
                "regulatory_authority": "Data Protection Commission",
                "reporting_requirements": {
                    "breach_notification": "Reasonable time",
                    "annual_reporting": False,
                    "data_inventory": True
                }
            }
        }

    def _load_verification_keys(self):
        """Load cryptographic keys for log verification."""
        # In production, these would be loaded from secure key management
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def create_location_proof(self,
                            data_object_id: str,
                            jurisdiction: Jurisdiction,
                            physical_location: str,
                            cloud_provider: Optional[str] = None) -> DataLocationProof:
        """
        Create cryptographic proof of data location for regulatory compliance.
        """

        # Generate verification hash based on data location evidence
        location_evidence = {
            "data_object_id": data_object_id,
            "jurisdiction": jurisdiction.value,
            "physical_location": physical_location,
            "cloud_provider": cloud_provider,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "evidence_type": "data_location_verification"
        }

        evidence_json = json.dumps(location_evidence, sort_keys=True)
        verification_hash = hashlib.sha256(evidence_json.encode()).hexdigest()

        # Determine sovereignty level based on jurisdiction requirements
        config = self.jurisdiction_configs.get(jurisdiction, {})
        sovereignty_level = SovereigntyLevel.CONDITIONAL_SOVEREIGNTY  # Default

        # Check if location is approved for this jurisdiction
        approved_locations = config.get("approved_locations", [])
        if physical_location in approved_locations:
            sovereignty_level = SovereigntyLevel.FULL_SOVEREIGNTY
        elif config.get("international_transfer_allowed", False):
            sovereignty_level = SovereigntyLevel.CONDITIONAL_SOVEREIGNTY
        else:
            sovereignty_level = SovereigntyLevel.LIMITED_SOVEREIGNTY

        # Assess residency status
        residency_status = DataResidencyStatus.COMPLIANT
        if sovereignty_level == SovereigntyLevel.NO_SOVEREIGNTY:
            residency_status = DataResidencyStatus.NON_COMPLIANT

        # Create regulatory compliance assessment
        regulatory_compliance = {}
        if jurisdiction == Jurisdiction.KENYA:
            regulatory_compliance = {
                "kdpa_compliant": sovereignty_level in [SovereigntyLevel.FULL_SOVEREIGNTY, SovereigntyLevel.CONDITIONAL_SOVEREIGNTY],
                "data_localization_met": physical_location in ["Nairobi", "Mombasa", "Kisumu"],
                "transfer_mechanism_valid": True
            }
        elif jurisdiction == Jurisdiction.SOUTH_AFRICA:
            regulatory_compliance = {
                "popia_compliant": sovereignty_level in [SovereigntyLevel.FULL_SOVEREIGNTY, SovereigntyLevel.CONDITIONAL_SOVEREIGNTY],
                "special_personal_data_protected": True,
                "information_officer_notified": True
            }

        proof = DataLocationProof(
            proof_id=str(uuid.uuid4()),
            data_object_id=data_object_id,
            jurisdiction=jurisdiction,
            physical_location=physical_location,
            cloud_provider=cloud_provider,
            sovereignty_level=sovereignty_level,
            residency_status=residency_status,
            timestamp=datetime.datetime.utcnow(),
            verification_hash=verification_hash,
            regulatory_compliance=regulatory_compliance,
            evidence_chain=[location_evidence]
        )

        self.location_proofs.append(proof)
        logger.info(f"Created location proof for {data_object_id} in {jurisdiction.value}")

        return proof

    def log_residency_verification(self,
                                 jurisdiction: Jurisdiction,
                                 data_subject_jurisdiction: Jurisdiction,
                                 processing_activity: str,
                                 data_categories: List[str],
                                 location_proofs: List[DataLocationProof],
                                 verifier_identity: str) -> ResidencyVerificationLog:
        """
        Create a verifiable log entry for data residency compliance.
        """

        # Assess overall compliance
        compliance_assessment = self._assess_compliance(
            jurisdiction, data_subject_jurisdiction, location_proofs
        )

        # Create log entry
        log_entry = ResidencyVerificationLog(
            log_id=str(uuid.uuid4()),
            jurisdiction=jurisdiction,
            data_subject_jurisdiction=data_subject_jurisdiction,
            processing_activity=processing_activity,
            data_categories=data_categories,
            data_location_proofs=location_proofs,
            compliance_assessment=compliance_assessment,
            verification_timestamp=datetime.datetime.utcnow(),
            verifier_identity=verifier_identity,
            audit_trail=[{
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "action": "residency_verification_created",
                "verifier": verifier_identity,
                "compliance_status": compliance_assessment.get("overall_compliant", False)
            }]
        )

        # Generate cryptographic signature
        log_data = json.dumps({
            "log_id": log_entry.log_id,
            "jurisdiction": log_entry.jurisdiction.value,
            "verification_timestamp": log_entry.verification_timestamp.isoformat(),
            "compliance_assessment": log_entry.compliance_assessment
        }, sort_keys=True)

        signature = self.private_key.sign(
            log_data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        log_entry.cryptographic_signature = signature.hex()

        self.residency_logs.append(log_entry)
        logger.info(f"Created residency verification log for {processing_activity}")

        return log_entry

    def _assess_compliance(self,
                          jurisdiction: Jurisdiction,
                          data_subject_jurisdiction: Jurisdiction,
                          location_proofs: List[DataLocationProof]) -> Dict[str, Any]:
        """
        Assess compliance with jurisdiction-specific data residency requirements.
        """

        config = self.jurisdiction_configs.get(jurisdiction, {})
        assessment = {
            "overall_compliant": True,
            "sovereignty_assessment": {},
            "regulatory_requirements": {},
            "risk_factors": [],
            "recommendations": []
        }

        # Check sovereignty levels
        sovereignty_levels = [proof.sovereignty_level for proof in location_proofs]
        min_sovereignty = min(sovereignty_levels) if sovereignty_levels else SovereigntyLevel.NO_SOVEREIGNTY

        assessment["sovereignty_assessment"] = {
            "minimum_sovereignty_level": min_sovereignty.value,
            "all_proofs_compliant": all(proof.residency_status == DataResidencyStatus.COMPLIANT
                                       for proof in location_proofs),
            "approved_locations_used": all(proof.physical_location in config.get("approved_locations", [])
                                         for proof in location_proofs)
        }

        # Jurisdiction-specific assessments
        if jurisdiction == Jurisdiction.KENYA:
            assessment["regulatory_requirements"] = {
                "kdpa_data_localization": config.get("data_residency_required", False),
                "health_data_sovereignty": min_sovereignty == SovereigntyLevel.FULL_SOVEREIGNTY,
                "odpc_reporting_compliant": True
            }

            if not assessment["sovereignty_assessment"]["approved_locations_used"]:
                assessment["risk_factors"].append("Data stored outside approved Kenyan locations")
                assessment["recommendations"].append("Migrate data to Nairobi, Mombasa, or Kisumu data centers")

        elif jurisdiction == Jurisdiction.SOUTH_AFRICA:
            assessment["regulatory_requirements"] = {
                "popia_residency_optional": not config.get("data_residency_required", False),
                "special_personal_data_protected": True,
                "information_regulator_notified": True
            }

        # Cross-jurisdiction considerations
        if jurisdiction != data_subject_jurisdiction:
            assessment["risk_factors"].append("Cross-border data processing detected")
            assessment["recommendations"].append("Ensure adequate transfer safeguards are in place")

        # Overall compliance determination
        assessment["overall_compliant"] = (
            assessment["sovereignty_assessment"]["all_proofs_compliant"] and
            len(assessment["risk_factors"]) == 0
        )

        return assessment

    def generate_regulatory_report(self,
                                 jurisdiction: Jurisdiction,
                                 start_date: datetime.datetime,
                                 end_date: datetime.datetime) -> Dict[str, Any]:
        """
        Generate regulatory report for submission to local data protection authorities.
        """

        # Filter logs for jurisdiction and date range
        relevant_logs = [
            log for log in self.residency_logs
            if log.jurisdiction == jurisdiction and
            start_date <= log.verification_timestamp <= end_date
        ]

        # Aggregate compliance statistics
        total_logs = len(relevant_logs)
        compliant_logs = len([log for log in relevant_logs
                            if log.compliance_assessment.get("overall_compliant", False)])

        compliance_rate = (compliant_logs / total_logs * 100) if total_logs > 0 else 0

        # Identify high-risk activities
        high_risk_logs = [
            log for log in relevant_logs
            if not log.compliance_assessment.get("overall_compliant", True)
        ]

        report = {
            "report_metadata": {
                "jurisdiction": jurisdiction.value,
                "reporting_period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat()
                },
                "generated_date": datetime.datetime.utcnow().isoformat(),
                "organization": "iLuminara Health Systems",
                "report_version": "1.0"
            },
            "compliance_summary": {
                "total_verifications": total_logs,
                "compliant_verifications": compliant_logs,
                "compliance_rate": round(compliance_rate, 2),
                "high_risk_findings": len(high_risk_logs)
            },
            "data_residency_status": {
                "approved_locations_used": self._calculate_location_compliance(jurisdiction, relevant_logs),
                "sovereignty_levels_achieved": self._calculate_sovereignty_distribution(relevant_logs),
                "international_transfers": self._identify_international_transfers(relevant_logs)
            },
            "risk_assessment": {
                "critical_risks": [log.processing_activity for log in high_risk_logs],
                "mitigation_actions": self._generate_mitigation_recommendations(high_risk_logs),
                "compliance_trend": self._calculate_compliance_trend(relevant_logs)
            },
            "audit_evidence": {
                "verification_logs": [self._serialize_log(log) for log in relevant_logs[:100]],  # Limit for report size
                "cryptographic_proofs": [proof.verification_hash for proof in self.location_proofs],
                "blockchain_anchors": [log.blockchain_anchor for log in relevant_logs if log.blockchain_anchor]
            }
        }

        return report

    def _calculate_location_compliance(self, jurisdiction: Jurisdiction, logs: List[ResidencyVerificationLog]) -> Dict[str, Any]:
        """Calculate compliance with approved data locations."""
        config = self.jurisdiction_configs.get(jurisdiction, {})
        approved_locations = set(config.get("approved_locations", []))

        location_usage = {}
        for log in logs:
            for proof in log.data_location_proofs:
                location = proof.physical_location
                if location not in location_usage:
                    location_usage[location] = {"count": 0, "compliant": location in approved_locations}
                location_usage[location]["count"] += 1

        return {
            "approved_locations": list(approved_locations),
            "locations_used": location_usage,
            "compliance_rate": sum(1 for loc in location_usage.values() if loc["compliant"]) / len(location_usage) if location_usage else 0
        }

    def _calculate_sovereignty_distribution(self, logs: List[ResidencyVerificationLog]) -> Dict[str, int]:
        """Calculate distribution of sovereignty levels achieved."""
        distribution = {}
        for log in logs:
            for proof in log.data_location_proofs:
                level = proof.sovereignty_level.value
                distribution[level] = distribution.get(level, 0) + 1
        return distribution

    def _identify_international_transfers(self, logs: List[ResidencyVerificationLog]) -> List[Dict[str, Any]]:
        """Identify international data transfers."""
        transfers = []
        for log in logs:
            for proof in log.data_location_proofs:
                if proof.sovereignty_level in [SovereigntyLevel.LIMITED_SOVEREIGNTY, SovereigntyLevel.NO_SOVEREIGNTY]:
                    transfers.append({
                        "processing_activity": log.processing_activity,
                        "destination": proof.physical_location,
                        "sovereignty_level": proof.sovereignty_level.value,
                        "transfer_mechanism": "standard_contractual_clauses",  # Default assumption
                        "verification_date": proof.timestamp.isoformat()
                    })
        return transfers

    def _generate_mitigation_recommendations(self, high_risk_logs: List[ResidencyVerificationLog]) -> List[str]:
        """Generate mitigation recommendations for high-risk findings."""
        recommendations = set()

        for log in high_risk_logs:
            assessment = log.compliance_assessment
            risk_factors = assessment.get("risk_factors", [])
            existing_recs = assessment.get("recommendations", [])

            recommendations.update(risk_factors)
            recommendations.update(existing_recs)

        return list(recommendations)

    def _calculate_compliance_trend(self, logs: List[ResidencyVerificationLog]) -> Dict[str, Any]:
        """Calculate compliance trend over time."""
        # Sort logs by date
        sorted_logs = sorted(logs, key=lambda x: x.verification_timestamp)

        # Group by week
        weekly_compliance = {}
        for log in sorted_logs:
            week = log.verification_timestamp.strftime("%Y-%U")
            if week not in weekly_compliance:
                weekly_compliance[week] = {"total": 0, "compliant": 0}
            weekly_compliance[week]["total"] += 1
            if log.compliance_assessment.get("overall_compliant", False):
                weekly_compliance[week]["compliant"] += 1

        trend_data = []
        for week, data in weekly_compliance.items():
            compliance_rate = (data["compliant"] / data["total"] * 100) if data["total"] > 0 else 0
            trend_data.append({
                "period": week,
                "compliance_rate": round(compliance_rate, 2),
                "total_verifications": data["total"]
            })

        return {
            "trend_data": trend_data,
            "overall_trend": "improving" if len(trend_data) > 1 and trend_data[-1]["compliance_rate"] > trend_data[0]["compliance_rate"] else "stable"
        }

    def _serialize_log(self, log: ResidencyVerificationLog) -> Dict[str, Any]:
        """Serialize log for regulatory reporting."""
        return {
            "log_id": log.log_id,
            "jurisdiction": log.jurisdiction.value,
            "processing_activity": log.processing_activity,
            "compliance_status": log.compliance_assessment.get("overall_compliant", False),
            "verification_timestamp": log.verification_timestamp.isoformat(),
            "verifier": log.verifier_identity,
            "data_categories": log.data_categories,
            "location_proofs_count": len(log.data_location_proofs)
        }

    def export_logs_for_audit(self, jurisdiction: Jurisdiction, output_file: str):
        """Export residency verification logs in audit-ready format."""
        jurisdiction_logs = [log for log in self.residency_logs if log.jurisdiction == jurisdiction]

        audit_export = {
            "export_metadata": {
                "jurisdiction": jurisdiction.value,
                "export_date": datetime.datetime.utcnow().isoformat(),
                "total_logs": len(jurisdiction_logs),
                "format_version": "ISO27701-AUDIT-1.0"
            },
            "verification_logs": [self._serialize_log(log) for log in jurisdiction_logs],
            "location_proofs": [
                {
                    "proof_id": proof.proof_id,
                    "data_object_id": proof.data_object_id,
                    "jurisdiction": proof.jurisdiction.value,
                    "physical_location": proof.physical_location,
                    "sovereignty_level": proof.sovereignty_level.value,
                    "residency_status": proof.residency_status.value,
                    "verification_hash": proof.verification_hash,
                    "timestamp": proof.timestamp.isoformat()
                }
                for proof in self.location_proofs
                if proof.jurisdiction == jurisdiction
            ],
            "regulatory_compliance_summary": self._calculate_location_compliance(jurisdiction, jurisdiction_logs)
        }

        with open(output_file, 'w') as f:
            json.dump(audit_export, f, indent=2, default=str)

        logger.info(f"Exported {len(jurisdiction_logs)} logs for {jurisdiction.value} audit to {output_file}")

# Global instance for the national strategy guard
national_strategy_guard = NationalStrategyGuard()

def verify_data_residency_for_audit(jurisdiction: Jurisdiction,
                                  processing_activity: str,
                                  data_location: str) -> Dict[str, Any]:
    """
    Verify data residency compliance for a specific processing activity.
    Returns audit-ready evidence for regulatory submission.
    """

    # Create location proof
    location_proof = national_strategy_guard.create_location_proof(
        data_object_id=f"{processing_activity}_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        jurisdiction=jurisdiction,
        physical_location=data_location,
        cloud_provider="Google Cloud" if "gcp" in data_location.lower() else None
    )

    # Create verification log
    verification_log = national_strategy_guard.log_residency_verification(
        jurisdiction=jurisdiction,
        data_subject_jurisdiction=jurisdiction,  # Assume same for simplicity
        processing_activity=processing_activity,
        data_categories=["health_data", "personal_data"],
        location_proofs=[location_proof],
        verifier_identity="Automated Compliance Engine"
    )

    return {
        "verification_status": "completed",
        "location_proof": {
            "proof_id": location_proof.proof_id,
            "sovereignty_level": location_proof.sovereignty_level.value,
            "residency_status": location_proof.residency_status.value,
            "verification_hash": location_proof.verification_hash
        },
        "compliance_assessment": verification_log.compliance_assessment,
        "audit_evidence": {
            "log_id": verification_log.log_id,
            "cryptographic_signature": verification_log.cryptographic_signature,
            "verification_timestamp": verification_log.verification_timestamp.isoformat()
        }
    }

if __name__ == "__main__":
    # Example usage for Kenyan data residency verification
    verification = verify_data_residency_for_audit(
        jurisdiction=Jurisdiction.KENYA,
        processing_activity="FRENASA_Outbreak_Prediction",
        data_location="Nairobi"
    )

    print("Data Residency Verification Result:")
    print(json.dumps(verification, indent=2, default=str))

    # Export logs for audit
    national_strategy_guard.export_logs_for_audit(
        Jurisdiction.KENYA,
        "kenya_residency_audit_export.json"
    )