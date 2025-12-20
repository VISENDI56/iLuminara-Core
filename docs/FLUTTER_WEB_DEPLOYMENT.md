# Flutter Web Frontend Deployment Guide

## Overview

This guide covers deploying the iLuminara Flutter Web frontend to Google Cloud Run with Firebase integration.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Cloud Run                          │
│  ┌──────────────────────────────────────────────┐  │
│  │  Nginx (Static File Server)                  │  │
│  │  ├─ Flutter Web App (Dart compiled to JS)    │  │
│  │  ├─ Service Worker (Offline support)         │  │
│  │  └─ Compassionate UI Components              │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │     Firebase Services          │
        ├────────────────────────────────┤
        │  • Authentication (CHW login)  │
        │  • Cloud Storage (voice notes) │
        │  • Firestore (metadata)        │
        └────────────────────────────────┘
```

## Prerequisites

1. **Google Cloud Project**
   - Enable Cloud Run API
   - Enable Container Registry API
   - Enable Cloud Build API

2. **Firebase Project**
   - Create a Firebase project
   - Enable Authentication (Email/Password)
   - Enable Cloud Storage
   - Enable Firestore

3. **Local Development**
   - Flutter SDK 3.16.0 or higher
   - Docker (for building container images)
   - gcloud CLI

## Firebase Configuration

### 1. Create Firebase Web App

```bash
# Go to Firebase Console
# Navigate to Project Settings > General
# Add a Web App to your Firebase project
# Copy the configuration values
```

### 2. Set Environment Variables

Create a `.env` file in the project root:

```env
FIREBASE_API_KEY=your_api_key_here
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
```

### 3. Configure Firebase Security Rules

**Firestore Rules** (`firestore.rules`):
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Only authenticated users can read/write their own data
    match /users/{userId}/{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Voice notes metadata
    match /voice_notes/{noteId} {
      allow read, write: if request.auth != null && 
                          request.auth.uid == resource.data.userId;
    }
  }
}
```

**Storage Rules** (`storage.rules`):
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Voice notes - only owner can access
    match /voice_notes/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

Deploy rules:
```bash
firebase deploy --only firestore:rules
firebase deploy --only storage:rules
```

## Local Development

### 1. Install Dependencies

```bash
cd frontend_web
flutter pub get
```

### 2. Run Locally

```bash
# Set Firebase config as environment variables
export FIREBASE_API_KEY="your_api_key"
export FIREBASE_AUTH_DOMAIN="your-project.firebaseapp.com"
export FIREBASE_PROJECT_ID="your-project-id"
export FIREBASE_STORAGE_BUCKET="your-project.appspot.com"
export FIREBASE_MESSAGING_SENDER_ID="your_sender_id"
export FIREBASE_APP_ID="your_app_id"

# Run the app
flutter run -d chrome --dart-define=FIREBASE_API_KEY=$FIREBASE_API_KEY \
  --dart-define=FIREBASE_AUTH_DOMAIN=$FIREBASE_AUTH_DOMAIN \
  --dart-define=FIREBASE_PROJECT_ID=$FIREBASE_PROJECT_ID \
  --dart-define=FIREBASE_STORAGE_BUCKET=$FIREBASE_STORAGE_BUCKET \
  --dart-define=FIREBASE_MESSAGING_SENDER_ID=$FIREBASE_MESSAGING_SENDER_ID \
  --dart-define=FIREBASE_APP_ID=$FIREBASE_APP_ID
```

### 3. Build for Production

```bash
flutter build web --release --web-renderer canvaskit
```

## Cloud Run Deployment

### Method 1: Using Cloud Build (Recommended)

1. **Set up Cloud Build substitutions:**

```bash
# Set your GCP project
gcloud config set project YOUR_PROJECT_ID

# Submit build with Firebase config
gcloud builds submit \
  --config=cloudbuild.yaml \
  --substitutions=_FIREBASE_API_KEY="$FIREBASE_API_KEY",_FIREBASE_AUTH_DOMAIN="$FIREBASE_AUTH_DOMAIN",_FIREBASE_PROJECT_ID="$FIREBASE_PROJECT_ID",_FIREBASE_STORAGE_BUCKET="$FIREBASE_STORAGE_BUCKET",_FIREBASE_MESSAGING_SENDER_ID="$FIREBASE_MESSAGING_SENDER_ID",_FIREBASE_APP_ID="$FIREBASE_APP_ID"
```

### Method 2: Manual Deployment

1. **Build Docker image:**

```bash
docker build -t gcr.io/YOUR_PROJECT_ID/iluminara-web:latest \
  --build-arg FIREBASE_API_KEY=$FIREBASE_API_KEY \
  --build-arg FIREBASE_AUTH_DOMAIN=$FIREBASE_AUTH_DOMAIN \
  --build-arg FIREBASE_PROJECT_ID=$FIREBASE_PROJECT_ID \
  --build-arg FIREBASE_STORAGE_BUCKET=$FIREBASE_STORAGE_BUCKET \
  --build-arg FIREBASE_MESSAGING_SENDER_ID=$FIREBASE_MESSAGING_SENDER_ID \
  --build-arg FIREBASE_APP_ID=$FIREBASE_APP_ID \
  -f frontend_web/Dockerfile .
```

2. **Push to Container Registry:**

```bash
docker push gcr.io/YOUR_PROJECT_ID/iluminara-web:latest
```

3. **Deploy to Cloud Run:**

```bash
gcloud run deploy iluminara-web \
  --image gcr.io/YOUR_PROJECT_ID/iluminara-web:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 10 \
  --memory 512Mi \
  --cpu 1 \
  --port 8080
```

### Method 3: Using Service YAML

```bash
# Update PROJECT_ID in frontend_web/cloud-run-service.yaml
kubectl apply -f frontend_web/cloud-run-service.yaml
```

## CI/CD with GitHub Actions

Create `.github/workflows/deploy-frontend.yml`:

```yaml
name: Deploy Flutter Web to Cloud Run

on:
  push:
    branches:
      - main
    paths:
      - 'frontend_web/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - id: auth
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
      
      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v1
      
      - name: Build and Deploy
        env:
          FIREBASE_API_KEY: ${{ secrets.FIREBASE_API_KEY }}
          FIREBASE_AUTH_DOMAIN: ${{ secrets.FIREBASE_AUTH_DOMAIN }}
          FIREBASE_PROJECT_ID: ${{ secrets.FIREBASE_PROJECT_ID }}
          FIREBASE_STORAGE_BUCKET: ${{ secrets.FIREBASE_STORAGE_BUCKET }}
          FIREBASE_MESSAGING_SENDER_ID: ${{ secrets.FIREBASE_MESSAGING_SENDER_ID }}
          FIREBASE_APP_ID: ${{ secrets.FIREBASE_APP_ID }}
        run: |
          gcloud builds submit --config=cloudbuild.yaml \
            --substitutions=_FIREBASE_API_KEY="$FIREBASE_API_KEY",_FIREBASE_AUTH_DOMAIN="$FIREBASE_AUTH_DOMAIN",_FIREBASE_PROJECT_ID="$FIREBASE_PROJECT_ID",_FIREBASE_STORAGE_BUCKET="$FIREBASE_STORAGE_BUCKET",_FIREBASE_MESSAGING_SENDER_ID="$FIREBASE_MESSAGING_SENDER_ID",_FIREBASE_APP_ID="$FIREBASE_APP_ID"
```

## Testing Deployment

1. **Get Cloud Run URL:**

```bash
gcloud run services describe iluminara-web --region us-central1 --format='value(status.url)'
```

2. **Test endpoints:**

```bash
# Health check
curl https://YOUR-SERVICE-URL/health

# Access the app
open https://YOUR-SERVICE-URL
```

## Compassionate UI Features

### 1. Anxiety-Reducing Design
- Soft color palette (primary: #667eea, secondary: #764ba2)
- Gentle animations and transitions
- Clear, encouraging error messages
- Progress indicators for long operations

### 2. Offline-First Capabilities
- Service Worker for offline functionality
- Local storage with Hive
- Automatic sync when connection restored
- Clear offline/online indicators

### 3. CHW-Focused UX
- Large touch targets (minimum 44x44 pixels)
- High contrast text (WCAG AAA compliant)
- Simple navigation with bottom tabs
- Voice recording with location tagging
- Patient ID tracking

## Monitoring and Logs

### View Logs

```bash
# Cloud Run logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=iluminara-web" --limit 50

# Firebase logs
firebase functions:log
```

### Set Up Monitoring

```bash
# Create uptime check
gcloud monitoring uptime-checks create https YOUR-SERVICE-URL \
  --display-name="iLuminara Web Uptime" \
  --period=60
```

## Scaling Configuration

The service is configured to:
- **Min instances:** 0 (scale to zero when not in use)
- **Max instances:** 10 (handle up to 800 concurrent requests)
- **CPU:** 1 core
- **Memory:** 512 MB
- **Request timeout:** 300 seconds

Adjust in `cloudbuild.yaml` or via gcloud:

```bash
gcloud run services update iluminara-web \
  --min-instances=1 \
  --max-instances=20 \
  --memory=1Gi \
  --cpu=2
```

## Security Considerations

1. **Authentication:** Firebase Auth with secure tokens
2. **CORS:** Configured in Firestore and Storage rules
3. **HTTPS:** Enforced by Cloud Run
4. **Content Security Policy:** Configured in nginx.conf
5. **Data Encryption:** 
   - In transit: TLS 1.3
   - At rest: Google-managed encryption

## Cost Optimization

- **Scale to zero:** No charges when not in use
- **Small container:** ~50MB compressed image
- **CDN:** Use Cloud CDN for static assets
- **Caching:** Aggressive caching for static files

Estimated costs:
- **Cloud Run:** ~$0.05 per 10,000 requests
- **Firebase:** Free tier for < 50k reads/day
- **Storage:** ~$0.02 per GB per month

## Troubleshooting

### Build Fails

```bash
# Check Cloud Build logs
gcloud builds list --limit=10

# View specific build
gcloud builds log BUILD_ID
```

### Service Won't Start

```bash
# Check service status
gcloud run services describe iluminara-web --region us-central1

# View recent logs
gcloud logging read "resource.type=cloud_run_revision" --limit=50
```

### Firebase Connection Issues

- Verify Firebase config is correct
- Check Firebase console for authentication errors
- Ensure Storage and Firestore rules are deployed

## Support

For issues or questions:
- GitHub Issues: https://github.com/VISENDI56/iLuminara-Core/issues
- Documentation: See `/docs` folder
- Firebase Support: https://firebase.google.com/support

## Next Steps

1. Set up custom domain with Cloud Run
2. Configure Cloud CDN for better performance
3. Add monitoring alerts
4. Set up automated backups
5. Implement A/B testing with Firebase Remote Config
