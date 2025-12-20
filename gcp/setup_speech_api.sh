#!/bin/bash
# Speech-to-Text API Setup for Swahili (sw-KE)
# This script enables the Google Cloud Speech-to-Text API and configures it for Swahili language support

set -e

echo "=================================================="
echo "iLuminara: Speech-to-Text API Setup (Swahili)"
echo "=================================================="
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed"
    echo "   Please install: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if project is set
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: No GCP project configured"
    echo "   Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "📋 Using GCP Project: $PROJECT_ID"
echo ""

# Step 1: Enable Speech-to-Text API
echo "🔧 Step 1: Enabling Speech-to-Text API..."
gcloud services enable speech.googleapis.com --project=$PROJECT_ID
echo "✅ Speech API enabled"
echo ""

# Step 2: Test Swahili speech recognition (if audio file provided)
if [ -n "$1" ] && [ -f "$1" ]; then
    AUDIO_FILE="$1"
    echo "🎤 Step 2: Testing Swahili speech recognition..."
    echo "   Audio file: $AUDIO_FILE"
    
    gcloud ml speech recognize "$AUDIO_FILE" \
        --language-code=sw-KE \
        --project=$PROJECT_ID
    
    echo "✅ Speech recognition test completed"
else
    echo "ℹ️  Step 2: Skipping speech recognition test"
    echo "   To test, provide an audio file as argument:"
    echo "   ./setup_speech_api.sh swahili-audio.wav"
fi

echo ""
echo "=================================================="
echo "✅ Speech-to-Text API Setup Complete"
echo "=================================================="
echo ""
echo "Supported Swahili Language Codes:"
echo "  • sw-KE (Kenya) - Primary"
echo "  • sw-TZ (Tanzania)"
echo ""
echo "Next Steps:"
echo "  1. Use the Python SDK: from google.cloud import speech"
echo "  2. See: edge_node/speech_recognition/swahili_recognizer.py"
echo ""
