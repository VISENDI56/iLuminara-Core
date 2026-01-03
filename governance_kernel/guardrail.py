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

    Digital Strategy Integration (WHO Global Strategy 2020-2025):
    - Guiding Principles: Institutionalization, Integration, Appropriate Use, Address Impediments
    - Strategic Objectives: Global collaboration, National strategies, Multi-level governance
    - Action Framework: Commit-Catalyse-Measure-Enhance cycle
    - Triple Billion Targets: UHC, Emergency Preparedness, Health & Well-being
    """

    # WHO Global Strategy on Digital Health 2020-2025 - Guiding Principles
    GUIDING_PRINCIPLES = [
        "institutionalize",
        "integrate",
        "appropriate_use",
        "address_impediments"
    ]

    # Strategic Objectives
    STRATEGIC_OBJECTIVES = [
        "global_collaboration",
        "national_strategy_development",
        "multi_level_governance",
        "autonomy_enhancement"
    ]

    # Action Framework (Commit-Catalyse-Measure-Enhance)
    ACTION_FRAMEWORK = [
        "commit",
        "catalyse",
        "measure",
        "enhance"
    ]

    # Triple Billion Targets
    TRIPLE_BILLION_TARGETS = [
        "universal_health_coverage",
        "emergency_preparedness",
        "health_wellbeing"
    ]

    def __init__(self, rco_engine: Optional[RegenerativeComplianceOracle] = None):
        """
        Initialize the Sovereign Guardrail.

        Args:
            rco_engine: RegenerativeComplianceOracle instance (creates new if None)
        """
        self.rco = rco_engine or RegenerativeComplianceOracle()
        self.emergency_mode = False
        self.validation_history: List[ValidationResult] = []
        self.digital_strategy_maturity = self._initialize_digital_strategy_maturity()
        logger.info("SovereignGuardrail v3.0 initialized with Digital Strategy integration")
    
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

    # =====================================================
    # DIGITAL STRATEGY INTEGRATION METHODS
    # =====================================================

    def _initialize_digital_strategy_maturity(self) -> Dict[str, float]:
        """Initialize digital strategy maturity levels for different principles"""
        return {
            principle: 0.5 for principle in self.GUIDING_PRINCIPLES
        }

    def validate_digital_strategy_compliance(
        self,
        operation: Dict[str, Any],
        sector: str = "health"
    ) -> Dict[str, Any]:
        """
        Validate operation against WHO Global Strategy on Digital Health 2020-2025

        Args:
            operation: Operation details
            sector: Health sector context

        Returns:
            Digital strategy compliance assessment
        """
        assessment = {
            "guiding_principles_compliance": {},
            "strategic_objectives_alignment": {},
            "action_framework_status": {},
            "triple_billion_impact": {},
            "overall_maturity_score": 0.0,
            "recommendations": []
        }

        # Check guiding principles compliance
        for principle in self.GUIDING_PRINCIPLES:
            compliance = self._check_principle_compliance(principle, operation)
            assessment["guiding_principles_compliance"][principle] = compliance
            self.digital_strategy_maturity[principle] = (
                self.digital_strategy_maturity[principle] * 0.8 + compliance * 0.2
            )

        # Assess strategic objectives alignment
        for objective in self.STRATEGIC_OBJECTIVES:
            alignment = self._assess_objective_alignment(objective, operation, sector)
            assessment["strategic_objectives_alignment"][objective] = alignment

        # Evaluate action framework status
        for action in self.ACTION_FRAMEWORK:
            status = self._evaluate_action_status(action, operation)
            assessment["action_framework_status"][action] = status

        # Calculate triple billion impact
        for target in self.TRIPLE_BILLION_TARGETS:
            impact = self._calculate_triple_billion_impact(target, operation)
            assessment["triple_billion_impact"][target] = impact

        # Calculate overall maturity
        assessment["overall_maturity_score"] = self._calculate_maturity_score(assessment)

        # Generate recommendations
        assessment["recommendations"] = self._generate_digital_strategy_recommendations(assessment)

        return assessment

    def _check_principle_compliance(self, principle: str, operation: Dict[str, Any]) -> float:
        """Check compliance with a specific guiding principle"""
        compliance_checks = {
            "institutionalize": self._check_institutionalization,
            "integrate": self._check_integration,
            "appropriate_use": self._check_appropriate_use,
            "address_impediments": self._check_impediment_addressing
        }

        check_func = compliance_checks.get(principle, lambda x: 0.5)
        return check_func(operation)

    def _check_institutionalization(self, operation: Dict[str, Any]) -> float:
        """Check if operation demonstrates institutional commitment to digital health"""
        indicators = [
            operation.get("institutional_commitment", False),
            operation.get("policy_framework", False),
            operation.get("governance_structure", False),
            operation.get("resource_allocation", False)
        ]
        return sum(indicators) / len(indicators)

    def _check_integration(self, operation: Dict[str, Any]) -> float:
        """Check if operation integrates digital health across health systems"""
        integration_indicators = operation.get("integration_indicators", {})
        return integration_indicators.get("system_integration", 0.5)

    def _check_appropriate_use(self, operation: Dict[str, Any]) -> float:
        """Check if operation demonstrates appropriate use of digital technologies"""
        ethics_score = operation.get("ethics_assessment", {}).get("appropriateness", 0.5)
        privacy_score = operation.get("privacy_impact", {}).get("appropriateness", 0.5)
        return (ethics_score + privacy_score) / 2

    def _check_impediment_addressing(self, operation: Dict[str, Any]) -> float:
        """Check if operation addresses potential impediments"""
        impediments_addressed = operation.get("impediments_addressed", [])
        total_impediments = operation.get("identified_impediments", [])
        if not total_impediments:
            return 1.0
        return len(impediments_addressed) / len(total_impediments)

    def _assess_objective_alignment(self, objective: str, operation: Dict[str, Any], sector: str) -> float:
        """Assess alignment with strategic objectives"""
        alignment_scores = {
            "global_collaboration": self._check_global_collaboration,
            "national_strategy_development": self._check_national_strategy,
            "multi_level_governance": self._check_multi_level_governance,
            "autonomy_enhancement": self._check_autonomy_enhancement
        }

        check_func = alignment_scores.get(objective, lambda x, y: 0.5)
        return check_func(operation, sector)

    def _check_global_collaboration(self, operation: Dict[str, Any], sector: str) -> float:
        """Check global collaboration indicators"""
        collaboration_indicators = [
            operation.get("international_partnerships", False),
            operation.get("knowledge_sharing", False),
            operation.get("cross_border_data_flow", False)
        ]
        return sum(collaboration_indicators) / len(collaboration_indicators)

    def _check_national_strategy(self, operation: Dict[str, Any], sector: str) -> float:
        """Check national strategy development alignment"""
        strategy_elements = operation.get("national_strategy_elements", [])
        required_elements = ["policy", "governance", "infrastructure", "workforce", "standards"]
        return len(set(strategy_elements) & set(required_elements)) / len(required_elements)

    def _check_multi_level_governance(self, operation: Dict[str, Any], sector: str) -> float:
        """Check multi-level governance implementation"""
        governance_levels = operation.get("governance_levels", [])
        required_levels = ["national", "regional", "local", "facility"]
        return len(set(governance_levels) & set(required_levels)) / len(required_levels)

    def _check_autonomy_enhancement(self, operation: Dict[str, Any], sector: str) -> float:
        """Check autonomy enhancement measures"""
        autonomy_indicators = [
            operation.get("sovereign_data_control", False),
            operation.get("local_capacity_building", False),
            operation.get("offline_capability", False)
        ]
        return sum(autonomy_indicators) / len(autonomy_indicators)

    def _evaluate_action_status(self, action: str, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate status of action framework components"""
        action_status = {
            "commit": {
                "status": "completed" if operation.get("commitment_made", False) else "pending",
                "evidence": operation.get("commitment_evidence", [])
            },
            "catalyse": {
                "status": "active" if operation.get("catalyzing_activities", []) else "inactive",
                "initiatives": operation.get("catalyzing_activities", [])
            },
            "measure": {
                "status": "implemented" if operation.get("measurement_system", False) else "not_started",
                "indicators": operation.get("m_e_indicators", [])
            },
            "enhance": {
                "status": "ongoing" if operation.get("enhancement_cycle", False) else "pending",
                "improvements": operation.get("enhancement_actions", [])
            }
        }

        return action_status.get(action, {"status": "unknown"})

    def _calculate_triple_billion_impact(self, target: str, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate impact on Triple Billion targets"""
        impact_calculators = {
            "universal_health_coverage": self._calculate_uhc_impact,
            "emergency_preparedness": self._calculate_emergency_impact,
            "health_wellbeing": self._calculate_wellbeing_impact
        }

        calculator = impact_calculators.get(target, lambda x: {"impact_score": 0.5})
        return calculator(operation)

    def _calculate_uhc_impact(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate UHC impact"""
        uhc_indicators = operation.get("uhc_indicators", {})
        return {
            "impact_score": uhc_indicators.get("coverage_expansion", 0.5),
            "services_reached": uhc_indicators.get("services_improved", []),
            "equity_improvement": uhc_indicators.get("equity_impact", 0.5)
        }

    def _calculate_emergency_impact(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate emergency preparedness impact"""
        emergency_indicators = operation.get("emergency_indicators", {})
        return {
            "impact_score": emergency_indicators.get("preparedness_level", 0.5),
            "response_capability": emergency_indicators.get("response_time", 0),
            "resilience_building": emergency_indicators.get("resilience_measures", [])
        }

    def _calculate_wellbeing_impact(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate health and wellbeing impact"""
        wellbeing_indicators = operation.get("wellbeing_indicators", {})
        return {
            "impact_score": wellbeing_indicators.get("wellbeing_improvement", 0.5),
            "quality_of_life": wellbeing_indicators.get("qol_metrics", []),
            "preventive_focus": wellbeing_indicators.get("prevention_emphasis", 0.5)
        }

    def _calculate_maturity_score(self, assessment: Dict[str, Any]) -> float:
        """Calculate overall digital strategy maturity score"""
        principle_avg = sum(assessment["guiding_principles_compliance"].values()) / len(assessment["guiding_principles_compliance"])

        objective_avg = sum(assessment["strategic_objectives_alignment"].values()) / len(assessment["strategic_objectives_alignment"])

        action_completion = sum(1 for status in assessment["action_framework_status"].values()
                              if isinstance(status, dict) and status.get("status") in ["completed", "active", "implemented", "ongoing"]) / len(assessment["action_framework_status"])

        target_impact = sum(target["impact_score"] for target in assessment["triple_billion_impact"].values()) / len(assessment["triple_billion_impact"])

        return (principle_avg * 0.3 + objective_avg * 0.3 + action_completion * 0.2 + target_impact * 0.2)

    def _generate_digital_strategy_recommendations(self, assessment: Dict[str, Any]) -> List[str]:
        """Generate recommendations for digital strategy improvement"""
        recommendations = []

        # Check principle compliance
        for principle, score in assessment["guiding_principles_compliance"].items():
            if score < 0.7:
                recommendations.append(f"Strengthen {principle.replace('_', ' ')} implementation")

        # Check objective alignment
        for objective, score in assessment["strategic_objectives_alignment"].items():
            if score < 0.6:
                recommendations.append(f"Improve alignment with {objective.replace('_', ' ')} objective")

        # Check action framework
        for action, status in assessment["action_framework_status"].items():
            if isinstance(status, dict) and status.get("status") in ["pending", "inactive", "not_started"]:
                recommendations.append(f"Activate {action} phase in action framework")

        # Check triple billion impact
        for target, impact in assessment["triple_billion_impact"].items():
            if impact.get("impact_score", 0) < 0.5:
                recommendations.append(f"Enhance contribution to {target.replace('_', ' ')} target")

        if assessment["overall_maturity_score"] < 0.6:
            recommendations.append("Develop comprehensive digital health strategy implementation plan")

        return recommendations

    def generate_national_strategy_template(self, country_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a national digital health strategy template based on WHO guidelines

        Args:
            country_context: Country-specific context and requirements

        Returns:
            Complete strategy template
        """
        template = {
            "strategy_overview": {
                "country": country_context.get("country", "Unknown"),
                "timeframe": "2025-2030",
                "alignment": "WHO Global Strategy on Digital Health 2020-2025"
            },
            "vision_mission": {
                "vision": "Digital technologies for health for all",
                "mission": "Accelerate progress towards UHC and health-related SDGs through digital health"
            },
            "guiding_principles": self.GUIDING_PRINCIPLES,
            "strategic_objectives": self.STRATEGIC_OBJECTIVES,
            "action_framework": {
                "commit": self._generate_commit_actions(country_context),
                "catalyse": self._generate_catalyse_actions(country_context),
                "measure": self._generate_measure_actions(country_context),
                "enhance": self._generate_enhance_actions(country_context)
            },
            "triple_billion_targets": self._generate_triple_billion_targets(country_context),
            "implementation_roadmap": self._generate_implementation_roadmap(country_context),
            "monitoring_evaluation": self._generate_m_e_framework(country_context)
        }

        return template

    def _generate_commit_actions(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate commit phase actions"""
        return [
            {
                "action": "Establish national digital health governance structure",
                "timeline": "Q1 2025",
                "responsible": "Ministry of Health",
                "resources_required": ["policy_experts", "stakeholders"]
            },
            {
                "action": "Develop national digital health policy framework",
                "timeline": "Q2 2025",
                "responsible": "Digital Health Committee",
                "resources_required": ["legal_experts", "international_consultants"]
            }
        ]

    def _generate_catalyse_actions(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate catalyse phase actions"""
        return [
            {
                "action": "Launch digital health innovation challenges",
                "timeline": "Q3 2025",
                "responsible": "Innovation Hub",
                "resources_required": ["funding", "technical_experts"]
            },
            {
                "action": "Establish public-private partnerships",
                "timeline": "Q4 2025",
                "responsible": "PPP Office",
                "resources_required": ["negotiation_team", "legal_support"]
            }
        ]

    def _generate_measure_actions(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate measure phase actions"""
        return [
            {
                "action": "Implement digital health indicators monitoring system",
                "timeline": "Q1 2026",
                "responsible": "M&E Department",
                "resources_required": ["data_analysts", "monitoring_tools"]
            },
            {
                "action": "Conduct baseline digital health assessment",
                "timeline": "Q2 2026",
                "responsible": "Assessment Team",
                "resources_required": ["survey_tools", "field_staff"]
            }
        ]

    def _generate_enhance_actions(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate enhance phase actions"""
        return [
            {
                "action": "Scale successful digital health interventions",
                "timeline": "Q3 2026",
                "responsible": "Implementation Team",
                "resources_required": ["scaling_experts", "additional_funding"]
            },
            {
                "action": "Continuous improvement through feedback loops",
                "timeline": "Ongoing",
                "responsible": "Quality Assurance",
                "resources_required": ["feedback_systems", "improvement_team"]
            }
        ]

    def _generate_triple_billion_targets(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate country-specific triple billion targets"""
        return {
            "universal_health_coverage": {
                "target_2030": "80% of population with essential digital health services",
                "baseline_2025": context.get("uhc_baseline", "50%"),
                "key_interventions": ["telemedicine", "digital_records", "mobile_health"]
            },
            "emergency_preparedness": {
                "target_2030": "70% emergency response digital readiness",
                "baseline_2025": context.get("emergency_baseline", "30%"),
                "key_interventions": ["early_warning_systems", "emergency_communication", "rapid_response"]
            },
            "health_wellbeing": {
                "target_2030": "75% digital health literacy",
                "baseline_2025": context.get("wellbeing_baseline", "25%"),
                "key_interventions": ["health_education", "preventive_care", "wellness_tracking"]
            }
        }

    def _generate_implementation_roadmap(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate implementation roadmap"""
        return {
            "phase_1_foundation": {
                "duration": "6 months",
                "focus": "Governance and policy development",
                "milestones": ["Strategy approval", "Governance structure", "Initial funding"]
            },
            "phase_2_piloting": {
                "duration": "12 months",
                "focus": "Pilot implementation and testing",
                "milestones": ["Technology selection", "Pilot deployment", "User training"]
            },
            "phase_3_scaling": {
                "duration": "24 months",
                "focus": "National scale implementation",
                "milestones": ["Infrastructure expansion", "Service integration", "Monitoring systems"]
            },
            "phase_4_sustainability": {
                "duration": "Ongoing",
                "focus": "Sustainability and continuous improvement",
                "milestones": ["Cost optimization", "Impact evaluation", "Knowledge sharing"]
            }
        }

    def _generate_m_e_framework(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate monitoring and evaluation framework"""
        return {
            "indicators": {
                "process_indicators": [
                    "Digital health policies developed",
                    "Infrastructure deployed",
                    "Workforce trained"
                ],
                "output_indicators": [
                    "Digital health services available",
                    "Users registered",
                    "Data systems operational"
                ],
                "outcome_indicators": [
                    "Health service utilization",
                    "Quality of care improvement",
                    "Efficiency gains"
                ],
                "impact_indicators": [
                    "Health outcomes improvement",
                    "Equity enhancement",
                    "System resilience"
                ]
            },
            "data_collection": {
                "frequency": "Quarterly",
                "methods": ["Digital monitoring", "Surveys", "Health facility reports"],
                "tools": ["DHIS2", "Custom dashboards", "Mobile data collection"]
            },
            "reporting": {
                "frequency": "Biennial",
                "audiences": ["Government", "Development partners", "Public"],
                "formats": ["Technical reports", "Policy briefs", "Infographics"]
            }
        }
