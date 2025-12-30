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
Tests for Humanitarian Constraint Encoding System
═════════════════════════════════════════════════════════════════════════════

Tests the three core components:
1. Vertex AI Explainable AI (SHAP analysis)
2. Cloud Functions Constraint Checker
3. Secret Manager Protocol Store
"""

import unittest
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from governance_kernel.humanitarian_constraints import (
    VertexAIExplainableAI,
    CloudFunctionConstraintChecker,
    SecretManagerProtocolStore,
    HumanitarianProtocol,
    ConstraintCategory,
    ConstraintSeverity,
    SHAPExplanation,
    ConstraintViolation,
)


class TestVertexAIExplainableAI(unittest.TestCase):
    """Tests for Vertex AI Explainable AI SHAP analysis."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.explainer = VertexAIExplainableAI(
            project_id="test-project",
            region="us-central1"
        )
    
    def test_explain_prediction(self):
        """Test SHAP explanation generation."""
        input_data = {
            "symptom_severity": 8,
            "temperature": 39.5,
            "risk_score": 7.5,
        }
        
        explanation = self.explainer.explain_prediction(
            model_id="test-model",
            input_data=input_data,
            prediction="HIGH_RISK",
            feature_names=list(input_data.keys()),
        )
        
        self.assertIsInstance(explanation, SHAPExplanation)
        self.assertEqual(explanation.model_prediction, "HIGH_RISK")
        self.assertEqual(len(explanation.shap_values), 3)
        self.assertIn("symptom_severity", explanation.shap_values)
        self.assertIn("temperature", explanation.shap_values)
        self.assertIn("risk_score", explanation.shap_values)
    
    def test_get_top_contributors(self):
        """Test getting top contributing features."""
        input_data = {
            "feature_a": 5,
            "feature_b": 3,
            "feature_c": 8,
        }
        
        explanation = self.explainer.explain_prediction(
            model_id="test-model",
            input_data=input_data,
            prediction="POSITIVE",
            feature_names=list(input_data.keys()),
        )
        
        top_contributors = explanation.get_top_contributors(n=2)
        self.assertEqual(len(top_contributors), 2)
        self.assertIsInstance(top_contributors[0], tuple)
        self.assertEqual(len(top_contributors[0]), 2)  # (feature_name, shap_value)
    
    def test_validate_explainability_valid(self):
        """Test explainability validation with valid explanation."""
        input_data = {
            "feature_1": 10,
            "feature_2": 5,
            "feature_3": 8,
        }
        
        explanation = self.explainer.explain_prediction(
            model_id="test-model",
            input_data=input_data,
            prediction="OUTCOME",
            feature_names=list(input_data.keys()),
        )
        
        # Manually set strong SHAP values to pass validation
        explanation.shap_values = {
            "feature_1": 0.35,
            "feature_2": 0.12,
            "feature_3": 0.08,
        }
        
        is_valid = self.explainer.validate_explainability(explanation)
        self.assertTrue(is_valid)
    
    def test_validate_explainability_insufficient_features(self):
        """Test explainability validation fails with too few features."""
        explanation = SHAPExplanation(
            decision_id="test-decision",
            model_prediction="OUTCOME",
            base_value=0.5,
            shap_values={"feature_1": 0.2},  # Only 1 feature
            feature_values={"feature_1": 5},
        )
        
        is_valid = self.explainer.validate_explainability(explanation)
        self.assertFalse(is_valid)
    
    def test_explanation_caching(self):
        """Test that explanations are cached."""
        input_data = {"feature": 5}
        
        explanation = self.explainer.explain_prediction(
            model_id="test-model",
            input_data=input_data,
            prediction="RESULT",
            feature_names=["feature"],
        )
        
        # Retrieve from cache
        cached = self.explainer.get_explanation(explanation.decision_id)
        self.assertIsNotNone(cached)
        self.assertEqual(cached.decision_id, explanation.decision_id)


class TestCloudFunctionConstraintChecker(unittest.TestCase):
    """Tests for Cloud Function Constraint Checker."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = CloudFunctionConstraintChecker()
    
    def test_protocols_loaded(self):
        """Test that humanitarian protocols are loaded."""
        self.assertGreater(len(self.checker.protocols), 0)
        self.assertIn("MEDICAL_TRIAGE", self.checker.protocols)
        self.assertIn("RESOURCE_EQUITY", self.checker.protocols)
        self.assertIn("DATA_PROTECTION", self.checker.protocols)
    
    def test_triage_fairness_valid(self):
        """Test medical triage validation with valid data."""
        action_data = {
            "priority_level": "HIGH",
            "patient_id": "PAT-001",
            "medical_severity": "CRITICAL",
            "decision_factors": ["respiratory_distress", "vitals"],
        }
        
        is_valid, violation = self.checker.check_constraint(
            protocol_id="MEDICAL_TRIAGE",
            action_data=action_data,
        )
        
        self.assertTrue(is_valid)
        self.assertIsNone(violation)
    
    def test_triage_fairness_discriminatory(self):
        """Test medical triage fails with discriminatory factors."""
        action_data = {
            "priority_level": "LOW",
            "patient_id": "PAT-002",
            "medical_severity": "MODERATE",
            "decision_factors": ["fever", "race", "ethnicity"],
        }
        
        is_valid, violation = self.checker.check_constraint(
            protocol_id="MEDICAL_TRIAGE",
            action_data=action_data,
        )
        
        self.assertFalse(is_valid)
        self.assertIsNotNone(violation)
        self.assertEqual(violation.severity, ConstraintSeverity.CRITICAL)
        self.assertGreater(len(violation.remediation_steps), 0)
    
    def test_triage_fairness_missing_severity(self):
        """Test medical triage fails without medical severity."""
        action_data = {
            "priority_level": "HIGH",
            "patient_id": "PAT-003",
            "decision_factors": ["symptoms"],
        }
        
        is_valid, violation = self.checker.check_constraint(
            protocol_id="MEDICAL_TRIAGE",
            action_data=action_data,
        )
        
        self.assertFalse(is_valid)
        self.assertIsNotNone(violation)
    
    def test_resource_equity_valid(self):
        """Test resource allocation validation with valid data."""
        action_data = {
            "resource_type": "medical_supplies",
            "allocation_method": "NEEDS_BASED",
            "beneficiaries": ["FACILITY-001", "FACILITY-002"],
        }
        
        is_valid, violation = self.checker.check_constraint(
            protocol_id="RESOURCE_EQUITY",
            action_data=action_data,
        )
        
        self.assertTrue(is_valid)
        self.assertIsNone(violation)
    
    def test_resource_equity_no_beneficiaries(self):
        """Test resource allocation fails without beneficiaries."""
        action_data = {
            "resource_type": "vaccines",
            "allocation_method": "FIFO",
            "beneficiaries": [],
        }
        
        is_valid, violation = self.checker.check_constraint(
            protocol_id="RESOURCE_EQUITY",
            action_data=action_data,
        )
        
        self.assertFalse(is_valid)
        self.assertIsNotNone(violation)
    
    def test_data_protection_valid(self):
        """Test data protection validation with valid encryption."""
        action_data = {
            "data_type": "PHI",
            "encryption_status": "ENCRYPTED",
            "access_control": "RBAC",
            "affected_patients": ["PAT-001"],
        }
        
        is_valid, violation = self.checker.check_constraint(
            protocol_id="DATA_PROTECTION",
            action_data=action_data,
        )
        
        self.assertTrue(is_valid)
        self.assertIsNone(violation)
    
    def test_data_protection_unencrypted_phi(self):
        """Test data protection fails with unencrypted PHI."""
        action_data = {
            "data_type": "PHI",
            "encryption_status": "NONE",
            "access_control": "RBAC",
            "affected_patients": ["PAT-002"],
        }
        
        is_valid, violation = self.checker.check_constraint(
            protocol_id="DATA_PROTECTION",
            action_data=action_data,
        )
        
        self.assertFalse(is_valid)
        self.assertIsNotNone(violation)
        self.assertIn("encrypted", violation.description.lower())
    
    def test_vulnerable_protection_valid(self):
        """Test vulnerable population protection with valid measures."""
        action_data = {
            "vulnerable_categories": ["children", "refugees"],
            "protection_measures": [
                "guardian_consent",
                "cultural_sensitivity",
                "enhanced_documentation"
            ],
            "affected_individuals": ["GROUP-001"],
        }
        
        is_valid, violation = self.checker.check_constraint(
            protocol_id="VULNERABLE_POPULATIONS",
            action_data=action_data,
        )
        
        self.assertTrue(is_valid)
        self.assertIsNone(violation)
    
    def test_vulnerable_protection_missing_measures(self):
        """Test vulnerable protection fails without protection measures."""
        action_data = {
            "vulnerable_categories": ["children", "elderly"],
            "protection_measures": [],
            "affected_individuals": ["GROUP-002"],
        }
        
        is_valid, violation = self.checker.check_constraint(
            protocol_id="VULNERABLE_POPULATIONS",
            action_data=action_data,
        )
        
        self.assertFalse(is_valid)
        self.assertIsNotNone(violation)
    
    def test_emergency_access_valid(self):
        """Test emergency access validation without barriers."""
        action_data = {
            "patient_id": "PAT-EMERG-001",
            "emergency_severity": "CRITICAL",
            "access_barriers": [],
        }
        
        is_valid, violation = self.checker.check_constraint(
            protocol_id="EMERGENCY_ACCESS",
            action_data=action_data,
        )
        
        self.assertTrue(is_valid)
        self.assertIsNone(violation)
    
    def test_emergency_access_blocked(self):
        """Test emergency access fails with blocking barriers."""
        action_data = {
            "patient_id": "PAT-EMERG-002",
            "emergency_severity": "LIFE_THREATENING",
            "access_barriers": ["PAYMENT_REQUIRED", "INSURANCE_VERIFICATION"],
        }
        
        is_valid, violation = self.checker.check_constraint(
            protocol_id="EMERGENCY_ACCESS",
            action_data=action_data,
        )
        
        self.assertFalse(is_valid)
        self.assertIsNotNone(violation)
        self.assertIn("blocked", violation.description.lower())
    
    def test_get_violations_filtering(self):
        """Test violation log retrieval with filtering."""
        # Create some violations
        self.checker.check_constraint(
            "MEDICAL_TRIAGE",
            {"patient_id": "P1", "decision_factors": ["race"]},
        )
        
        # Get all unresolved violations
        violations = self.checker.get_violations(unresolved_only=True)
        self.assertGreater(len(violations), 0)
        
        # Get only critical violations
        critical = self.checker.get_violations(
            severity=ConstraintSeverity.CRITICAL,
            unresolved_only=True,
        )
        for v in critical:
            self.assertEqual(v.severity, ConstraintSeverity.CRITICAL)


class TestSecretManagerProtocolStore(unittest.TestCase):
    """Tests for Secret Manager Protocol Store."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.store = SecretManagerProtocolStore(project_id="test-project")
    
    def test_store_and_retrieve_protocol(self):
        """Test storing and retrieving a protocol."""
        protocol = HumanitarianProtocol(
            protocol_id="TEST-001",
            name="Test Protocol",
            category=ConstraintCategory.MEDICAL_ETHICS,
            severity=ConstraintSeverity.HIGH,
            description="Test protocol for unit testing",
            constraint_function="test_function",
            legal_citations=["Test Citation 1"],
        )
        
        # Store protocol
        secret_path = self.store.store_protocol(protocol)
        self.assertIn("humanitarian-protocol-TEST-001", secret_path)
        
        # Retrieve protocol
        retrieved = self.store.retrieve_protocol("humanitarian-protocol-TEST-001")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.protocol_id, protocol.protocol_id)
        self.assertEqual(retrieved.name, protocol.name)
        self.assertEqual(retrieved.category, protocol.category)
        self.assertEqual(retrieved.severity, protocol.severity)
    
    def test_list_protocols(self):
        """Test listing stored protocols."""
        # Store some protocols
        for i in range(3):
            protocol = HumanitarianProtocol(
                protocol_id=f"TEST-{i:03d}",
                name=f"Test Protocol {i}",
                category=ConstraintCategory.RESOURCE_ALLOCATION,
                severity=ConstraintSeverity.MEDIUM,
                description="Test",
                constraint_function="test",
            )
            self.store.store_protocol(protocol)
        
        # List protocols
        protocols = self.store.list_protocols()
        self.assertGreaterEqual(len(protocols), 3)
    
    def test_delete_protocol(self):
        """Test deleting a protocol."""
        protocol = HumanitarianProtocol(
            protocol_id="DELETE-TEST",
            name="Delete Test",
            category=ConstraintCategory.EMERGENCY_RESPONSE,
            severity=ConstraintSeverity.LOW,
            description="To be deleted",
            constraint_function="test",
        )
        
        # Store and then delete
        secret_name = "humanitarian-protocol-DELETE-TEST"
        self.store.store_protocol(protocol, secret_name)
        
        deleted = self.store.delete_protocol(secret_name)
        self.assertTrue(deleted)
        
        # Verify it's gone
        retrieved = self.store.retrieve_protocol(secret_name)
        self.assertIsNone(retrieved)
    
    def test_retrieve_nonexistent_protocol(self):
        """Test retrieving a protocol that doesn't exist."""
        retrieved = self.store.retrieve_protocol("nonexistent-protocol")
        self.assertIsNone(retrieved)


class TestHumanitarianProtocol(unittest.TestCase):
    """Tests for HumanitarianProtocol data class."""
    
    def test_protocol_creation(self):
        """Test creating a humanitarian protocol."""
        protocol = HumanitarianProtocol(
            protocol_id="PROTO-TEST",
            name="Test Protocol",
            category=ConstraintCategory.CONSENT_DIGNITY,
            severity=ConstraintSeverity.CRITICAL,
            description="Test description",
            constraint_function="test_func",
            parameters={"param1": "value1"},
            legal_citations=["Citation 1", "Citation 2"],
        )
        
        self.assertEqual(protocol.protocol_id, "PROTO-TEST")
        self.assertEqual(protocol.name, "Test Protocol")
        self.assertEqual(protocol.category, ConstraintCategory.CONSENT_DIGNITY)
        self.assertEqual(protocol.severity, ConstraintSeverity.CRITICAL)
        self.assertIsInstance(protocol.created_at, datetime)


class TestSHAPExplanation(unittest.TestCase):
    """Tests for SHAPExplanation data class."""
    
    def test_shap_explanation_creation(self):
        """Test creating a SHAP explanation."""
        explanation = SHAPExplanation(
            decision_id="DEC-001",
            model_prediction="HIGH_RISK",
            base_value=0.5,
            shap_values={
                "feature_a": 0.3,
                "feature_b": -0.1,
                "feature_c": 0.15,
            },
            feature_values={
                "feature_a": 10,
                "feature_b": 5,
                "feature_c": 8,
            },
        )
        
        self.assertEqual(explanation.decision_id, "DEC-001")
        self.assertEqual(explanation.model_prediction, "HIGH_RISK")
        self.assertEqual(len(explanation.shap_values), 3)
    
    def test_to_dict_serialization(self):
        """Test serializing SHAP explanation to dictionary."""
        explanation = SHAPExplanation(
            decision_id="DEC-002",
            model_prediction="POSITIVE",
            base_value=0.5,
            shap_values={"feat1": 0.2, "feat2": 0.1, "feat3": 0.05},
            feature_values={"feat1": 1, "feat2": 2, "feat3": 3},
        )
        
        result = explanation.to_dict()
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["decision_id"], "DEC-002")
        self.assertIn("top_contributors", result)
        self.assertIn("timestamp", result)


if __name__ == "__main__":
    unittest.main()
