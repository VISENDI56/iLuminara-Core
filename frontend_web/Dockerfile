# Multi-stage build for Flutter Web on Cloud Run
# Stage 1: Build Flutter Web app
FROM debian:bullseye-slim AS build

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    unzip \
    xz-utils \
    zip \
    libglu1-mesa \
    && rm -rf /var/lib/apt/lists/*

# Install Flutter SDK
ENV FLUTTER_VERSION=3.16.0
ENV FLUTTER_HOME=/opt/flutter
ENV PATH="$FLUTTER_HOME/bin:$PATH"

RUN git clone https://github.com/flutter/flutter.git -b $FLUTTER_VERSION --depth 1 $FLUTTER_HOME \
    && flutter config --no-analytics \
    && flutter precache --web

# Set working directory
WORKDIR /app

# Copy Flutter project files
COPY frontend_web/pubspec.* ./
RUN flutter pub get

COPY frontend_web/ ./

# Build Flutter Web with optimizations
RUN flutter build web --release --web-renderer canvaskit \
    --dart-define=FIREBASE_API_KEY=$FIREBASE_API_KEY \
    --dart-define=FIREBASE_AUTH_DOMAIN=$FIREBASE_AUTH_DOMAIN \
    --dart-define=FIREBASE_PROJECT_ID=$FIREBASE_PROJECT_ID \
    --dart-define=FIREBASE_STORAGE_BUCKET=$FIREBASE_STORAGE_BUCKET \
    --dart-define=FIREBASE_MESSAGING_SENDER_ID=$FIREBASE_MESSAGING_SENDER_ID \
    --dart-define=FIREBASE_APP_ID=$FIREBASE_APP_ID

# Stage 2: Serve with Nginx
FROM nginx:1.29.3-alpine

# Copy nginx configuration
COPY frontend_web/nginx.conf /etc/nginx/nginx.conf

# Copy built Flutter web app
COPY --from=build /app/build/web /usr/share/nginx/html

# Add healthcheck endpoint
RUN echo '<!DOCTYPE html><html><body>OK</body></html>' > /usr/share/nginx/html/health

# Expose port for Cloud Run
ENV PORT=8080
EXPOSE 8080

# Start nginx
CMD ["sh", "-c", "envsubst < /etc/nginx/nginx.conf > /etc/nginx/nginx.conf && nginx -g 'daemon off;'"]
