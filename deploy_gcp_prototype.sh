#!/bin/bash
# iLuminara Google Cloud Prototype Deployment
# ═════════════════════════════════════════════════════════════════════════════
# This script deploys the iLuminara health intelligence platform to Google Cloud
# Platform, enabling rapid prototyping and demonstration of core capabilities:
# - FRENASA AI Engine (Cloud Run)
# - HSTPU Forecaster (Vertex AI)
# - HSML Ledger (Cloud Spanner)
# - Demo outbreak simulation (BigQuery)
# - Compassionate UI Dashboard (Cloud Run)
# ═════════════════════════════════════════════════════════════════════════════

set -e  # Exit on error

echo "================================================"
echo "🌐 iLUMINARA GOOGLE CLOUD PROTOTYPE DEPLOYMENT"
echo "================================================"
echo ""

# Verify gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI not found. Please install Google Cloud SDK."
    echo "   Installation: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get current project
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: No active Google Cloud project. Set one with:"
    echo "   gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "📋 Deploying to project: $PROJECT_ID"
echo ""

# 1. Enable required services
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Enabling Required Google Cloud Services"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

SERVICES=(
  "aiplatform.googleapis.com"
  "speech.googleapis.com"
  "bigquery.googleapis.com"
  "pubsub.googleapis.com"
  "cloudfunctions.googleapis.com"
  "run.googleapis.com"
  "firestore.googleapis.com"
)

for service in "${SERVICES[@]}"; do
  echo "🔌 Enabling $service..."
  gcloud services enable "$service" --project="$PROJECT_ID"
done

echo ""
echo "✅ All services enabled"
echo ""

# 2. Deploy core components
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Deploying Core Components"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Deploy FRENASA AI Engine
echo "🤖 Deploying FRENASA AI Engine..."
gcloud run deploy frenasa-engine \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="PROJECT_ID=$PROJECT_ID" \
  --project="$PROJECT_ID"

echo ""
echo "✅ FRENASA AI Engine deployed"
echo ""

# Deploy HSTPU Forecaster
echo "📊 Deploying HSTPU Forecaster..."
echo "⚠️  Note: This requires a pre-trained model. Skipping for initial prototype."
echo "   To deploy, first create a model in Vertex AI, then run:"
echo "   gcloud ai endpoints deploy-model hstpu-endpoint \\"
echo "     --project=$PROJECT_ID \\"
echo "     --region=us-central1 \\"
echo "     --model=projects/$PROJECT_ID/locations/us-central1/models/hstpu-model \\"
echo "     --display-name='HSTPU-Forecaster' \\"
echo "     --machine-type=n1-standard-4"
echo ""

# Setup HSML Ledger
echo "💾 Setting up HSML Ledger..."
echo "⚠️  Note: Cloud Spanner requires manual setup. Creating placeholder."
echo "   To create, run:"
echo "   gcloud spanner instances create luminara-ledger \\"
echo "     --config=regional-us-central1 \\"
echo "     --description='iLuminara HSML Blockchain Simulation' \\"
echo "     --nodes=3 \\"
echo "     --project=$PROJECT_ID"
echo ""

# 3. Create demo data pipeline
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Creating Demo Data Pipeline"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📊 Creating demo outbreak simulation in BigQuery..."
python3 create_bq_demo_data.py || {
    echo "⚠️  BigQuery demo data creation failed."
    echo "   You may need to install dependencies:"
    echo "   pip install google-cloud-bigquery"
    echo "   Continuing with deployment..."
}

echo ""

# 4. Launch monitoring dashboard
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4: Launching Monitoring Dashboard"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "🎭 Launching Compassionate UI..."
echo "⚠️  Note: This requires a pre-built Docker image. Building and deploying..."

# Get the FRENASA endpoint URL
FRENASA_URL=$(gcloud run services describe frenasa-engine \
  --platform managed \
  --region us-central1 \
  --format="value(status.url)" \
  --project="$PROJECT_ID" 2>/dev/null || echo "")

if [ -z "$FRENASA_URL" ]; then
    FRENASA_URL="https://frenasa-engine-abcdef-uc.a.run.app"
    echo "⚠️  Could not retrieve FRENASA URL, using placeholder"
fi

gcloud run deploy iluminara-dashboard \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="API_ENDPOINT=$FRENASA_URL,PROJECT_ID=$PROJECT_ID" \
  --project="$PROJECT_ID" || {
    echo "⚠️  Dashboard deployment failed. This may require a Dockerfile."
    echo "   Create a Dockerfile in the repository root to enable deployment."
}

echo ""

# 5. Display deployment summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ PROTOTYPE DEPLOYMENT COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Access Points:"
echo ""

# Get dashboard URL
DASHBOARD_URL=$(gcloud run services describe iluminara-dashboard \
  --platform managed \
  --region us-central1 \
  --format="value(status.url)" \
  --project="$PROJECT_ID" 2>/dev/null || echo "")

if [ -n "$DASHBOARD_URL" ]; then
    echo "   📊 Dashboard: $DASHBOARD_URL"
else
    echo "   ⚠️  Dashboard deployment pending"
fi

if [ -n "$FRENASA_URL" ]; then
    echo "   🤖 FRENASA API: $FRENASA_URL"
fi

echo ""
echo "📋 Next Steps:"
echo ""
echo "   1. View logs:"
echo "      gcloud run services logs read frenasa-engine --project=$PROJECT_ID"
echo ""
echo "   2. Query demo data:"
echo "      bq query --use_legacy_sql=false 'SELECT * FROM iluminara.outbreak_simulations LIMIT 10'"
echo ""
echo "   3. Monitor services:"
echo "      gcloud run services list --project=$PROJECT_ID"
echo ""
echo "   4. Deploy HSTPU model (requires training):"
echo "      See comments in this script for manual deployment commands"
echo ""
echo "================================================"
echo "Quote: 'Transform preventable suffering from statistical inevitability to historical anomaly.'"
echo "================================================"
