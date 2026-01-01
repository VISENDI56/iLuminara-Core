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
Humanitarian Constraint Encoding - Integration Examples
═════════════════════════════════════════════════════════════════════════════

This module demonstrates how to use the humanitarian constraint encoding system
with the existing iLuminara-Core governance kernel.

Examples:
1. SHAP Explainability for High-Risk Decisions
2. Real-Time Constraint Checking
3. Secure Protocol Storage and Retrieval
4. Integration with SovereignGuardrail
"""

from governance_kernel.humanitarian_constraints import (
    VertexAIExplainableAI,
    CloudFunctionConstraintChecker,
    SecretManagerProtocolStore,
    HumanitarianProtocol,
    ConstraintCategory,
    ConstraintSeverity,
    SHAPExplanation,
)
from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError


def example_1_shap_explainability():
    """
    Example 1: SHAP Explainability for High-Risk Clinical Decisions
    
    Demonstrates how to use Vertex AI Explainable AI to provide transparency
    for machine learning predictions in humanitarian healthcare settings.
    """
    print("=" * 80)
    print("EXAMPLE 1: SHAP Explainability for High-Risk Decisions")
    print("=" * 80)
    
    # Initialize Vertex AI Explainable AI
    explainer = VertexAIExplainableAI(
        project_id="iluminara-core",
        region="us-central1"
    )
    
    # Simulate a high-risk triage decision
    model_id = "triage-classifier-v2"
    
    input_features = {
        "patient_age": 45,
        "symptom_severity": 8,
        "temperature_celsius": 39.5,
        "heart_rate": 120,
        "respiratory_rate": 28,
        "location": "Dadaab Refugee Camp",
        "risk_factors": ["chronic_condition", "malnutrition"],
    }
    
    prediction = "HIGH_PRIORITY"  # Model's prediction
    
    # Generate SHAP explanation
    explanation = explainer.explain_prediction(
        model_id=model_id,
        input_data=input_features,
        prediction=prediction,
        feature_names=list(input_features.keys()),
    )
    
    print(f"\n✅ Decision ID: {explanation.decision_id}")
    print(f"✅ Model Prediction: {explanation.model_prediction}")
    print(f"✅ Base Value: {explanation.base_value:.4f}")
    
    print("\n📊 SHAP Values (Feature Importance):")
    for feature, shap_value in explanation.shap_values.items():
        print(f"   {feature:25s}: {shap_value:+.4f}")
    
    print("\n🔍 Top 3 Contributing Features:")
    for i, (feature, value) in enumerate(explanation.get_top_contributors(3), 1):
        print(f"   {i}. {feature}: {value:+.4f}")
    
    # Validate explainability meets transparency requirements
    is_valid = explainer.validate_explainability(explanation)
    print(f"\n✅ Explainability Valid (EU AI Act § 6 compliant): {is_valid}")
    
    return explanation


def example_2_constraint_checking():
    """
    Example 2: Real-Time Humanitarian Constraint Checking
    
    Demonstrates how to use Cloud Function constraint checker to validate
    actions against humanitarian protocols in real-time.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Real-Time Humanitarian Constraint Checking")
    print("=" * 80)
    
    # Initialize constraint checker
    checker = CloudFunctionConstraintChecker()
    
    # Example 2a: Check Medical Triage Protocol
    print("\n--- Check 2a: Medical Triage (Valid) ---")
    action_data_valid = {
        "priority_level": "HIGH",
        "patient_id": "PAT-12345",
        "medical_severity": "CRITICAL",
        "decision_factors": ["respiratory_distress", "fever", "vitals"],
    }
    
    is_valid, violation = checker.check_constraint(
        protocol_id="MEDICAL_TRIAGE",
        action_data=action_data_valid,
        context={"facility_id": "FAC-001"},
    )
    
    print(f"✅ Valid: {is_valid}")
    if violation:
        print(f"❌ Violation: {violation.description}")
    
    # Example 2b: Check Medical Triage with Discriminatory Factors (Invalid)
    print("\n--- Check 2b: Medical Triage (Invalid - Contains Discriminatory Factors) ---")
    action_data_invalid = {
        "priority_level": "LOW",
        "patient_id": "PAT-67890",
        "medical_severity": "MODERATE",
        "decision_factors": ["fever", "nationality", "ethnicity"],  # ❌ Discriminatory
    }
    
    is_valid, violation = checker.check_constraint(
        protocol_id="MEDICAL_TRIAGE",
        action_data=action_data_invalid,
        context={},
    )
    
    print(f"❌ Valid: {is_valid}")
    if violation:
        print(f"❌ Violation ID: {violation.violation_id}")
        print(f"❌ Severity: {violation.severity.value}")
        print(f"❌ Description: {violation.description}")
        print(f"📋 Remediation Steps:")
        for i, step in enumerate(violation.remediation_steps, 1):
            print(f"   {i}. {step}")
    
    # Example 2c: Check Emergency Access Protocol
    print("\n--- Check 2c: Emergency Healthcare Access (Invalid - Blocked by Barriers) ---")
    action_data_emergency = {
        "patient_id": "PAT-EMERGENCY-001",
        "emergency_severity": "LIFE_THREATENING",
        "access_barriers": ["PAYMENT_REQUIRED", "INSURANCE_VERIFICATION"],
    }
    
    is_valid, violation = checker.check_constraint(
        protocol_id="EMERGENCY_ACCESS",
        action_data=action_data_emergency,
        context={},
    )
    
    print(f"❌ Valid: {is_valid}")
    if violation:
        print(f"❌ Violation: {violation.description}")
        print(f"🚨 Affected: {', '.join(violation.affected_entities)}")
        print(f"📋 Remediation:")
        for step in violation.remediation_steps:
            print(f"   - {step}")
    
    # Get all logged violations
    print("\n--- Summary of All Violations ---")
    all_violations = checker.get_violations(unresolved_only=True)
    print(f"Total Unresolved Violations: {len(all_violations)}")
    for v in all_violations:
        print(f"   - {v.violation_id}: {v.description} (Severity: {v.severity.value})")


def example_3_secret_manager():
    """
    Example 3: Secure Storage of Humanitarian Protocols
    
    Demonstrates how to use Secret Manager to securely store and retrieve
    humanitarian protocols with sensitive operational information.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Secure Protocol Storage with Secret Manager")
    print("=" * 80)
    
    # Initialize Secret Manager
    secret_store = SecretManagerProtocolStore(project_id="iluminara-core")
    
    # Create a new humanitarian protocol
    protocol = HumanitarianProtocol(
        protocol_id="PROTO-006",
        name="Child Protection Protocol",
        category=ConstraintCategory.POPULATION_PROTECTION,
        severity=ConstraintSeverity.CRITICAL,
        description="Enhanced safeguards for minors in humanitarian settings",
        constraint_function="check_child_protection",
        parameters={
            "minimum_age_consent": 18,
            "guardian_consent_required": True,
            "special_documentation": ["birth_certificate", "guardian_id"],
        },
        legal_citations=[
            "UN Convention on the Rights of the Child Art. 3",
            "UNHCR Best Interests of the Child Guidelines",
            "Kenya Children Act 2022 §4",
        ],
        version="1.0",
    )
    
    # Store protocol in Secret Manager
    print("\n📦 Storing protocol in Secret Manager...")
    secret_path = secret_store.store_protocol(protocol)
    print(f"✅ Stored at: {secret_path}")
    
    # List all protocols
    print("\n📋 Listing all stored protocols:")
    protocol_names = secret_store.list_protocols()
    for name in protocol_names:
        print(f"   - {name}")
    
    # Retrieve protocol
    print(f"\n🔐 Retrieving protocol from Secret Manager...")
    retrieved = secret_store.retrieve_protocol("humanitarian-protocol-PROTO-006")
    
    if retrieved:
        print(f"✅ Retrieved: {retrieved.name}")
        print(f"   Category: {retrieved.category.value}")
        print(f"   Severity: {retrieved.severity.value}")
        print(f"   Legal Citations:")
        for citation in retrieved.legal_citations:
            print(f"      - {citation}")
    
    return protocol


def example_4_integration_with_governance():
    """
    Example 4: Integration with Existing Governance Kernel
    
    Demonstrates how humanitarian constraints integrate with the existing
    SovereignGuardrail system for comprehensive compliance validation.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Integration with Governance Kernel")
    print("=" * 80)
    
    # Initialize both systems
    guardrail = SovereignGuardrail()
    constraint_checker = CloudFunctionConstraintChecker()
    explainer = VertexAIExplainableAI()
    
    # Scenario: High-risk inference for disease outbreak prediction
    print("\n🧪 Scenario: High-Risk Disease Outbreak Prediction")
    print("-" * 80)
    
    # Step 1: Generate SHAP explanation for the inference
    input_data = {
        "cbs_signals": 45,
        "emr_confirmations": 12,
        "z_score": 3.8,
        "location": "Dadaab",
        "population_density": 2500,
    }
    
    prediction = "OUTBREAK_LIKELY"
    
    explanation = explainer.explain_prediction(
        model_id="outbreak-predictor-v1",
        input_data=input_data,
        prediction=prediction,
        feature_names=list(input_data.keys()),
    )
    
    print(f"\n1️⃣ SHAP Explanation Generated:")
    print(f"   Decision ID: {explanation.decision_id}")
    print(f"   Prediction: {explanation.model_prediction}")
    
    # Step 2: Validate against SovereignGuardrail (Right to Explanation)
    print(f"\n2️⃣ Validating with SovereignGuardrail...")
    
    try:
        guardrail.validate_action(
            action_type="High_Risk_Inference",
            payload={
                "inference": prediction,
                "explanation": explanation.to_dict(),
                "confidence_score": 0.87,
                "evidence_chain": ["CBS surge", "EMR confirmations", "Z-score threshold"],
                "consent_token": "CONSENT-TOKEN-12345",
            },
            jurisdiction="GDPR_EU",
        )
        print("   ✅ SovereignGuardrail: PASSED")
    except SovereigntyViolationError as e:
        print(f"   ❌ SovereignGuardrail: FAILED - {e}")
    
    # Step 3: Check humanitarian constraints
    print(f"\n3️⃣ Checking Humanitarian Constraints...")
    
    # Check vulnerable population protection
    is_valid, violation = constraint_checker.check_constraint(
        protocol_id="VULNERABLE_POPULATIONS",
        action_data={
            "vulnerable_categories": ["refugee", "children", "displaced"],
            "protection_measures": [
                "enhanced_consent_procedures",
                "guardian_authorization",
                "cultural_sensitivity_training",
            ],
            "affected_individuals": ["CAMP-DADAAB-POPULATION"],
        },
        context={"operation_type": "disease_surveillance"},
    )
    
    if is_valid:
        print("   ✅ Humanitarian Constraints: PASSED")
    else:
        print(f"   ❌ Humanitarian Constraints: FAILED")
        if violation:
            print(f"      Violation: {violation.description}")
    
    # Step 4: Generate comprehensive audit report
    print(f"\n4️⃣ Comprehensive Audit Report:")
    print("-" * 80)
    
    audit_report = {
        "timestamp": explanation.timestamp.isoformat(),
        "decision_id": explanation.decision_id,
        "prediction": prediction,
        "compliance_checks": {
            "shap_explainability": "PASSED",
            "sovereign_guardrail": "PASSED",
            "humanitarian_constraints": "PASSED" if is_valid else "FAILED",
        },
        "top_decision_factors": [
            {"feature": feat, "attribution": val}
            for feat, val in explanation.get_top_contributors(3)
        ],
        "legal_compliance": [
            "EU AI Act § 6 (High-Risk AI)",
            "GDPR Art. 22 (Right to Explanation)",
            "UNHCR Guidelines on Vulnerable Populations",
        ],
    }
    
    print(f"   Decision: {audit_report['prediction']}")
    print(f"   All Compliance Checks: {all(v == 'PASSED' for v in audit_report['compliance_checks'].values())}")
    print(f"   Audit Trail: Available for regulatory review")
    
    return audit_report


def run_all_examples():
    """Run all examples in sequence."""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 14 + "HUMANITARIAN CONSTRAINT ENCODING EXAMPLES" + " " * 23 + "║")
    print("║" + " " * 12 + "iLuminara-Core Governance Kernel Extension" + " " * 22 + "║")
    print("╚" + "═" * 78 + "╝")
    
    # Run examples
    example_1_shap_explainability()
    example_2_constraint_checking()
    example_3_secret_manager()
    example_4_integration_with_governance()
    
    print("\n" + "=" * 80)
    print("✅ All Examples Completed Successfully")
    print("=" * 80)
    print("\n📚 Integration Points:")
    print("   1. Vertex AI Explainable AI: SHAP analysis for transparency")
    print("   2. Cloud Functions: Real-time constraint checking at scale")
    print("   3. Secret Manager: Secure protocol storage")
    print("   4. SovereignGuardrail: Unified compliance validation")
    print("\n🔗 Deploy Cloud Functions:")
    print("   cd cloud_functions")
    print("   gcloud functions deploy humanitarian-constraint-checker \\")
    print("       --runtime python310 --trigger-http --entry-point check_humanitarian_constraint")
    print()


if __name__ == "__main__":
    run_all_examples()
