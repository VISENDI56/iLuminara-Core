"""
Test suite for Ethical Engine and Humanitarian Margin Calculator
═════════════════════════════════════════════════════════════════

Tests the EthicalEngine class to ensure proper application of:
- Geneva Convention Article 3 constraints
- WHO outbreak response guidelines
- Humanitarian margin calculations
"""

import pytest
from governance_kernel.ethical_engine import (
    EthicalEngine,
    HumanitarianViolationError,
    ActionContext
)


class TestEthicalEngine:
    """Test suite for the EthicalEngine class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.engine = EthicalEngine(use_cloud_secrets=False)

    def test_initialization(self):
        """Test that the engine initializes with default protocols."""
        assert self.engine is not None
        assert 'geneva_convention_article_3' in self.engine.protocols
        assert 'who_outbreak_response' in self.engine.protocols
        assert 'humanitarian_margin' in self.engine.protocols

    def test_apply_constraints_conflict_zone(self):
        """Test proportionality constraints in conflict zones."""
        action = {
            'type': 'quarantine',
            'scope': 'district',
            'estimated_civilian_impact': 0.2,
            'medical_benefit': 0.8
        }
        context = {
            'conflict_zone': True,
            'outbreak_suspected': False,
            'healthcare_capacity': 0.8
        }
        
        result = self.engine.apply_constraints(action, context)
        
        assert 'action' in result
        assert 'humanitarian_margin' in result
        assert 'Geneva Convention Article 3 - Proportionality' in result['constraints_applied']
        assert result['action']['civilian_protection_measures'] is not None

    def test_apply_constraints_outbreak(self):
        """Test necessity constraints for outbreaks."""
        action = {
            'type': 'isolation_facility',
            'scope': 'community',
            'attack_rate': 0.02,  # 2% attack rate
            'r_effective': 2.5,
            'severity_score': 0.7
        }
        context = {
            'conflict_zone': False,
            'outbreak_suspected': True,
            'healthcare_capacity': 1.0
        }
        
        result = self.engine.apply_constraints(action, context)
        
        assert 'action' in result
        assert 'WHO IHR (2005) - Necessity' in result['constraints_applied']
        assert result['action']['review_required'] is True
        assert result['action']['duration_days'] is not None

    def test_apply_constraints_both_contexts(self):
        """Test combined conflict zone + outbreak scenario."""
        action = {
            'type': 'emergency_response',
            'scope': 'regional',
            'estimated_civilian_impact': 0.15,
            'medical_benefit': 0.85,
            'attack_rate': 0.03,
            'r_effective': 1.8,
            'severity_score': 0.8
        }
        context = {
            'conflict_zone': True,
            'outbreak_suspected': True,
            'civilian_population': 50000,
            'healthcare_capacity': 0.6
        }
        
        result = self.engine.apply_constraints(action, context)
        
        assert len(result['constraints_applied']) == 2
        assert 'Geneva Convention Article 3 - Proportionality' in result['constraints_applied']
        assert 'WHO IHR (2005) - Necessity' in result['constraints_applied']
        
        # Should have high humanitarian margin
        assert result['humanitarian_margin']['margin'] > 0.3

    def test_proportionality_violation(self):
        """Test that disproportionate actions are rejected."""
        action = {
            'type': 'forced_relocation',
            'scope': 'entire_city',
            'estimated_civilian_impact': 0.9,  # Very high harm
            'medical_benefit': 0.1  # Low benefit
        }
        context = {
            'conflict_zone': True,
            'healthcare_capacity': 0.5
        }
        
        with pytest.raises(HumanitarianViolationError) as exc_info:
            self.engine.apply_constraints(action, context)
        
        assert "PROPORTIONALITY VIOLATION" in str(exc_info.value)
        assert "Geneva Convention" in str(exc_info.value)

    def test_necessity_violation(self):
        """Test that unnecessary outbreak measures are rejected."""
        action = {
            'type': 'full_lockdown',
            'scope': 'country',
            'attack_rate': 0.001,  # Very low - 0.1%
            'r_effective': 0.8,  # Not spreading
            'severity_score': 0.2  # Low severity
        }
        context = {
            'outbreak_suspected': True,
            'healthcare_capacity': 1.0
        }
        
        with pytest.raises(HumanitarianViolationError) as exc_info:
            self.engine.apply_constraints(action, context)
        
        assert "NECESSITY VIOLATION" in str(exc_info.value)
        assert "WHO International Health Regulations" in str(exc_info.value)

    def test_humanitarian_margin_calculation_baseline(self):
        """Test humanitarian margin calculation for baseline scenario."""
        action = {'type': 'standard_surveillance'}
        context = ActionContext(
            conflict_zone=False,
            outbreak_suspected=False,
            healthcare_capacity=1.0
        )
        
        margin_result = self.engine._calculate_humanitarian_margin(action, context)
        
        assert margin_result['margin'] == 0.20  # Base margin
        assert margin_result['base'] == 0.20
        assert len(margin_result['multipliers']) == 0

    def test_humanitarian_margin_conflict_multiplier(self):
        """Test humanitarian margin increases in conflict zones."""
        action = {'type': 'medical_intervention'}
        context = ActionContext(
            conflict_zone=True,
            outbreak_suspected=False,
            healthcare_capacity=1.0
        )
        
        margin_result = self.engine._calculate_humanitarian_margin(action, context)
        
        assert margin_result['margin'] > 0.20  # Should be higher than base
        assert any('Conflict zone' in m for m in margin_result['multipliers'])

    def test_humanitarian_margin_outbreak_multiplier(self):
        """Test humanitarian margin increases for outbreaks."""
        action = {'type': 'containment_measure'}
        context = ActionContext(
            conflict_zone=False,
            outbreak_suspected=True,
            healthcare_capacity=1.0
        )
        
        margin_result = self.engine._calculate_humanitarian_margin(action, context)
        
        assert margin_result['margin'] > 0.20  # Should be higher than base
        assert any('Outbreak' in m for m in margin_result['multipliers'])

    def test_humanitarian_margin_capacity_constraint(self):
        """Test margin adjusts for healthcare capacity constraints."""
        action = {'type': 'resource_allocation'}
        context = ActionContext(
            conflict_zone=False,
            outbreak_suspected=False,
            healthcare_capacity=0.3  # Low capacity
        )
        
        margin_result = self.engine._calculate_humanitarian_margin(action, context)
        
        assert any('Capacity constraint' in m for m in margin_result['multipliers'])
        assert margin_result['factors']['healthcare_capacity'] == 0.3

    def test_humanitarian_margin_combined_factors(self):
        """Test margin calculation with all factors combined."""
        action = {'type': 'crisis_response'}
        context = ActionContext(
            conflict_zone=True,
            outbreak_suspected=True,
            healthcare_capacity=0.4
        )
        
        margin_result = self.engine._calculate_humanitarian_margin(action, context)
        
        # Should have high margin due to multiple crisis factors
        assert margin_result['margin'] > 0.25
        assert len(margin_result['multipliers']) >= 2
        assert 'HIGH' in margin_result['interpretation'] or 'MODERATE' in margin_result['interpretation']

    def test_proportionality_with_low_capacity(self):
        """Test that low capacity triggers scope reduction."""
        action = {
            'type': 'vaccination_campaign',
            'scope': 'national',
            'estimated_civilian_impact': 0.05,
            'medical_benefit': 0.9
        }
        context = {
            'conflict_zone': True,
            'healthcare_capacity': 0.3  # Very low
        }
        
        result = self.engine.apply_constraints(action, context)
        
        # Should reduce scope due to capacity constraint
        assert result['action']['scope'] == 'limited'
        assert 'capacity_constraint' in result['action']

    def test_necessity_adds_time_limits(self):
        """Test that necessity constraints add time limits."""
        action = {
            'type': 'contact_tracing',
            'attack_rate': 0.05,
            'r_effective': 2.0,
            'severity_score': 0.6
        }
        context = {
            'outbreak_suspected': True
        }
        
        result = self.engine.apply_constraints(action, context)
        
        assert 'duration_days' in result['action']
        assert result['action']['review_required'] is True
        assert 'review_interval_days' in result['action']

    def test_audit_logging(self):
        """Test that actions are properly logged."""
        self.engine.clear_audit_log()
        
        action = {
            'type': 'test_action',
            'estimated_civilian_impact': 0.1,
            'medical_benefit': 0.8
        }
        context = {
            'conflict_zone': True
        }
        
        self.engine.apply_constraints(action, context)
        
        audit_log = self.engine.get_audit_log()
        assert len(audit_log) > 0
        assert any('CONSTRAINT_APPLICATION' in entry['level'] for entry in audit_log)

    def test_action_context_dataclass(self):
        """Test ActionContext dataclass creation."""
        ctx = ActionContext(
            conflict_zone=True,
            outbreak_suspected=True,
            civilian_population=100000,
            healthcare_capacity=0.7
        )
        
        assert ctx.conflict_zone is True
        assert ctx.outbreak_suspected is True
        assert ctx.civilian_population == 100000
        assert ctx.healthcare_capacity == 0.7
        assert ctx.timestamp is not None


class TestIntegrationScenarios:
    """Integration tests for realistic scenarios."""

    def setup_method(self):
        """Set up test fixtures."""
        self.engine = EthicalEngine(use_cloud_secrets=False)

    def test_dadaab_cholera_outbreak_scenario(self):
        """Test realistic cholera outbreak response in Dadaab."""
        action = {
            'type': 'cholera_response',
            'scope': 'refugee_camp',
            'estimated_civilian_impact': 0.3,
            'medical_benefit': 0.85,
            'attack_rate': 0.04,  # 4% attack rate
            'r_effective': 2.8,
            'severity_score': 0.75
        }
        context = {
            'conflict_zone': False,  # Non-conflict zone scenario
            'outbreak_suspected': True,
            'civilian_population': 200000,
            'healthcare_capacity': 0.5  # Limited capacity
        }
        
        result = self.engine.apply_constraints(action, context)
        
        # Should pass both constraints
        assert len(result['violations']) == 0
        assert result['humanitarian_margin']['margin'] > 0.2
        assert result['action']['review_required'] is True

    def test_syria_conflict_medical_response(self):
        """Test medical response in Syrian conflict context."""
        action = {
            'type': 'field_hospital',
            'scope': 'conflict_zone',
            'estimated_civilian_impact': 0.05,
            'medical_benefit': 0.95
        }
        context = {
            'conflict_zone': True,
            'outbreak_suspected': False,
            'civilian_population': 50000,
            'healthcare_capacity': 0.2  # Collapsed infrastructure
        }
        
        result = self.engine.apply_constraints(action, context)
        
        # Should have civilian protection measures
        assert 'civilian_protection_measures' in result['action']
        assert 'medical neutrality' in str(result['action']['civilian_protection_measures']).lower()
        
        # Should have high humanitarian margin
        assert result['humanitarian_margin']['margin'] > 0.25


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
