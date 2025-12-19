#!/bin/bash

# ══════════════════════════════════════════════════════════════════════════
# iLuminara GCP Deployment Script
# ══════════════════════════════════════════════════════════════════════════
# Deploys iLuminara backend to Google Cloud Run and frontend to Cloud Run
# with integrated Vertex AI, BigQuery, and Speech-to-Text services.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   iLuminara GCP Deployment - Sovereign Health Platform${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"

# ══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════

# Check if PROJECT_ID is set
if [ -z "$GCP_PROJECT_ID" ]; then
    echo -e "${RED}Error: GCP_PROJECT_ID environment variable not set${NC}"
    echo "Usage: export GCP_PROJECT_ID='your-project-id'"
    echo "       ./deploy.sh"
    exit 1
fi

PROJECT_ID="$GCP_PROJECT_ID"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME_BACKEND="${SERVICE_NAME_BACKEND:-iluminara-backend}"
SERVICE_NAME_FRONTEND="${SERVICE_NAME_FRONTEND:-iluminara-frontend}"

echo -e "${YELLOW}Configuration:${NC}"
echo "  Project ID: $PROJECT_ID"
echo "  Region: $REGION"
echo "  Backend Service: $SERVICE_NAME_BACKEND"
echo "  Frontend Service: $SERVICE_NAME_FRONTEND"
echo ""

# ══════════════════════════════════════════════════════════════════════════
# STEP 1: Enable Required GCP APIs
# ══════════════════════════════════════════════════════════════════════════

echo -e "${YELLOW}[1/6] Enabling GCP APIs...${NC}"

gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    containerregistry.googleapis.com \
    aiplatform.googleapis.com \
    bigquery.googleapis.com \
    speech.googleapis.com \
    storage.googleapis.com \
    --project="$PROJECT_ID"

echo -e "${GREEN}✓ APIs enabled${NC}\n"

# ══════════════════════════════════════════════════════════════════════════
# STEP 2: Set Default Project
# ══════════════════════════════════════════════════════════════════════════

echo -e "${YELLOW}[2/6] Setting default project...${NC}"
gcloud config set project "$PROJECT_ID"
echo -e "${GREEN}✓ Project set${NC}\n"

# ══════════════════════════════════════════════════════════════════════════
# STEP 3: Build and Deploy Backend Service
# ══════════════════════════════════════════════════════════════════════════

echo -e "${YELLOW}[3/6] Building and deploying backend service...${NC}"

# Create Dockerfile for backend if it doesn't exist
if [ ! -f "Dockerfile.backend" ]; then
    cat > Dockerfile.backend << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY governance_kernel/ ./governance_kernel/

# Expose port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "app.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
fi

# Deploy backend to Cloud Run
gcloud run deploy "$SERVICE_NAME_BACKEND" \
    --source . \
    --dockerfile Dockerfile.backend \
    --platform managed \
    --region "$REGION" \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10 \
    --set-env-vars "USE_MOCK_GCP=false,GCP_PROJECT_ID=$PROJECT_ID" \
    --project="$PROJECT_ID"

# Get backend URL
BACKEND_URL=$(gcloud run services describe "$SERVICE_NAME_BACKEND" \
    --platform managed \
    --region "$REGION" \
    --format 'value(status.url)' \
    --project="$PROJECT_ID")

echo -e "${GREEN}✓ Backend deployed at: $BACKEND_URL${NC}\n"

# ══════════════════════════════════════════════════════════════════════════
# STEP 4: Build and Deploy Frontend Service
# ══════════════════════════════════════════════════════════════════════════

echo -e "${YELLOW}[4/6] Building and deploying frontend service...${NC}"

# Create Dockerfile for frontend if it doesn't exist
if [ ! -f "Dockerfile.frontend" ]; then
    cat > Dockerfile.frontend << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app/frontend/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
EOF
fi

# Deploy frontend to Cloud Run
gcloud run deploy "$SERVICE_NAME_FRONTEND" \
    --source . \
    --dockerfile Dockerfile.frontend \
    --platform managed \
    --region "$REGION" \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10 \
    --set-env-vars "BACKEND_URL=$BACKEND_URL" \
    --project="$PROJECT_ID"

# Get frontend URL
FRONTEND_URL=$(gcloud run services describe "$SERVICE_NAME_FRONTEND" \
    --platform managed \
    --region "$REGION" \
    --format 'value(status.url)' \
    --project="$PROJECT_ID")

echo -e "${GREEN}✓ Frontend deployed at: $FRONTEND_URL${NC}\n"

# ══════════════════════════════════════════════════════════════════════════
# STEP 5: Create BigQuery Dataset (Optional)
# ══════════════════════════════════════════════════════════════════════════

echo -e "${YELLOW}[5/6] Creating BigQuery dataset...${NC}"

DATASET_NAME="health_intelligence"

# Check if dataset exists
if ! bq show --project_id="$PROJECT_ID" "$DATASET_NAME" &> /dev/null; then
    bq mk \
        --project_id="$PROJECT_ID" \
        --location="$REGION" \
        --dataset \
        "$DATASET_NAME"
    
    echo -e "${GREEN}✓ BigQuery dataset created: $DATASET_NAME${NC}\n"
else
    echo -e "${YELLOW}! BigQuery dataset already exists: $DATASET_NAME${NC}\n"
fi

# ══════════════════════════════════════════════════════════════════════════
# STEP 6: Display Deployment Summary
# ══════════════════════════════════════════════════════════════════════════

echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   Deployment Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Service URLs:${NC}"
echo "  Backend API:  $BACKEND_URL"
echo "  Frontend UI:  $FRONTEND_URL"
echo ""
echo -e "${YELLOW}GCP Resources:${NC}"
echo "  Project:      $PROJECT_ID"
echo "  Region:       $REGION"
echo "  BigQuery:     $DATASET_NAME"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Access the dashboard at: $FRONTEND_URL"
echo "  2. API documentation at: $BACKEND_URL/docs"
echo "  3. Configure Vertex AI endpoints in app/backend/*.py"
echo "  4. Load data into BigQuery dataset: $DATASET_NAME"
echo ""
echo -e "${GREEN}iLuminara is now live on Google Cloud Platform!${NC}"
