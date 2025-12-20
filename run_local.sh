#!/bin/bash
# Run Flutter Web app locally with Firebase configuration

set -e

cd "$(dirname "$0")"

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "❌ .env file not found. Run ./setup_flutter_web.sh first"
    exit 1
fi

# Validate Firebase config
if [ -z "$FIREBASE_API_KEY" ] || [ -z "$FIREBASE_PROJECT_ID" ]; then
    echo "❌ Firebase configuration is incomplete in .env file"
    exit 1
fi

cd frontend_web

echo "🚀 Starting iLuminara Flutter Web..."
echo "📱 Opening in browser..."
echo ""
echo "Firebase Project: $FIREBASE_PROJECT_ID"
echo ""

flutter run -d chrome \
  --dart-define=FIREBASE_API_KEY="$FIREBASE_API_KEY" \
  --dart-define=FIREBASE_AUTH_DOMAIN="$FIREBASE_AUTH_DOMAIN" \
  --dart-define=FIREBASE_PROJECT_ID="$FIREBASE_PROJECT_ID" \
  --dart-define=FIREBASE_STORAGE_BUCKET="$FIREBASE_STORAGE_BUCKET" \
  --dart-define=FIREBASE_MESSAGING_SENDER_ID="$FIREBASE_MESSAGING_SENDER_ID" \
  --dart-define=FIREBASE_APP_ID="$FIREBASE_APP_ID"
