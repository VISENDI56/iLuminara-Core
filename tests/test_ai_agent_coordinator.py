"""
Tests for AI Agent Coordinator
═════════════════════════════════════════════════════════════════════════════

Tests verify:
1. Integrated decision pipeline
2. Multi-layer ethical validation
3. Rejection of violations
4. Comprehensive audit trail
5. Export functionality
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from governance_kernel.ai_agent_coordinator import (
    AIAgentCoordinator,
    CrisisScenarioType,
    IntegratedDecisionResult
)
from governance_kernel.crisis_decision_agent import DecisionType


class TestAIAgentCoordinator(unittest.TestCase):
    """Test suite for AI Agent Coordinator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.coordinator = AIAgentCoordinator(
            fairness_threshold=0.8,
            confidence_threshold=0.7
        )
    
    def test_initialization(self):
        """Test coordinator initializes correctly."""
        self.assertIsNotNone(self.coordinator)
        self.assertIsNotNone(self.coordinator.crisis_agent)
        self.assertIsNotNone(self.coordinator.fairness_engine)
        self.assertIsNotNone(self.coordinator.sovereignty_guardrail)
    
    def test_integrated_decision_success(self):
        """Test successful integrated decision through full pipeline."""
        population_groups = [
            {
                "group_id": "children",
                "name": "Children_Under_5",
                "size": 300,
                "characteristics": {"age_group": "children"},
                "vulnerability_score": 1.5,
                "need_level": 0.8,
                "is_protected_group": True
            },
            {
                "group_id": "adults",
                "name": "Adults",
                "size": 1200,
                "characteristics": {"age_group": "adults"},
                "vulnerability_score": 1.0,
                "need_level": 0.6,
                "is_protected_group": False
            },
            {
                "group_id": "elderly",
                "name": "Elderly_Over_65",
                "size": 200,
                "characteristics": {"age_group": "elderly"},
                "vulnerability_score": 1.3,
                "need_level": 0.7,
                "is_protected_group": True
            }
        ]
        
        resources = {
            "medical_supplies": 5000,
            "food_packages": 10000,
            "water_liters": 20000
        }
        
        result = self.coordinator.execute_crisis_decision(
            scenario_type=CrisisScenarioType.DISEASE_OUTBREAK,
            decision_type=DecisionType.RESOURCE_ALLOCATION,
            affected_area="Dadaab_Refugee_Camp",
            population_groups=population_groups,
            resources_available=resources,
            jurisdiction="KDPA_KE"
        )
        
        # Verify result structure
        self.assertIsNotNone(result)
        self.assertIsInstance(result, IntegratedDecisionResult)
        
        # Verify decision output
        self.assertIsNotNone(result.decision_output)
        self.assertEqual(result.decision_output.decision_type, DecisionType.RESOURCE_ALLOCATION)
        
        # Verify fairness assessment
        self.assertIsNotNone(result.fairness_assessment)
        self.assertGreaterEqual(result.fairness_assessment.overall_fairness_score, 0.0)
        
        # Verify sovereignty compliance checked
        self.assertIsNotNone(result.sovereignty_compliance)
        self.assertIn("jurisdiction", result.sovereignty_compliance)
        
        # Verify ethical summary generated
        self.assertIsNotNone(result.ethical_summary)
        self.assertIn("ETHICAL DECISION SUMMARY", result.ethical_summary)
    
    def test_high_risk_requires_review(self):
        """Test that high-risk decisions require human review."""
        population_groups = [
            {
                "group_id": "population",
                "name": "Entire_Population",
                "size": 15000,
                "vulnerability_score": 1.0,
                "need_level": 0.9,
                "is_protected_group": False
            }
        ]
        
        result = self.coordinator.execute_crisis_decision(
            scenario_type=CrisisScenarioType.NATURAL_DISASTER,
            decision_type=DecisionType.EVACUATION_ORDER,
            affected_area="Coastal_Region",
            population_groups=population_groups,
            resources_available={},
            constraints={"time_sensitivity": "immediate"}
        )
        
        # Evacuation of large population should require review
        self.assertIn(result.approval_status, ["REQUIRES_HUMAN_REVIEW", "REJECTED"])
    
    def test_fairness_violation_handling(self):
        """Test handling of fairness violations."""
        # Create extremely unfair scenario
        population_groups = [
            {
                "group_id": "favored",
                "name": "Favored_Group",
                "size": 500,
                "need_level": 0.2,  # Low need
                "vulnerability_score": 1.0,
                "is_protected_group": False,
                "proposed_allocation": 1000  # Gets everything
            },
            {
                "group_id": "neglected",
                "name": "Neglected_Protected_Group",
                "size": 500,
                "need_level": 0.9,  # High need
                "vulnerability_score": 1.5,
                "is_protected_group": True,
                "proposed_allocation": 0  # Gets nothing - unfair!
            }
        ]
        
        result = self.coordinator.execute_crisis_decision(
            scenario_type=CrisisScenarioType.FOOD_SECURITY_CRISIS,
            decision_type=DecisionType.SUPPLY_DISTRIBUTION,
            affected_area="Rural_Area",
            population_groups=population_groups,
            resources_available={"food": 1000}
        )
        
        # Should be flagged for review or rejected due to fairness
        if result.fairness_assessment.overall_fairness_score < 0.8:
            self.assertIn(result.approval_status, ["REQUIRES_HUMAN_REVIEW", "REJECTED"])
    
    def test_multi_layer_validation(self):
        """Test that all validation layers are executed."""
        population_groups = [
            {
                "group_id": "group1",
                "name": "Test_Group",
                "size": 1000,
                "vulnerability_score": 1.0,
                "need_level": 0.7,
                "is_protected_group": False
            }
        ]
        
        result = self.coordinator.execute_crisis_decision(
            scenario_type=CrisisScenarioType.MEDICAL_EMERGENCY,
            decision_type=DecisionType.MEDICAL_TRIAGE,
            affected_area="Field_Hospital",
            population_groups=population_groups,
            resources_available={"medical_staff": 20}
        )
        
        # Verify all validation components present
        self.assertIsNotNone(result.decision_output)  # Crisis decision
        self.assertIsNotNone(result.fairness_assessment)  # Fairness check
        self.assertIsNotNone(result.sovereignty_compliance)  # Legal check
        
        # Verify audit trail in decision
        self.assertGreater(len(result.decision_output.audit_trail), 0)
    
    def test_decision_history_logging(self):
        """Test that decisions are logged to history."""
        initial_history_len = len(self.coordinator.get_decision_history())
        
        population_groups = [
            {
                "group_id": "group1",
                "name": "Test_Group",
                "size": 500,
                "vulnerability_score": 1.0,
                "need_level": 0.5,
                "is_protected_group": False
            }
        ]
        
        result = self.coordinator.execute_crisis_decision(
            scenario_type=CrisisScenarioType.WATER_EMERGENCY,
            decision_type=DecisionType.SUPPLY_DISTRIBUTION,
            affected_area="Drought_Region",
            population_groups=population_groups,
            resources_available={"water": 5000}
        )
        
        # Verify decision was logged
        new_history_len = len(self.coordinator.get_decision_history())
        self.assertEqual(new_history_len, initial_history_len + 1)
        
        # Verify history entry
        latest_entry = self.coordinator.get_decision_history()[-1]
        self.assertEqual(latest_entry["decision_id"], result.decision_output.decision_id)
        self.assertEqual(latest_entry["scenario_type"], result.scenario_type.value)
    
    def test_export_decision_report(self):
        """Test exporting comprehensive decision report."""
        population_groups = [
            {
                "group_id": "group1",
                "name": "Test_Group",
                "size": 800,
                "vulnerability_score": 1.0,
                "need_level": 0.6,
                "is_protected_group": False
            }
        ]
        
        result = self.coordinator.execute_crisis_decision(
            scenario_type=CrisisScenarioType.DISEASE_OUTBREAK,
            decision_type=DecisionType.ALERT_BROADCAST,
            affected_area="Urban_Center",
            population_groups=population_groups,
            resources_available={}
        )
        
        # Export report
        report_json = self.coordinator.export_decision_report(result)
        
        # Verify export
        self.assertIsNotNone(report_json)
        self.assertIn("decision_metadata", report_json)
        self.assertIn("crisis_decision", report_json)
        self.assertIn("ethical_compliance", report_json)
        self.assertIn("fairness_assessment", report_json)
        self.assertIn("sovereignty_compliance", report_json)
    
    def test_protected_groups_prioritization(self):
        """Test that protected groups are properly prioritized."""
        population_groups = [
            {
                "group_id": "children",
                "name": "Children",
                "size": 400,
                "vulnerability_score": 1.5,
                "need_level": 0.8,
                "is_protected_group": True
            },
            {
                "group_id": "adults",
                "name": "Adults",
                "size": 1000,
                "vulnerability_score": 1.0,
                "need_level": 0.6,
                "is_protected_group": False
            }
        ]
        
        result = self.coordinator.execute_crisis_decision(
            scenario_type=CrisisScenarioType.CONFLICT_DISPLACEMENT,
            decision_type=DecisionType.SHELTER_ASSIGNMENT,
            affected_area="Displacement_Camp",
            population_groups=population_groups,
            resources_available={"shelter_units": 200}
        )
        
        # Check fairness assessment shows protected group consideration
        protected_group_score = result.fairness_assessment.metric_scores.get(
            "protected_group_fairness", 0
        )
        
        # Should have evaluated protected groups
        self.assertGreater(protected_group_score, 0.0)
    
    def test_rejection_result_structure(self):
        """Test structure of rejection results."""
        # Create scenario that will be rejected
        population_groups = [
            {
                "group_id": "group1",
                "name": "Test_Group",
                "size": 1000,
                "characteristics": {"test": True},
                "vulnerability_score": 1.0,
                "need_level": 0.5,
                "is_protected_group": False
            }
        ]
        
        # Note: This may not actually reject with our current implementation,
        # but we test the rejection path exists
        result = self.coordinator.execute_crisis_decision(
            scenario_type=CrisisScenarioType.DISEASE_OUTBREAK,
            decision_type=DecisionType.RESOURCE_ALLOCATION,
            affected_area="Test_Area",
            population_groups=population_groups,
            resources_available={}
        )
        
        # Verify result has all required fields even if not rejected
        self.assertIsNotNone(result.approval_status)
        self.assertIsNotNone(result.rejection_reasons)
        self.assertIsInstance(result.rejection_reasons, list)


if __name__ == "__main__":
    unittest.main()
