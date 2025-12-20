#!/bin/bash

# Dashboard Launcher for iLuminara Swahili AI Agents
# Opens all monitoring dashboards and management consoles in Chrome

echo "🚀 iLuminara Swahili AI - Opening Dashboards..."
echo "================================================"

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CHROME="google-chrome"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    CHROME="open -a 'Google Chrome'"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    CHROME="start chrome"
else
    echo "⚠️  Unknown OS. Attempting to use 'google-chrome'..."
    CHROME="google-chrome"
fi

# Function to open URL in Chrome
open_url() {
    local url=$1
    local name=$2
    echo "  📂 Opening: $name"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open -a "Google Chrome" "$url" 2>/dev/null
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        start chrome "$url" 2>/dev/null
    else
        google-chrome "$url" 2>/dev/null &
    fi
    sleep 0.5
}

# Main menu
echo ""
echo "Select which dashboards to open:"
echo "1) All Cloud Consoles (Dialogflow, Vertex AI, Translation, Storage)"
echo "2) All Monitoring (Grafana, Prometheus, Cloud Monitoring, GitHub Actions)"
echo "3) All Documentation"
echo "4) Local Dashboard HTML"
echo "5) Everything"
echo "6) Exit"
echo ""
read -p "Enter choice [1-6]: " choice

case $choice in
    1)
        echo ""
        echo "☁️  Opening Google Cloud Consoles..."
        open_url "https://dialogflow.cloud.google.com/cx" "Dialogflow CX"
        open_url "https://console.cloud.google.com/vertex-ai" "Vertex AI"
        open_url "https://console.cloud.google.com/apis/library/translate.googleapis.com" "Translation API"
        open_url "https://console.cloud.google.com/storage" "Cloud Storage"
        ;;
    2)
        echo ""
        echo "📊 Opening Monitoring Dashboards..."
        open_url "http://localhost:3000" "Grafana"
        open_url "http://localhost:9090" "Prometheus"
        open_url "https://console.cloud.google.com/monitoring" "Cloud Monitoring"
        open_url "https://github.com/VISENDI56/iLuminara-Core/actions" "GitHub Actions"
        ;;
    3)
        echo ""
        echo "📚 Opening Documentation..."
        open_url "file://$(pwd)/docs/google_cloud_ai_swahili_research.md" "Research Report"
        open_url "file://$(pwd)/SWAHILI_AI_IMPLEMENTATION.md" "Implementation Guide"
        open_url "file://$(pwd)/TESTING.md" "Testing Guide"
        open_url "file://$(pwd)/JETSON_DEPLOYMENT.md" "Deployment Guide"
        open_url "file://$(pwd)/DIALOGFLOW_CX_CONFIG.md" "Dialogflow Config"
        ;;
    4)
        echo ""
        echo "🎮 Opening Local Dashboard..."
        open_url "file://$(pwd)/dashboard_launcher.html" "Dashboard Launcher"
        ;;
    5)
        echo ""
        echo "🌐 Opening Everything..."
        
        # Cloud Consoles
        echo ""
        echo "☁️  Google Cloud Consoles..."
        open_url "https://dialogflow.cloud.google.com/cx" "Dialogflow CX"
        open_url "https://console.cloud.google.com/vertex-ai" "Vertex AI"
        open_url "https://console.cloud.google.com/apis/library/translate.googleapis.com" "Translation API"
        open_url "https://console.cloud.google.com/storage" "Cloud Storage"
        
        sleep 2
        
        # Monitoring
        echo ""
        echo "📊 Monitoring Dashboards..."
        open_url "http://localhost:3000" "Grafana"
        open_url "http://localhost:9090" "Prometheus"
        open_url "https://console.cloud.google.com/monitoring" "Cloud Monitoring"
        open_url "https://github.com/VISENDI56/iLuminara-Core/actions" "GitHub Actions"
        
        sleep 2
        
        # Dashboard
        echo ""
        echo "🎮 Local Dashboard..."
        open_url "file://$(pwd)/dashboard_launcher.html" "Dashboard Launcher"
        ;;
    6)
        echo "👋 Exiting..."
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Exiting..."
        exit 1
        ;;
esac

echo ""
echo "✅ Done! All requested dashboards opened in Chrome."
echo ""
echo "💡 Tip: You can also open 'dashboard_launcher.html' directly in your browser"
echo "   for a visual interface with all links."
