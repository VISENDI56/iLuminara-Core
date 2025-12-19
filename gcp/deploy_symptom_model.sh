#!/bin/bash
# FRENASA Symptom Extraction Model Deployment to Google Cloud AI Platform
# Deploys the symptom extraction model to GCP for inference

set -e

echo "=================================================="
echo "iLuminara: FRENASA Symptom Extractor Deployment"
echo "=================================================="
echo ""

# Configuration
REGION="${GCP_REGION:-us-central1}"
MODEL_NAME="${MODEL_NAME:-frenasa-symptom-extractor}"
DISPLAY_NAME="${DISPLAY_NAME:-FRENASA-Symptom-Extractor}"
CONTAINER_IMAGE_TEMPLATE="${CONTAINER_IMAGE:-gcr.io/PROJECT_ID/frenasa-symptom:latest}"

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

# Substitute PROJECT_ID in container image URI using sed
CONTAINER_IMAGE=$(echo "$CONTAINER_IMAGE_TEMPLATE" | sed "s/PROJECT_ID/${PROJECT_ID}/g")

echo "📋 Configuration:"
echo "   Project: $PROJECT_ID"
echo "   Region: $REGION"
echo "   Model Name: $MODEL_NAME"
echo "   Display Name: $DISPLAY_NAME"
echo "   Container: $CONTAINER_IMAGE"
echo ""

# Step 1: Enable required APIs
echo "🔧 Step 1: Enabling required APIs..."
gcloud services enable aiplatform.googleapis.com --project=$PROJECT_ID
gcloud services enable containerregistry.googleapis.com --project=$PROJECT_ID
echo "✅ APIs enabled"
echo ""

# Step 2: Build and push container image (if Dockerfile exists)
if [ -f "edge_node/frenasa_engine/Dockerfile" ]; then
    echo "🐳 Step 2: Building and pushing container image..."
    
    docker build -t "$CONTAINER_IMAGE" -f edge_node/frenasa_engine/Dockerfile .
    docker push "$CONTAINER_IMAGE"
    
    echo "✅ Container image built and pushed"
else
    echo "ℹ️  Step 2: Skipping container build (no Dockerfile found)"
    echo "   Expected: edge_node/frenasa_engine/Dockerfile"
    echo "   You can build manually and update CONTAINER_IMAGE variable"
fi
echo ""

# Step 3: Upload model to Vertex AI
echo "🚀 Step 3: Uploading model to Vertex AI..."
gcloud ai models upload \
    --region="$REGION" \
    --display-name="$DISPLAY_NAME" \
    --container-image-uri="$CONTAINER_IMAGE" \
    --project="$PROJECT_ID"

echo "✅ Model uploaded successfully"
echo ""

echo "=================================================="
echo "✅ FRENASA Symptom Extractor Deployed"
echo "=================================================="
echo ""
echo "Model Details:"
echo "  • Region: $REGION"
echo "  • Name: $DISPLAY_NAME"
echo "  • Endpoint: Check Vertex AI console"
echo ""
echo "Next Steps:"
echo "  1. Create an endpoint for online predictions"
echo "  2. Deploy model to endpoint"
echo "  3. Test with sample data"
echo ""
echo "Commands:"
echo "  gcloud ai endpoints create --region=$REGION --display-name=$DISPLAY_NAME-endpoint"
echo "  gcloud ai endpoints deploy-model ENDPOINT_ID --region=$REGION --model=MODEL_ID"
echo ""
