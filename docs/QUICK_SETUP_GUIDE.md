# iLuminara Flutter Web - Quick Setup Guide

## Prerequisites

- **Flutter SDK** 3.16.0 or higher
- **Firebase Account** with a project created
- **Google Cloud Account** (for Cloud Run deployment)
- **Docker** (for local container testing)

## Step 1: Firebase Setup

### 1.1 Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Click "Add project"
3. Name it `iluminara-core` (or your preferred name)
4. Enable Google Analytics (optional)
5. Click "Create project"

### 1.2 Add Web App to Firebase

1. In Firebase Console, click the web icon (</>) to add a web app
2. Register app with nickname: `iLuminara Web`
3. Enable Firebase Hosting (optional)
4. Copy the Firebase configuration

### 1.3 Enable Firebase Services

**Authentication:**
1. Go to Authentication > Sign-in method
2. Enable "Email/Password" provider
3. Click "Save"

**Cloud Storage:**
1. Go to Storage > Get Started
2. Choose "Start in production mode"
3. Select your location (e.g., us-central1)
4. Click "Done"

**Firestore Database:**
1. Go to Firestore Database > Create database
2. Start in "production mode"
3. Select your location
4. Click "Enable"

### 1.4 Deploy Security Rules

```bash
cd frontend_web

# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize Firebase (select your project)
firebase use YOUR_PROJECT_ID

# Deploy security rules
firebase deploy --only firestore:rules,storage:rules,firestore:indexes
```

## Step 2: Local Development Setup

### 2.1 Clone Repository

```bash
git clone https://github.com/VISENDI56/iLuminara-Core.git
cd iLuminara-Core
```

### 2.2 Run Setup Script

```bash
chmod +x setup_flutter_web.sh
./setup_flutter_web.sh
```

This will:
- Check Flutter installation
- Create `.env` template
- Prompt for Firebase configuration
- Install dependencies

### 2.3 Configure Environment Variables

Edit the `.env` file with your Firebase configuration:

```env
FIREBASE_API_KEY=AIzaSy...
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=123456789
FIREBASE_APP_ID=1:123456789:web:abc123
```

### 2.4 Run Locally

```bash
./run_local.sh
```

Or manually:

```bash
cd frontend_web
flutter run -d chrome \
  --dart-define=FIREBASE_API_KEY="$FIREBASE_API_KEY" \
  --dart-define=FIREBASE_AUTH_DOMAIN="$FIREBASE_AUTH_DOMAIN" \
  --dart-define=FIREBASE_PROJECT_ID="$FIREBASE_PROJECT_ID" \
  --dart-define=FIREBASE_STORAGE_BUCKET="$FIREBASE_STORAGE_BUCKET" \
  --dart-define=FIREBASE_MESSAGING_SENDER_ID="$FIREBASE_MESSAGING_SENDER_ID" \
  --dart-define=FIREBASE_APP_ID="$FIREBASE_APP_ID"
```

## Step 3: Cloud Run Deployment

### 3.1 Google Cloud Setup

```bash
# Install gcloud CLI
# See: https://cloud.google.com/sdk/docs/install

# Login to Google Cloud
gcloud auth login

# Set your project
gcloud config set project YOUR_GCP_PROJECT_ID

# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  containerregistry.googleapis.com
```

### 3.2 Deploy to Cloud Run

```bash
# From project root
gcloud builds submit \
  --config=cloudbuild.yaml \
  --substitutions=_FIREBASE_API_KEY="$FIREBASE_API_KEY",_FIREBASE_AUTH_DOMAIN="$FIREBASE_AUTH_DOMAIN",_FIREBASE_PROJECT_ID="$FIREBASE_PROJECT_ID",_FIREBASE_STORAGE_BUCKET="$FIREBASE_STORAGE_BUCKET",_FIREBASE_MESSAGING_SENDER_ID="$FIREBASE_MESSAGING_SENDER_ID",_FIREBASE_APP_ID="$FIREBASE_APP_ID"
```

### 3.3 Get Service URL

```bash
gcloud run services describe iluminara-web \
  --region us-central1 \
  --format='value(status.url)'
```

Visit the URL to access your deployed app!

## Step 4: Create First CHW Account

1. Open the deployed app or local version
2. Click "Need an account? Create one"
3. Fill in:
   - **Full Name**: Your name (e.g., "Jane Doe")
   - **Email**: Your email (e.g., "jane@example.com")
   - **Password**: Secure password (min 6 characters)
4. Click "Create Account"
5. You're now signed in!

## Step 5: Test Voice Recording

1. Navigate to "Record" tab
2. Optionally fill in:
   - **Patient ID**: e.g., "PAT-001"
   - **Notes**: e.g., "Fever and cough symptoms"
3. Click "Start Recording"
4. Click "Stop Recording"
5. Voice note is saved locally and synced to cloud (if online)

## Troubleshooting

### "Flutter not found"

Install Flutter SDK:
```bash
# macOS/Linux
git clone https://github.com/flutter/flutter.git -b stable
export PATH="$PATH:`pwd`/flutter/bin"

# Windows
# Download from https://docs.flutter.dev/get-started/install/windows
```

### "Firebase initialization error"

Check that:
- Firebase configuration in `.env` is correct
- Firebase project exists
- Web app is registered in Firebase Console

### "Permission denied" on scripts

Make scripts executable:
```bash
chmod +x setup_flutter_web.sh run_local.sh
```

### Build fails on Cloud Run

Check:
- All Firebase substitutions are provided
- GCP project has billing enabled
- Required APIs are enabled

### Voice recording not working

Browser permissions needed:
- Microphone access
- Location access (for GPS coordinates)

## Next Steps

1. **Custom Domain**: Map a custom domain to Cloud Run
2. **CI/CD**: Set up GitHub Actions for automatic deployment
3. **Monitoring**: Configure Cloud Monitoring alerts
4. **Backup**: Set up automated Firestore backups
5. **Testing**: Add integration tests

## Resources

- [Flutter Web Documentation](https://docs.flutter.dev/platform-integration/web)
- [Firebase Documentation](https://firebase.google.com/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Project README](../README.md)
- [Deployment Guide](../docs/FLUTTER_WEB_DEPLOYMENT.md)

## Support

- **GitHub Issues**: https://github.com/VISENDI56/iLuminara-Core/issues
- **Email**: support@iluminara.health
- **Documentation**: `/docs` folder

---

**You're ready to start using iLuminara!** 🎉
