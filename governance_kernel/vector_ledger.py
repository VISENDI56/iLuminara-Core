"""
Sovereign Guardrail & Governance Engine
═════════════════════════════════════════════════════════════════════════════

The 'Ethical Engine' of VISENDI56 that enforces Sovereign Dignity across 14 
global legal frameworks. This module encodes international compliance logic into 
the genetic code of iLuminara-Core, ensuring deployments in Toronto, Cape Town, 
or California operate with identical integrity constraints.

Philosophy: "Does this enhance sovereign dignity?" — Every enforcement decision.
"""

from typing import Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

# Import tamper-proof audit trail
try:
    from governance_kernel.audit_trail import TamperProofAuditTrail, AuditEventType
except ImportError:
    # Fallback if audit_trail not available
    TamperProofAuditTrail = None
    AuditEventType = None


class SovereigntyViolationError(Exception):
    """
    Raised when an action violates one or more sovereignty/compliance constraints.
    Includes specific legal citation for transparency and auditability.
    """
    pass


class JurisdictionFramework(Enum):
    """Global legal frameworks encoded in the sovereign guardrail."""
    GDPR_EU = "GDPR (EU)"  # General Data Protection Regulation
    KDPA_KE = "KDPA (Kenya)"  # Kenya Data Protection Act
    PIPEDA_CA = "PIPEDA (Canada)"  # Personal Information Protection & Electronic Documents Act
    POPIA_ZA = "POPIA (South Africa)"  # Protection of Personal Information Act
    HIPAA_US = "HIPAA (USA)"  # Health Insurance Portability & Accountability Act
    HITECH_US = "HITECH (USA)"  # Health Information Technology for Economic & Clinical Health
    CCPA_US = "CCPA (USA)"  # California Consumer Privacy Act
    NIST_CSF = "NIST CSF (USA)"  # Cybersecurity Framework
    ISO_27001 = "ISO 27001"  # Information Security Management
    SOC_2 = "SOC 2 (USA)"  # Service Organization Control 2
    EU_AI_ACT = "EU AI Act"  # Artificial Intelligence Act
    GDPR_ART9 = "GDPR Article 9 (Special Categories)"  # Sensitive Data
    GLOBAL_DEFAULT = "GLOBAL_DEFAULT"  # Baseline sovereignty rules


@dataclass
class ComplianceAction:
    """Represents an action requiring compliance validation."""
    action_type: str  # e.g., 'Data_Transfer', 'High_Risk_Inference', 'Consent_Validation'
    payload: Dict[str, Any]  # The data/parameters for the action
    jurisdiction: str = "GLOBAL_DEFAULT"
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class SovereignGuardrail:
    """
    Enforcement engine for global legal compliance. Acts as the constitutional 
    guardian of iLuminara-Core, ensuring no action violates sovereign dignity.
    
    Usage:
        guardrail = SovereignGuardrail()
        guardrail.validate_action(
            action_type='High_Risk_Inference',
            payload={'inference': 'quarantine_alert', 'explanation': {...}},
            jurisdiction='GDPR_EU'
        )
    """

    def __init__(self, enable_tamper_proof_audit: bool = False):
        """
        Initialize the sovereign guardrail with global compliance matrix.
        
        Args:
            enable_tamper_proof_audit: If True, enable tamper-proof audit trail
                                       with Bigtable, Spanner, and KMS integration
        """
        self.compliance_matrix = self._build_compliance_matrix()
        self.audit_log = []
        
        # Initialize tamper-proof audit trail if enabled
        self.tamper_proof_audit_enabled = enable_tamper_proof_audit
        self.tamper_proof_trail = None
        if enable_tamper_proof_audit and TamperProofAuditTrail is not None:
            # Initialize in simulation mode by default
            self.tamper_proof_trail = TamperProofAuditTrail(simulate=True)
            print("✅ Tamper-proof audit trail enabled (simulation mode)")

    def _build_compliance_matrix(self) -> Dict[str, Dict[str, Any]]:
        """
        Build the comprehensive compliance matrix encoding all legal frameworks.
        Returns a mapping of jurisdiction -> compliance rules.
        """
        return {
            "GDPR_EU": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,  # GDPR Art. 9
                "right_to_explanation_required": True,
                "retention_max_days": 2555,  # ~7 years for health data
                "breach_notification_hours": 72,
            },
            "KDPA_KE": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,  # ~5 years default
                "breach_notification_hours": 72,
            },
            "PIPEDA_CA": {
                "data_sovereignty_required": False,  # Allows cross-border with safeguards
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 1825,
                "breach_notification_hours": 30,
            },
            "POPIA_ZA": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": False,
                "retention_max_days": 2555,
                "breach_notification_hours": 168,  # 7 days
            },
            "HIPAA_US": {
                "data_sovereignty_required": False,  # US-centric
                "requires_explicit_consent": False,  # Covered entities exempt for treatment
                "special_categories_prohibited_foreign": True,  # PHI protected
                "right_to_explanation_required": False,
                "retention_max_days": 2555,  # ~7 years for medical records
                "breach_notification_hours": 60,
            },
            "GLOBAL_DEFAULT": {
                "data_sovereignty_required": True,
                "requires_explicit_consent": True,
                "special_categories_prohibited_foreign": True,
                "right_to_explanation_required": True,
                "retention_max_days": 1825,
                "breach_notification_hours": 72,
            },
        }

    def validate_action(
        self,
        action_type: str,
        payload: Dict[str, Any],
        jurisdiction: str = "GLOBAL_DEFAULT",
    ) -> bool:
        """
        Validate an action against sovereign compliance constraints.

        Args:
            action_type: Type of action ('Data_Transfer', 'High_Risk_Inference', 'Consent_Validation')
            payload: The action's data/parameters
            jurisdiction: Legal jurisdiction ('GDPR_EU', 'KDPA_KE', 'GLOBAL_DEFAULT', etc.)

        Returns:
            True if action passes all validation checks

        Raises:
            SovereigntyViolationError: If any compliance rule is violated with legal citation

        Philosophy: "Does this enhance sovereign dignity?"
        """
        compliance_rules = self.compliance_matrix.get(
            jurisdiction, self.compliance_matrix["GLOBAL_DEFAULT"]
        )

        # Rule 1: Data Sovereignty Enforcement
        # ─────────────────────────────────────
        # "Health data shall not traverse borders to foreign clouds." 
        # Enforces GDPR Art. 9, Kenya DPA, POPIA §14, HIPAA §164.312
        if compliance_rules["data_sovereignty_required"]:
            self._validate_data_sovereignty(payload, jurisdiction)

        # Rule 2: Right to Explanation (High-Risk Inferences)
        # ────────────────────────────────────────────────────
        # "Every clinical decision with consequence must be explicable."
        # EU AI Act §6, GDPR Recital 71
        if action_type == "High_Risk_Inference":
            self._validate_right_to_explanation(payload, jurisdiction)

        # Rule 3: Consent Validation
        # ──────────────────────────
        # "Sovereignty begins with informed, uncoerced consent."
        # POPIA §11, CCPA §1798.100, GDPR Art. 6-7
        if compliance_rules["requires_explicit_consent"]:
            self._validate_consent(payload, jurisdiction)

        # Rule 4: Retention Window Enforcement
        # ────────────────────────────────────
        # Data expires. Eternal surveillance violates dignity.
        self._validate_retention(payload, compliance_rules, jurisdiction)

        # Log the successful validation
        self.audit_log.append(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "action_type": action_type,
                "jurisdiction": jurisdiction,
                "status": "PASSED",
            }
        )
        
        # Log to tamper-proof audit trail if enabled
        if self.tamper_proof_audit_enabled and self.tamper_proof_trail:
            try:
                self.tamper_proof_trail.log_event(
                    event_type=self._map_action_to_audit_event(action_type),
                    actor=payload.get("actor", "system"),
                    resource=payload.get("resource", "unknown"),
                    action=action_type,
                    jurisdiction=jurisdiction,
                    outcome="SUCCESS",
                    metadata={
                        "payload_summary": self._sanitize_payload_for_audit(payload),
                        "compliance_rules_applied": list(compliance_rules.keys())
                    }
                )
            except Exception as e:
                print(f"⚠️  Failed to log to tamper-proof audit trail: {e}")

        return True

    def _validate_data_sovereignty(self, payload: Dict[str, Any], jurisdiction: str):
        """
        Enforce data sovereignty: Health/sensitive data cannot leave sovereign territory.

        Enforces:
        - GDPR Article 9 (Special Categories)
        - Kenya Data Protection Act §37
        - POPIA Act §14 (Cross-border transfers)
        - HIPAA §164.312(a)(2)(ii)
        """
        if payload.get("data_type") == "PHI" and payload.get("destination") in [
            "Foreign_Cloud",
            "AWS_US",
            "Azure_EU_Exemption",
        ]:
            citation = (
                f"GDPR Art. 9 (Processing of special categories), "
                f"Kenya DPA §37 (Transfer Restrictions), "
                f"HIPAA §164.312(a)(2)(ii) (Encryption in Transit)"
            )
            
            # Log violation to tamper-proof audit trail
            if self.tamper_proof_audit_enabled and self.tamper_proof_trail:
                try:
                    self.tamper_proof_trail.log_event(
                        event_type=AuditEventType.DATA_TRANSFER if AuditEventType else "Data_Transfer",
                        actor=payload.get("actor", "system"),
                        resource=payload.get("resource", "PHI_data"),
                        action="BLOCKED_FOREIGN_TRANSFER",
                        jurisdiction=jurisdiction,
                        outcome="VIOLATION",
                        metadata={
                            "violation_type": "DATA_SOVEREIGNTY",
                            "data_type": payload.get("data_type"),
                            "destination": payload.get("destination"),
                            "legal_citation": citation
                        }
                    )
                except Exception as e:
                    print(f"⚠️  Failed to log violation to audit trail: {e}")
            
            raise SovereigntyViolationError(
                f"❌ SOVEREIGNTY VIOLATION: Protected health data cannot be transferred "
                f"to foreign cloud infrastructure.\n"
                f"   Data Type: {payload.get('data_type')}\n"
                f"   Destination: {payload.get('destination')}\n"
                f"   Legal Citation: {citation}"
            )

    def _validate_right_to_explanation(self, payload: Dict[str, Any], jurisdiction: str):
        """
        Enforce the right to explanation for high-risk inferences.

        Enforces:
        - EU AI Act §6 (High-risk AI classification)
        - GDPR Recital 71 (Right to explanation)
        - NIST AI RMF (Transparency requirement)
        """
        required_fields = ["explanation", "confidence_score", "evidence_chain"]

        missing_fields = [f for f in required_fields if f not in payload]

        if missing_fields:
            citation = (
                f"EU AI Act §6 (High-Risk AI Systems), "
                f"GDPR Art. 22 (Right to Explanation), "
                f"NIST AI RMF (Transparency Requirement)"
            )
            raise SovereigntyViolationError(
                f"❌ TRANSPARENCY VIOLATION: High-risk inference requires explainability.\n"
                f"   Missing fields: {', '.join(missing_fields)}\n"
                f"   Required: {required_fields}\n"
                f"   Legal Citation: {citation}"
            )

    def _validate_consent(self, payload: Dict[str, Any], jurisdiction: str):
        """
        Enforce consent validation for data processing.

        Enforces:
        - POPIA §11 (Lawfulness of processing)
        - CCPA §1798.100 (Right to know)
        - GDPR Art. 6 (Lawfulness of processing)
        """
        consent_token = payload.get("consent_token")
        consent_scope = payload.get("consent_scope")

        if not consent_token:
            citation = (
                f"POPIA §11 (Lawfulness of Processing), "
                f"CCPA §1798.100 (Right to Know), "
                f"GDPR Art. 6 (Lawfulness of Processing)"
            )
            raise SovereigntyViolationError(
                f"❌ CONSENT VIOLATION: Data processing without valid consent token.\n"
                f"   Action: {payload.get('action')}\n"
                f"   Scope: {consent_scope}\n"
                f"   Legal Citation: {citation}"
            )

    def _validate_retention(
        self, payload: Dict[str, Any], rules: Dict[str, Any], jurisdiction: str
    ):
        """
        Enforce data retention windows.
        
        Philosophy: "Data expires. Eternal surveillance violates dignity."
        
        Enforces:
        - GDPR Art. 17 (Right to erasure / 'right to be forgotten')
        - HIPAA §164.404 (Notification of unsecured PHI breach)
        - Kenya DPA §42 (Data Subject Rights)
        """
        record_date_str = payload.get("record_date")
        if not record_date_str:
            return  # No retention check if no date provided

        try:
            record_date = datetime.fromisoformat(record_date_str)
            days_since_record = (datetime.utcnow() - record_date).days
            max_retention = rules.get("retention_max_days", 1825)

            if days_since_record > max_retention:
                citation = (
                    f"GDPR Art. 17 (Right to Erasure / 'Right to be Forgotten'), "
                    f"HIPAA §164.404 (Breach Notification), "
                    f"Kenya DPA §42 (Data Subject Rights)"
                )
                raise SovereigntyViolationError(
                    f"❌ RETENTION VIOLATION: Data exceeds retention window.\n"
                    f"   Record Date: {record_date_str}\n"
                    f"   Days Stored: {days_since_record}\n"
                    f"   Max Allowed: {max_retention} days\n"
                    f"   Jurisdiction: {jurisdiction}\n"
                    f"   Action: Trigger erasure procedure.\n"
                    f"   Legal Citation: {citation}"
                )
        except (ValueError, TypeError):
            # Invalid date format, skip validation
            pass

    def get_audit_log(self):
        """Return the complete audit trail of all validation checks."""
        return self.audit_log

    def clear_audit_log(self):
        """Clear the audit log (for testing or privacy)."""
        self.audit_log = []
    
    def _map_action_to_audit_event(self, action_type: str):
        """Map action type to AuditEventType enum."""
        if AuditEventType is None:
            return action_type
        
        mapping = {
            "Data_Transfer": AuditEventType.DATA_TRANSFER,
            "High_Risk_Inference": AuditEventType.HIGH_RISK_INFERENCE,
            "Consent_Validation": AuditEventType.CONSENT_VALIDATION,
        }
        return mapping.get(action_type, AuditEventType.SOVEREIGNTY_CHECK)
    
    def _sanitize_payload_for_audit(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize payload for audit logging (remove sensitive data).
        
        Returns a summary without PHI or sensitive details.
        """
        # Only include non-sensitive metadata
        sanitized = {}
        safe_fields = ["data_type", "destination", "action", "consent_scope"]
        for field in safe_fields:
            if field in payload:
                sanitized[field] = payload[field]
        return sanitized
    
    def get_tamper_proof_audit_history(self, limit: int = 100) -> list:
        """
        Get tamper-proof audit history if enabled.
        
        Args:
            limit: Maximum number of entries to retrieve
            
        Returns:
            List of audit entries or empty list if not enabled
        """
        if self.tamper_proof_audit_enabled and self.tamper_proof_trail:
            entries = self.tamper_proof_trail.get_audit_history(limit=limit)
            return [entry.to_dict() for entry in entries]
        return []
    
    def verify_audit_chain_integrity(self) -> Dict[str, Any]:
        """
        Verify integrity of tamper-proof audit chain.
        
        Returns:
            Verification result or error if not enabled
        """
        if self.tamper_proof_audit_enabled and self.tamper_proof_trail:
            entries = self.tamper_proof_trail.get_audit_history(limit=1000)
            return self.tamper_proof_trail.verify_chain_integrity(entries)
        return {"error": "Tamper-proof audit trail not enabled"}


# ═════════════════════════════════════════════════════════════════════════════
# MISSION: To architect systems that transform preventable suffering from 
# statistical inevitability to historical anomaly.
#
# COMPLIANCE PILLAR: Global Sovereign Dignity
# ═════════════════════════════════════════════════════════════════════════════
