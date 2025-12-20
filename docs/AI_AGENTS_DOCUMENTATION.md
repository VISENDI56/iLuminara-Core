# AI Agents with Ethical Guardrails

This document provides comprehensive documentation for the AI agent system implemented in iLuminara-Core for crisis response scenarios.

## Overview

The AI agent system consists of three integrated components designed to ensure ethical, fair, and legally compliant autonomous decisions in humanitarian crises:

1. **Crisis Decision Agent** - Enforces international humanitarian law
2. **Fairness Constraint Engine** - Ensures equitable resource allocation
3. **AI Agent Coordinator** - Multi-layer ethical validation and synthesis

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                  AI Agent Coordinator                           │
│  (Orchestrates multi-layer ethical validation)                 │
└────────────────────┬───────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────▼────┐  ┌────▼────┐  ┌───▼─────┐
   │ Crisis  │  │Fairness │  │Sovereign│
   │Decision │  │Engine   │  │Guardrail│
   │ Agent   │  │         │  │         │
   └─────────┘  └─────────┘  └─────────┘
```

## Crisis Decision Agent

### Purpose
Autonomous decision-making system that enforces international humanitarian law and ethical principles in crisis response scenarios.

### Key Features

#### 1. Humanitarian Law Compliance
Implements and enforces:
- **Geneva Conventions (1949)** - Protection of civilians and medical personnel
- **UN OCHA Humanitarian Principles** - Humanity, impartiality, neutrality, independence
- **WHO Emergency Response Framework** - Health emergency protocols
- **Core Humanitarian Standard (CHS)** - Quality and accountability standards
- **International Health Regulations (2005)** - Disease outbreak response

#### 2. Seven Core Humanitarian Principles

1. **Humanity** - Human suffering must be addressed wherever found
2. **Impartiality** - Action based solely on need, without discrimination
3. **Neutrality** - Must not take sides in hostilities
4. **Independence** - Autonomy from political/military objectives
5. **Distinction** - Distinguish between civilians and combatants
6. **Proportionality** - Response proportional to humanitarian need
7. **Precaution** - Take all feasible precautions to avoid harm

#### 3. Protected Groups
Special protection for:
- Children under 5
- Pregnant women
- Elderly persons (65+)
- Persons with disabilities
- Medical personnel
- Displaced persons
- Refugees

#### 4. Prohibited Actions
Blocks decisions that involve:
- Collective punishment
- Discrimination based on protected characteristics
- Arbitrary detention
- Forced displacement without justification
- Denial of medical care
- Use of starvation as weapon
- Targeting of civilians

### Decision Types

1. **RESOURCE_ALLOCATION** - Fair distribution of supplies
2. **EVACUATION_ORDER** - Safe evacuation planning
3. **QUARANTINE_ZONE** - Targeted disease containment
4. **MEDICAL_TRIAGE** - Priority-based medical care
5. **ALERT_BROADCAST** - Public health communications
6. **SUPPLY_DISTRIBUTION** - Food/water distribution
7. **SHELTER_ASSIGNMENT** - Housing allocation

### Risk Levels

- **LOW** - Routine decisions with minimal impact
- **MEDIUM** - Decisions requiring review
- **HIGH** - Significant consequences, likely requires approval
- **CRITICAL** - Life-or-death, always requires human oversight

### Usage Example

```python
from governance_kernel.crisis_decision_agent import (
    CrisisDecisionAgent,
    DecisionType
)

# Initialize agent
agent = CrisisDecisionAgent()

# Make decision
decision = agent.make_decision(
    decision_type=DecisionType.RESOURCE_ALLOCATION,
    context={
        'affected_population': 5000,
        'location': 'Dadaab_Refugee_Camp',
        'resources': {
            'medical_supplies': 2000,
            'food_rations': 3000,
            'water_liters': 10000
        },
        'time_sensitivity': 'urgent'
    },
    affected_groups=[
        {
            'name': 'Children_Under_5',
            'size': 800,
            'need_level': 0.9,
            'is_protected_group': True,
            'civilian_status': 'civilian'
        },
        {
            'name': 'Adults',
            'size': 4200,
            'need_level': 0.6,
            'is_protected_group': False,
            'civilian_status': 'civilian'
        }
    ]
)

# Review decision
print(f"Decision ID: {decision.decision_id}")
print(f"Recommendation: {decision.recommendation}")
print(f"Confidence: {decision.confidence_score:.2f}")
print(f"Requires Approval: {decision.requires_human_approval}")
print(f"\nEthical Compliance:")
for principle, compliant in decision.ethical_compliance.items():
    print(f"  {principle}: {'✓' if compliant else '✗'}")
print(f"\nLegal Citations:")
for citation in decision.humanitarian_law_citations:
    print(f"  - {citation}")
```

### Audit Trail

Every decision includes complete audit trail:
- Context validation
- Ethical validation
- Humanitarian law check
- Fairness assessment
- Recommendation generation
- Approval determination

## Fairness Constraint Engine

### Purpose
Ensures equitable resource allocation with bias detection and equity gap identification.

### Fairness Metrics

#### 1. Demographic Parity
Equal per-capita allocation across groups of similar need.

**Score Calculation:**
```
coefficient_of_variation = std_dev / mean
score = 1.0 / (1.0 + coefficient_of_variation)
```

#### 2. Equal Opportunity
All groups with need receive access to resources.

**Score Calculation:**
```
score = (groups_receiving_aid) / (groups_with_need)
```

#### 3. Proportional Allocation
Resources proportional to need level.

**Score Calculation:**
```
Pearson correlation between need_level and allocation
score = (correlation + 1) / 2
```

#### 4. Protected Group Fairness
Vulnerable populations not disadvantaged.

**Score Calculation:**
```
ratio = avg_protected_per_capita / avg_non_protected_per_capita
score = min(1.0, ratio)
```

#### 5. Vulnerability Equity
Higher vulnerability receives more support.

**Score Calculation:**
```
Compare actual vs. vulnerability-weighted expected allocation
score = 1.0 / (1.0 + mean_absolute_percentage_error)
```

### Protected Characteristics

The engine detects bias across 16 protected characteristics:
- Race, ethnicity, national origin
- Gender, gender identity, sexual orientation
- Religion, belief system
- Age
- Disability status
- Socioeconomic status
- Geographic location
- Language
- Political opinion
- Refugee/IDP status

### Vulnerability Factors

Legitimate factors that justify differentiated treatment:
- Children under 5: 1.5x
- Pregnant women: 1.4x
- Elderly over 65: 1.3x
- Persons with disabilities: 1.4x
- Chronic illness: 1.3x
- Recent displacement: 1.3x
- No shelter: 1.5x
- Food insecurity: 1.4x

### Equity Gaps

Types of gaps identified:
1. **High need, low allocation** - Severe under-serving
2. **Protected group under-allocation** - Discrimination indicator
3. **Vulnerable group excluded** - Critical gap requiring immediate action

### Usage Example

```python
from governance_kernel.fairness_constraints import (
    FairnessConstraintEngine,
    PopulationGroup
)

# Initialize engine
engine = FairnessConstraintEngine(fairness_threshold=0.8)

# Define population groups
groups = [
    PopulationGroup(
        group_id="children",
        name="Children_Under_5",
        size=800,
        vulnerability_score=1.5,
        need_level=0.9,
        is_protected_group=True,
        proposed_allocation=1350
    ),
    PopulationGroup(
        group_id="adults",
        name="Adults",
        size=4200,
        vulnerability_score=1.0,
        need_level=0.6,
        is_protected_group=False,
        proposed_allocation=2520
    )
]

# Evaluate fairness
assessment = engine.evaluate_fairness(
    groups=groups,
    allocation_plan={},
    enforce_constraints=True
)

# Review assessment
print(f"Overall Fairness: {assessment.overall_fairness_score:.2f}")
print(f"\nMetric Scores:")
for metric, score in assessment.metric_scores.items():
    print(f"  {metric}: {score:.2f}")

if assessment.violations:
    print(f"\n⚠️ Violations:")
    for violation in assessment.violations:
        print(f"  - {violation}")

if assessment.equity_gaps:
    print(f"\n⚠️ Equity Gaps:")
    for gap in assessment.equity_gaps:
        print(f"  - {gap['type']}: {gap['group']}")

print(f"\nRecommendations:")
for rec in assessment.recommendations:
    print(f"  - {rec}")
```

### Automatic Adjustment

The engine can automatically adjust allocations to meet fairness constraints:

```python
adjusted_groups = engine.adjust_allocation_for_fairness(
    groups=groups,
    total_resources=5000,
    min_fairness_score=0.85
)

for group in adjusted_groups:
    print(f"{group.name}: {group.proposed_allocation}")
```

## AI Agent Coordinator

### Purpose
Orchestrates all three components for integrated ethical validation with full transparency.

### Decision Pipeline

1. **Prepare Population Groups** - Parse and validate input data
2. **Generate Crisis Decision** - Apply humanitarian law constraints
3. **Validate Fairness** - Check equity and bias
4. **Check Sovereignty** - Ensure legal compliance (GDPR, KDPA, etc.)
5. **Synthesize Recommendation** - Combine all validations
6. **Determine Approval** - Human oversight check
7. **Generate Summary** - Transparent explanation

### Approval Statuses

- **APPROVED** - All constraints satisfied, can proceed
- **REQUIRES_HUMAN_REVIEW** - High-risk or low confidence
- **REJECTED** - Ethical/legal violations detected

### Usage Example

```python
from governance_kernel.ai_agent_coordinator import (
    AIAgentCoordinator,
    CrisisScenarioType
)
from governance_kernel.crisis_decision_agent import DecisionType

# Initialize coordinator
coordinator = AIAgentCoordinator(
    fairness_threshold=0.8,
    confidence_threshold=0.7
)

# Define population groups
population_groups = [
    {
        'group_id': 'children',
        'name': 'Children_Under_5',
        'size': 800,
        'vulnerability_score': 1.5,
        'need_level': 0.9,
        'is_protected_group': True
    },
    # ... more groups
]

# Execute decision
result = coordinator.execute_crisis_decision(
    scenario_type=CrisisScenarioType.DISEASE_OUTBREAK,
    decision_type=DecisionType.RESOURCE_ALLOCATION,
    affected_area='Dadaab_Refugee_Camp',
    population_groups=population_groups,
    resources_available={
        'medical_supplies': 2000,
        'food_rations': 3000
    },
    jurisdiction='KDPA_KE'
)

# Review results
print(f"Approval Status: {result.approval_status}")
print(f"Fairness Score: {result.fairness_assessment.overall_fairness_score:.2f}")
print(f"Confidence: {result.decision_output.confidence_score:.2f}")
print(f"Legal Compliant: {result.sovereignty_compliance['compliant']}")

# Export report
coordinator.export_decision_report(result, 'decision_report.json')
```

## Testing

### Run All Tests

```bash
# All tests
python -m unittest discover -s tests -p "test_*.py" -v

# Individual test suites
python -m unittest tests.test_crisis_decision_agent -v
python -m unittest tests.test_fairness_constraints -v
python -m unittest tests.test_ai_agent_coordinator -v
```

### Test Coverage

- **Crisis Decision Agent**: 11 tests
  - Humanitarian law violations
  - Protected group prioritization
  - Audit trail completeness
  - Legal citations
  - Human approval logic

- **Fairness Constraints**: 15 tests
  - All fairness metrics
  - Bias detection
  - Equity gap identification
  - Automatic adjustment
  - Protected group treatment

- **AI Coordinator**: 9 tests
  - Integrated pipeline
  - Multi-layer validation
  - Rejection handling
  - Decision logging
  - Export functionality

## Example Scenarios

### Example 1: Disease Outbreak Response

Run the included demonstration:
```bash
python examples/ai_agent_crisis_response_demo.py
```

This simulates a cholera outbreak in Dadaab refugee camp with:
- 5,500 affected people across 6 population groups
- Multiple vulnerability factors
- Fair resource allocation with ethical constraints
- Complete transparency and audit trail

### Example 2: Evacuation Decision

```python
result = coordinator.execute_crisis_decision(
    scenario_type=CrisisScenarioType.NATURAL_DISASTER,
    decision_type=DecisionType.EVACUATION_ORDER,
    affected_area='Coastal_Region',
    population_groups=[...],
    resources_available={'transport_capacity': 5000}
)
```

### Example 3: Medical Triage

```python
result = coordinator.execute_crisis_decision(
    scenario_type=CrisisScenarioType.MEDICAL_EMERGENCY,
    decision_type=DecisionType.MEDICAL_TRIAGE,
    affected_area='Field_Hospital',
    population_groups=[...],
    resources_available={'medical_staff_hours': 800}
)
```

## Legal Compliance

The AI agent system ensures compliance with:

### International Humanitarian Law
- Geneva Conventions (1949) and Additional Protocols
- UN OCHA Humanitarian Principles (2012)
- WHO Emergency Response Framework
- Core Humanitarian Standard (CHS)
- International Health Regulations (2005)

### Data Protection & Privacy
- GDPR (EU) - Data sovereignty and consent
- KDPA (Kenya) - Local data protection
- HIPAA (USA) - Health data protection
- POPIA (South Africa) - Personal information protection
- PIPEDA (Canada) - Privacy regulations

### Human Rights
- Universal Declaration of Human Rights (UDHR)
- International Covenant on Civil and Political Rights (ICCPR)
- Convention on the Elimination of All Forms of Discrimination (CEDAW)

## Best Practices

### 1. Always Review High-Risk Decisions
Never bypass human review for critical decisions affecting large populations.

### 2. Document Rationale
Include clear explanations for all decisions in audit trails.

### 3. Monitor Fairness Metrics
Regularly review fairness assessments to identify systemic issues.

### 4. Update Vulnerability Factors
Adjust vulnerability scores based on latest humanitarian guidance.

### 5. Maintain Audit Logs
Preserve complete decision history for accountability and learning.

### 6. Test Regularly
Run comprehensive tests before deploying in production environments.

## Philosophy

**"No algorithm operates without constraint. Sovereignty includes the right to question every automated decision."**

The AI agent system embodies this philosophy through:
- Multi-layer ethical validation
- Transparent decision-making
- Human oversight requirements
- Complete audit trails
- Legal citations for accountability
- Continuous fairness monitoring

## Support

For questions, issues, or contributions related to AI agents:
1. Review this documentation
2. Check test examples in `/tests`
3. Run the demonstration in `/examples`
4. Consult the source code docstrings

---

**Last Updated:** December 2025
**Version:** 1.0
**Status:** Production Ready
