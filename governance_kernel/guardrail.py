"""
Sovereign Guardrail v3.0
═════════════════════════════════════════════════════════════════════════════

The enforcement layer that routes all operations through the 45-Law Quantum Nexus,
ensuring real-time regulatory compliance with auto-correction capabilities.

This module implements:
- validate_operation: Routes data through 45-law compliance checks
- trigger_pandemic_emergency: IHR 2005 emergency response activation
- check_ai_conformity: EU AI Act risk pyramid validation

Philosophy: "Every operation. Every regulation. No exceptions."
"""

import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

from .rco_engine import RegenerativeComplianceOracle, RegulatorySignal

logger = logging.getLogger(__name__)


class ComplianceViolation(Exception):
    """Raised when an operation violates regulatory requirements."""
    pass


class OperationStatus(Enum):
    """Status of operation validation."""
    APPROVED = "approved"
    REJECTED = "rejected"
    CONDITIONAL = "conditional"
    EMERGENCY_OVERRIDE = "emergency_override"


@dataclass
class ValidationResult:
    """Result of operation validation."""
    status: OperationStatus
    law_checks: Dict[str, bool]
    violations: List[str]
    requirements: List[str]
    risk_score: float
    timestamp: datetime
    emergency_mode: bool = False


class SovereignGuardrail:
    """
    Main guardrail class that enforces the 45-Law Quantum Nexus
    on all system operations.
    """
    
    def __init__(self, rco_engine: Optional[RegenerativeComplianceOracle] = None):
        """
        Initialize the Sovereign Guardrail.
        
        Args:
            rco_engine: RegenerativeComplianceOracle instance (creates new if None)
        """
        self.rco = rco_engine or RegenerativeComplianceOracle()
        self.emergency_mode = False
        self.validation_history: List[ValidationResult] = []
        logger.info("SovereignGuardrail v3.0 initialized")
    
    def validate_operation(
        self, 
        sector: str, 
        payload: Dict[str, Any]
    ) -> ValidationResult:
        """
        Validate an operation against all applicable laws in the 45-Law Nexus.
        
        Args:
            sector: Sector of operation (e.g., "healthcare", "finance", "ai_deployment")
            payload: Operation data including context, parameters, and metadata
            
        Returns:
            ValidationResult with compliance status and requirements
        """
        timestamp = datetime.now(timezone.utc)
        law_checks = {}
        violations = []
        requirements = []
        
        logger.info(f"Validating operation in sector: {sector}")
        
        # Load sectoral laws
        laws_registry = self.rco.patch_generator.laws_registry
        laws = laws_registry.get("45_law_quantum_nexus", {}).get("laws", {})
        
        # Check each applicable law
        for law_key, law_data in laws.items():
            if self._is_law_applicable(law_data, sector, payload):
                check_result = self._check_law_compliance(law_key, law_data, payload)
                law_checks[law_data.get("id", law_key)] = check_result["compliant"]
                
                if not check_result["compliant"]:
                    violations.extend(check_result["violations"])
                
                requirements.extend(check_result["requirements"])
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(law_checks, violations)
        
        # Determine status
        if violations and not self.emergency_mode:
            status = OperationStatus.REJECTED
        elif requirements and not all(law_checks.values()):
            status = OperationStatus.CONDITIONAL
        elif self.emergency_mode:
            status = OperationStatus.EMERGENCY_OVERRIDE
        else:
            status = OperationStatus.APPROVED
        
        result = ValidationResult(
            status=status,
            law_checks=law_checks,
            violations=violations,
            requirements=requirements,
            risk_score=risk_score,
            timestamp=timestamp,
            emergency_mode=self.emergency_mode
        )
        
        self.validation_history.append(result)
        
        logger.info(f"Validation complete: {status.value}, risk_score: {risk_score:.2f}")
        
        return result
    
    def _is_law_applicable(
        self, 
        law_data: Dict[str, Any], 
        sector: str, 
        payload: Dict[str, Any]
    ) -> bool:
        """
        Determine if a law is applicable to the operation.
        
        Args:
            law_data: Law details from registry
            sector: Operation sector
            payload: Operation payload
            
        Returns:
            True if law applies
        """
        trigger = law_data.get("trigger_condition", {})
        trigger_type = trigger.get("type", "")
        params = trigger.get("parameters", {})
        
        # Check sector match
        if "sector" in params:
            if isinstance(params["sector"], list):
                if sector not in params["sector"]:
                    return False
            elif sector != params["sector"]:
                return False
        
        # Check location/jurisdiction
        if "data_subject_location" in params:
            payload_location = payload.get("location", "")
            if payload_location and payload_location not in params["data_subject_location"]:
                return False
        
        # Check entity type
        if "entity_type" in params:
            payload_entity = payload.get("entity_type", "")
            if payload_entity:
                entity_types = params["entity_type"]
                if isinstance(entity_types, list):
                    if payload_entity not in entity_types:
                        return False
                elif payload_entity != entity_types:
                    return False
        
        # Check risk threshold for AI operations
        if "risk_score_threshold" in params:
            risk_score = payload.get("risk_score", 0.0)
            if risk_score < params["risk_score_threshold"]:
                return False
        
        return True
    
    def _check_law_compliance(
        self, 
        law_key: str, 
        law_data: Dict[str, Any], 
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check compliance with a specific law.
        
        Args:
            law_key: Law key in registry
            law_data: Law details
            payload: Operation payload
            
        Returns:
            Dictionary with compliance status and details
        """
        enforcement = law_data.get("enforcement_action", {})
        requirements = enforcement.get("requirements", [])
        validation_method = enforcement.get("validation", "")
        
        violations = []
        met_requirements = []
        
        # Check each requirement
        for req in requirements:
            req_key = req.lower().replace(" ", "_").replace("-", "_")
            if req_key in payload.get("compliance_evidence", {}):
                met_requirements.append(req)
            else:
                violations.append(f"Missing requirement: {req}")
        
        compliant = len(violations) == 0
        
        return {
            "compliant": compliant,
            "violations": violations,
            "requirements": requirements,
            "met_requirements": met_requirements,
            "validation_method": validation_method
        }
    
    def _calculate_risk_score(
        self, 
        law_checks: Dict[str, bool], 
        violations: List[str]
    ) -> float:
        """
        Calculate overall risk score for the operation.
        
        Args:
            law_checks: Dictionary of law compliance checks
            violations: List of violations
            
        Returns:
            Risk score from 0.0 (low risk) to 1.0 (high risk)
        """
        if not law_checks:
            return 0.0
        
        # Base risk from failed checks
        failed_checks = sum(1 for compliant in law_checks.values() if not compliant)
        total_checks = len(law_checks)
        check_risk = failed_checks / total_checks if total_checks > 0 else 0.0
        
        # Additional risk from violation count
        violation_risk = min(len(violations) * 0.1, 0.5)
        
        total_risk = min(check_risk + violation_risk, 1.0)
        
        return total_risk
    
    def trigger_pandemic_emergency(
        self, 
        outbreak_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Trigger pandemic emergency response under IHR 2005.
        
        Args:
            outbreak_data: Data about the outbreak including:
                - cases: Number of cases
                - timeframe_hours: Time window for cases
                - geographic_spread: Geographic extent
                - disease_pattern: Description of disease characteristics
                
        Returns:
            Dictionary with emergency activation status and required actions
        """
        logger.warning("PANDEMIC EMERGENCY ACTIVATION REQUESTED")
        
        # Validate outbreak criteria
        cases = outbreak_data.get("cases", 0)
        timeframe = outbreak_data.get("timeframe_hours", 0)
        spread = outbreak_data.get("geographic_spread", "")
        
        # Check IHR 2005 thresholds
        meets_threshold = (
            cases >= 10 and 
            timeframe <= 24 and 
            spread in ["multi_region", "international"]
        )
        
        response = {
            "emergency_activated": meets_threshold,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "outbreak_assessment": {
                "cases": cases,
                "timeframe_hours": timeframe,
                "geographic_spread": spread,
                "meets_ihr_threshold": meets_threshold
            },
            "actions_required": [],
            "data_sharing_override": False
        }
        
        if meets_threshold:
            # Activate emergency mode
            self.emergency_mode = True
            response["data_sharing_override"] = True
            
            # IHR 2005 required actions
            response["actions_required"] = [
                "immediate_notification_to_who",
                "contact_tracing_activation",
                "quarantine_protocols",
                "emergency_resource_allocation",
                "cross_border_coordination"
            ]
            
            # Create regulatory signal for RCO
            signal = RegulatorySignal(
                source="IHR_2005_Emergency",
                signal_type="emergency",
                jurisdiction="Global",
                content=f"Pandemic emergency declared: {cases} cases in {timeframe}h",
                confidence_score=1.0
            )
            
            self.rco.predict_amendment(signal)
            
            logger.critical(
                f"PANDEMIC EMERGENCY ACTIVATED: {cases} cases, "
                f"{timeframe}h, {spread} spread"
            )
        else:
            logger.info("Outbreak does not meet IHR 2005 emergency threshold")
        
        return response
    
    def check_ai_conformity(
        self, 
        ai_system: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check AI system conformity with EU AI Act risk pyramid.
        
        Args:
            ai_system: AI system details including:
                - purpose: Purpose of the AI system
                - sector: Deployment sector
                - capabilities: List of capabilities
                - risk_assessment: Risk assessment data
                
        Returns:
            Dictionary with conformity assessment and requirements
        """
        logger.info("Performing EU AI Act conformity check")
        
        purpose = ai_system.get("purpose", "")
        sector = ai_system.get("sector", "")
        capabilities = ai_system.get("capabilities", [])
        
        # Determine risk level
        risk_level = self._assess_ai_risk_level(purpose, sector, capabilities)
        
        conformity = {
            "risk_level": risk_level,
            "conformity_status": "pending",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "requirements": [],
            "prohibited": False
        }
        
        # Unacceptable risk - prohibited
        if risk_level == "unacceptable":
            conformity["conformity_status"] = "prohibited"
            conformity["prohibited"] = True
            conformity["reason"] = "AI system falls under prohibited category per EU AI Act"
            logger.error(f"AI system PROHIBITED: {purpose}")
        
        # High risk - strict requirements
        elif risk_level == "high":
            conformity["requirements"] = [
                "risk_assessment",
                "data_governance",
                "technical_documentation",
                "human_oversight",
                "accuracy_metrics",
                "cybersecurity_measures",
                "conformity_assessment"
            ]
            conformity["conformity_status"] = "requires_assessment"
            logger.warning(f"HIGH-RISK AI system requires full conformity assessment")
        
        # Limited risk - transparency requirements
        elif risk_level == "limited":
            conformity["requirements"] = [
                "transparency_disclosure",
                "user_notification",
                "documentation"
            ]
            conformity["conformity_status"] = "transparency_required"
        
        # Minimal risk - no special requirements
        else:
            conformity["conformity_status"] = "approved"
            conformity["requirements"] = []
        
        # Check if requirements are met
        if conformity["requirements"]:
            evidence = ai_system.get("compliance_evidence", {})
            met_requirements = [
                req for req in conformity["requirements"]
                if req in evidence
            ]
            conformity["requirements_met"] = met_requirements
            conformity["requirements_pending"] = [
                req for req in conformity["requirements"]
                if req not in evidence
            ]
        
        return conformity
    
    def _assess_ai_risk_level(
        self, 
        purpose: str, 
        sector: str, 
        capabilities: List[str]
    ) -> str:
        """
        Assess AI system risk level according to EU AI Act.
        
        Args:
            purpose: Purpose of AI system
            sector: Deployment sector
            capabilities: System capabilities
            
        Returns:
            Risk level: "unacceptable", "high", "limited", or "minimal"
        """
        purpose_lower = purpose.lower()
        
        # Unacceptable risk patterns
        unacceptable_patterns = [
            "social_scoring",
            "social scoring",
            "real_time_biometric",
            "manipulative",
            "subliminal"
        ]
        
        for pattern in unacceptable_patterns:
            if pattern in purpose_lower:
                return "unacceptable"
        
        # High risk sectors
        high_risk_sectors = [
            "healthcare",
            "critical_infrastructure",
            "law_enforcement",
            "education",
            "employment",
            "border_control"
        ]
        
        if sector in high_risk_sectors:
            return "high"
        
        # High risk capabilities
        high_risk_capabilities = [
            "biometric_identification",
            "emotion_recognition",
            "medical_diagnosis",
            "automated_decision_making"
        ]
        
        for cap in capabilities:
            if cap in high_risk_capabilities:
                return "high"
        
        # Limited risk patterns
        limited_risk_patterns = [
            "chatbot",
            "deepfake",
            "synthetic_media",
            "emotion_detection"
        ]
        
        for pattern in limited_risk_patterns:
            if pattern in purpose_lower:
                return "limited"
        
        # Default to minimal risk
        return "minimal"
    
    def deactivate_emergency_mode(self) -> bool:
        """
        Deactivate emergency mode.
        
        Returns:
            True if deactivated successfully
        """
        if self.emergency_mode:
            self.emergency_mode = False
            logger.info("Emergency mode DEACTIVATED")
            return True
        return False
    
    def get_compliance_summary(self) -> Dict[str, Any]:
        """
        Get summary of recent compliance validations.
        
        Returns:
            Dictionary with compliance statistics
        """
        if not self.validation_history:
            return {
                "total_validations": 0,
                "approval_rate": 0.0,
                "average_risk_score": 0.0
            }
        
        recent = self.validation_history[-100:]  # Last 100 validations
        
        approved = sum(1 for v in recent if v.status == OperationStatus.APPROVED)
        total = len(recent)
        avg_risk = sum(v.risk_score for v in recent) / total
        
        return {
            "total_validations": total,
            "approval_rate": approved / total if total > 0 else 0.0,
            "rejection_rate": sum(
                1 for v in recent if v.status == OperationStatus.REJECTED
            ) / total if total > 0 else 0.0,
            "average_risk_score": avg_risk,
            "emergency_mode_active": self.emergency_mode,
            "rco_health_score": self.rco.get_compliance_health_score()
        }
