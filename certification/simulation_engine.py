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
Living Certifications Simulation Engine
Advanced compliance scenario simulation and testing framework

This module provides comprehensive simulation capabilities for testing
ISO compliance scenarios, risk events, audit responses, and system resilience.
"""

import asyncio
import json
import datetime
import random
import uuid
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import threading
import time
from pathlib import Path
import numpy as np
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimulationMode(Enum):
    """Simulation execution modes."""
    REAL_TIME = "real_time"
    ACCELERATED = "accelerated"
    STEP_BY_STEP = "step_by_step"
    MONTE_CARLO = "monte_carlo"

class ScenarioType(Enum):
    """Types of compliance scenarios."""
    RISK_EVENT = "risk_event"
    AUDIT_SIMULATION = "audit_simulation"
    BREACH_SIMULATION = "breach_simulation"
    COMPLIANCE_DRIFT = "compliance_drift"
    REGULATORY_CHANGE = "regulatory_change"
    SYSTEM_FAILURE = "system_failure"
    CYBER_ATTACK = "cyber_attack"

class SimulationStatus(Enum):
    """Simulation status states."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class SimulationEvent:
    """Represents a simulation event."""
    event_id: str
    timestamp: datetime.datetime
    event_type: str
    description: str
    parameters: Dict[str, Any]
    impact_score: float
    affected_standards: List[str]
    triggered_responses: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data

@dataclass
class SimulationResult:
    """Represents simulation results."""
    simulation_id: str
    scenario_type: ScenarioType
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime]
    status: SimulationStatus
    events_generated: int
    compliance_impact: float
    risk_exposure: float
    response_effectiveness: float
    key_findings: List[str]
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['scenario_type'] = self.scenario_type.value
        data['status'] = self.status.value
        data['start_time'] = self.start_time.isoformat()
        if self.end_time:
            data['end_time'] = self.end_time.isoformat()
        return data

class ComplianceScenario:
    """Base class for compliance scenarios."""

    def __init__(self, scenario_id: str, name: str, description: str):
        self.scenario_id = scenario_id
        self.name = name
        self.description = description
        self.events: List[SimulationEvent] = []
        self.parameters: Dict[str, Any] = {}

    def add_event(self, event: SimulationEvent):
        """Add an event to the scenario."""
        self.events.append(event)

    def get_events_in_timerange(self, start: datetime.datetime, end: datetime.datetime) -> List[SimulationEvent]:
        """Get events within a time range."""
        return [e for e in self.events if start <= e.timestamp <= end]

    async def execute(self, simulation_engine: 'LivingCertificationsSimulation') -> List[SimulationEvent]:
        """Execute the scenario. Override in subclasses."""
        return []

class RiskEventScenario(ComplianceScenario):
    """Simulates risk events and their compliance impact."""

    def __init__(self, scenario_id: str):
        super().__init__(
            scenario_id,
            "Risk Event Simulation",
            "Simulates various risk events and tests compliance response effectiveness"
        )

        self.parameters = {
            "risk_types": ["data_breach", "system_failure", "human_error", "cyber_attack"],
            "event_frequency": 0.1,  # Probability per hour
            "max_events": 10,
            "severity_distribution": [0.6, 0.3, 0.8, 0.2]  # Low, Medium, High, Critical
        }

    async def execute(self, simulation_engine: 'LivingCertificationsSimulation') -> List[SimulationEvent]:
        """Execute risk event simulation."""
        events = []
        duration_hours = self.parameters.get("duration_hours", 24)

        for hour in range(duration_hours):
            if random.random() < self.parameters["event_frequency"]:
                event = self._generate_risk_event(hour)
                events.append(event)
                self.add_event(event)

                # Trigger response simulation
                await simulation_engine.simulate_response(event)

        return events

    def _generate_risk_event(self, hour: int) -> SimulationEvent:
        """Generate a random risk event."""
        risk_types = self.parameters["risk_types"]
        severities = ["Low", "Medium", "High", "Critical"]
        severity_weights = self.parameters["severity_distribution"]

        risk_type = random.choice(risk_types)
        severity = random.choices(severities, weights=severity_weights)[0]

        event_descriptions = {
            "data_breach": f"Potential data breach detected in {random.choice(['patient_records', 'ai_models', 'audit_logs'])}",
            "system_failure": f"System component failure in {random.choice(['evidence_engine', 'risk_monitor', 'audit_agent'])}",
            "human_error": f"Configuration error by {random.choice(['admin', 'auditor', 'developer'])}",
            "cyber_attack": f"Suspicious activity detected from {random.choice(['external_ip', 'internal_user', 'api_endpoint'])}"
        }

        impact_scores = {"Low": 0.2, "Medium": 0.5, "High": 0.8, "Critical": 1.0}
        affected_standards_map = {
            "data_breach": ["ISO 27001", "ISO 27701"],
            "system_failure": ["ISO 42001", "ISO 80001-1"],
            "human_error": ["ISO 13485", "ISO 14971"],
            "cyber_attack": ["ISO 27001", "ISO 23894"]
        }

        return SimulationEvent(
            event_id=f"RE-{uuid.uuid4().hex[:8]}",
            timestamp=datetime.datetime.now() + datetime.timedelta(hours=hour),
            event_type="risk_event",
            description=f"{severity} severity: {event_descriptions[risk_type]}",
            parameters={"risk_type": risk_type, "severity": severity},
            impact_score=impact_scores[severity],
            affected_standards=affected_standards_map[risk_type],
            triggered_responses=["alert_generation", "evidence_collection", "risk_assessment"]
        )

class AuditSimulationScenario(ComplianceScenario):
    """Simulates external audit scenarios."""

    def __init__(self, scenario_id: str):
        super().__init__(
            scenario_id,
            "External Audit Simulation",
            "Simulates external audit processes and evidence requests"
        )

        self.parameters = {
            "audit_types": ["ISO_27001", "ISO_42001", "ISO_13485", "Combined"],
            "audit_duration_days": 5,
            "evidence_request_frequency": 0.3,  # Requests per hour
            "finding_probability": 0.15  # Probability of findings per request
        }

    async def execute(self, simulation_engine: 'LivingCertificationsSimulation') -> List[SimulationEvent]:
        """Execute audit simulation."""
        events = []
        audit_type = random.choice(self.parameters["audit_types"])
        duration_days = self.parameters["audit_duration_days"]

        # Audit start event
        start_event = SimulationEvent(
            event_id=f"AUDIT-START-{uuid.uuid4().hex[:8]}",
            timestamp=datetime.datetime.now(),
            event_type="audit_start",
            description=f"External {audit_type} audit initiated",
            parameters={"audit_type": audit_type, "scope": self._get_audit_scope(audit_type)},
            impact_score=0.1,
            affected_standards=self._get_audit_scope(audit_type),
            triggered_responses=["audit_preparation", "evidence_review"]
        )
        events.append(start_event)
        self.add_event(start_event)

        # Simulate audit activities
        for day in range(duration_days):
            for hour in range(24):
                if random.random() < self.parameters["evidence_request_frequency"]:
                    event = self._generate_evidence_request(day, hour, audit_type)
                    events.append(event)
                    self.add_event(event)

                    # Simulate finding if applicable
                    if random.random() < self.parameters["finding_probability"]:
                        finding_event = self._generate_audit_finding(event)
                        events.append(finding_event)
                        self.add_event(finding_event)

        # Audit completion event
        end_event = SimulationEvent(
            event_id=f"AUDIT-END-{uuid.uuid4().hex[:8]}",
            timestamp=datetime.datetime.now() + datetime.timedelta(days=duration_days),
            event_type="audit_complete",
            description=f"{audit_type} audit completed with {len([e for e in events if e.event_type == 'audit_finding'])} findings",
            parameters={"findings_count": len([e for e in events if e.event_type == 'audit_finding'])},
            impact_score=0.0,
            affected_standards=self._get_audit_scope(audit_type),
            triggered_responses=["audit_report", "corrective_actions"]
        )
        events.append(end_event)
        self.add_event(end_event)

        return events

    def _get_audit_scope(self, audit_type: str) -> List[str]:
        """Get audit scope based on type."""
        scopes = {
            "ISO_27001": ["ISO 27001"],
            "ISO_42001": ["ISO 42001"],
            "ISO_13485": ["ISO 13485", "ISO 14971", "ISO 80001-1"],
            "Combined": ["ISO 42001", "ISO 27001", "ISO 27701", "ISO 13485"]
        }
        return scopes.get(audit_type, ["ISO 42001"])

    def _generate_evidence_request(self, day: int, hour: int, audit_type: str) -> SimulationEvent:
        """Generate evidence request event."""
        evidence_types = ["policy_document", "procedure", "evidence_bundle", "risk_assessment", "audit_trail"]
        evidence_type = random.choice(evidence_types)

        return SimulationEvent(
            event_id=f"REQ-{uuid.uuid4().hex[:8]}",
            timestamp=datetime.datetime.now() + datetime.timedelta(days=day, hours=hour),
            event_type="evidence_request",
            description=f"Auditor requested {evidence_type} for {audit_type} compliance",
            parameters={"evidence_type": evidence_type, "audit_type": audit_type},
            impact_score=0.5,
            affected_standards=self._get_audit_scope(audit_type),
            triggered_responses=["evidence_provision", "validation_check"]
        )

    def _generate_audit_finding(self, request_event: SimulationEvent) -> SimulationEvent:
        """Generate audit finding based on evidence request."""
        findings = [
            "Evidence format inconsistency",
            "Missing version control",
            "Incomplete documentation",
            "Process deviation detected",
            "Training record gap"
        ]
        finding = random.choice(findings)

        return SimulationEvent(
            event_id=f"FIND-{uuid.uuid4().hex[:8]}",
            timestamp=request_event.timestamp + datetime.timedelta(minutes=random.randint(30, 120)),
            event_type="audit_finding",
            description=f"Audit finding: {finding}",
            parameters={"finding": finding, "related_request": request_event.event_id},
            impact_score=0.3,
            affected_standards=request_event.affected_standards,
            triggered_responses=["finding_response", "corrective_action", "evidence_update"]
        )

class LivingCertificationsSimulation:
    """
    Main simulation engine for living certifications testing.
    """

    def __init__(self, repository_root: Path):
        self.repository_root = repository_root
        self.simulation_results_dir = repository_root / "certification" / "simulation_results"
        self.simulation_results_dir.mkdir(exist_ok=True)

        self.active_simulations: Dict[str, SimulationResult] = {}
        self.scenarios: Dict[str, ComplianceScenario] = {}

        # Simulation parameters
        self.time_acceleration = 1.0  # 1.0 = real time, 60.0 = 1 minute = 1 hour
        self.random_seed = 42
        random.seed(self.random_seed)
        np.random.seed(self.random_seed)

        # Response simulation
        self.response_handlers: Dict[str, Callable] = {
            "alert_generation": self._simulate_alert_response,
            "evidence_collection": self._simulate_evidence_response,
            "risk_assessment": self._simulate_risk_response,
            "audit_preparation": self._simulate_audit_prep_response,
            "corrective_action": self._simulate_corrective_response
        }

    def create_scenario(self, scenario_type: ScenarioType, scenario_id: Optional[str] = None) -> str:
        """Create a new simulation scenario."""
        if scenario_id is None:
            scenario_id = f"scenario-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

        if scenario_type == ScenarioType.RISK_EVENT:
            scenario = RiskEventScenario(scenario_id)
        elif scenario_type == ScenarioType.AUDIT_SIMULATION:
            scenario = AuditSimulationScenario(scenario_id)
        else:
            raise ValueError(f"Unsupported scenario type: {scenario_type}")

        self.scenarios[scenario_id] = scenario
        logger.info(f"Created scenario: {scenario_id} - {scenario.name}")
        return scenario_id

    async def run_simulation(self, scenario_id: str, mode: SimulationMode = SimulationMode.ACCELERATED,
                           duration_hours: int = 24) -> str:
        """Run a simulation scenario."""
        if scenario_id not in self.scenarios:
            raise ValueError(f"Scenario {scenario_id} not found")

        simulation_id = f"sim-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

        simulation_result = SimulationResult(
            simulation_id=simulation_id,
            scenario_type=self.scenarios[scenario_id].__class__.__name__.replace('Scenario', '').lower(),
            start_time=datetime.datetime.now(),
            end_time=None,
            status=SimulationStatus.RUNNING,
            events_generated=0,
            compliance_impact=0.0,
            risk_exposure=0.0,
            response_effectiveness=0.0,
            key_findings=[],
            recommendations=[]
        )

        self.active_simulations[simulation_id] = simulation_result

        try:
            logger.info(f"Starting simulation: {simulation_id} for scenario: {scenario_id}")

            # Set scenario parameters
            self.scenarios[scenario_id].parameters["duration_hours"] = duration_hours

            # Execute scenario
            events = await self.scenarios[scenario_id].execute(self)

            # Analyze results
            analysis = self._analyze_simulation_results(events)

            # Complete simulation
            simulation_result.end_time = datetime.datetime.now()
            simulation_result.status = SimulationStatus.COMPLETED
            simulation_result.events_generated = len(events)
            simulation_result.compliance_impact = analysis["compliance_impact"]
            simulation_result.risk_exposure = analysis["risk_exposure"]
            simulation_result.response_effectiveness = analysis["response_effectiveness"]
            simulation_result.key_findings = analysis["key_findings"]
            simulation_result.recommendations = analysis["recommendations"]

            # Save results
            self._save_simulation_result(simulation_result, events)

            logger.info(f"Simulation completed: {simulation_id} - {len(events)} events generated")

        except Exception as e:
            logger.error(f"Simulation failed: {simulation_id} - {e}")
            simulation_result.status = SimulationStatus.FAILED
            simulation_result.end_time = datetime.datetime.now()

        return simulation_id

    async def simulate_response(self, event: SimulationEvent):
        """Simulate system response to an event."""
        for response in event.triggered_responses:
            if response in self.response_handlers:
                await self.response_handlers[response](event)

    async def _simulate_alert_response(self, event: SimulationEvent):
        """Simulate alert generation response."""
        # Simulate alert processing time
        await asyncio.sleep(0.1 * self.time_acceleration)
        logger.debug(f"Alert generated for event: {event.event_id}")

    async def _simulate_evidence_response(self, event: SimulationEvent):
        """Simulate evidence collection response."""
        # Simulate evidence gathering time
        await asyncio.sleep(0.5 * self.time_acceleration)
        logger.debug(f"Evidence collected for event: {event.event_id}")

    async def _simulate_risk_response(self, event: SimulationEvent):
        """Simulate risk assessment response."""
        # Simulate risk analysis time
        await asyncio.sleep(0.3 * self.time_acceleration)
        logger.debug(f"Risk assessment completed for event: {event.event_id}")

    async def _simulate_audit_prep_response(self, event: SimulationEvent):
        """Simulate audit preparation response."""
        # Simulate preparation time
        await asyncio.sleep(1.0 * self.time_acceleration)
        logger.debug(f"Audit preparation completed for event: {event.event_id}")

    async def _simulate_corrective_response(self, event: SimulationEvent):
        """Simulate corrective action response."""
        # Simulate corrective action time
        await asyncio.sleep(2.0 * self.time_acceleration)
        logger.debug(f"Corrective action completed for event: {event.event_id}")

    def _analyze_simulation_results(self, events: List[SimulationEvent]) -> Dict[str, Any]:
        """Analyze simulation results."""
        analysis = {
            "compliance_impact": 0.0,
            "risk_exposure": 0.0,
            "response_effectiveness": 0.0,
            "key_findings": [],
            "recommendations": []
        }

        if not events:
            return analysis

        # Calculate compliance impact
        high_impact_events = [e for e in events if e.impact_score > 0.7]
        analysis["compliance_impact"] = len(high_impact_events) / len(events)

        # Calculate risk exposure
        total_impact = sum(e.impact_score for e in events)
        analysis["risk_exposure"] = min(1.0, total_impact / len(events))

        # Calculate response effectiveness (simplified)
        response_events = [e for e in events if e.triggered_responses]
        analysis["response_effectiveness"] = len(response_events) / len(events)

        # Generate key findings
        event_types = defaultdict(int)
        for event in events:
            event_types[event.event_type] += 1

        analysis["key_findings"] = [
            f"Generated {count} {event_type} events" for event_type, count in event_types.items()
        ]

        # Generate recommendations
        if analysis["compliance_impact"] > 0.5:
            analysis["recommendations"].append("Strengthen compliance monitoring for high-impact events")
        if analysis["risk_exposure"] > 0.7:
            analysis["recommendations"].append("Implement additional risk mitigation controls")
        if analysis["response_effectiveness"] < 0.8:
            analysis["recommendations"].append("Improve automated response effectiveness")

        return analysis

    def _save_simulation_result(self, result: SimulationResult, events: List[SimulationEvent]):
        """Save simulation results to file."""
        result_file = self.simulation_results_dir / f"simulation_result_{result.simulation_id}.json"

        data = result.to_dict()
        data["events"] = [event.to_dict() for event in events]

        with open(result_file, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"Simulation results saved: {result_file}")

    def get_simulation_history(self) -> List[Dict]:
        """Get simulation history."""
        result_files = list(self.simulation_results_dir.glob("simulation_result_*.json"))
        history = []

        for result_file in result_files:
            try:
                with open(result_file, 'r') as f:
                    data = json.load(f)
                    history.append(data)
            except Exception as e:
                logger.error(f"Error reading simulation result file {result_file}: {e}")

        # Sort by start time, most recent first
        history.sort(key=lambda x: x.get('start_time', ''), reverse=True)
        return history

    def get_scenario_templates(self) -> List[Dict]:
        """Get available scenario templates."""
        return [
            {
                "type": "risk_event",
                "name": "Risk Event Simulation",
                "description": "Simulates various risk events and compliance responses",
                "parameters": {
                    "duration_hours": 24,
                    "risk_types": ["data_breach", "system_failure", "human_error", "cyber_attack"],
                    "event_frequency": 0.1
                }
            },
            {
                "type": "audit_simulation",
                "name": "External Audit Simulation",
                "description": "Simulates external audit processes and evidence requests",
                "parameters": {
                    "audit_types": ["ISO_27001", "ISO_42001", "ISO_13485", "Combined"],
                    "audit_duration_days": 5,
                    "evidence_request_frequency": 0.3
                }
            }
        ]

    async def run_monte_carlo_simulation(self, scenario_type: ScenarioType, runs: int = 100,
                                          duration_hours: int = 24) -> Dict[str, Any]:
        """Run Monte Carlo simulation for statistical analysis."""
        results = []

        for run in range(runs):
            # Create scenario
            scenario_id = self.create_scenario(scenario_type, f"mc-{run}")

            # Run simulation
            simulation_id = await self.run_simulation(scenario_id, SimulationMode.ACCELERATED, duration_hours)

            # Get result
            result = self.active_simulations.get(simulation_id)
            if result:
                results.append({
                    "compliance_impact": result.compliance_impact,
                    "risk_exposure": result.risk_exposure,
                    "response_effectiveness": result.response_effectiveness,
                    "events_generated": result.events_generated
                })

        # Calculate statistics
        if results:
            stats = {
                "runs": runs,
                "mean_compliance_impact": np.mean([r["compliance_impact"] for r in results]),
                "std_compliance_impact": np.std([r["compliance_impact"] for r in results]),
                "mean_risk_exposure": np.mean([r["risk_exposure"] for r in results]),
                "std_risk_exposure": np.std([r["risk_exposure"] for r in results]),
                "mean_response_effectiveness": np.mean([r["response_effectiveness"] for r in results]),
                "std_response_effectiveness": np.std([r["response_effectiveness"] for r in results]),
                "mean_events": np.mean([r["events_generated"] for r in results]),
                "confidence_intervals": {
                    "compliance_impact_95": self._calculate_confidence_interval([r["compliance_impact"] for r in results]),
                    "risk_exposure_95": self._calculate_confidence_interval([r["risk_exposure"] for r in results])
                }
            }
        else:
            stats = {"error": "No simulation results available"}

        return stats

    def _calculate_confidence_interval(self, data: List[float], confidence: float = 0.95) -> Tuple[float, float]:
        """Calculate confidence interval for data."""
        mean = np.mean(data)
        std = np.std(data)
        n = len(data)

        # t-score for 95% confidence (approximate)
        t_score = 1.96

        margin = t_score * (std / np.sqrt(n))
        return (mean - margin, mean + margin)

# Global simulation instance
_simulation_instance = None

def get_simulation_engine(repository_root: Path = None) -> LivingCertificationsSimulation:
    """Get the global simulation engine instance."""
    global _simulation_instance

    if _simulation_instance is None:
        if repository_root is None:
            repository_root = Path("/workspaces/iLuminara-Core")
        _simulation_instance = LivingCertificationsSimulation(repository_root)

    return _simulation_instance

# Convenience functions
async def run_risk_simulation(duration_hours: int = 24) -> str:
    """Run a risk event simulation."""
    engine = get_simulation_engine()
    scenario_id = engine.create_scenario(ScenarioType.RISK_EVENT)
    return await engine.run_simulation(scenario_id, duration_hours=duration_hours)

async def run_audit_simulation() -> str:
    """Run an audit simulation."""
    engine = get_simulation_engine()
    scenario_id = engine.create_scenario(ScenarioType.AUDIT_SIMULATION)
    return await engine.run_simulation(scenario_id)

async def run_monte_carlo_analysis(runs: int = 50) -> Dict[str, Any]:
    """Run Monte Carlo analysis."""
    engine = get_simulation_engine()
    return await engine.run_monte_carlo_simulation(ScenarioType.RISK_EVENT, runs=runs)

def get_simulation_history() -> List[Dict]:
    """Get simulation history."""
    engine = get_simulation_engine()
    return engine.get_simulation_history()

if __name__ == "__main__":
    # Example usage
    async def main():
        # Run a risk simulation
        sim_id = await run_risk_simulation(duration_hours=12)
        print(f"Risk simulation completed: {sim_id}")

        # Run an audit simulation
        audit_sim_id = await run_audit_simulation()
        print(f"Audit simulation completed: {audit_sim_id}")

        # Run Monte Carlo analysis
        mc_results = await run_monte_carlo_analysis(runs=10)
        print(f"Monte Carlo results: {mc_results}")

        # Get simulation history
        history = get_simulation_history()
        print(f"Total simulations: {len(history)}")

    asyncio.run(main())