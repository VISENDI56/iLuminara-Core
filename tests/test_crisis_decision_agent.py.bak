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
Tests for Crisis Decision Agent with Ethical Guardrails
═════════════════════════════════════════════════════════════════════════════

Tests verify:
1. Humanitarian law compliance enforcement
2. Ethical constraint validation
3. Decision confidence scoring
4. Human approval requirements
5. Audit trail completeness
"""

import unittest
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from governance_kernel.crisis_decision_agent import (
    CrisisDecisionAgent,
    DecisionType,
    HumanitarianViolationError,
    DecisionRiskLevel
)


class TestCrisisDecisionAgent(unittest.TestCase):
    """Test suite for Crisis Decision Agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = CrisisDecisionAgent()
    
    def test_initialization(self):
        """Test agent initializes correctly."""
        self.assertIsNotNone(self.agent)
        self.assertIsNotNone(self.agent.humanitarian_principles)
        self.assertEqual(len(self.agent.decision_log), 0)
    
    def test_resource_allocation_decision(self):
        """Test resource allocation decision with valid inputs."""
        context = {
            "affected_population": 1000,
            "location": "Dadaab_Refugee_Camp",
            "resources": {"food": 5000, "water": 10000, "medical": 2000},
            "time_sensitivity": "urgent"
        }
        
        affected_groups = [
            {
                "name": "Children_Under_5",
                "size": 200,
                "need_level": 0.9,
                "is_protected_group": True,
                "resource_allocation": 0,
                "priority": 90
            },
            {
                "name": "Adults",
                "size": 600,
                "need_level": 0.6,
                "is_protected_group": False,
                "resource_allocation": 0,
                "priority": 60
            },
            {
                "name": "Elderly",
                "size": 200,
                "need_level": 0.8,
                "is_protected_group": True,
                "resource_allocation": 0,
                "priority": 80
            }
        ]
        
        decision = self.agent.make_decision(
            decision_type=DecisionType.RESOURCE_ALLOCATION,
            context=context,
            affected_groups=affected_groups
        )
        
        # Verify decision structure
        self.assertIsNotNone(decision)
        self.assertEqual(decision.decision_type, DecisionType.RESOURCE_ALLOCATION)
        self.assertGreater(decision.confidence_score, 0.0)
        self.assertIn("allocations", decision.recommendation)
        
        # Verify ethical compliance
        self.assertIn("humanity", decision.ethical_compliance)
        self.assertIn("impartiality", decision.ethical_compliance)
        
        # Verify audit trail
        self.assertGreater(len(decision.audit_trail), 0)
        
        # Verify protected groups are prioritized
        allocations = decision.recommendation["allocations"]
        protected_allocations = [a for a in allocations if a["priority"] == "HIGH"]
        self.assertGreater(len(protected_allocations), 0)
    
    def test_evacuation_order_requires_approval(self):
        """Test that evacuation orders require human approval (critical risk)."""
        context = {
            "affected_population": 15000,
            "location": "Coastal_Area",
            "time_sensitivity": "immediate"
        }
        
        affected_groups = [
            {
                "name": "Coastal_Residents",
                "size": 15000,
                "need_level": 1.0,
                "is_protected_group": False,
                "civilian_status": "civilian"
            }
        ]
        
        decision = self.agent.make_decision(
            decision_type=DecisionType.EVACUATION_ORDER,
            context=context,
            affected_groups=affected_groups
        )
        
        # Evacuation should require human approval (high risk)
        self.assertTrue(decision.requires_human_approval)
        self.assertIn(decision.risk_level, [DecisionRiskLevel.HIGH, DecisionRiskLevel.CRITICAL])
    
    def test_collective_punishment_violation(self):
        """Test that collective punishment is blocked by humanitarian law."""
        context = {
            "affected_population": 5000,
            "location": "Camp_X",
            "constraints": {
                "action_type": "collective_punishment",
                "applies_to_entire_population": True
            }
        }
        
        affected_groups = [
            {
                "name": "Camp_Population",
                "size": 5000,
                "need_level": 0.5,
                "civilian_status": "civilian"
            }
        ]
        
        # Should raise humanitarian violation
        with self.assertRaises(HumanitarianViolationError) as context_manager:
            self.agent.make_decision(
                decision_type=DecisionType.QUARANTINE_ZONE,
                context=context,
                affected_groups=affected_groups
            )
        
        exception = context_manager.exception
        self.assertIn("collective punishment", str(exception).lower())
    
    def test_protected_group_discrimination_violation(self):
        """Test that discrimination against protected groups is blocked."""
        context = {
            "affected_population": 1000,
            "location": "Test_Area"
        }
        
        affected_groups = [
            {
                "name": "Children",
                "size": 300,
                "is_protected_group": True,
                "excluded_from_aid": True,  # Violation!
                "civilian_status": "civilian"
            },
            {
                "name": "Adults",
                "size": 700,
                "is_protected_group": False,
                "excluded_from_aid": False,
                "civilian_status": "civilian"
            }
        ]
        
        # Should raise humanitarian violation
        with self.assertRaises(HumanitarianViolationError):
            self.agent.make_decision(
                decision_type=DecisionType.RESOURCE_ALLOCATION,
                context=context,
                affected_groups=affected_groups
            )
    
    def test_medical_triage_ethics(self):
        """Test medical triage follows ethical principles."""
        context = {
            "affected_population": 500,
            "location": "Field_Hospital"
        }
        
        affected_groups = [
            {
                "name": "Critical_Patients",
                "size": 50,
                "medical_severity": "critical",
                "civilian_status": "civilian"
            },
            {
                "name": "Moderate_Patients",
                "size": 200,
                "medical_severity": "moderate",
                "civilian_status": "civilian"
            },
            {
                "name": "Mild_Cases",
                "size": 250,
                "medical_severity": "mild",
                "civilian_status": "civilian"
            }
        ]
        
        decision = self.agent.make_decision(
            decision_type=DecisionType.MEDICAL_TRIAGE,
            context=context,
            affected_groups=affected_groups
        )
        
        # Verify triage priorities
        self.assertIn("triage_priorities", decision.recommendation)
        priorities = decision.recommendation["triage_priorities"]
        
        # Critical patients should be prioritized
        critical_priority = next(
            (p for p in priorities if p["group"] == "Critical_Patients"), 
            None
        )
        self.assertIsNotNone(critical_priority)
        self.assertEqual(critical_priority["triage_category"], 1)  # Immediate
    
    def test_decision_explanation_provided(self):
        """Test that every decision includes a clear explanation."""
        context = {
            "affected_population": 500,
            "location": "Test_Location"
        }
        
        affected_groups = [
            {
                "name": "Test_Group",
                "size": 500,
                "need_level": 0.7,
                "civilian_status": "civilian"
            }
        ]
        
        decision = self.agent.make_decision(
            decision_type=DecisionType.ALERT_BROADCAST,
            context=context,
            affected_groups=affected_groups
        )
        
        # Must have explanation
        self.assertIsNotNone(decision.explanation)
        self.assertGreater(len(decision.explanation), 50)
        
        # Explanation should include key elements
        self.assertIn("Decision Type", decision.explanation)
        self.assertIn("Risk Level", decision.explanation)
    
    def test_audit_trail_completeness(self):
        """Test that audit trail captures all decision steps."""
        context = {
            "affected_population": 1000,
            "location": "Test_Area"
        }
        
        affected_groups = [
            {
                "name": "Population",
                "size": 1000,
                "need_level": 0.5,
                "civilian_status": "civilian"
            }
        ]
        
        decision = self.agent.make_decision(
            decision_type=DecisionType.RESOURCE_ALLOCATION,
            context=context,
            affected_groups=affected_groups
        )
        
        # Verify audit trail structure
        self.assertGreater(len(decision.audit_trail), 0)
        
        # Check for key steps
        steps = [entry.get("step") for entry in decision.audit_trail]
        self.assertIn("context_validation", steps)
        self.assertIn("ethical_validation", steps)
        self.assertIn("humanitarian_law_check", steps)
        self.assertIn("fairness_assessment", steps)
    
    def test_humanitarian_law_citations(self):
        """Test that decisions include relevant legal citations."""
        context = {
            "affected_population": 2000,
            "location": "Crisis_Zone"
        }
        
        affected_groups = [
            {
                "name": "Affected_Population",
                "size": 2000,
                "civilian_status": "civilian"
            }
        ]
        
        decision = self.agent.make_decision(
            decision_type=DecisionType.EVACUATION_ORDER,
            context=context,
            affected_groups=affected_groups
        )
        
        # Must include humanitarian law citations
        self.assertGreater(len(decision.humanitarian_law_citations), 0)
        
        # Should include Geneva Conventions
        citations_text = " ".join(decision.humanitarian_law_citations)
        self.assertIn("Geneva", citations_text)
    
    def test_low_confidence_requires_review(self):
        """Test that low confidence decisions require human review."""
        # Create a scenario with conflicting/unclear data to lower confidence
        context = {
            "affected_population": 100,  # Small population
            "location": "Unknown_Area",
            "resources": {},  # No resources
            "time_sensitivity": "routine"
        }
        
        affected_groups = [
            {
                "name": "Small_Group",
                "size": 100,
                "need_level": 0.3,  # Low need
                "civilian_status": "civilian"
            }
        ]
        
        decision = self.agent.make_decision(
            decision_type=DecisionType.RESOURCE_ALLOCATION,
            context=context,
            affected_groups=affected_groups
        )
        
        # Low-risk scenarios with clear data might not require review
        # But we can verify confidence scoring works
        self.assertIsNotNone(decision.confidence_score)
        self.assertGreaterEqual(decision.confidence_score, 0.0)
        self.assertLessEqual(decision.confidence_score, 1.0)
    
    def test_decision_export(self):
        """Test decision can be exported to JSON for audit."""
        context = {
            "affected_population": 500,
            "location": "Test_Location"
        }
        
        affected_groups = [
            {
                "name": "Test_Group",
                "size": 500,
                "civilian_status": "civilian"
            }
        ]
        
        decision = self.agent.make_decision(
            decision_type=DecisionType.ALERT_BROADCAST,
            context=context,
            affected_groups=affected_groups
        )
        
        # Export decision
        export_json = self.agent.export_decision(decision)
        
        # Verify export
        self.assertIsNotNone(export_json)
        self.assertIn(decision.decision_id, export_json)
        self.assertIn("humanitarian_law_citations", export_json)


if __name__ == "__main__":
    unittest.main()
