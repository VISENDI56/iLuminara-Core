# iLuminara GCP Deployment Guide

This directory contains all scripts and configurations for deploying iLuminara infrastructure on Google Cloud Platform (GCP).

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    iLuminara GCP Stack                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐      ┌──────────────────┐            │
│  │  Speech-to-Text  │      │  Vertex AI       │            │
│  │  API (Swahili)   │──────▶  Symptom         │            │
│  │  sw-KE           │      │  Extractor       │            │
│  └──────────────────┘      └──────────────────┘            │
│           │                         │                       │
│           │                         │                       │
│           ▼                         ▼                       │
│  ┌────────────────────────────────────────┐                │
│  │      Pub/Sub: luminara-alerts          │                │
│  └────────────────────────────────────────┘                │
│                    │                                        │
│                    ▼                                        │
│  ┌────────────────────────────────────────┐                │
│  │  Cloud Function: alert-distributor     │                │
│  │  • Slack notifications                 │                │
│  │  • Email alerts (future)               │                │
│  │  • SMS alerts (future)                 │                │
│  └────────────────────────────────────────┘                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Components

### 1. Speech-to-Text for Swahili
**Purpose:** Enable voice input from Community Health Volunteers (CHVs) in East Africa

**Files:**
- `setup_speech_api.sh` - API enablement and configuration
- `../edge_node/speech_recognition/swahili_recognizer.py` - Python SDK integration

**Features:**
- Swahili language support (sw-KE for Kenya, sw-TZ for Tanzania)
- Real-time streaming recognition
- Batch audio transcription
- Health keyword extraction

**Deployment:**
```bash
./gcp/setup_speech_api.sh [optional-test-audio.wav]
```

**Testing:**
```bash
# Using Python module
python edge_node/speech_recognition/swahili_recognizer.py test_audio.wav

# Using gcloud CLI
gcloud ml speech recognize test_audio.wav --language-code=sw-KE
```

### 2. FRENASA Symptom Extraction Model
**Purpose:** Extract structured health symptoms from Swahili transcripts

**Files:**
- `deploy_symptom_model.sh` - Vertex AI model deployment
- `../edge_node/frenasa_engine/Dockerfile` - Container definition
- `../edge_node/frenasa_engine/symptom_extractor_server.py` - Inference server

**Features:**
- RESTful API for symptom extraction
- Support for 13+ Swahili health terms
- Disease risk assessment (cholera, malaria, COVID-19, etc.)
- Severity classification (mild, moderate, severe)

**Deployment:**
```bash
# Option 1: Automated deployment
./gcp/deploy_symptom_model.sh

# Option 2: Manual deployment with custom container
export CONTAINER_IMAGE=gcr.io/YOUR_PROJECT/frenasa-symptom:v1.0
./gcp/deploy_symptom_model.sh
```

**API Usage:**
```bash
# Health check
curl http://localhost:8080/health

# Extract symptoms
curl -X POST http://localhost:8080/predict \
  -H 'Content-Type: application/json' \
  -d '{
    "transcript": "Mgonjwa ana homa na kikohozi",
    "metadata": {
      "location": "Nairobi",
      "patient_id": "P12345"
    }
  }'
```

**Response Example:**
```json
{
  "symptoms": [
    {
      "swahili": "homa",
      "english": "fever",
      "severity": "moderate",
      "category": "systemic"
    },
    {
      "swahili": "kikohozi",
      "english": "cough",
      "severity": "mild",
      "category": "respiratory"
    }
  ],
  "symptom_count": 2,
  "overall_severity": "moderate",
  "disease_risks": [
    {
      "disease": "respiratory_infection",
      "confidence": 0.67
    }
  ],
  "requires_immediate_attention": false
}
```

### 3. Alert Distribution System
**Purpose:** Distribute health alerts to multiple channels (Slack, email, SMS)

**Files:**
- `setup_alert_distribution.sh` - Pub/Sub topic and Cloud Function deployment
- `cloud_functions/alert_distributor/main.py` - Alert distribution logic
- `cloud_functions/alert_distributor/requirements.txt` - Dependencies

**Features:**
- Google Cloud Pub/Sub for reliable message delivery
- Slack integration with rich formatting
- Color-coded severity levels
- Extensible for email/SMS channels

**Deployment:**
```bash
# Set Slack webhook (required for Slack notifications)
export SLACK_WEBHOOK=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Deploy
./gcp/setup_alert_distribution.sh
```

**Publishing Alerts:**
```bash
# Via gcloud CLI
gcloud pubsub topics publish luminara-alerts \
  --message='{
    "alert_type": "outbreak",
    "severity": "critical",
    "title": "Cholera Outbreak Detected",
    "message": "10 cases in Dadaab refugee camp",
    "location": "Dadaab, Kenya",
    "metadata": {
      "disease_risk": "cholera",
      "confidence": 0.85
    }
  }'

# Via Python
from google.cloud import pubsub_v1
import json

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('YOUR_PROJECT', 'luminara-alerts')

alert = {
    "alert_type": "outbreak",
    "severity": "critical",
    "message": "10 cases detected"
}

publisher.publish(topic_path, json.dumps(alert).encode('utf-8'))
```

## 🚀 Quick Start

### Prerequisites
- Google Cloud SDK (`gcloud`) installed
- Docker installed (for model deployment)
- Active GCP project with billing enabled
- Python 3.10+

### One-Command Deployment
```bash
# Deploy all components
./gcp/deploy_all.sh
```

### Manual Step-by-Step Deployment

1. **Configure GCP Project:**
```bash
gcloud config set project YOUR_PROJECT_ID
gcloud auth application-default login
```

2. **Deploy Speech-to-Text:**
```bash
./gcp/setup_speech_api.sh
```

3. **Deploy Symptom Extractor:**
```bash
# Build and push Docker image
cd edge_node/frenasa_engine
docker build -t gcr.io/YOUR_PROJECT/frenasa-symptom:latest .
docker push gcr.io/YOUR_PROJECT/frenasa-symptom:latest

# Deploy to Vertex AI
cd ../..
./gcp/deploy_symptom_model.sh
```

4. **Deploy Alert Distribution:**
```bash
export SLACK_WEBHOOK=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
./gcp/setup_alert_distribution.sh
```

## 🧪 Testing

### Test Speech Recognition
```bash
# Create test audio (requires sox)
echo "Mgonjwa ana homa" | \
  gtts-cli -l sw --output test.wav

# Transcribe
python edge_node/speech_recognition/swahili_recognizer.py test.wav
```

### Test Symptom Extraction
```bash
# Start local server
python edge_node/frenasa_engine/symptom_extractor_server.py

# In another terminal
curl -X POST http://localhost:8080/predict \
  -H 'Content-Type: application/json' \
  -d '{"transcript":"Mgonjwa ana homa na kuhara"}'
```

### Test Alert Distribution
```bash
gcloud pubsub topics publish luminara-alerts \
  --message='{"alert_type":"test","severity":"low","message":"Test alert"}'

# View function logs
gcloud functions logs read alert-distributor --region=us-central1 --limit=10
```

## 📊 Monitoring

### View Logs
```bash
# Speech-to-Text usage
gcloud logging read "resource.type=api AND resource.labels.service=speech.googleapis.com"

# Cloud Function logs
gcloud functions logs read alert-distributor --region=us-central1

# Pub/Sub metrics
gcloud pubsub topics describe luminara-alerts
gcloud pubsub subscriptions list
```

### Cost Estimation
- **Speech-to-Text:** $0.024 per minute (first 60 minutes free monthly)
- **Vertex AI:** Variable based on instance type and usage
- **Pub/Sub:** $0.40 per million messages (first 10GB free monthly)
- **Cloud Functions:** $0.40 per million invocations (first 2 million free monthly)

## 🔐 Security & Compliance

### Data Sovereignty
All components are deployable within a single GCP region to maintain data sovereignty (GDPR/KDPA compliance).

### Authentication
- Service accounts for automated processes
- IAM roles for access control
- Workload Identity for Kubernetes integration

### Secrets Management
```bash
# Store Slack webhook securely
gcloud secrets create slack-webhook --data-file=-
# Paste webhook URL and press Ctrl+D

# Use in Cloud Function
gcloud functions deploy alert-distributor \
  --set-secrets=SLACK_WEBHOOK=slack-webhook:latest
```

## 🛠️ Troubleshooting

### Common Issues

**1. "API not enabled" errors:**
```bash
gcloud services enable speech.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable pubsub.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
```

**2. Docker push authentication:**
```bash
gcloud auth configure-docker
```

**3. Cloud Function deployment fails:**
```bash
# Check service account permissions
gcloud projects get-iam-policy YOUR_PROJECT

# Grant Cloud Functions service account Pub/Sub permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT \
  --member="serviceAccount:YOUR_PROJECT@appspot.gserviceaccount.com" \
  --role="roles/pubsub.subscriber"
```

**4. Speech recognition language not supported:**
- Verify language code: `sw-KE` (Kenya) or `sw-TZ` (Tanzania)
- Check regional availability in GCP console

## 📚 Additional Resources

- [Google Cloud Speech-to-Text Documentation](https://cloud.google.com/speech-to-text/docs)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Cloud Pub/Sub Documentation](https://cloud.google.com/pubsub/docs)
- [Cloud Functions Documentation](https://cloud.google.com/functions/docs)

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Cloud Function logs for alert distribution issues
3. Open an issue in the GitHub repository

---

**Last Updated:** December 19, 2025  
**Status:** Production-Ready  
**Compliance:** GDPR, KDPA, HIPAA-aligned
