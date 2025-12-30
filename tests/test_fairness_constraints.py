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
Tests for Fairness Constraint Engine
═════════════════════════════════════════════════════════════════════════════

Tests verify:
1. Fairness metrics calculation
2. Bias detection
3. Equity gap identification
4. Protected group treatment
5. Vulnerability-adjusted allocation
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from governance_kernel.fairness_constraints import (
    FairnessConstraintEngine,
    PopulationGroup,
    FairnessViolationError
)


class TestFairnessConstraintEngine(unittest.TestCase):
    """Test suite for Fairness Constraint Engine."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = FairnessConstraintEngine(fairness_threshold=0.8)
    
    def test_initialization(self):
        """Test engine initializes correctly."""
        self.assertIsNotNone(self.engine)
        self.assertEqual(self.engine.fairness_threshold, 0.8)
        self.assertGreater(len(self.engine.protected_characteristics), 0)
    
    def test_demographic_parity_perfect(self):
        """Test demographic parity with equal per-capita allocation."""
        groups = [
            PopulationGroup(
                group_id="G1",
                name="Group_1",
                size=1000,
                need_level=0.5,
                proposed_allocation=1000  # 1.0 per capita
            ),
            PopulationGroup(
                group_id="G2",
                name="Group_2",
                size=2000,
                need_level=0.5,
                proposed_allocation=2000  # 1.0 per capita
            )
        ]
        
        score = self.engine._evaluate_demographic_parity(groups)
        
        # Perfect parity should give high score
        self.assertGreater(score, 0.95)
    
    def test_demographic_parity_unequal(self):
        """Test demographic parity detects unequal allocation."""
        groups = [
            PopulationGroup(
                group_id="G1",
                name="Group_1",
                size=1000,
                need_level=0.5,
                proposed_allocation=100  # 0.1 per capita
            ),
            PopulationGroup(
                group_id="G2",
                name="Group_2",
                size=1000,
                need_level=0.5,
                proposed_allocation=900  # 0.9 per capita
            )
        ]
        
        score = self.engine._evaluate_demographic_parity(groups)
        
        # Unequal allocation should give lower score
        self.assertLess(score, 0.8)
    
    def test_equal_opportunity_all_included(self):
        """Test equal opportunity when all groups receive something."""
        groups = [
            PopulationGroup(
                group_id="G1",
                name="Group_1",
                size=500,
                need_level=0.8,
                proposed_allocation=100
            ),
            PopulationGroup(
                group_id="G2",
                name="Group_2",
                size=500,
                need_level=0.6,
                proposed_allocation=50
            )
        ]
        
        score = self.engine._evaluate_equal_opportunity(groups)
        
        # All groups with need receive something = perfect score
        self.assertEqual(score, 1.0)
    
    def test_equal_opportunity_exclusion_detected(self):
        """Test equal opportunity detects excluded groups."""
        groups = [
            PopulationGroup(
                group_id="G1",
                name="Group_1",
                size=500,
                need_level=0.8,
                proposed_allocation=200
            ),
            PopulationGroup(
                group_id="G2",
                name="Group_2",
                size=500,
                need_level=0.7,  # Has need
                proposed_allocation=0  # But receives nothing - exclusion!
            )
        ]
        
        score = self.engine._evaluate_equal_opportunity(groups)
        
        # One group excluded = score should be 0.5 (50% inclusion)
        self.assertAlmostEqual(score, 0.5, places=2)
    
    def test_proportional_allocation_aligned(self):
        """Test proportional allocation when allocation matches need."""
        groups = [
            PopulationGroup(
                group_id="G1",
                name="Group_1",
                size=100,
                need_level=0.9,
                proposed_allocation=90
            ),
            PopulationGroup(
                group_id="G2",
                name="Group_2",
                size=100,
                need_level=0.5,
                proposed_allocation=50
            ),
            PopulationGroup(
                group_id="G3",
                name="Group_3",
                size=100,
                need_level=0.3,
                proposed_allocation=30
            )
        ]
        
        score = self.engine._evaluate_proportional_allocation(groups)
        
        # Perfectly aligned allocation should give high score
        self.assertGreater(score, 0.9)
    
    def test_protected_groups_prioritized(self):
        """Test that protected groups receive at least equal treatment."""
        groups = [
            PopulationGroup(
                group_id="G1",
                name="Children",
                size=200,
                is_protected_group=True,
                proposed_allocation=400  # 2.0 per capita
            ),
            PopulationGroup(
                group_id="G2",
                name="Adults",
                size=800,
                is_protected_group=False,
                proposed_allocation=800  # 1.0 per capita
            )
        ]
        
        score = self.engine._evaluate_protected_groups(groups)
        
        # Protected groups getting more should give perfect score
        self.assertEqual(score, 1.0)
    
    def test_protected_groups_disadvantaged_detected(self):
        """Test detection when protected groups are disadvantaged."""
        groups = [
            PopulationGroup(
                group_id="G1",
                name="Children",
                size=200,
                is_protected_group=True,
                proposed_allocation=100  # 0.5 per capita
            ),
            PopulationGroup(
                group_id="G2",
                name="Adults",
                size=800,
                is_protected_group=False,
                proposed_allocation=1600  # 2.0 per capita
            )
        ]
        
        score = self.engine._evaluate_protected_groups(groups)
        
        # Protected groups getting less should give low score
        self.assertLess(score, 0.5)
    
    def test_vulnerability_equity_weighted(self):
        """Test vulnerability-weighted equity calculation."""
        groups = [
            PopulationGroup(
                group_id="G1",
                name="Highly_Vulnerable",
                size=100,
                need_level=0.9,
                vulnerability_score=1.5,
                proposed_allocation=135  # Should get more due to vulnerability
            ),
            PopulationGroup(
                group_id="G2",
                name="Less_Vulnerable",
                size=100,
                need_level=0.9,
                vulnerability_score=1.0,
                proposed_allocation=90
            )
        ]
        
        score = self.engine._evaluate_vulnerability_equity(groups)
        
        # Vulnerability-weighted allocation should give reasonable score
        self.assertGreater(score, 0.5)
    
    def test_bias_detection(self):
        """Test bias detection across characteristics."""
        groups = [
            PopulationGroup(
                group_id="G1",
                name="Group_A",
                size=500,
                characteristics={"ethnicity": True},  # Group A ethnicity
                proposed_allocation=50  # 0.1 per capita
            ),
            PopulationGroup(
                group_id="G2",
                name="Group_B",
                size=500,
                characteristics={"ethnicity": False},  # Group B ethnicity
                proposed_allocation=450  # 0.9 per capita
            )
        ]
        
        bias_indicators = self.engine._detect_bias(groups)
        
        # Should detect bias in ethnicity
        self.assertIn("ethnicity", bias_indicators)
        self.assertGreater(bias_indicators["ethnicity"], 0.5)  # Significant bias
    
    def test_equity_gap_identification(self):
        """Test identification of equity gaps."""
        groups = [
            PopulationGroup(
                group_id="G1",
                name="High_Need_Group",
                size=200,
                need_level=0.9,  # High need
                proposed_allocation=20  # Very low allocation - gap!
            ),
            PopulationGroup(
                group_id="G2",
                name="Vulnerable_Excluded",
                size=100,
                vulnerability_score=1.4,  # Vulnerable
                proposed_allocation=0  # Excluded - critical gap!
            )
        ]
        
        equity_gaps = self.engine._identify_equity_gaps(groups)
        
        # Should identify both gaps
        self.assertGreater(len(equity_gaps), 0)
        
        # Check for high need low allocation gap
        high_need_gaps = [g for g in equity_gaps if g["type"] == "high_need_low_allocation"]
        self.assertGreater(len(high_need_gaps), 0)
        
        # Check for vulnerable exclusion gap
        exclusion_gaps = [g for g in equity_gaps if g["type"] == "vulnerable_group_excluded"]
        self.assertGreater(len(exclusion_gaps), 0)
    
    def test_fairness_assessment_comprehensive(self):
        """Test comprehensive fairness assessment."""
        groups = [
            PopulationGroup(
                group_id="G1",
                name="Group_1",
                size=1000,
                need_level=0.8,
                vulnerability_score=1.2,
                is_protected_group=True,
                proposed_allocation=960
            ),
            PopulationGroup(
                group_id="G2",
                name="Group_2",
                size=2000,
                need_level=0.6,
                vulnerability_score=1.0,
                is_protected_group=False,
                proposed_allocation=1200
            )
        ]
        
        assessment = self.engine.evaluate_fairness(
            groups=groups,
            allocation_plan={},
            enforce_constraints=False
        )
        
        # Verify assessment structure
        self.assertIsNotNone(assessment)
        self.assertGreater(assessment.overall_fairness_score, 0.0)
        self.assertLessEqual(assessment.overall_fairness_score, 1.0)
        
        # Verify metrics calculated
        self.assertIn("demographic_parity", assessment.metric_scores)
        self.assertIn("equal_opportunity", assessment.metric_scores)
        self.assertIn("proportional_allocation", assessment.metric_scores)
    
    def test_fairness_violation_enforcement(self):
        """Test that fairness violations are enforced when requested."""
        groups = [
            PopulationGroup(
                group_id="G1",
                name="Excluded_Group",
                size=1000,
                need_level=0.9,  # High need
                proposed_allocation=0  # No allocation - unfair!
            ),
            PopulationGroup(
                group_id="G2",
                name="Favored_Group",
                size=1000,
                need_level=0.2,  # Low need
                proposed_allocation=1000  # All resources - unfair!
            )
        ]
        
        # Should raise FairnessViolationError
        with self.assertRaises(FairnessViolationError):
            self.engine.evaluate_fairness(
                groups=groups,
                allocation_plan={},
                enforce_constraints=True
            )
    
    def test_fairness_recommendations_generated(self):
        """Test that recommendations are generated for low scores."""
        groups = [
            PopulationGroup(
                group_id="G1",
                name="Group_1",
                size=1000,
                need_level=0.9,
                proposed_allocation=100  # Under-allocated
            ),
            PopulationGroup(
                group_id="G2",
                name="Group_2",
                size=1000,
                need_level=0.3,
                proposed_allocation=900  # Over-allocated
            )
        ]
        
        assessment = self.engine.evaluate_fairness(
            groups=groups,
            allocation_plan={},
            enforce_constraints=False
        )
        
        # Should generate recommendations
        self.assertGreater(len(assessment.recommendations), 0)
    
    def test_automatic_fairness_adjustment(self):
        """Test automatic adjustment to meet fairness constraints."""
        groups = [
            PopulationGroup(
                group_id="G1",
                name="High_Need_Group",
                size=500,
                need_level=0.9,
                vulnerability_score=1.4,
                is_protected_group=True,
                proposed_allocation=0  # Start with unfair allocation
            ),
            PopulationGroup(
                group_id="G2",
                name="Standard_Group",
                size=1500,
                need_level=0.5,
                vulnerability_score=1.0,
                is_protected_group=False,
                proposed_allocation=0
            )
        ]
        
        total_resources = 2000
        
        # Adjust allocation for fairness
        adjusted_groups = self.engine.adjust_allocation_for_fairness(
            groups=groups,
            total_resources=total_resources,
            min_fairness_score=0.85
        )
        
        # Verify adjustments made
        self.assertGreater(adjusted_groups[0].proposed_allocation, 0)
        self.assertGreater(adjusted_groups[1].proposed_allocation, 0)
        
        # Verify total allocation equals available resources
        total_allocated = sum(g.proposed_allocation for g in adjusted_groups)
        self.assertAlmostEqual(total_allocated, total_resources, places=1)
        
        # Verify protected group prioritized
        protected_per_capita = adjusted_groups[0].proposed_allocation / adjusted_groups[0].size
        standard_per_capita = adjusted_groups[1].proposed_allocation / adjusted_groups[1].size
        self.assertGreaterEqual(protected_per_capita, standard_per_capita * 0.9)


if __name__ == "__main__":
    unittest.main()
