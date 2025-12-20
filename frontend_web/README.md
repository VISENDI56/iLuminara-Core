# iLuminara Flutter Web Frontend

Compassionate UI for Community Health Workers with offline-first capabilities.

## Features

### 🎨 Compassionate Design Principles

- **Anxiety-Reducing UI**: Soft colors, gentle animations, encouraging messages
- **Clear Visual Hierarchy**: Important actions are obvious and accessible
- **Accessible**: WCAG AAA compliant, large touch targets, high contrast
- **Calming Color Palette**: Primary (#667eea) and Secondary (#764ba2)

### 🔒 Firebase Authentication

- Email/password authentication for Community Health Workers
- Offline authentication caching for continued access
- Secure token management
- Automatic session persistence

### ☁️ Cloud Storage Integration

- Voice note recording with location tagging
- Automatic GPS coordinate capture
- Offline-first storage with automatic sync
- Encrypted upload to Firebase Cloud Storage
- Patient ID association

### 📱 Offline-First Architecture

- **Service Worker**: Full offline support after first load
- **Hive Database**: Local encrypted storage
- **Sync Queue**: Automatic upload when connection restored
- **Status Indicators**: Clear online/offline/syncing states

### 🎙️ Voice Recording Features

- Simple one-tap recording
- Location automatically captured
- Optional patient ID tagging
- Additional notes field
- Visual recording feedback
- Sync status per recording

## Technology Stack

- **Framework**: Flutter 3.16.0 (Web)
- **State Management**: Provider
- **Auth**: Firebase Authentication
- **Storage**: Firebase Cloud Storage + Hive (offline)
- **Location**: Geolocator
- **Voice Recording**: Record package
- **UI**: Material Design 3 with custom theming

## Quick Start

### Prerequisites

- Flutter SDK 3.16.0+
- Firebase project with Authentication and Storage enabled
- Node.js (for Firebase CLI)

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/VISENDI56/iLuminara-Core.git
cd iLuminara-Core/frontend_web
```

2. **Install dependencies:**

```bash
flutter pub get
```

3. **Configure Firebase:**

Create a `.env` file in the project root:

```env
FIREBASE_API_KEY=your_api_key
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
```

4. **Run the app:**

```bash
flutter run -d chrome --dart-define=FIREBASE_API_KEY=$FIREBASE_API_KEY \
  --dart-define=FIREBASE_AUTH_DOMAIN=$FIREBASE_AUTH_DOMAIN \
  --dart-define=FIREBASE_PROJECT_ID=$FIREBASE_PROJECT_ID \
  --dart-define=FIREBASE_STORAGE_BUCKET=$FIREBASE_STORAGE_BUCKET \
  --dart-define=FIREBASE_MESSAGING_SENDER_ID=$FIREBASE_MESSAGING_SENDER_ID \
  --dart-define=FIREBASE_APP_ID=$FIREBASE_APP_ID
```

## Project Structure

```
frontend_web/
├── lib/
│   ├── main.dart                          # App entry point
│   ├── models/
│   │   └── voice_note.dart                # Voice note data model
│   ├── screens/
│   │   ├── loading_screen.dart            # Loading state
│   │   ├── login_screen.dart              # Authentication
│   │   └── home_screen.dart               # Main app interface
│   ├── services/
│   │   ├── auth_service.dart              # Firebase Auth + offline
│   │   ├── storage_service.dart           # Cloud Storage + sync
│   │   └── connectivity_service.dart      # Network status
│   └── widgets/
│       ├── voice_recorder_widget.dart     # Recording interface
│       └── voice_notes_list.dart          # Notes display
├── web/
│   ├── index.html                         # Web entry point
│   └── manifest.json                      # PWA manifest
├── Dockerfile                             # Cloud Run deployment
├── nginx.conf                             # Nginx configuration
└── pubspec.yaml                           # Dependencies
```

## Key Components

### AuthService

Handles Firebase Authentication with offline caching:

```dart
final authService = Provider.of<AuthService>(context);

// Sign in
await authService.signInWithEmailPassword(email, password);

// Register
await authService.registerWithEmailPassword(email, password, name);

// Sign out
await authService.signOut();
```

### StorageService

Manages voice notes with offline-first approach:

```dart
final storageService = Provider.of<StorageService>(context);

// Upload voice note
await storageService.uploadVoiceNote(
  audioData: audioData,
  userId: userId,
  latitude: latitude,
  longitude: longitude,
  patientId: patientId,
  metadata: metadata,
);

// Get all notes
final notes = storageService.getAllVoiceNotes();

// Manual sync
await storageService.syncNow();
```

### ConnectivityService

Monitors network status:

```dart
final connectivityService = Provider.of<ConnectivityService>(context);

// Check status
final isOnline = connectivityService.isOnline;
final connectionType = connectivityService.connectionType; // WiFi, Mobile, etc.
```

## Compassionate UI Guidelines

### Error Messages

Instead of technical errors, we show compassionate messages:

- ❌ "Authentication failed: invalid-email"
- ✅ "This email address doesn't look quite right. Please check and try again."

### Loading States

All loading states have:
- Clear progress indicators
- Explanatory text
- Gentle animations
- Timeout handling

### Offline Mode

Users are always informed about:
- Current connection status
- Pending uploads count
- Automatic sync progress
- Offline capabilities

## Deployment

See [Flutter Web Deployment Guide](../docs/FLUTTER_WEB_DEPLOYMENT.md) for:
- Firebase setup
- Cloud Run deployment
- CI/CD configuration
- Monitoring and logs

Quick deploy to Cloud Run:

```bash
gcloud builds submit --config=../cloudbuild.yaml
```

## Testing

```bash
# Run tests
flutter test

# Run with coverage
flutter test --coverage

# Widget tests
flutter test test/widgets/

# Integration tests
flutter test integration_test/
```

## Performance

- **First Paint:** < 2 seconds
- **Time to Interactive:** < 3 seconds
- **Lighthouse Score:** 95+
- **Bundle Size:** ~2MB (gzipped)

Optimizations:
- CanvasKit renderer for consistent rendering
- Code splitting with deferred imports
- Image optimization
- Service Worker caching

## Accessibility

- WCAG AAA compliant
- Screen reader support
- Keyboard navigation
- High contrast mode
- Minimum touch target: 44x44px

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Follow Flutter style guide
2. Write compassionate error messages
3. Test offline functionality
4. Maintain accessibility standards
5. Document new features

## License

VISENDI56 © 2025. All rights reserved.

## Support

- Issues: [GitHub Issues](https://github.com/VISENDI56/iLuminara-Core/issues)
- Docs: `/docs/FLUTTER_WEB_DEPLOYMENT.md`
- Email: support@iluminara.health

---

**Built with ❤️ for Community Health Workers**
