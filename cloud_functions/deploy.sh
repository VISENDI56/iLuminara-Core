#!/bin/bash

# Deployment script for Humanitarian Constraint Checker Cloud Functions
# ═════════════════════════════════════════════════════════════════════════════

set -e

echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║  Humanitarian Constraint Encoding - Cloud Functions Deployment       ║"
echo "║  iLuminara-Core Governance Kernel Extension                           ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""

# Load configuration
source config.env

echo "📋 Configuration:"
echo "   Project ID: $GCP_PROJECT_ID"
echo "   Region: $CLOUD_FUNCTIONS_REGION"
echo "   Runtime: $CLOUD_FUNCTIONS_RUNTIME"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI not found. Please install Google Cloud SDK."
    exit 1
fi

echo "🔐 Authenticating with Google Cloud..."
gcloud config set project $GCP_PROJECT_ID

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "1️⃣  Deploying Constraint Checker Function"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "⚠️  WARNING: Deploying with --allow-unauthenticated for development."
echo "   For production humanitarian systems, implement proper authentication:"
echo "   - Remove --allow-unauthenticated flag"
echo "   - Add IAM policies for authorized users/services"
echo "   - Use Cloud Identity-Aware Proxy (IAP) for web access"
echo "   - Implement API keys or OAuth for service-to-service calls"
echo ""

gcloud functions deploy humanitarian-constraint-checker \
    --gen2 \
    --runtime=$CLOUD_FUNCTIONS_RUNTIME \
    --region=$CLOUD_FUNCTIONS_REGION \
    --source=. \
    --entry-point=check_humanitarian_constraint \
    --trigger-http \
    --allow-unauthenticated \
    --memory=$CLOUD_FUNCTIONS_MEMORY \
    --timeout=$CLOUD_FUNCTIONS_TIMEOUT \
    --service-account=$SERVICE_ACCOUNT_EMAIL

echo "✅ Constraint checker deployed"
echo ""

echo "═══════════════════════════════════════════════════════════════════════"
echo "2️⃣  Deploying Protocol List Function"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

gcloud functions deploy humanitarian-list-protocols \
    --gen2 \
    --runtime=$CLOUD_FUNCTIONS_RUNTIME \
    --region=$CLOUD_FUNCTIONS_REGION \
    --source=. \
    --entry-point=list_protocols \
    --trigger-http \
    --allow-unauthenticated \
    --memory=$CLOUD_FUNCTIONS_MEMORY \
    --timeout=$CLOUD_FUNCTIONS_TIMEOUT \
    --service-account=$SERVICE_ACCOUNT_EMAIL

echo "✅ Protocol list function deployed"
echo ""

echo "═══════════════════════════════════════════════════════════════════════"
echo "3️⃣  Deploying Violations Retrieval Function"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

gcloud functions deploy humanitarian-get-violations \
    --gen2 \
    --runtime=$CLOUD_FUNCTIONS_RUNTIME \
    --region=$CLOUD_FUNCTIONS_REGION \
    --source=. \
    --entry-point=get_violations \
    --trigger-http \
    --allow-unauthenticated \
    --memory=$CLOUD_FUNCTIONS_MEMORY \
    --timeout=$CLOUD_FUNCTIONS_TIMEOUT \
    --service-account=$SERVICE_ACCOUNT_EMAIL

echo "✅ Violations function deployed"
echo ""

echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║  ✅ All Cloud Functions Deployed Successfully                         ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📡 Endpoints:"
echo ""

# Get function URLs
CONSTRAINT_CHECKER_URL=$(gcloud functions describe humanitarian-constraint-checker \
    --region=$CLOUD_FUNCTIONS_REGION \
    --format='value(serviceConfig.uri)')

LIST_PROTOCOLS_URL=$(gcloud functions describe humanitarian-list-protocols \
    --region=$CLOUD_FUNCTIONS_REGION \
    --format='value(serviceConfig.uri)')

GET_VIOLATIONS_URL=$(gcloud functions describe humanitarian-get-violations \
    --region=$CLOUD_FUNCTIONS_REGION \
    --format='value(serviceConfig.uri)')

echo "   Constraint Checker: $CONSTRAINT_CHECKER_URL"
echo "   List Protocols:     $LIST_PROTOCOLS_URL"
echo "   Get Violations:     $GET_VIOLATIONS_URL"
echo ""
echo "📚 Usage Examples:"
echo ""
echo "# Check a constraint:"
echo "curl -X POST $CONSTRAINT_CHECKER_URL \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"protocol_id\":\"MEDICAL_TRIAGE\",\"action_data\":{\"patient_id\":\"PAT-001\",\"medical_severity\":\"CRITICAL\"}}'"
echo ""
echo "# List protocols:"
echo "curl $LIST_PROTOCOLS_URL"
echo ""
echo "# Get violations:"
echo "curl \"$GET_VIOLATIONS_URL?severity=CRITICAL&unresolved_only=true\""
echo ""
echo "🎉 Deployment complete!"
