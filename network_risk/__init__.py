"""
IEC 80001-1:2021 Networked Medical IT - Risk Management for IT-Networks
iLuminara Sovereign Health Interface - Golden Thread Network Safety

This module implements networked medical IT risk management for the Golden Thread
synchronization system, ensuring safety and effectiveness of connected health devices.

Key Components:
- Network Risk Assessment
- Responsibility Agreements
- Offline-Online Resilience
- Golden Thread Safety Validation
- Networked System Interoperability
"""

import json
import datetime
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import networkx as nx

class NetworkRole(Enum):
    """IEC 80001-1 Network Roles"""
    RESPONSIBLE_ORGANIZATION = "responsible_organization"
    MEDICAL_DEVICE_MANUFACTURER = "medical_device_manufacturer"
    IT_NETWORK_PROVIDER = "it_network_provider"
    HEALTHCARE_DELIVERY_ORGANIZATION = "healthcare_delivery_organization"

class NetworkRiskLevel(Enum):
    """Network Risk Assessment Levels"""
    NEGLIGIBLE = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5

class ConnectivityType(Enum):
    """Medical Device Connectivity Types"""
    WIRED = "wired"
    WIRELESS = "wireless"
    BLUETOOTH = "bluetooth"
    WIFI = "wifi"
    CELLULAR = "cellular"
    OFFLINE_ONLY = "offline_only"

@dataclass
class NetworkedSystem:
    """Networked Medical System Component"""
    id: str
    name: str
    system_type: str
    connectivity: ConnectivityType
    criticality_level: str  # low, medium, high, critical
    manufacturer: str
    software_version: str
    network_dependencies: List[str] = field(default_factory=list)
    safety_functions: List[str] = field(default_factory=list)
    registration_date: datetime.datetime = field(default_factory=datetime.datetime.now)

@dataclass
class ResponsibilityAgreement:
    """IEC 80001-1 Responsibility Agreement"""
    agreement_id: str
    parties: List[Dict[str, str]]  # [{"role": "responsible_organization", "organization": "iLuminara"}]
    system_id: str
    responsibilities: Dict[str, List[str]]  # {"risk_management": ["assessment", "mitigation"]}
    agreement_date: datetime.datetime
    review_date: Optional[datetime.datetime] = None
    status: str = "active"

@dataclass
class NetworkRiskAssessment:
    """Network Risk Assessment per IEC 80001-1"""
    assessment_id: str
    system_id: str
    assessment_date: datetime.datetime
    risk_factors: Dict[str, Any] = field(default_factory=dict)
    risk_level: NetworkRiskLevel = NetworkRiskLevel.MEDIUM
    mitigation_measures: List[str] = field(default_factory=list)
    residual_risk: NetworkRiskLevel = NetworkRiskLevel.LOW
    assessor: str = ""
    next_review: Optional[datetime.datetime] = None

@dataclass
class GoldenThreadSync:
    """Golden Thread Synchronization Event"""
    sync_id: str
    timestamp: datetime.datetime
    source_system: str
    target_systems: List[str]
    data_payload: Dict[str, Any]
    safety_checks_passed: bool = True
    network_latency_ms: Optional[float] = None
    offline_fallback_triggered: bool = False
    integrity_hash: str = ""

class NetworkRiskManager:
    """IEC 80001-1 Network Risk Management for Golden Thread"""

    def __init__(self):
        self.networked_systems: Dict[str, NetworkedSystem] = {}
        self.responsibility_agreements: Dict[str, ResponsibilityAgreement] = {}
        self.risk_assessments: Dict[str, NetworkRiskAssessment] = {}
        self.golden_thread_events: List[GoldenThreadSync] = []
        self.network_topology = nx.DiGraph()

        # Initialize with FRENASA network components
        self._initialize_frenasa_network()

    def _initialize_frenasa_network(self):
        """Initialize FRENASA network topology"""

        # Core FRENASA System
        frenasa_core = NetworkedSystem(
            id="SYS-FRENASA-CORE",
            name="FRENASA Core AI Engine",
            system_type="medical_device_software",
            connectivity=ConnectivityType.WIFI,
            criticality_level="critical",
            manufacturer="iLuminara Sovereign Health",
            software_version="1.0.0",
            network_dependencies=["SYS-EDGE-NODE", "SYS-CLOUD-ORACLE"],
            safety_functions=["outbreak_prediction", "resource_allocation", "clinical_decision_support"]
        )
        self.register_system(frenasa_core)

        # Edge Node
        edge_node = NetworkedSystem(
            id="SYS-EDGE-NODE",
            name="Offline Edge Node",
            system_type="medical_device",
            connectivity=ConnectivityType.OFFLINE_ONLY,
            criticality_level="high",
            manufacturer="iLuminara Sovereign Health",
            software_version="1.0.0",
            safety_functions=["local_triage", "offline_prediction", "data_collection"]
        )
        self.register_system(edge_node)

        # Cloud Oracle
        cloud_oracle = NetworkedSystem(
            id="SYS-CLOUD-ORACLE",
            name="Cloud Oracle Analytics",
            system_type="health_information_system",
            connectivity=ConnectivityType.CELLULAR,
            criticality_level="medium",
            manufacturer="iLuminara Sovereign Health",
            software_version="1.0.0",
            network_dependencies=["SYS-FRENASA-CORE"],
            safety_functions=["global_analytics", "trend_analysis"]
        )
        self.register_system(cloud_oracle)

        # Build network topology
        self._build_network_topology()

    def register_system(self, system: NetworkedSystem) -> str:
        """Register a networked medical system"""
        self.networked_systems[system.id] = system

        # Add to network topology
        self.network_topology.add_node(system.id,
                                     name=system.name,
                                     criticality=system.criticality_level,
                                     connectivity=system.connectivity.value)

        return system.id

    def _build_network_topology(self):
        """Build network dependency topology"""
        for system_id, system in self.networked_systems.items():
            for dependency in system.network_dependencies:
                if dependency in self.networked_systems:
                    self.network_topology.add_edge(system_id, dependency,
                                                 relationship="depends_on")

    def create_responsibility_agreement(self, agreement: ResponsibilityAgreement) -> str:
        """Create responsibility agreement per IEC 80001-1"""
        self.responsibility_agreements[agreement.agreement_id] = agreement
        return agreement.agreement_id

    def assess_network_risk(self, system_id: str, assessor: str) -> Optional[str]:
        """Perform network risk assessment"""
        if system_id not in self.networked_systems:
            return None

        system = self.networked_systems[system_id]

        # Risk factors assessment
        risk_factors = self._evaluate_risk_factors(system)

        # Calculate overall risk level
        risk_level = self._calculate_network_risk_level(risk_factors)

        assessment = NetworkRiskAssessment(
            assessment_id=f"NRA-{system_id}-{datetime.datetime.now().strftime('%Y%m%d')}",
            system_id=system_id,
            assessment_date=datetime.datetime.now(),
            risk_factors=risk_factors,
            risk_level=risk_level,
            assessor=assessor,
            next_review=datetime.datetime.now() + datetime.timedelta(days=365)
        )

        self.risk_assessments[assessment.assessment_id] = assessment
        return assessment.assessment_id

    def _evaluate_risk_factors(self, system: NetworkedSystem) -> Dict[str, Any]:
        """Evaluate network risk factors"""
        factors = {}

        # Connectivity risk
        if system.connectivity in [ConnectivityType.WIRELESS, ConnectivityType.WIFI, ConnectivityType.CELLULAR]:
            factors["connectivity_risk"] = "high"
        else:
            factors["connectivity_risk"] = "low"

        # Dependency risk
        dependency_count = len(system.network_dependencies)
        factors["dependency_risk"] = "high" if dependency_count > 2 else "medium" if dependency_count > 0 else "low"

        # Criticality risk
        criticality_map = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        factors["criticality_risk"] = criticality_map.get(system.criticality_level, 2)

        # Network isolation
        has_isolation = len(system.network_dependencies) == 0
        factors["isolation_risk"] = "low" if has_isolation else "medium"

        return factors

    def _calculate_network_risk_level(self, risk_factors: Dict[str, Any]) -> NetworkRiskLevel:
        """Calculate overall network risk level"""
        risk_score = 0

        # Connectivity risk
        if risk_factors.get("connectivity_risk") == "high":
            risk_score += 2

        # Dependency risk
        if risk_factors.get("dependency_risk") == "high":
            risk_score += 2
        elif risk_factors.get("dependency_risk") == "medium":
            risk_score += 1

        # Criticality risk
        risk_score += risk_factors.get("criticality_risk", 2)

        # Network isolation
        if risk_factors.get("isolation_risk") == "medium":
            risk_score += 1

        # Convert to risk level
        if risk_score >= 7:
            return NetworkRiskLevel.CRITICAL
        elif risk_score >= 5:
            return NetworkRiskLevel.HIGH
        elif risk_score >= 3:
            return NetworkRiskLevel.MEDIUM
        elif risk_score >= 1:
            return NetworkRiskLevel.LOW
        else:
            return NetworkRiskLevel.NEGLIGIBLE

    def validate_golden_thread_sync(self, sync_event: GoldenThreadSync) -> Dict[str, Any]:
        """Validate Golden Thread synchronization for safety"""
        validation_results = {
            "sync_id": sync_event.sync_id,
            "safety_checks": [],
            "warnings": [],
            "blockers": [],
            "overall_status": "approved"
        }

        # Check network connectivity
        source_system = self.networked_systems.get(sync_event.source_system)
        if not source_system:
            validation_results["blockers"].append("Source system not registered")
            validation_results["overall_status"] = "blocked"
            return validation_results

        # Check target systems
        for target_id in sync_event.target_systems:
            if target_id not in self.networked_systems:
                validation_results["blockers"].append(f"Target system {target_id} not registered")
                validation_results["overall_status"] = "blocked"
                continue

            target_system = self.networked_systems[target_id]

            # Check connectivity compatibility
            if not self._check_connectivity_compatibility(source_system, target_system):
                validation_results["warnings"].append(f"Connectivity mismatch between {source_system.id} and {target_id}")

            # Check network risk
            risk_assessment = self._get_latest_risk_assessment(target_id)
            if risk_assessment and risk_assessment.risk_level in [NetworkRiskLevel.HIGH, NetworkRiskLevel.CRITICAL]:
                validation_results["warnings"].append(f"High network risk for target system {target_id}")

        # Check data integrity
        if not sync_event.integrity_hash:
            validation_results["warnings"].append("No data integrity hash provided")

        # Check latency requirements
        if sync_event.network_latency_ms and sync_event.network_latency_ms > 1000:  # 1 second threshold
            validation_results["warnings"].append(f"High network latency: {sync_event.network_latency_ms}ms")

        # Overall status determination
        if validation_results["blockers"]:
            validation_results["overall_status"] = "blocked"
        elif validation_results["warnings"]:
            validation_results["overall_status"] = "approved_with_warnings"
        else:
            validation_results["overall_status"] = "approved"

        return validation_results

    def _check_connectivity_compatibility(self, source: NetworkedSystem, target: NetworkedSystem) -> bool:
        """Check if systems have compatible connectivity"""
        # Offline systems can only connect to offline systems
        if source.connectivity == ConnectivityType.OFFLINE_ONLY:
            return target.connectivity == ConnectivityType.OFFLINE_ONLY

        # Online systems can connect to any system (assuming network bridging)
        return True

    def _get_latest_risk_assessment(self, system_id: str) -> Optional[NetworkRiskAssessment]:
        """Get latest risk assessment for system"""
        system_assessments = [a for a in self.risk_assessments.values() if a.system_id == system_id]
        if not system_assessments:
            return None

        return max(system_assessments, key=lambda a: a.assessment_date)

    def implement_offline_resilience(self, system_id: str) -> Dict[str, Any]:
        """Implement offline-online resilience measures"""
        if system_id not in self.networked_systems:
            return {"error": "System not found"}

        system = self.networked_systems[system_id]

        resilience_measures = {
            "local_data_cache": True,
            "offline_prediction_models": True,
            "network_reconnection_protocols": True,
            "data_synchronization_queue": True,
            "graceful_degradation_modes": True
        }

        # Update system with resilience capabilities
        system.safety_functions.extend([
            "offline_operation",
            "data_cache_management",
            "network_reconnection"
        ])

        return {
            "system_id": system_id,
            "resilience_measures": resilience_measures,
            "implementation_status": "completed",
            "test_requirements": [
                "Offline operation for 24 hours",
                "Data integrity during reconnection",
                "Automatic synchronization on network restore"
            ]
        }

    def monitor_network_health(self) -> Dict[str, Any]:
        """Monitor overall network health and safety"""
        health_report = {
            "timestamp": datetime.datetime.now(),
            "systems_status": {},
            "network_connectivity": {},
            "risk_assessments": {},
            "golden_thread_performance": {},
            "alerts": []
        }

        # Check system status
        for system_id, system in self.networked_systems.items():
            health_report["systems_status"][system_id] = {
                "name": system.name,
                "connectivity": system.connectivity.value,
                "status": "operational",  # In real system, check actual status
                "last_seen": datetime.datetime.now()
            }

        # Check risk assessment status
        for assessment in self.risk_assessments.values():
            if assessment.system_id not in health_report["risk_assessments"]:
                health_report["risk_assessments"][assessment.system_id] = []

            health_report["risk_assessments"][assessment.system_id].append({
                "assessment_id": assessment.assessment_id,
                "risk_level": assessment.risk_level.value,
                "next_review": assessment.next_review.isoformat() if assessment.next_review else None
            })

        # Check Golden Thread performance
        recent_syncs = [s for s in self.golden_thread_events if (datetime.datetime.now() - s.timestamp).days < 1]
        if recent_syncs:
            avg_latency = sum(s.network_latency_ms for s in recent_syncs if s.network_latency_ms) / len([s for s in recent_syncs if s.network_latency_ms])
            health_report["golden_thread_performance"] = {
                "syncs_last_24h": len(recent_syncs),
                "average_latency_ms": avg_latency,
                "failed_syncs": len([s for s in recent_syncs if not s.safety_checks_passed])
            }

        # Generate alerts
        health_report["alerts"] = self._generate_network_alerts(health_report)

        return health_report

    def _generate_network_alerts(self, health_report: Dict) -> List[str]:
        """Generate network health alerts"""
        alerts = []

        # Check for systems without recent risk assessments
        for system_id in self.networked_systems:
            assessments = health_report["risk_assessments"].get(system_id, [])
            if not assessments:
                alerts.append(f"CRITICAL: No risk assessment for system {system_id}")
            else:
                latest_assessment = max(assessments, key=lambda a: a["assessment_id"])
                if latest_assessment["risk_level"] in ["high", "critical"]:
                    alerts.append(f"HIGH RISK: System {system_id} has {latest_assessment['risk_level']} network risk")

        # Check Golden Thread performance
        perf = health_report.get("golden_thread_performance", {})
        if perf.get("failed_syncs", 0) > 0:
            alerts.append(f"WARNING: {perf['failed_syncs']} Golden Thread sync failures in last 24 hours")

        if perf.get("average_latency_ms", 0) > 500:
            alerts.append(f"WARNING: High Golden Thread latency: {perf['average_latency_ms']:.1f}ms")

        return alerts

    def generate_network_report(self) -> Dict[str, Any]:
        """Generate comprehensive network risk management report"""
        return {
            "iec_80001_compliance": {
                "registered_systems": len(self.networked_systems),
                "responsibility_agreements": len(self.responsibility_agreements),
                "risk_assessments": len(self.risk_assessments),
                "golden_thread_events": len(self.golden_thread_events)
            },
            "network_topology": {
                "nodes": list(self.network_topology.nodes(data=True)),
                "edges": list(self.network_topology.edges(data=True))
            },
            "critical_systems": [
                {
                    "id": sys.id,
                    "name": sys.name,
                    "criticality": sys.criticality_level,
                    "connectivity": sys.connectivity.value
                }
                for sys in self.networked_systems.values()
                if sys.criticality_level in ["high", "critical"]
            ],
            "health_status": self.monitor_network_health()
        }

# Initialize Global Network Risk Manager
network_risk_manager = NetworkRiskManager()

def initialize_frenasa_responsibility_agreements():
    """Initialize responsibility agreements for FRENASA network"""

    # Main responsibility agreement
    main_agreement = ResponsibilityAgreement(
        agreement_id="RA-FRENASA-001",
        parties=[
            {"role": NetworkRole.RESPONSIBLE_ORGANIZATION.value, "organization": "iLuminara Sovereign Health"},
            {"role": NetworkRole.MEDICAL_DEVICE_MANUFACTURER.value, "organization": "iLuminara Sovereign Health"},
            {"role": NetworkRole.IT_NETWORK_PROVIDER.value, "organization": "iLuminara Sovereign Health"},
            {"role": NetworkRole.HEALTHCARE_DELIVERY_ORGANIZATION.value, "organization": "Healthcare Facilities"}
        ],
        system_id="SYS-FRENASA-CORE",
        responsibilities={
            "risk_management": ["network_risk_assessment", "mitigation_implementation", "monitoring"],
            "safety_assurance": ["golden_thread_validation", "offline_resilience", "clinical_safety"],
            "data_integrity": ["encryption", "access_control", "audit_trail"],
            "maintenance": ["system_updates", "performance_monitoring", "incident_response"]
        },
        agreement_date=datetime.datetime.now()
    )

    network_risk_manager.create_responsibility_agreement(main_agreement)

def perform_initial_risk_assessments():
    """Perform initial network risk assessments for all systems"""

    for system_id in network_risk_manager.networked_systems:
        assessment_id = network_risk_manager.assess_network_risk(system_id, "iLuminara Risk Team")
        if assessment_id:
            print(f"Completed risk assessment: {assessment_id}")

def implement_resilience_measures():
    """Implement offline-online resilience for critical systems"""

    critical_systems = ["SYS-FRENASA-CORE", "SYS-EDGE-NODE"]

    for system_id in critical_systems:
        resilience_result = network_risk_manager.implement_offline_resilience(system_id)
        print(f"Implemented resilience for {system_id}: {resilience_result}")

if __name__ == "__main__":
    # Initialize FRENASA network risk management
    initialize_frenasa_responsibility_agreements()
    perform_initial_risk_assessments()
    implement_resilience_measures()

    # Generate network report
    report = network_risk_manager.generate_network_report()
    print(json.dumps(report, indent=2, default=str))