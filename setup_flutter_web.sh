#!/bin/bash
# Quick setup script for iLuminara Flutter Web Frontend

set -e

echo "🚀 Setting up iLuminara Flutter Web Frontend"
echo "============================================="
echo ""

# Check if Flutter is installed
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter is not installed. Please install Flutter first:"
    echo "   https://docs.flutter.dev/get-started/install"
    exit 1
fi

echo "✅ Flutter found: $(flutter --version | head -n 1)"
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")/frontend_web"

# Check if .env file exists
if [ ! -f "../.env" ]; then
    echo "📝 Creating .env template file..."
    cat > ../.env << 'EOF'
# Firebase Configuration
# Get these values from Firebase Console > Project Settings > General > Your apps > Web app
FIREBASE_API_KEY=
FIREBASE_AUTH_DOMAIN=
FIREBASE_PROJECT_ID=iluminara-core
FIREBASE_STORAGE_BUCKET=
FIREBASE_MESSAGING_SENDER_ID=
FIREBASE_APP_ID=
EOF
    echo "⚠️  Please fill in the .env file with your Firebase credentials"
    echo "   Location: $(pwd)/../.env"
    echo ""
    echo "   Get your Firebase config from:"
    echo "   https://console.firebase.google.com"
    echo ""
    read -p "Press Enter after filling in .env to continue..."
fi

# Load environment variables
if [ -f "../.env" ]; then
    export $(cat ../.env | grep -v '^#' | xargs)
fi

# Validate Firebase config
if [ -z "$FIREBASE_API_KEY" ] || [ -z "$FIREBASE_PROJECT_ID" ]; then
    echo "❌ Firebase configuration is incomplete in .env file"
    exit 1
fi

echo "✅ Firebase configuration loaded"
echo ""

# Install Flutter dependencies
echo "📦 Installing Flutter dependencies..."
flutter pub get

echo ""
echo "✅ Setup complete!"
echo ""
echo "Available commands:"
echo "  1. Run locally:       ./run_local.sh"
echo "  2. Build for web:     flutter build web --release"
echo "  3. Deploy to Cloud:   gcloud builds submit --config=../cloudbuild.yaml"
echo ""
echo "For detailed instructions, see:"
echo "  - frontend_web/README.md"
echo "  - docs/FLUTTER_WEB_DEPLOYMENT.md"
echo ""
