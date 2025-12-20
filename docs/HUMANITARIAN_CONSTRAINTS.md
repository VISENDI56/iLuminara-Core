# Humanitarian Constraint Encoding System

## Overview

The Humanitarian Constraint Encoding System extends iLuminara-Core's governance kernel with three critical Google Cloud Platform integrations:

1. **Vertex AI Explainable AI**: SHAP (SHapley Additive exPlanations) analysis for AI decision transparency
2. **Cloud Functions**: Serverless, scalable real-time constraint checking
3. **Secret Manager**: Secure storage of humanitarian protocols and sensitive configurations

This system ensures that all decisions affecting humanitarian operations are transparent, auditable, and aligned with international humanitarian standards including WHO guidelines, ICRC protocols, Sphere Standards, and UN humanitarian principles.

---

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                   HUMANITARIAN CONSTRAINT SYSTEM                │
└────────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐      ┌──────▼──────┐    ┌──────▼──────┐
   │ VERTEX  │      │   CLOUD     │    │   SECRET    │
   │   AI    │      │ FUNCTIONS   │    │  MANAGER    │
   │ (SHAP)  │      │ (Checker)   │    │ (Protocols) │
   └────┬────┘      └──────┬──────┘    └──────┬──────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                     ▼
          ┌────────────────────────┐
          │  GOVERNANCE KERNEL     │
          │  (SovereignGuardrail)  │
          └────────────────────────┘
```

---

## Components

### 1. Vertex AI Explainable AI

**Purpose**: Provides SHAP analysis for AI model predictions to fulfill "Right to Explanation" requirements under EU AI Act and GDPR.

**Features**:
- SHAP value calculation for all model features
- Feature importance attribution
- Top contributor identification
- Explainability validation against regulatory standards
- Explanation caching for audit trails

**Usage**:
```python
from governance_kernel.humanitarian_constraints import VertexAIExplainableAI

explainer = VertexAIExplainableAI(project_id="iluminara-core")

explanation = explainer.explain_prediction(
    model_id="outbreak-predictor-v1",
    input_data={
        "cbs_signals": 45,
        "z_score": 3.8,
        "location": "Dadaab"
    },
    prediction="OUTBREAK_LIKELY",
    feature_names=["cbs_signals", "z_score", "location"]
)

# Get top contributing factors
top_factors = explanation.get_top_contributors(n=3)
```

**Compliance**: EU AI Act § 6, GDPR Art. 22, NIST AI RMF

---

### 2. Cloud Functions Constraint Checker

**Purpose**: Real-time validation of humanitarian actions against international protocols with serverless scalability.

**Available Protocols**:

| Protocol ID | Name | Category | Severity |
|------------|------|----------|----------|
| `MEDICAL_TRIAGE` | Medical Triage Protocol | Medical Ethics | CRITICAL |
| `RESOURCE_EQUITY` | Resource Allocation Equity | Resource Allocation | HIGH |
| `DATA_PROTECTION` | Humanitarian Data Protection | Data Sovereignty | CRITICAL |
| `VULNERABLE_POPULATIONS` | Vulnerable Population Protection | Population Protection | CRITICAL |
| `EMERGENCY_ACCESS` | Emergency Healthcare Access | Emergency Response | CRITICAL |

**Constraint Checks**:

1. **Medical Triage Fairness**: Ensures triage decisions are based solely on medical need, not discriminatory factors
2. **Resource Equity**: Prevents systematic bias in resource distribution
3. **Data Protection**: Validates encryption and access controls for humanitarian data
4. **Vulnerable Protection**: Ensures special safeguards for children, refugees, displaced persons
5. **Emergency Access**: Guarantees access to emergency care regardless of administrative barriers

**Usage**:
```python
from governance_kernel.humanitarian_constraints import CloudFunctionConstraintChecker

checker = CloudFunctionConstraintChecker()

is_valid, violation = checker.check_constraint(
    protocol_id="MEDICAL_TRIAGE",
    action_data={
        "patient_id": "PAT-12345",
        "medical_severity": "CRITICAL",
        "decision_factors": ["respiratory_distress", "vitals"]
    }
)

if not is_valid:
    print(f"Violation: {violation.description}")
    for step in violation.remediation_steps:
        print(f"  - {step}")
```

**Compliance**: WHO Emergency Triage Guidelines, ICRC Medical Ethics, Sphere Standards, UN Humanitarian Principles, Geneva Conventions

---

### 3. Secret Manager Protocol Store

**Purpose**: Secure storage and retrieval of humanitarian protocols containing sensitive operational information.

**Features**:
- Encrypted storage of protocol definitions
- Version control for protocol updates
- Access control and audit logging
- Secure retrieval with authentication

**Usage**:
```python
from governance_kernel.humanitarian_constraints import (
    SecretManagerProtocolStore,
    HumanitarianProtocol,
    ConstraintCategory,
    ConstraintSeverity
)

store = SecretManagerProtocolStore(project_id="iluminara-core")

# Store a protocol
protocol = HumanitarianProtocol(
    protocol_id="PROTO-006",
    name="Child Protection Protocol",
    category=ConstraintCategory.POPULATION_PROTECTION,
    severity=ConstraintSeverity.CRITICAL,
    description="Enhanced safeguards for minors",
    constraint_function="check_child_protection",
    legal_citations=["UN Convention on Rights of the Child Art. 3"]
)

secret_path = store.store_protocol(protocol)

# Retrieve a protocol
retrieved = store.retrieve_protocol("humanitarian-protocol-PROTO-006")
```

**Compliance**: Google Cloud Security Best Practices, CMEK support, Audit logging

---

## Deployment

### Prerequisites

1. Google Cloud SDK installed
2. GCP project with billing enabled
3. Required APIs enabled:
   - Cloud Functions API
   - Secret Manager API
   - Vertex AI API
4. Service account with appropriate IAM roles:
   - `roles/aiplatform.user`
   - `roles/cloudfunctions.developer`
   - `roles/secretmanager.admin`

### Cloud Functions Deployment

```bash
cd cloud_functions
source config.env
./deploy.sh
```

This deploys three Cloud Functions:
1. `humanitarian-constraint-checker`: Real-time constraint validation
2. `humanitarian-list-protocols`: Protocol discovery
3. `humanitarian-get-violations`: Violation retrieval

### API Endpoints

After deployment, you'll receive three HTTPS endpoints:

**1. Check Constraint**
```bash
curl -X POST https://REGION-PROJECT.cloudfunctions.net/humanitarian-constraint-checker \
  -H 'Content-Type: application/json' \
  -d '{
    "protocol_id": "MEDICAL_TRIAGE",
    "action_data": {
      "patient_id": "PAT-001",
      "medical_severity": "CRITICAL"
    }
  }'
```

**2. List Protocols**
```bash
curl https://REGION-PROJECT.cloudfunctions.net/humanitarian-list-protocols
```

**3. Get Violations**
```bash
curl "https://REGION-PROJECT.cloudfunctions.net/humanitarian-get-violations?severity=CRITICAL"
```

---

## Integration with Existing Systems

### Integration with SovereignGuardrail

The humanitarian constraint system seamlessly integrates with the existing `SovereignGuardrail`:

```python
from governance_kernel.vector_ledger import SovereignGuardrail
from governance_kernel.humanitarian_constraints import (
    VertexAIExplainableAI,
    CloudFunctionConstraintChecker
)

# Initialize systems
guardrail = SovereignGuardrail()
explainer = VertexAIExplainableAI()
checker = CloudFunctionConstraintChecker()

# 1. Generate SHAP explanation
explanation = explainer.explain_prediction(
    model_id="risk-model",
    input_data={"feature1": 10},
    prediction="HIGH_RISK",
    feature_names=["feature1"]
)

# 2. Validate with SovereignGuardrail
guardrail.validate_action(
    action_type="High_Risk_Inference",
    payload={
        "explanation": explanation.to_dict(),
        "confidence_score": 0.87,
        "evidence_chain": ["factor1", "factor2"],
        "consent_token": "TOKEN-123"
    },
    jurisdiction="GDPR_EU"
)

# 3. Check humanitarian constraints
checker.check_constraint(
    protocol_id="VULNERABLE_POPULATIONS",
    action_data={"vulnerable_categories": ["refugees"]}
)
```

### Integration with Golden Thread

```python
from edge_node.sync_protocol.golden_thread import GoldenThread
from governance_kernel.humanitarian_constraints import CloudFunctionConstraintChecker

gt = GoldenThread()
checker = CloudFunctionConstraintChecker()

# Fuse data streams
fused_record = gt.fuse_data_streams(
    cbs_signal={"location": "Nairobi", "symptom": "fever"},
    emr_record={"location": "Nairobi", "diagnosis": "malaria"},
    patient_id="PAT-12345"
)

# Validate data protection
checker.check_constraint(
    protocol_id="DATA_PROTECTION",
    action_data={
        "data_type": "PHI",
        "encryption_status": "ENCRYPTED",
        "access_control": "RBAC",
        "affected_patients": ["PAT-12345"]
    }
)
```

---

## Testing

Run the comprehensive test suite:

```bash
python -m pytest tests/test_humanitarian_constraints.py -v
```

Run examples:

```bash
python governance_kernel/humanitarian_examples.py
```

---

## Legal & Compliance Framework

### International Standards

- **WHO Emergency Triage Guidelines**: Medical prioritization
- **ICRC Medical Ethics**: Humanitarian healthcare principles
- **Sphere Standards**: Humanitarian response quality standards
- **UN Humanitarian Principles**: Humanity, neutrality, impartiality, independence
- **Geneva Conventions**: Protection of civilians in conflict

### Data Protection

- **GDPR Article 9**: Special categories of data
- **GDPR Article 22**: Right to explanation
- **EU AI Act § 6**: High-risk AI systems
- **HIPAA § 164.312**: PHI safeguards
- **Kenya DPA § 37**: Cross-border transfers

### Population Protection

- **UN Convention on the Rights of the Child**: Child protection
- **UNHCR Guidelines**: Refugee protection
- **Geneva Conventions**: Civilian protection

---

## Monitoring & Audit

### Cloud Logging

All constraint checks, SHAP explanations, and protocol accesses are logged to Cloud Logging:

```bash
gcloud logging read "resource.type=cloud_function \
  AND resource.labels.function_name=humanitarian-constraint-checker" \
  --limit 50
```

### Violation Tracking

Retrieve violations programmatically:

```python
violations = checker.get_violations(
    severity=ConstraintSeverity.CRITICAL,
    unresolved_only=True
)

for v in violations:
    print(f"{v.violation_id}: {v.description}")
```

### Audit Trail

All explanations are cached for regulatory audit:

```python
explanation = explainer.get_explanation(decision_id)
audit_report = explanation.to_dict()
```

---

## Configuration

### Environment Variables

See `cloud_functions/config.env`:

```bash
GCP_PROJECT_ID=iluminara-core
GCP_REGION=us-central1
VERTEX_AI_REGION=us-central1
SECRET_MANAGER_PROJECT=iluminara-core
```

### Customization

Add custom humanitarian protocols:

```python
custom_protocol = HumanitarianProtocol(
    protocol_id="CUSTOM-001",
    name="Custom Protocol",
    category=ConstraintCategory.MEDICAL_ETHICS,
    severity=ConstraintSeverity.HIGH,
    description="Custom validation logic",
    constraint_function="check_custom",
    legal_citations=["Citation 1"]
)

store.store_protocol(custom_protocol)
```

---

## Support

For questions or issues:
- Review examples in `governance_kernel/humanitarian_examples.py`
- Check test cases in `tests/test_humanitarian_constraints.py`
- Consult iLuminara-Core main documentation

---

## License

VISENDI56 © 2025. All rights reserved.

---

**Philosophy**: "Every decision affecting human welfare must be transparent, auditable, and aligned with humanitarian principles."

**Mission**: Transform preventable suffering from statistical inevitability to historical anomaly.
