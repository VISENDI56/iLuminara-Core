#!/bin/bash
# Alert Distribution System Setup for iLuminara
# Creates Pub/Sub topic and deploys Cloud Function for alert distribution

set -e

echo "=================================================="
echo "iLuminara: Alert Distribution System Setup"
echo "=================================================="
echo ""

# Configuration
TOPIC_NAME="${TOPIC_NAME:-luminara-alerts}"
FUNCTION_NAME="${FUNCTION_NAME:-alert-distributor}"
REGION="${GCP_REGION:-us-central1}"
RUNTIME="${RUNTIME:-python310}"
SLACK_WEBHOOK="${SLACK_WEBHOOK:-}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed"
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: No GCP project configured"
    exit 1
fi

echo "📋 Configuration:"
echo "   Project: $PROJECT_ID"
echo "   Region: $REGION"
echo "   Topic: $TOPIC_NAME"
echo "   Function: $FUNCTION_NAME"
echo "   Runtime: $RUNTIME"
echo ""

# Step 1: Enable required APIs
echo "🔧 Step 1: Enabling required APIs..."
gcloud services enable pubsub.googleapis.com --project=$PROJECT_ID
gcloud services enable cloudfunctions.googleapis.com --project=$PROJECT_ID
gcloud services enable cloudbuild.googleapis.com --project=$PROJECT_ID
echo "✅ APIs enabled"
echo ""

# Step 2: Create Pub/Sub topic
echo "📬 Step 2: Creating Pub/Sub topic..."
if gcloud pubsub topics describe "$TOPIC_NAME" --project=$PROJECT_ID &>/dev/null; then
    echo "ℹ️  Topic '$TOPIC_NAME' already exists"
else
    gcloud pubsub topics create "$TOPIC_NAME" --project=$PROJECT_ID
    echo "✅ Topic '$TOPIC_NAME' created"
fi
echo ""

# Step 3: Deploy Cloud Function
echo "☁️  Step 3: Deploying Cloud Function..."

# Check if function code exists
if [ ! -f "gcp/cloud_functions/alert_distributor/main.py" ]; then
    echo "❌ Error: Function code not found at gcp/cloud_functions/alert_distributor/main.py"
    exit 1
fi

# Set environment variables for function
ENV_VARS="SLACK_WEBHOOK=$SLACK_WEBHOOK"

# Deploy function
gcloud functions deploy "$FUNCTION_NAME" \
    --region="$REGION" \
    --runtime="$RUNTIME" \
    --trigger-topic="$TOPIC_NAME" \
    --entry-point=alert_distributor \
    --source=gcp/cloud_functions/alert_distributor \
    --set-env-vars="$ENV_VARS" \
    --project="$PROJECT_ID" \
    --max-instances=10 \
    --memory=256MB \
    --timeout=60s

echo "✅ Cloud Function deployed"
echo ""

echo "=================================================="
echo "✅ Alert Distribution System Ready"
echo "=================================================="
echo ""
echo "System Details:"
echo "  • Pub/Sub Topic: $TOPIC_NAME"
echo "  • Cloud Function: $FUNCTION_NAME"
echo "  • Region: $REGION"
echo ""
echo "Testing:"
echo "  # Publish a test message"
echo "  gcloud pubsub topics publish $TOPIC_NAME \\"
echo "    --message='{\"alert_type\":\"test\",\"message\":\"Test alert\"}' \\"
echo "    --project=$PROJECT_ID"
echo ""
echo "Monitoring:"
echo "  # View function logs"
echo "  gcloud functions logs read $FUNCTION_NAME \\"
echo "    --region=$REGION \\"
echo "    --project=$PROJECT_ID"
echo ""
