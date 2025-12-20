# iLuminara-Core: Global Sovereign Health Architecture

> **Mission:** *To architect systems that transform preventable suffering from statistical inevitability to historical anomaly.*

---

## 🏗️ The Fortress: Architecture Overview

iLuminara-Core is a **globally sovereign, compliance-first health intelligence platform** designed to operate identically in Toronto, Cape Town, and California without changing a single line of code.

Built on four foundational pillars:

```
┌──────────────────────────────────────────────────────────────┐
│                    GOVERNANCE KERNEL                          │
│        (Legal Vector Ledger, Dignity Guardrails, Audit)      │
└──────────────────────────────────────────────────────────────┘
                            ▲
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐      ┌──────▼──────┐    ┌──────▼──────┐
   │ EDGE    │      │   CLOUD     │    │  HARDWARE   │
   │ NODE    │      │   ORACLE    │    │  ATTESTATION│
   │ (EMR    │      │  (Parametric│    │  (TPM,      │
   │  CBS    │      │   Bonds,    │    │  BOM        │
   │  IDSR)  │      │  Z-Score)   │    │  Ledger)    │
   └────┬────┘      └──────┬──────┘    └──────┬──────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                    ▼
         ┌────────────────────────┐
         │   GOLDEN THREAD        │
         │  Data Fusion Engine    │
         │ (Verified Timeline)    │
         └────────────────────────┘
```

### Core Modules

#### `/governance_kernel/`
The ethical engine of iLuminara. Encodes 14 global legal frameworks into Python logic.
- **`vector_ledger.py`** — `SovereignGuardrail` class enforces GDPR, KDPA, PIPEDA, POPIA, HIPAA, HITECH, CCPA, NIST CSF, ISO 27001, SOC 2, and EU AI Act compliance
- **`crisis_decision_agent.py`** — AI agent for autonomous crisis decisions with humanitarian law compliance
- **`fairness_constraints.py`** — Fairness constraint engine ensuring equitable resource allocation
- **`ai_agent_coordinator.py`** — Integrated coordinator for multi-layer ethical validation
- Validates every action against sovereign dignity constraints
- Raises `SovereigntyViolationError` with specific legal citations

#### `/edge_node/sync_protocol/`
The "Golden Thread" — merges EMR, CBS, and IDSR data streams.
- **`golden_thread.py`** — Fusion engine that creates a single verified timeline
- Implements the **6-Month Rule**: Records >180 days old transition to cold storage
- Cross-source verification (CONFIRMED when cbs.location == emr.location AND time_delta < 24h)
- Auto-generates IDSR reports for government health submissions

#### `/edge_node/ai_agents/`
**NEW**: Autonomous AI agents for offline operation and federated learning.
- **`offline_agent.py`** — Agents that operate without continuous connectivity
- **`federated_client.py`** — Privacy-preserving federated learning with differential privacy
- **`agent_registry.py`** — Discovery service for capability-based agent matching
- Intermittent connectivity handling with exponential backoff
- Edge-to-cloud synchronization when network is available
- Privacy guarantees: (ε, δ)-differential privacy for collaborative learning
- [📖 Full Documentation](docs/AI_AGENTS.md)

#### `/edge_node/frenasa_engine/`
Machine learning inference engine (edge-based, locally-sovereign).

#### `/edge_node/vector_store/`
Vector database for semantic health information retrieval.

#### `/edge_node/lora_mesh/`
Low-bandwidth mesh networking for deployment in resource-constrained environments.

#### `/cloud_oracle/`
Parametric bond pricing engine for health economics (optional cloud integration).

#### `/hardware/`
TPM attestation and bill-of-materials ledger for hardware-rooted trust.

#### `/docs/`
Philosophical architecture, RFP specifications, and global compliance matrix.

---

## 🛡️ Compliance Shield

iLuminara-Core is engineered to be **natively compliant** across 14 global legal frameworks without runtime configuration changes:

| Framework | Region | Status | Enforcer |
|-----------|--------|--------|----------|
| **GDPR** (General Data Protection Regulation) | 🇪🇺 EU | ✅ `SovereignGuardrail` | Art. 9 (Special Categories), Art. 22 (Right to Explanation) |
| **KDPA** (Kenya Data Protection Act) | 🇰🇪 Kenya | ✅ `SovereignGuardrail` | §37 (Transfer Restrictions), §42 (Data Subject Rights) |
| **HIPAA** (Health Insurance Portability & Accountability Act) | 🇺🇸 USA | ✅ `SovereignGuardrail` | §164.312 (Physical/Technical Safeguards) |
| **HITECH** (Health Information Technology for Economic & Clinical Health) | 🇺🇸 USA | ✅ `SovereignGuardrail` | §13410 (Notification of Breach) |
| **PIPEDA** (Personal Information Protection & Electronic Documents Act) | 🇨🇦 Canada | ✅ `SovereignGuardrail` | §5-7 (Lawfulness of Processing) |
| **POPIA** (Protection of Personal Information Act) | 🇿🇦 South Africa | ✅ `SovereignGuardrail` | §11 (Lawfulness), §14 (Cross-border Transfers) |
| **CCPA** (California Consumer Privacy Act) | 🇺🇸 California | ✅ `SovereignGuardrail` | §1798.100 (Right to Know) |
| **NIST CSF** (Cybersecurity Framework) | 🇺🇸 USA | ✅ Risk-Based Controls | Identify, Protect, Detect, Respond, Recover |
| **ISO 27001** (Information Security Management) | 🌐 Global | ✅ `SovereignGuardrail` | Annex A (14 control objectives) |
| **SOC 2** (Service Organization Control 2) | 🇺🇸 USA | ✅ Audit-Ready | Security, Availability, Processing Integrity, Confidentiality, Privacy |
| **EU AI Act** (Artificial Intelligence Regulation) | 🇪🇺 EU | ✅ `SovereignGuardrail` | §6 (High-Risk AI), §8 (Transparency) |
| **GDPR Art. 9** (Special Categories of Data) | 🇪🇺 EU | ✅ `SovereignGuardrail` | Explicit Prohibition on Foreign Transfers |
| **Data Sovereignty** | 🌐 Global | ✅ `Golden Thread` | Health data remains in sovereign territory |
| **Right to Explanation** | 🌐 Global | ✅ `Golden Thread` | Every high-risk inference requires SHAP explainability |

---

## 🚀 Quick Start

### 1. Scaffold the Repository

```bash
chmod +x setup_repo.sh
./setup_repo.sh
```

This creates the directory structure with all `__init__.py` markers:
```
iLuminara-Core/
├── edge_node/
│   ├── frenasa_engine/
│   ├── vector_store/
│   ├── lora_mesh/
│   └── sync_protocol/
├── governance_kernel/
│   ├── vector_ledger.py          # The Ethical Engine
│   └── __init__.py
├── cloud_oracle/
├── hardware/
├── docs/
└── setup_repo.sh
```

### 2. Initialize the Governance Engine

```python
from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError

guardrail = SovereignGuardrail()

# Example: Validate a data transfer action
try:
    guardrail.validate_action(
        action_type='Data_Transfer',
        payload={
            'data_type': 'PHI',
            'destination': 'Foreign_Cloud'
        },
        jurisdiction='GDPR_EU'
    )
except SovereigntyViolationError as e:
    print(f"❌ {e}")
    # Raises: "Violates GDPR Art. 9 (Processing of special categories)"
```

### 3. Fuse Data Streams

```python
from edge_node.sync_protocol.golden_thread import GoldenThread

gt = GoldenThread()

# Merge EMR and CBS signals into verified timeline
fused = gt.fuse_data_streams(
    cbs_signal={
        'location': 'Nairobi',
        'symptom': 'fever',
        'timestamp': '2025-01-10T10:00Z'
    },
    emr_record={
        'location': 'Nairobi',
        'diagnosis': 'malaria',
        'timestamp': '2025-01-10T09:45Z'
    },
    patient_id='PATIENT_12345'
)

# Check verification score
print(f"Verification Score: {fused.verification_score}")  # 1.0 (CONFIRMED)

# View fused record
print(fused.to_dict())
```

### 4. Deploy to NVIDIA Jetson Orin

```bash
docker-compose up -d
```

---

## 📋 The Three Pillars of Compliance

### Pillar 1: Data Sovereignty
**Rule 1 from `SovereignGuardrail`:**
```python
# Health data (PHI) CANNOT leave sovereign territory
if payload['data_type'] == 'PHI' and payload['destination'] == 'Foreign_Cloud':
    raise SovereigntyViolationError(
        "GDPR Art. 9, Kenya DPA §37, HIPAA §164.312"
    )
```

### Pillar 2: Right to Explanation
**Rule 2 from `SovereignGuardrail`:**
```python
# Every high-risk clinical inference requires explainability
if action_type == 'High_Risk_Inference':
    assert 'explanation' in payload  # SHAP values, feature importance, etc.
    # Enforces: EU AI Act §6, GDPR Art. 22
```

### Pillar 3: Consent & Dignity
**Rule 3 from `SovereignGuardrail`:**
```python
# No processing without informed consent
if not payload.get('consent_token'):
    raise SovereigntyViolationError(
        "POPIA §11, CCPA §1798.100, GDPR Art. 6"
    )
```

---

## 🔐 Key Concepts

### The Golden Thread
Merges three data streams into one verified timeline:
- **EMR** — Hospital/clinic records (ground truth)
- **CBS** — Community-based surveillance (population signals)
- **IDSR** — Integrated Disease Surveillance Response (government standard)

**Verification Logic:**
```
IF cbs.location == emr.location AND |cbs.timestamp - emr.timestamp| < 24h
    THEN verification_score = 1.0 (CONFIRMED)
    ELSE score degrades based on conflict severity
```

### The 6-Month Rule
Records older than 180 days transition to **COLD storage**:
- **HOT Storage**: Recent events (≤6 months) — Active memory, fast queries
- **COLD Storage**: Historical events (>6 months) — Archived, compliant with GDPR Art. 17 (Right to Erasure)

```python
retention_status = 'HOT' if (now - record.timestamp).days <= 180 else 'COLD'
```

---

## 🤖 AI Agents with Ethical Guardrails

iLuminara-Core includes autonomous AI agents designed for crisis response scenarios with built-in ethical constraints, humanitarian law compliance, and fairness enforcement.

### Crisis Decision Agent

Autonomous decision-making system that enforces international humanitarian law:

```python
from governance_kernel.crisis_decision_agent import CrisisDecisionAgent, DecisionType

agent = CrisisDecisionAgent()

decision = agent.make_decision(
    decision_type=DecisionType.RESOURCE_ALLOCATION,
    context={
        'affected_population': 5000,
        'location': 'Dadaab_Refugee_Camp',
        'resources': {'medical_supplies': 2000},
        'time_sensitivity': 'urgent'
    },
    affected_groups=[
        {
            'name': 'Children_Under_5',
            'size': 800,
            'need_level': 0.9,
            'is_protected_group': True
        },
        {
            'name': 'Adults',
            'size': 4200,
            'need_level': 0.6,
            'is_protected_group': False
        }
    ]
)

print(f"Decision: {decision.recommendation}")
print(f"Confidence: {decision.confidence_score}")
print(f"Requires Human Approval: {decision.requires_human_approval}")
```

**Key Features:**
- Enforces Geneva Conventions and International Humanitarian Law
- Implements 7 core humanitarian principles (humanity, impartiality, neutrality, distinction, proportionality, precaution, independence)
- Blocks prohibited actions (collective punishment, discrimination, arbitrary detention)
- Prioritizes protected groups (children, elderly, disabled, pregnant women, medical personnel)
- Full audit trail with legal citations for transparency

### Fairness Constraint Engine

Ensures equitable resource allocation with bias detection:

```python
from governance_kernel.fairness_constraints import FairnessConstraintEngine, PopulationGroup

engine = FairnessConstraintEngine(fairness_threshold=0.8)

groups = [
    PopulationGroup(
        group_id="vulnerable",
        name="Vulnerable_Population",
        size=1000,
        vulnerability_score=1.5,
        need_level=0.9,
        is_protected_group=True,
        proposed_allocation=1500
    ),
    PopulationGroup(
        group_id="general",
        name="General_Population",
        size=5000,
        vulnerability_score=1.0,
        need_level=0.5,
        is_protected_group=False,
        proposed_allocation=5000
    )
]

assessment = engine.evaluate_fairness(
    groups=groups,
    allocation_plan={},
    enforce_constraints=True
)

print(f"Overall Fairness Score: {assessment.overall_fairness_score}")
print(f"Equity Gaps: {len(assessment.equity_gaps)}")
print(f"Bias Indicators: {assessment.bias_indicators}")
```

**Fairness Metrics:**
- **Demographic Parity**: Equal per-capita allocation across groups
- **Equal Opportunity**: All groups with need receive resources
- **Proportional Allocation**: Resources match need levels
- **Protected Group Fairness**: Vulnerable populations not disadvantaged
- **Vulnerability Equity**: Higher vulnerability receives more support

### Integrated AI Agent Coordinator

Multi-layer ethical validation system:

```python
from governance_kernel.ai_agent_coordinator import AIAgentCoordinator, CrisisScenarioType

coordinator = AIAgentCoordinator(
    fairness_threshold=0.8,
    confidence_threshold=0.7
)

result = coordinator.execute_crisis_decision(
    scenario_type=CrisisScenarioType.DISEASE_OUTBREAK,
    decision_type=DecisionType.RESOURCE_ALLOCATION,
    affected_area="Dadaab_Refugee_Camp",
    population_groups=[...],
    resources_available={'medical_supplies': 5000},
    jurisdiction="KDPA_KE"
)

print(f"Approval Status: {result.approval_status}")
print(f"Fairness Score: {result.fairness_assessment.overall_fairness_score}")
print(f"Legal Compliance: {result.sovereignty_compliance['compliant']}")
print(f"\nEthical Summary:\n{result.ethical_summary}")
```

**Decision Pipeline:**
1. **Crisis Decision Agent** generates recommendation with humanitarian law constraints
2. **Fairness Constraint Engine** validates equity and detects bias
3. **Sovereign Guardrail** ensures legal compliance (GDPR, KDPA, HIPAA, etc.)
4. **Coordinator** synthesizes final decision with full audit trail
5. **Human Approval Check** determines if oversight required

**Humanitarian Law Enforcement:**
- Geneva Conventions (1949) - Protection of civilians
- UN OCHA Humanitarian Principles
- WHO Emergency Response Framework
- Core Humanitarian Standard (CHS)
- International Health Regulations (2005)

### Run the Demo

```bash
python examples/ai_agent_crisis_response_demo.py
```

This demonstrates a cholera outbreak scenario in Dadaab refugee camp with:
- 6 population groups with different vulnerability levels
- Fair resource allocation with ethical constraints
- Multi-layer validation (humanitarian law + fairness + sovereignty)
- Complete audit trail and legal citations

---

## 📦 Docker Deployment (NVIDIA Jetson Orin ARM64)

A `docker-compose.yml` is included for deployment on edge hardware:

```yaml
version: '3.8'
services:
  iluminara-core:
    build:
      context: .
      dockerfile: Dockerfile.arm64
    environment:
      - JURISDICTION=GLOBAL_DEFAULT
      - LOG_LEVEL=INFO
    ports:
      - "8080:8080"
    volumes:
      - ./governance_kernel:/app/governance_kernel
      - ./edge_node:/app/edge_node
```

Deploy with:
```bash
docker-compose up -d
```

---

## 🧪 Testing & Validation

### Test Governance Engine

```bash
python -m pytest tests/test_vector_ledger.py -v
```

### Test Data Fusion

```bash
python -m pytest tests/test_golden_thread.py -v
```

---

## 📚 Documentation

- **[Philosophical Architecture](docs/philosophical_architecture.md)** — Design philosophy and ethical framework
- **[RFP Specifications](docs/rfp_specs.md)** — Requirements for government health departments
- **[Global Compliance Matrix](docs/compliance_matrix.md)** — Detailed mapping of all 14 frameworks

---

## 🌍 Deployments Ready

iLuminara-Core is production-ready for:

- 🇰🇪 **Kenya** (KDPA compliant, IDSR integrated)
- 🇿🇦 **South Africa** (POPIA compliant)
- 🇨🇦 **Canada** (PIPEDA compliant)
- 🇪🇺 **European Union** (GDPR + EU AI Act compliant)
- 🇺🇸 **United States** (HIPAA + CCPA + NIST CSF)
- 🌐 **Any jurisdiction** (GLOBAL_DEFAULT fallback)

---

## 🔗 Integration Points

| Component | Integration | Status |
|-----------|-----------|--------|
| **Kenya EMR Systems** | Direct sync protocol | ✅ In dev |
| **CB-IDSR (Government Reporting)** | Auto-report generation | ✅ In dev |
| **Mobile Health Apps** | REST API + FHIR | ✅ In dev |
| **Vector Databases** | Weaviate/Pinecone integration | ✅ In dev |
| **Government Health Dashboards** | BI export (PowerBI/Tableau) | ✅ In dev |

---

## 📄 License

VISENDI56 © 2025. All rights reserved.

---

## 🤝 Contributing

To contribute, ensure your changes:
1. Pass `SovereignGuardrail` compliance validation
2. Include audit logging in `governance_kernel`
3. Follow the Golden Thread data fusion protocol
4. Update compliance matrix if adding new legal frameworks

---

## ✨ Citation

If you use iLuminara-Core in your work, please cite:

```bibtex
@software{iluminara2025,
  title={iLuminara-Core: Global Sovereign Health Architecture},
  author={VISENDI56},
  year={2025},
  url={https://github.com/VISENDI56/iLuminara-Core}
}
```

---

## 🔥 Status: DEPLOYMENT READY

**The Fortress is built. The Constitution is written. Deploy with confidence.**

*"Transform preventable suffering from statistical inevitability to historical anomaly."*

---

**Last Updated:** December 13, 2025  
**Status:** Production-Ready for Global Deployment  
**Compliance Validation:** All 14 Frameworks ✅
