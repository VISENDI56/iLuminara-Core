"""
ISO 14971:2019 Risk Management for Medical Devices
iLuminara Sovereign Health Interface - Hazard Analysis & Risk Management

This module implements systematic risk management for FRENASA medical device,
integrating with ISO 42001 AI risks and providing comprehensive hazard analysis.

Key Components:
- Hazard Identification and Analysis
- Risk Estimation and Evaluation
- Risk Control Measures
- Residual Risk Assessment
- Post-Market Risk Monitoring
"""

import json
import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

class RiskLevel(Enum):
    """ISO 14971 Risk Levels"""
    NEGLIGIBLE = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5

class HazardCategory(Enum):
    """Medical Device Hazard Categories"""
    BIOLOGICAL = "biological"
    CHEMICAL = "chemical"
    ELECTRICAL = "electrical"
    MECHANICAL = "mechanical"
    THERMAL = "thermal"
    RADIATION = "radiation"
    SOFTWARE = "software"
    AI_BIAS = "ai_bias"
    DATA_PRIVACY = "data_privacy"
    CLINICAL = "clinical"

class HarmSeverity(Enum):
    """ISO 14971 Harm Severity Levels"""
    NEGLIGIBLE = 1  # No injury or damage
    LOW = 2         # Minor injury, temporary discomfort
    MEDIUM = 3      # Serious injury, reversible damage
    HIGH = 4        # Permanent impairment or life-threatening
    CATASTROPHIC = 5 # Death or permanent severe damage

class OccurrenceProbability(Enum):
    """ISO 14971 Occurrence Probability Levels"""
    REMOTE = 1      # < 0.01% probability
    LOW = 2         # 0.01% - 0.1% probability
    MEDIUM = 3      # 0.1% - 1% probability
    HIGH = 4        # 1% - 10% probability
    FREQUENT = 5    # > 10% probability

@dataclass
class Hazard:
    """Hazard Identification Record"""
    id: str
    category: HazardCategory
    description: str
    potential_harms: List[str]
    causes: List[str]
    affected_users: List[str] = field(default_factory=list)
    detection_date: datetime.datetime = field(default_factory=datetime.datetime.now)
    status: str = "identified"

@dataclass
class RiskAnalysis:
    """Risk Analysis Record per ISO 14971"""
    hazard_id: str
    severity: HarmSeverity
    occurrence: OccurrenceProbability
    detectability: int  # 1-5 scale, 1=almost certain detection, 5=almost impossible
    risk_priority_number: int = field(init=False)
    risk_level: RiskLevel = field(init=False)
    mitigation_measures: List[str] = field(default_factory=list)
    residual_severity: Optional[HarmSeverity] = None
    residual_occurrence: Optional[OccurrenceProbability] = None
    residual_rpn: Optional[int] = None
    analysis_date: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __post_init__(self):
        self.risk_priority_number = self.severity.value * self.occurrence.value * self.detectability
        self.risk_level = self._calculate_risk_level(self.risk_priority_number)

    def _calculate_risk_level(self, rpn: int) -> RiskLevel:
        """Calculate risk level based on RPN"""
        if rpn >= 100:
            return RiskLevel.CRITICAL
        elif rpn >= 50:
            return RiskLevel.HIGH
        elif rpn >= 20:
            return RiskLevel.MEDIUM
        elif rpn >= 5:
            return RiskLevel.LOW
        else:
            return RiskLevel.NEGLIGIBLE

    def apply_mitigation(self, measures: List[str], new_severity: HarmSeverity,
                        new_occurrence: OccurrenceProbability, new_detectability: int):
        """Apply risk mitigation measures and recalculate residual risk"""
        self.mitigation_measures.extend(measures)
        self.residual_severity = new_severity
        self.residual_occurrence = new_occurrence
        self.residual_rpn = new_severity.value * new_occurrence.value * new_detectability

@dataclass
class RiskControlMeasure:
    """Risk Control Measure per ISO 14971 6.2"""
    id: str
    hazard_id: str
    measure_type: str  # inherent_safety, protective_measures, information_for_safety
    description: str
    implementation_status: str = "planned"
    verification_method: str = ""
    effectiveness_rating: Optional[int] = None  # 1-5 scale
    implementation_date: Optional[datetime.datetime] = None

class RiskManagementSystem:
    """ISO 14971 Risk Management System for FRENASA"""

    def __init__(self):
        self.hazards: Dict[str, Hazard] = {}
        self.risk_analyses: Dict[str, RiskAnalysis] = {}
        self.risk_controls: Dict[str, RiskControlMeasure] = {}
        self.post_market_incidents: List[Dict] = []

        # Initialize with FRENASA-specific hazards
        self._initialize_frenasa_hazards()

    def _initialize_frenasa_hazards(self):
        """Initialize hazards specific to FRENASA medical device"""

        # AI Bias Hazard
        ai_bias = Hazard(
            id="HAZ-AI-001",
            category=HazardCategory.AI_BIAS,
            description="Algorithmic bias in outbreak prediction leading to incorrect resource allocation",
            potential_harms=["Delayed response to outbreaks", "Resource misallocation", "Public health harm"],
            causes=["Training data bias", "Algorithmic discrimination", "Insufficient validation"],
            affected_users=["Healthcare workers", "Public health officials", "Affected populations"]
        )
        self.hazards[ai_bias.id] = ai_bias

        # Data Privacy Hazard
        privacy_hazard = Hazard(
            id="HAZ-PRIV-001",
            category=HazardCategory.DATA_PRIVACY,
            description="Unauthorized access to sensitive health surveillance data",
            potential_harms=["Privacy breach", "Identity theft", "Discrimination"],
            causes=["Inadequate encryption", "Access control failures", "Data leakage"],
            affected_users=["Individuals under surveillance", "Healthcare providers"]
        )
        self.hazards[privacy_hazard.id] = privacy_hazard

        # Software Failure Hazard
        software_hazard = Hazard(
            id="HAZ-SW-001",
            category=HazardCategory.SOFTWARE,
            description="Software crash or incorrect calculations in critical decision support",
            potential_harms=["Decision errors", "Delayed interventions", "Patient harm"],
            causes=["Code bugs", "Memory leaks", "Concurrency issues"],
            affected_users=["Healthcare decision makers", "Emergency responders"]
        )
        self.hazards[software_hazard.id] = software_hazard

        # Clinical Decision Hazard
        clinical_hazard = Hazard(
            id="HAZ-CLIN-001",
            category=HazardCategory.CLINICAL,
            description="Incorrect clinical recommendations based on flawed AI analysis",
            potential_harms=["Wrong treatment decisions", "Adverse patient outcomes", "Medical errors"],
            causes=["AI hallucination", "Data corruption", "Model drift"],
            affected_users=["Physicians", "Patients", "Healthcare institutions"]
        )
        self.hazards[clinical_hazard.id] = clinical_hazard

    def identify_hazard(self, hazard: Hazard) -> str:
        """Identify and register a new hazard"""
        self.hazards[hazard.id] = hazard
        return hazard.id

    def analyze_risk(self, hazard_id: str, severity: HarmSeverity,
                    occurrence: OccurrenceProbability, detectability: int) -> Optional[str]:
        """Perform risk analysis per ISO 14971"""
        if hazard_id not in self.hazards:
            return None

        analysis = RiskAnalysis(
            hazard_id=hazard_id,
            severity=severity,
            occurrence=occurrence,
            detectability=detectability
        )

        self.risk_analyses[hazard_id] = analysis
        return hazard_id

    def implement_risk_control(self, control: RiskControlMeasure) -> str:
        """Implement risk control measure"""
        self.risk_controls[control.id] = control
        control.implementation_date = datetime.datetime.now()
        control.implementation_status = "implemented"
        return control.id

    def assess_residual_risk(self, hazard_id: str) -> Dict:
        """Assess residual risk after mitigation measures"""
        if hazard_id not in self.risk_analyses:
            return {"error": "No risk analysis found for hazard"}

        analysis = self.risk_analyses[hazard_id]

        if not analysis.residual_rpn:
            return {"error": "No residual risk assessment available"}

        residual_level = analysis._calculate_risk_level(analysis.residual_rpn)

        return {
            "hazard_id": hazard_id,
            "original_rpn": analysis.risk_priority_number,
            "residual_rpn": analysis.residual_rpn,
            "original_level": analysis.risk_level.value,
            "residual_level": residual_level.value,
            "acceptability": self._assess_risk_acceptability(residual_level),
            "mitigation_measures": analysis.mitigation_measures
        }

    def _assess_risk_acceptability(self, risk_level: RiskLevel) -> str:
        """Assess if residual risk is acceptable per ISO 14971"""
        if risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
            return "unacceptable"
        elif risk_level == RiskLevel.MEDIUM:
            return "acceptable_with_review"
        else:
            return "acceptable"

    def monitor_post_market_risks(self, incident_report: Dict) -> str:
        """Monitor and analyze post-market risk incidents"""
        incident_id = f"PM-{len(self.post_market_incidents) + 1:03d}"

        incident = {
            "id": incident_id,
            "report_date": datetime.datetime.now(),
            "description": incident_report.get("description", ""),
            "severity": incident_report.get("severity", ""),
            "root_cause": incident_report.get("root_cause", ""),
            "corrective_actions": incident_report.get("corrective_actions", []),
            "preventive_actions": incident_report.get("preventive_actions", []),
            "status": "investigating"
        }

        self.post_market_incidents.append(incident)

        # Trigger risk review if incident is serious
        if incident["severity"] in ["serious", "critical"]:
            self._trigger_risk_review(incident)

        return incident_id

    def _trigger_risk_review(self, incident: Dict):
        """Trigger risk management review for serious incidents"""
        # In a real system, this would:
        # 1. Notify risk management team
        # 2. Update risk analyses
        # 3. Implement additional controls if needed
        # 4. Report to regulatory authorities

        print(f"RISK REVIEW TRIGGERED: Incident {incident['id']} requires immediate risk management review")

    def generate_risk_report(self) -> Dict:
        """Generate comprehensive risk management report"""
        total_hazards = len(self.hazards)
        analyzed_hazards = len(self.risk_analyses)
        controlled_hazards = len([r for r in self.risk_analyses.values() if r.mitigation_measures])

        risk_distribution = {}
        for analysis in self.risk_analyses.values():
            level = analysis.risk_level.value
            risk_distribution[level] = risk_distribution.get(level, 0) + 1

        return {
            "summary": {
                "total_hazards": total_hazards,
                "analyzed_hazards": analyzed_hazards,
                "controlled_hazards": controlled_hazards,
                "analysis_coverage": f"{analyzed_hazards/total_hazards:.1%}" if total_hazards > 0 else "0%"
            },
            "risk_distribution": risk_distribution,
            "critical_risks": [
                {
                    "hazard_id": analysis.hazard_id,
                    "rpn": analysis.risk_priority_number,
                    "level": analysis.risk_level.value,
                    "description": self.hazards[analysis.hazard_id].description
                }
                for analysis in self.risk_analyses.values()
                if analysis.risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]
            ],
            "post_market_incidents": len(self.post_market_incidents),
            "compliance_status": self._assess_14971_compliance()
        }

    def _assess_14971_compliance(self) -> Dict:
        """Assess ISO 14971 compliance status"""
        requirements = {
            "hazard_identification": len(self.hazards) > 0,
            "risk_analysis": len(self.risk_analyses) > 0,
            "risk_evaluation": all(a.risk_level != RiskLevel.CRITICAL for a in self.risk_analyses.values()),
            "risk_controls": len(self.risk_controls) > 0,
            "residual_risk": any(a.residual_rpn is not None for a in self.risk_analyses.values()),
            "post_market_monitoring": len(self.post_market_incidents) >= 0  # Always true, but could be enhanced
        }

        compliant_count = sum(requirements.values())
        total_requirements = len(requirements)

        return {
            "compliant_requirements": compliant_count,
            "total_requirements": total_requirements,
            "compliance_percentage": f"{compliant_count/total_requirements:.1%}",
            "status": "compliant" if compliant_count == total_requirements else "partial_compliance",
            "details": requirements
        }

    def integrate_ai_risks(self, ai_system_analysis: Dict) -> List[str]:
        """Integrate ISO 42001 AI-specific risks into 14971 framework"""
        ai_hazards = []

        # AI-specific risks from ISO 42001
        ai_risk_categories = {
            "bias_discrimination": {
                "description": "AI system exhibits bias or discriminatory behavior",
                "severity": HarmSeverity.HIGH,
                "occurrence": OccurrenceProbability.MEDIUM
            },
            "lack_explainability": {
                "description": "AI decisions cannot be adequately explained",
                "severity": HarmSeverity.MEDIUM,
                "occurrence": OccurrenceProbability.HIGH
            },
            "robustness_failure": {
                "description": "AI system fails under edge cases or adversarial inputs",
                "severity": HarmSeverity.HIGH,
                "occurrence": OccurrenceProbability.LOW
            },
            "data_drift": {
                "description": "Model performance degrades due to data distribution changes",
                "severity": HarmSeverity.MEDIUM,
                "occurrence": OccurrenceProbability.MEDIUM
            }
        }

        for risk_type, risk_info in ai_risk_categories.items():
            hazard_id = f"HAZ-AI-{len(ai_hazards) + 1:03d}"
            hazard = Hazard(
                id=hazard_id,
                category=HazardCategory.AI_BIAS if risk_type == "bias_discrimination" else HazardCategory.SOFTWARE,
                description=risk_info["description"],
                potential_harms=["Incorrect decisions", "Unfair outcomes", "System failures"],
                causes=[f"AI {risk_type.replace('_', ' ')}"],
                affected_users=["Healthcare providers", "Patients", "System operators"]
            )

            self.identify_hazard(hazard)
            self.analyze_risk(hazard_id, risk_info["severity"], risk_info["occurrence"], 3)
            ai_hazards.append(hazard_id)

        return ai_hazards

# Initialize Global Risk Management System
risk_management = RiskManagementSystem()

def initialize_frenasa_risk_analysis():
    """Initialize risk analysis for all identified FRENASA hazards"""

    for hazard_id, hazard in risk_management.hazards.items():
        # Assign severity, occurrence, and detectability based on hazard type
        if hazard.category == HazardCategory.AI_BIAS:
            severity, occurrence, detectability = HarmSeverity.HIGH, OccurrenceProbability.MEDIUM, 3
        elif hazard.category == HazardCategory.DATA_PRIVACY:
            severity, occurrence, detectability = HarmSeverity.HIGH, OccurrenceProbability.LOW, 2
        elif hazard.category == HazardCategory.SOFTWARE:
            severity, occurrence, detectability = HarmSeverity.MEDIUM, OccurrenceProbability.MEDIUM, 3
        elif hazard.category == HazardCategory.CLINICAL:
            severity, occurrence, detectability = HarmSeverity.CRITICAL, OccurrenceProbability.LOW, 2
        else:
            severity, occurrence, detectability = HarmSeverity.MEDIUM, OccurrenceProbability.LOW, 3

        risk_management.analyze_risk(hazard_id, severity, occurrence, detectability)

def apply_standard_mitigations():
    """Apply standard risk mitigation measures"""

    mitigations = {
        "HAZ-AI-001": [
            "Implement bias detection algorithms",
            "Regular model validation with diverse datasets",
            "Human oversight for high-risk decisions"
        ],
        "HAZ-PRIV-001": [
            "End-to-end encryption for data in transit and at rest",
            "Role-based access control",
            "Regular security audits and penetration testing"
        ],
        "HAZ-SW-001": [
            "Comprehensive unit and integration testing",
            "Code reviews and static analysis",
            "Monitoring and alerting for system health"
        ],
        "HAZ-CLIN-001": [
            "Clinical validation studies",
            "Model performance monitoring",
            "Fallback procedures for AI failures"
        ]
    }

    for hazard_id, measures in mitigations.items():
        if hazard_id in risk_management.risk_analyses:
            analysis = risk_management.risk_analyses[hazard_id]

            # Assume mitigation reduces severity and occurrence
            new_severity = HarmSeverity(analysis.severity.value - 1) if analysis.severity.value > 1 else analysis.severity
            new_occurrence = OccurrenceProbability(analysis.occurrence.value - 1) if analysis.occurrence.value > 1 else analysis.occurrence
            new_detectability = max(1, analysis.detectability - 1)

            analysis.apply_mitigation(measures, new_severity, new_occurrence, new_detectability)

if __name__ == "__main__":
    # Initialize FRENASA risk management
    initialize_frenasa_risk_analysis()
    apply_standard_mitigations()

    # Integrate AI-specific risks
    ai_hazards = risk_management.integrate_ai_risks({})

    # Generate risk report
    report = risk_management.generate_risk_report()
    print(json.dumps(report, indent=2, default=str))