# Ethical Engine Cloud Function Deployment

## Overview

The Ethical Validator is deployed as a Google Cloud Function that validates humanitarian constraints on health system actions. It enforces:

- **Geneva Convention Article 3** constraints for conflict zones
- **WHO International Health Regulations (2005)** for outbreak response
- **Humanitarian margin calculations** for decision-making under uncertainty

## Quick Start

### Prerequisites

1. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. Authenticate: `gcloud auth login`
3. Set up a Google Cloud project

### Deploy

```bash
# Basic deployment (uses defaults)
./deploy_cloud_function.sh

# Custom project and region
./deploy_cloud_function.sh my-project-id us-central1
```

### Test

```bash
curl -X POST https://REGION-PROJECT_ID.cloudfunctions.net/ethical-validator \
  -H 'Content-Type: application/json' \
  -d '{
    "action": {
      "type": "quarantine",
      "scope": "district",
      "estimated_civilian_impact": 0.2,
      "medical_benefit": 0.8,
      "attack_rate": 0.02,
      "r_effective": 1.5,
      "severity_score": 0.6
    },
    "context": {
      "conflict_zone": true,
      "outbreak_suspected": true,
      "healthcare_capacity": 0.7
    }
  }'
```

## API Reference

### POST /validate_action

Validates an action against humanitarian constraints.

**Request Body:**

```json
{
  "action": {
    "type": "string",
    "scope": "string",
    "estimated_civilian_impact": 0.0-1.0,
    "medical_benefit": 0.0-1.0,
    "attack_rate": 0.0-1.0,
    "r_effective": number,
    "severity_score": 0.0-1.0
  },
  "context": {
    "conflict_zone": boolean,
    "outbreak_suspected": boolean,
    "civilian_population": number,
    "healthcare_capacity": 0.0-1.0
  }
}
```

**Response (Success):**

```json
{
  "status": "approved",
  "action": { ... },
  "humanitarian_margin": {
    "margin": 0.39,
    "base": 0.20,
    "multipliers": ["Conflict zone: 1.5x", "Outbreak: 1.3x"],
    "interpretation": "MODERATE - Balanced approach with safety buffer"
  },
  "constraints_applied": [
    "Geneva Convention Article 3 - Proportionality",
    "WHO IHR (2005) - Necessity"
  ],
  "violations": [],
  "protocol_version": "2025.1"
}
```

**Response (Rejected):**

```json
{
  "status": "rejected",
  "message": "❌ PROPORTIONALITY VIOLATION: ...",
  "protocol_version": "2025.1"
}
```

## Environment Variables

- `PROTOCOL_VERSION`: Version of humanitarian protocols (default: `2025.1`)
- `GCP_PROJECT_ID`: Google Cloud project ID for Secret Manager
- `USE_CLOUD_SECRETS`: Enable loading protocols from Secret Manager (`true`/`false`)

## Secret Manager Integration (Optional)

To use Google Cloud Secret Manager for protocol configuration:

1. Create a secret:
```bash
gcloud secrets create humanitarian-protocols \
  --replication-policy="automatic" \
  --data-file=protocols.json
```

2. Grant access to the Cloud Function:
```bash
gcloud secrets add-iam-policy-binding humanitarian-protocols \
  --member="serviceAccount:PROJECT_ID@appspot.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

3. Set `USE_CLOUD_SECRETS=true` in deployment

## Local Development

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Tests

```bash
pytest tests/test_ethical_engine.py -v
```

### Run Locally

```bash
functions-framework --target=validate_action --debug
```

Then test with:
```bash
curl -X POST http://localhost:8080 \
  -H 'Content-Type: application/json' \
  -d @test_request.json
```

## Example Scenarios

### Cholera Outbreak in Refugee Camp

```json
{
  "action": {
    "type": "cholera_response",
    "scope": "refugee_camp",
    "estimated_civilian_impact": 0.3,
    "medical_benefit": 0.85,
    "attack_rate": 0.04,
    "r_effective": 2.8,
    "severity_score": 0.75
  },
  "context": {
    "conflict_zone": false,
    "outbreak_suspected": true,
    "civilian_population": 200000,
    "healthcare_capacity": 0.5
  }
}
```

### Field Hospital in Conflict Zone

```json
{
  "action": {
    "type": "field_hospital",
    "scope": "conflict_zone",
    "estimated_civilian_impact": 0.05,
    "medical_benefit": 0.95
  },
  "context": {
    "conflict_zone": true,
    "outbreak_suspected": false,
    "civilian_population": 50000,
    "healthcare_capacity": 0.2
  }
}
```

## Compliance

The Ethical Validator enforces:

- ✅ Geneva Convention Article 3 (Common Article)
- ✅ WHO International Health Regulations (2005)
- ✅ Proportionality principle
- ✅ Necessity principle
- ✅ Medical neutrality
- ✅ Distinction (civilian/combatant)
- ✅ Time-limited measures
- ✅ Scientific evidence requirement

## Monitoring

View logs:
```bash
gcloud functions logs read ethical-validator \
  --region=us-central1 \
  --limit=50
```

View metrics:
```bash
gcloud monitoring dashboards list
```

## Support

For issues or questions, refer to:
- [iLuminara-Core Documentation](../README.md)
- [Geneva Conventions](https://www.icrc.org/en/doc/war-and-law/treaties-customary-law/geneva-conventions/overview-geneva-conventions.htm)
- [WHO IHR (2005)](https://www.who.int/publications/i/item/9789241580496)
