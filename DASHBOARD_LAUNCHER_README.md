# Dashboard Launcher for iLuminara Swahili AI Agents

Quick access to all monitoring dashboards, management consoles, and documentation.

---

## 🚀 Quick Start

### Option 1: Visual HTML Dashboard (Recommended)

Open `dashboard_launcher.html` in any web browser:

```bash
# Linux/Mac
open dashboard_launcher.html

# Windows
start dashboard_launcher.html

# Or just double-click the file
```

**Features:**
- Beautiful visual interface
- One-click access to all dashboards
- Quick action buttons to open multiple dashboards at once
- Works offline, runs locally in your browser

---

### Option 2: Command-Line Launcher Scripts

#### Linux/Mac:
```bash
./open_dashboards.sh
```

#### Windows:
```batch
open_dashboards.bat
```

**Interactive Menu:**
1. Open all Google Cloud Consoles
2. Open all Monitoring Dashboards
3. Open all Documentation
4. Open HTML Dashboard
5. Open Everything
6. Exit

---

## 📊 What Gets Opened

### Google Cloud Consoles
- **Dialogflow CX** - https://dialogflow.cloud.google.com/cx
- **Vertex AI** - https://console.cloud.google.com/vertex-ai
- **Translation API** - https://console.cloud.google.com/apis/library/translate.googleapis.com
- **Cloud Storage** - https://console.cloud.google.com/storage

### Monitoring Dashboards
- **Grafana** - http://localhost:3000 (requires local setup)
- **Prometheus** - http://localhost:9090 (requires local setup)
- **Cloud Monitoring** - https://console.cloud.google.com/monitoring
- **GitHub Actions** - https://github.com/VISENDI56/iLuminara-Core/actions

### Documentation
- Research Report (25 pages)
- Implementation Guide
- Testing Guide
- Deployment Guide (Jetson)
- Dialogflow CX Configuration
- Vertex AI Training Guide
- Golden Thread Integration
- CI/CD Pipeline Documentation

### Additional Resources
- **Kenya MoH CB-IDSR** - https://www.health.go.ke/cbs/
- **KEMRI** - https://www.kemri.go.ke/
- **GitHub Repository** - https://github.com/VISENDI56/iLuminara-Core

---

## 🎯 Use Cases

### For Developers
```bash
# Open all cloud consoles for development
./open_dashboards.sh
# Select option 1
```

### For DevOps/SRE
```bash
# Open all monitoring dashboards
./open_dashboards.sh
# Select option 2
```

### For Documentation Review
```bash
# Open all documentation
./open_dashboards.sh
# Select option 3
```

### For Demo/Presentation
```bash
# Open everything for a complete overview
./open_dashboards.sh
# Select option 5
```

---

## 📋 Prerequisites

### For Web Dashboards
- Google Chrome browser installed
- Active internet connection (for cloud consoles)

### For Local Monitoring (Optional)
If you want to use Grafana and Prometheus:

1. Install Prometheus:
```bash
# Linux
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
cd prometheus-*
./prometheus --config.file=prometheus.yml
```

2. Install Grafana:
```bash
# Linux (Debian/Ubuntu)
sudo apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana_10.2.0_amd64.deb
sudo dpkg -i grafana_10.2.0_amd64.deb
sudo systemctl start grafana-server

# macOS (Homebrew)
brew install grafana
brew services start grafana

# Access at http://localhost:3000
# Default credentials: admin/admin
```

3. Configure metrics endpoint:
```python
# Already included in edge_node/ai_agents/metrics.py
from prometheus_client import start_http_server
start_http_server(8000)
```

---

## 🔒 Security Notes

- Dashboard HTML runs entirely locally in your browser
- No data is sent to external servers
- Shell scripts only open URLs, they don't modify anything
- Google Cloud consoles require authentication
- Local monitoring dashboards (Grafana/Prometheus) should be firewalled in production

---

## 🛠️ Customization

### Add Your Own Dashboard

Edit `dashboard_launcher.html`:

```html
<!-- Add new card in the dashboard-grid -->
<div class="dashboard-card">
    <div class="card-header">
        <div class="card-icon">🎯</div>
        <div class="card-title">Your Dashboard</div>
    </div>
    <p class="card-description">Your description</p>
    <ul class="link-list">
        <li class="link-item">
            <span class="link-label">Your Link</span>
            <a href="https://your-url.com" class="link-button" target="_blank">Open →</a>
        </li>
    </ul>
</div>
```

### Add URL to Shell Scripts

Edit `open_dashboards.sh` or `open_dashboards.bat`:

```bash
# In the appropriate section, add:
open_url "https://your-url.com" "Your Dashboard Name"
```

---

## 📱 Mobile Access

The HTML dashboard is mobile-responsive. Access it on your phone:

1. Start a local web server:
```bash
python -m http.server 8080
```

2. Access from phone: `http://your-computer-ip:8080/dashboard_launcher.html`

---

## 🧪 Testing

Test the HTML dashboard:
```bash
# Open in default browser
open dashboard_launcher.html
```

Test the shell script:
```bash
# Dry run (won't actually open browsers)
bash -n open_dashboards.sh
echo $?  # Should output 0 if no syntax errors
```

---

## 📞 Support

**Issues with dashboards:** Check browser console (F12)  
**Issues with scripts:** Check shell output for errors  
**Missing dashboards:** Ensure services are running (Grafana, Prometheus)  
**Chrome not found:** Update script with correct Chrome path

---

## 📈 What's Included

| Component | Status | Access |
|-----------|--------|--------|
| HTML Dashboard | ✅ Ready | `dashboard_launcher.html` |
| Linux Script | ✅ Ready | `open_dashboards.sh` |
| Windows Script | ✅ Ready | `open_dashboards.bat` |
| Google Cloud Consoles | ✅ Links | Requires Google account |
| Monitoring Dashboards | ⚙️ Setup Required | Grafana/Prometheus |
| Documentation | ✅ Ready | Local markdown files |
| GitHub Integration | ✅ Ready | Public access |

---

## 🎉 Quick Demo

**One Command to Rule Them All:**

```bash
# Linux/Mac
./open_dashboards.sh  # Select option 5 (Everything)

# Windows
open_dashboards.bat  # Select option 5 (Everything)

# Or just open the HTML file
open dashboard_launcher.html
```

This will open:
- 4 Google Cloud consoles
- 4 Monitoring dashboards
- 8+ Documentation pages
- 1 Beautiful HTML dashboard

All in Chrome, ready for your demo! 🚀

---

**Created:** December 19, 2025  
**Status:** ✅ Production Ready  
**Compatibility:** Linux, macOS, Windows
