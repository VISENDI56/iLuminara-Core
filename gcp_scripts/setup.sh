#!/bin/bash

# ══════════════════════════════════════════════════════════════════════════
# iLuminara GCP Setup Script
# ══════════════════════════════════════════════════════════════════════════
# Initial setup for GCP project configuration and service accounts

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   iLuminara GCP Setup${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"

# Check if PROJECT_ID is set
if [ -z "$GCP_PROJECT_ID" ]; then
    echo "Please enter your GCP Project ID:"
    read -r PROJECT_ID
    export GCP_PROJECT_ID="$PROJECT_ID"
else
    PROJECT_ID="$GCP_PROJECT_ID"
fi

REGION="${GCP_REGION:-us-central1}"

echo ""
echo -e "${YELLOW}Configuration:${NC}"
echo "  Project ID: $PROJECT_ID"
echo "  Region: $REGION"
echo ""

# Authenticate
echo -e "${YELLOW}Authenticating with GCP...${NC}"
gcloud auth login
gcloud config set project "$PROJECT_ID"

echo -e "${GREEN}✓ Setup complete${NC}"
echo ""
echo "You can now run: ./gcp_scripts/deploy.sh"
