#!/bin/bash
# ═════════════════════════════════════════════════════════════════════════════
# Google Cloud Function Deployment Script
# ═════════════════════════════════════════════════════════════════════════════
#
# Deploys the Ethical Validator as a Google Cloud Function
#
# Usage:
#   ./deploy_cloud_function.sh [PROJECT_ID] [REGION] [RUNTIME]
#
# Example:
#   ./deploy_cloud_function.sh iluminara us-central1 python310
#   ./deploy_cloud_function.sh iluminara us-central1 python311
#
# ═════════════════════════════════════════════════════════════════════════════

set -e  # Exit on error

# Configuration
PROJECT_ID="${1:-iluminara}"
REGION="${2:-us-central1}"
RUNTIME="${3:-python310}"
FUNCTION_NAME="ethical-validator"
ENTRY_POINT="validate_action"
PROTOCOL_VERSION="2025.1"

echo "═══════════════════════════════════════════════════════════════════════════"
echo "Deploying Ethical Validator Cloud Function"
echo "═══════════════════════════════════════════════════════════════════════════"
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Runtime: $RUNTIME"
echo "Function Name: $FUNCTION_NAME"
echo "Protocol Version: $PROTOCOL_VERSION"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed"
    echo "   Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Set the project
echo "📋 Setting project to $PROJECT_ID..."
gcloud config set project "$PROJECT_ID"

# Enable required APIs
echo "🔌 Enabling required APIs..."
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable secretmanager.googleapis.com

# Deploy the function
echo "🚀 Deploying function..."
gcloud functions deploy "$FUNCTION_NAME" \
    --gen2 \
    --runtime="$RUNTIME" \
    --region="$REGION" \
    --source=. \
    --entry-point="$ENTRY_POINT" \
    --trigger-http \
    --allow-unauthenticated \
    --set-env-vars="PROTOCOL_VERSION=$PROTOCOL_VERSION,GCP_PROJECT_ID=$PROJECT_ID,USE_CLOUD_SECRETS=true" \
    --memory=256MB \
    --timeout=60s

# Get the function URL
FUNCTION_URL=$(gcloud functions describe "$FUNCTION_NAME" \
    --region="$REGION" \
    --gen2 \
    --format="value(serviceConfig.uri)")

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo "✅ Deployment Complete"
echo "═══════════════════════════════════════════════════════════════════════════"
echo "Function URL: $FUNCTION_URL"
echo ""
echo "Test with:"
echo "curl -X POST $FUNCTION_URL \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{"
echo "    \"action\": {"
echo "      \"type\": \"quarantine\","
echo "      \"scope\": \"district\","
echo "      \"estimated_civilian_impact\": 0.2,"
echo "      \"medical_benefit\": 0.8,"
echo "      \"attack_rate\": 0.02,"
echo "      \"r_effective\": 1.5,"
echo "      \"severity_score\": 0.6"
echo "    },"
echo "    \"context\": {"
echo "      \"conflict_zone\": true,"
echo "      \"outbreak_suspected\": true,"
echo "      \"healthcare_capacity\": 0.7"
echo "    }"
echo "  }'"
echo "═══════════════════════════════════════════════════════════════════════════"
