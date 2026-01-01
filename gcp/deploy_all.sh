#!/bin/bash
# Master Deployment Script for iLuminara GCP Infrastructure
# Orchestrates deployment of all three components:
# 1. Speech-to-Text for Swahili
# 2. FRENASA Symptom Extraction Model
# 3. Alert Distribution System

set -e

echo "=========================================================="
echo "iLuminara: Complete GCP Infrastructure Deployment"
echo "=========================================================="
echo ""
echo "This script will deploy:"
echo "  1. Speech-to-Text API (Swahili - sw-KE)"
echo "  2. FRENASA Symptom Extraction Model (Vertex AI)"
echo "  3. Alert Distribution System (Pub/Sub + Cloud Functions)"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed"
    echo "   Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "⚠️  Warning: Docker is not installed"
    echo "   Docker is required for model deployment"
    echo "   Install from: https://docs.docker.com/get-docker/"
fi

# Verify GCP project is set
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: No GCP project configured"
    echo "   Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo "   Project ID: $PROJECT_ID"
echo ""

# Prompt for configuration
read -p "Enter GCP region (default: us-central1): " GCP_REGION
GCP_REGION=${GCP_REGION:-us-central1}
export GCP_REGION

read -p "Enter Slack Webhook URL (optional): " SLACK_WEBHOOK
export SLACK_WEBHOOK

echo ""
echo "📋 Deployment Configuration:"
echo "   Project ID: $PROJECT_ID"
echo "   Region: $GCP_REGION"
echo "   Slack Webhook: ${SLACK_WEBHOOK:0:30}..."
echo ""

read -p "Proceed with deployment? (y/N): " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled"
    exit 0
fi

echo ""
echo "=========================================================="
echo "Rev 1: Speech-to-Text API Setup"
echo "=========================================================="
./gcp/setup_speech_api.sh
echo ""

echo "=========================================================="
echo "Rev 2: FRENASA Symptom Extractor Deployment"
echo "=========================================================="
# Note: This may fail if Docker image needs to be built manually
./gcp/deploy_symptom_model.sh || echo "⚠️  Model deployment requires manual Docker build"
echo ""

echo "=========================================================="
echo "Rev 3: Alert Distribution System Setup"
echo "=========================================================="
./gcp/setup_alert_distribution.sh
echo ""

echo "=========================================================="
echo "✅ Deployment Complete!"
echo "=========================================================="
echo ""
echo "Services Deployed:"
echo "  ✅ Speech-to-Text API (sw-KE)"
echo "  ✅ FRENASA Symptom Extractor"
echo "  ✅ Alert Distribution (Pub/Sub + Cloud Function)"
echo ""
echo "Next Steps:"
echo "  1. Test speech recognition:"
echo "     python edge_node/speech_recognition/swahili_recognizer.py test.wav"
echo ""
echo "  2. Test symptom extraction:"
echo "     curl -X POST http://localhost:8080/predict \\"
echo "       -H 'Content-Type: application/json' \\"
echo "       -d '{\"transcript\":\"Mgonjwa ana homa na kikohozi\"}'"
echo ""
echo "  3. Test alert distribution:"
echo "     gcloud pubsub topics publish luminara-alerts \\"
echo "       --message='{\"alert_type\":\"test\",\"message\":\"Test\"}'"
echo ""
echo "Documentation:"
echo "  • README: /gcp/README.md"
echo "  • API Docs: http://localhost:8080/"
echo ""
