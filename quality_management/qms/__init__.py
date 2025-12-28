"""
ISO 13485:2016 Quality Management System for Medical Devices
iLuminara Sovereign Health Interface - FRENASA Medical Device Classification

This module implements the complete QMS foundation for FRENASA (Framework for
Real-time Epidemiological Neural Analysis and Sovereign Assessment) as a
potential Class II medical device under FDA/EU regulations.

Key Components:
- Design Controls (21 CFR 820.30)
- Risk Management Integration (ISO 14971)
- Validation Protocols
- Post-Market Surveillance
- Usability Engineering (IEC 62366 alignment)
- Traceability Matrix
"""

import json
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

class DeviceClass(Enum):
    """FDA Medical Device Classification"""
    CLASS_I = "I"      # Low risk, general controls
    CLASS_II = "II"    # Moderate risk, special controls
    CLASS_III = "III"  # High risk, premarket approval

class DesignControlPhase(Enum):
    """ISO 13485 Design Control Phases"""
    PLANNING = "planning"
    INPUTS = "inputs"
    OUTPUTS = "outputs"
    REVIEW = "review"
    VERIFICATION = "verification"
    VALIDATION = "validation"
    TRANSFER = "transfer"
    CHANGES = "changes"

@dataclass
class DesignControl:
    """ISO 13485 Design Control Record"""
    id: str
    phase: DesignControlPhase
    title: str
    description: str
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    verification_method: str = ""
    validation_method: str = ""
    status: str = "draft"
    created_date: datetime.datetime = field(default_factory=datetime.datetime.now)
    approved_date: Optional[datetime.datetime] = None
    approver: str = ""

@dataclass
class ValidationProtocol:
    """Validation Protocol for Medical Device Software"""
    protocol_id: str
    device_name: str = "FRENASA"
    version: str = "1.0.0"
    test_cases: List[Dict] = field(default_factory=list)
    acceptance_criteria: Dict = field(default_factory=dict)
    execution_date: Optional[datetime.datetime] = None
    results: Dict = field(default_factory=dict)
    conclusion: str = "pending"

@dataclass
class PostMarketSurveillance:
    """Post-Market Surveillance Record (ISO 13485 8.2.1)"""
    incident_id: str
    date_reported: datetime.datetime
    device_version: str
    description: str
    severity: str  # minor, serious, critical
    root_cause: str = ""
    corrective_action: str = ""
    preventive_action: str = ""
    status: str = "investigating"
    follow_up_date: Optional[datetime.datetime] = None

class QMSManager:
    """ISO 13485 Quality Management System Manager"""

    def __init__(self):
        self.device_class = DeviceClass.CLASS_II  # FRENASA classification
        self.design_controls: Dict[str, DesignControl] = {}
        self.validation_protocols: Dict[str, ValidationProtocol] = {}
        self.post_market_incidents: List[PostMarketSurveillance] = []
        self.traceability_matrix: Dict[str, List[str]] = {}

    def create_design_control(self, dc: DesignControl) -> str:
        """Create a new design control record"""
        self.design_controls[dc.id] = dc
        return dc.id

    def validate_design_control(self, dc_id: str, approver: str) -> bool:
        """Validate and approve a design control"""
        if dc_id not in self.design_controls:
            return False

        dc = self.design_controls[dc_id]
        dc.status = "approved"
        dc.approved_date = datetime.datetime.now()
        dc.approver = approver
        return True

    def create_validation_protocol(self, protocol: ValidationProtocol) -> str:
        """Create validation protocol for software testing"""
        self.validation_protocols[protocol.protocol_id] = protocol
        return protocol.protocol_id

    def execute_validation(self, protocol_id: str, results: Dict) -> bool:
        """Execute validation protocol and record results"""
        if protocol_id not in self.validation_protocols:
            return False

        protocol = self.validation_protocols[protocol_id]
        protocol.execution_date = datetime.datetime.now()
        protocol.results = results

        # Check acceptance criteria
        all_passed = True
        for criterion, expected in protocol.acceptance_criteria.items():
            if criterion in results:
                if not self._check_criterion(results[criterion], expected):
                    all_passed = False
                    break

        protocol.conclusion = "passed" if all_passed else "failed"
        return all_passed

    def _check_criterion(self, actual: Any, expected: Any) -> bool:
        """Check if validation criterion is met"""
        if isinstance(expected, dict):
            if "min" in expected and "max" in expected:
                return expected["min"] <= actual <= expected["max"]
            elif "threshold" in expected:
                return actual >= expected["threshold"]
        return actual == expected

    def report_incident(self, incident: PostMarketSurveillance) -> str:
        """Report post-market surveillance incident"""
        self.post_market_incidents.append(incident)
        return incident.incident_id

    def update_traceability_matrix(self, requirement_id: str, linked_items: List[str]):
        """Update requirements traceability matrix"""
        self.traceability_matrix[requirement_id] = linked_items

    def generate_qms_report(self) -> Dict:
        """Generate comprehensive QMS status report"""
        return {
            "device_info": {
                "name": "FRENASA",
                "classification": self.device_class.value,
                "version": "1.0.0"
            },
            "design_controls": {
                "total": len(self.design_controls),
                "approved": len([dc for dc in self.design_controls.values() if dc.status == "approved"]),
                "pending": len([dc for dc in self.design_controls.values() if dc.status == "draft"])
            },
            "validation_protocols": {
                "total": len(self.validation_protocols),
                "passed": len([vp for vp in self.validation_protocols.values() if vp.conclusion == "passed"]),
                "failed": len([vp for vp in self.validation_protocols.values() if vp.conclusion == "failed"])
            },
            "post_market_surveillance": {
                "total_incidents": len(self.post_market_incidents),
                "critical_incidents": len([inc for inc in self.post_market_incidents if inc.severity == "critical"]),
                "open_investigations": len([inc for inc in self.post_market_incidents if inc.status == "investigating"])
            },
            "compliance_status": self._assess_compliance()
        }

    def _assess_compliance(self) -> Dict:
        """Assess overall ISO 13485 compliance status"""
        design_compliance = len([dc for dc in self.design_controls.values() if dc.status == "approved"]) / max(len(self.design_controls), 1)
        validation_compliance = len([vp for vp in self.validation_protocols.values() if vp.conclusion == "passed"]) / max(len(self.validation_protocols), 1)

        overall_compliance = (design_compliance + validation_compliance) / 2

        return {
            "design_controls": f"{design_compliance:.1%}",
            "validation_protocols": f"{validation_compliance:.1%}",
            "overall": f"{overall_compliance:.1%}",
            "status": "compliant" if overall_compliance >= 0.95 else "needs_attention"
        }

# Initialize Global QMS Manager
qms_manager = QMSManager()

def initialize_fda_design_controls():
    """Initialize FDA-required design controls for FRENASA"""

    # Design Planning
    planning_dc = DesignControl(
        id="DC-001",
        phase=DesignControlPhase.PLANNING,
        title="FRENASA Design Planning",
        description="Planning for sovereign epidemiological neural analysis system",
        inputs=["User requirements", "Regulatory requirements", "Technical specifications"],
        outputs=["Design plan", "Risk management plan", "Verification/validation plan"]
    )
    qms_manager.create_design_control(planning_dc)

    # Design Inputs
    inputs_dc = DesignControl(
        id="DC-002",
        phase=DesignControlPhase.INPUTS,
        title="Design Input Requirements",
        description="Specification of design inputs for FRENASA Class II device",
        inputs=["ISO 13485 requirements", "FDA 21 CFR 820", "IEC 62366 usability"],
        outputs=["Design input document", "Requirements traceability matrix"]
    )
    qms_manager.create_design_control(inputs_dc)

    # Design Verification
    verification_dc = DesignControl(
        id="DC-003",
        phase=DesignControlPhase.VERIFICATION,
        title="Design Verification",
        description="Verification that design outputs meet design inputs",
        verification_method="Testing, inspection, analysis"
    )
    qms_manager.create_design_control(verification_dc)

    # Design Validation
    validation_dc = DesignControl(
        id="DC-004",
        phase=DesignControlPhase.VALIDATION,
        title="Design Validation",
        description="Validation that device meets user needs and intended uses",
        validation_method="Clinical validation, user acceptance testing"
    )
    qms_manager.create_design_control(validation_dc)

def create_usability_validation_protocol():
    """Create usability engineering validation per IEC 62366"""

    protocol = ValidationProtocol(
        protocol_id="UVP-001",
        device_name="FRENASA Usability Validation",
        test_cases=[
            {
                "id": "UV-001",
                "description": "Offline edge triage usability test",
                "method": "Cognitive walkthrough with healthcare workers",
                "success_criteria": "Task completion rate >= 95%"
            },
            {
                "id": "UV-002",
                "description": "Error detection and recovery",
                "method": "Usability testing with error scenarios",
                "success_criteria": "Error recovery time < 30 seconds"
            }
        ],
        acceptance_criteria={
            "task_completion_rate": {"min": 0.95, "max": 1.0},
            "error_recovery_time": {"max": 30},
            "user_satisfaction_score": {"min": 4.0, "max": 5.0}
        }
    )

    qms_manager.create_validation_protocol(protocol)

if __name__ == "__main__":
    # Initialize FRENASA QMS
    initialize_fda_design_controls()
    create_usability_validation_protocol()

    # Generate compliance report
    report = qms_manager.generate_qms_report()
    print(json.dumps(report, indent=2, default=str))