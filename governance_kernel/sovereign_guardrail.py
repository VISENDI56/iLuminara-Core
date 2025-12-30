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

import json
import datetime
import hashlib
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

class PrivacyRole(Enum):
    """ISO 27701 Privacy Roles"""
    CONTROLLER = "controller"
    PROCESSOR = "processor"
    JOINT_CONTROLLER = "joint_controller"

class ConsentStatus(Enum):
    """Consent Management Status"""
    GIVEN = "given"
    WITHDRAWN = "withdrawn"
    EXPIRED = "expired"
    PENDING = "pending"

@dataclass
class PrivacyConsent:
    """ISO 27701 Consent Record"""
    consent_id: str
    individual_id: str
    purpose: str
    data_categories: List[str]
    processing_activities: List[str]
    status: ConsentStatus
    given_date: datetime.datetime
    expiry_date: Optional[datetime.datetime] = None
    withdrawal_date: Optional[datetime.datetime] = None
    legal_basis: str = "consent"

@dataclass
class BreachRecord:
    """ISO 27701 Breach Response Record"""
    breach_id: str
    detection_date: datetime.datetime
    description: str
    data_categories_affected: List[str]
    individuals_affected: int
    risk_assessment: str
    notification_sent: bool = False
    notification_date: Optional[datetime.datetime] = None
    corrective_actions: List[str] = field(default_factory=list)

class SovereignGuardrail:
    """
    The Omni-Law Enforcer with ISO 27701 Privacy Extensions.
    Checks payloads against the 'sectoral_laws.json' database.
    Extended with Privacy Information Management System (PIMS) controls.
    """
    def __init__(self):
        with open("governance_kernel/sectoral_laws.json", "r") as f:
            self.laws = json.load(f)
        # Mock Sanctions Database
        self.sanctions_db = ["SC-9982", "TERROR-ORG-01"]

        # ISO 27701 Privacy Extensions
        self.privacy_role = PrivacyRole.CONTROLLER
        self.consent_records: Dict[str, PrivacyConsent] = {}
        self.breach_records: List[BreachRecord] = {}
        self.privacy_impact_assessments: Dict[str, Dict] = {}
        self.data_minimization_rules: Dict[str, List[str]] = {
            "health_data": ["necessary_identifiers_only", "anonymize_when_possible"],
            "surveillance_data": ["temporal_limits", "geographic_bounds"],
            "genai_training": ["opt_out_respected", "purpose_limitation"]
        }

    def check_sectoral_compliance(self, context, payload):
        """
        Universal check: Iterates through laws relevant to the context.
        Enhanced with ISO 27701 privacy controls.
        """
        compliance_report = {"status": "PASS", "alerts": [], "actions_taken": []}

        # ISO 27701 Privacy Checks First
        privacy_check = self._check_privacy_compliance(context, payload)
        if privacy_check["status"] != "PASS":
            compliance_report["status"] = privacy_check["status"]
            compliance_report["alerts"].extend(privacy_check["alerts"])

        # 1. SUPPLY CHAIN CHECKS
        if context == "SUPPLY_CHAIN":
            if payload.get("origin") == "XUAR": # UFLPA Logic
                compliance_report["status"] = "BLOCKED"
                compliance_report["alerts"].append(self.laws["SUPPLY_CHAIN"]["UFLPA"]["alert"])
            if payload.get("material") in ['Tin', 'Gold'] and not payload.get("audit_proof"): # Dodd-Frank
                compliance_report["alerts"].append(self.laws["SUPPLY_CHAIN"]["DODD_FRANK_1502"]["alert"])

        # 2. FINANCE CHECKS
        if context == "FINANCE":
            if payload.get("payee_id") in self.sanctions_db: # OFAC Logic
                compliance_report["status"] = "FROZEN"
                compliance_report["alerts"].append(self.laws["FINANCE"]["OFAC"]["alert"])

        # 3. ESG CHECKS
        if context == "LOGISTICS" and payload.get("destination") == "EU":
            # CBAM Logic
            emissions = self.calculate_cbam_emissions(payload)
            compliance_report["actions_taken"].append(f"CBAM Report Generated: {emissions}kg CO2")

        # 4. PHARMA CHECKS
        if context == "CLINICAL":
            # EU MDR Logic
            compliance_report["actions_taken"].append("Logged to Post-Market Surveillance (PMS) Ledger")

        return compliance_report

    def _check_privacy_compliance(self, context: str, payload: Dict) -> Dict:
        """ISO 27701 Privacy Compliance Check"""
        privacy_report = {"status": "PASS", "alerts": [], "actions_taken": []}

        # Check data minimization
        if context in self.data_minimization_rules:
            minimization_check = self._enforce_data_minimization(context, payload)
            if not minimization_check["compliant"]:
                privacy_report["status"] = "BLOCKED"
                privacy_report["alerts"].extend(minimization_check["violations"])

        # Check consent for personal data processing
        if self._contains_personal_data(payload):
            consent_check = self._verify_consent(payload)
            if not consent_check["valid"]:
                privacy_report["status"] = "BLOCKED"
                privacy_report["alerts"].extend(consent_check["issues"])

        # Privacy by design assessment
        if context in ["surveillance", "genai", "health_monitoring"]:
            pbd_check = self._assess_privacy_by_design(context, payload)
            privacy_report["actions_taken"].extend(pbd_check["recommendations"])

        return privacy_report

    def _enforce_data_minimization(self, context: str, payload: Dict) -> Dict:
        """Enforce data minimization principles per ISO 27701"""
        rules = self.data_minimization_rules.get(context, [])
        violations = []

        for rule in rules:
            if rule == "necessary_identifiers_only":
                if "unnecessary_pii" in payload:
                    violations.append("Unnecessary PII detected in payload")
            elif rule == "anonymize_when_possible":
                if "direct_identifiers" in payload and not payload.get("anonymized", False):
                    violations.append("Direct identifiers present without anonymization")
            elif rule == "temporal_limits":
                if "retention_period" in payload and payload["retention_period"] > 365:
                    violations.append("Data retention exceeds 1 year limit")
            elif rule == "geographic_bounds":
                if "location_data" in payload and not payload.get("geographic_bounds_applied", False):
                    violations.append("Geographic bounds not applied to location data")

        return {
            "compliant": len(violations) == 0,
            "violations": violations
        }

    def _contains_personal_data(self, payload: Dict) -> bool:
        """Check if payload contains personal data"""
        personal_data_indicators = [
            "individual_id", "name", "email", "phone", "address",
            "health_data", "biometric_data", "genetic_data"
        ]
        return any(key in payload for key in personal_data_indicators)

    def _verify_consent(self, payload: Dict) -> Dict:
        """Verify consent for personal data processing"""
        issues = []
        individual_id = payload.get("individual_id")

        if not individual_id:
            return {"valid": False, "issues": ["No individual identifier for consent verification"]}

        # Check if consent exists and is valid
        consent = self.consent_records.get(individual_id)
        if not consent:
            issues.append(f"No consent record found for individual {individual_id}")
        elif consent.status != ConsentStatus.GIVEN:
            issues.append(f"Consent status is {consent.status.value}")
        elif consent.expiry_date and datetime.datetime.now() > consent.expiry_date:
            issues.append("Consent has expired")
            consent.status = ConsentStatus.EXPIRED

        # Check if processing purpose matches consented purpose
        if consent and payload.get("purpose") not in consent.processing_activities:
            issues.append("Processing purpose not covered by consent")

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }

    def _assess_privacy_by_design(self, context: str, payload: Dict) -> Dict:
        """Assess privacy by design implementation"""
        recommendations = []

        if context == "surveillance":
            if not payload.get("privacy_impact_assessment_completed", False):
                recommendations.append("Conduct Privacy Impact Assessment for surveillance activity")
            if not payload.get("data_protection_officer_consulted", False):
                recommendations.append("Consult Data Protection Officer")

        elif context == "genai":
            if not payload.get("differential_privacy_applied", False):
                recommendations.append("Apply differential privacy to training data")
            if payload.get("model_memory", 0) > 1000000:  # Arbitrary threshold
                recommendations.append("Implement model compression to reduce data exposure")

        return {"recommendations": recommendations}

    def record_consent(self, consent: PrivacyConsent) -> str:
        """Record privacy consent per ISO 27701"""
        self.consent_records[consent.individual_id] = consent
        return consent.consent_id

    def withdraw_consent(self, individual_id: str, reason: str) -> bool:
        """Process consent withdrawal"""
        if individual_id not in self.consent_records:
            return False

        consent = self.consent_records[individual_id]
        consent.status = ConsentStatus.WITHDRAWN
        consent.withdrawal_date = datetime.datetime.now()

        # Log withdrawal for audit
        self._log_privacy_event("consent_withdrawal", {
            "individual_id": individual_id,
            "reason": reason,
            "timestamp": consent.withdrawal_date.isoformat()
        })

        return True

    def report_privacy_breach(self, breach: BreachRecord) -> str:
        """Report privacy breach per ISO 27701 requirements"""
        self.breach_records.append(breach)

        # Automatic risk assessment
        breach.risk_assessment = self._assess_breach_risk(breach)

        # Trigger notification if high risk
        if breach.risk_assessment in ["high", "critical"]:
            self._trigger_breach_notification(breach)

        return breach.breach_id

    def _assess_breach_risk(self, breach: BreachRecord) -> str:
        """Assess breach risk level"""
        risk_score = 0

        # Risk factors
        if breach.individuals_affected > 1000:
            risk_score += 3
        elif breach.individuals_affected > 100:
            risk_score += 2

        if "health_data" in breach.data_categories_affected:
            risk_score += 2
        if "genetic_data" in breach.data_categories_affected:
            risk_score += 3

        # Determine risk level
        if risk_score >= 5:
            return "critical"
        elif risk_score >= 3:
            return "high"
        elif risk_score >= 1:
            return "medium"
        else:
            return "low"

    def _trigger_breach_notification(self, breach: BreachRecord):
        """Trigger breach notification workflow"""
        breach.notification_sent = True
        breach.notification_date = datetime.datetime.now()

        # In a real system, this would trigger:
        # 1. Notification to supervisory authority within 72 hours
        # 2. Notification to affected individuals
        # 3. Internal incident response

        self._log_privacy_event("breach_notification", {
            "breach_id": breach.breach_id,
            "notification_date": breach.notification_date.isoformat(),
            "individuals_affected": breach.individuals_affected
        })

    def _log_privacy_event(self, event_type: str, details: Dict):
        """Log privacy-related events for audit"""
        # In production, this would write to secure audit log
        print(f"PRIVACY EVENT: {event_type} - {json.dumps(details, default=str)}")

    def calculate_cbam_emissions(self, payload):
        # Simple Mock Calculation
        distance = payload.get("distance_km", 0)
        weight = payload.get("weight_kg", 0)
        return (distance * weight * 0.001) # Mock factor

if __name__ == "__main__":
    guard = SovereignGuardrail()
    # Test 1: OFAC Sanction
    print("Testing OFAC Sanctions...")
    res = guard.check_sectoral_compliance("FINANCE", {"payee_id": "SC-9982", "amount": 1000})
    print(res)
    # Test 2: UFLPA Violation
    print("\nTesting UFLPA Supply Chain...")
    res = guard.check_sectoral_compliance("SUPPLY_CHAIN", {"origin": "XUAR", "item": "Sensor"})
    print(res)
