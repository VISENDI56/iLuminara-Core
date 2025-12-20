# NVIDIA Jetson Deployment Guide for Swahili AI Agents

**Target Hardware:** NVIDIA Jetson Orin Nano / Jetson AGX Orin  
**OS:** JetPack 5.1+ (Ubuntu 20.04 ARM64)  
**Status:** Production-Ready  
**Date:** December 19, 2025

---

## 🎯 Overview

This guide provides step-by-step instructions for deploying iLuminara Swahili AI agents to NVIDIA Jetson edge devices for offline-first medical AI in East African healthcare facilities.

---

## 📋 Prerequisites

### Hardware Requirements
- **NVIDIA Jetson Orin Nano** (8GB RAM minimum) OR
- **NVIDIA Jetson AGX Orin** (32GB RAM recommended for production)
- **Storage:** 128GB+ NVMe SSD
- **Network:** WiFi/Ethernet (optional, for cloud sync)
- **Power:** 15W-60W depending on model

### Software Requirements
- JetPack 5.1 or later (includes Ubuntu 20.04, CUDA, cuDNN)
- Python 3.8+
- Docker 20.10+ (optional, for containerized deployment)

---

## 🚀 Deployment Steps

### Step 1: Prepare Jetson Device

```bash
# SSH into Jetson device
ssh jetson@<jetson-ip-address>

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
sudo apt install -y python3-pip python3-venv git

# Create application directory
sudo mkdir -p /opt/iluminara
sudo chown $USER:$USER /opt/iluminara
cd /opt/iluminara
```

### Step 2: Clone iLuminara Repository

```bash
# Clone repository
git clone https://github.com/VISENDI56/iLuminara-Core.git
cd iLuminara-Core

# Checkout Swahili AI branch (or main if merged)
git checkout copilot/find-ai-agents-for-swahili
```

### Step 3: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install core dependencies (offline-capable)
pip install --no-cache-dir -r requirements-swahili-ai.txt

# Note: Google Cloud SDKs are optional
# Agents will work in offline mode without them
```

### Step 4: Configure Environment

```bash
# Copy example environment file
cp .env.swahili-ai.example .env.swahili-ai

# Edit configuration
nano .env.swahili-ai
```

**Minimal Configuration (Offline Mode):**
```bash
# .env.swahili-ai
JURISDICTION=KDPA_KE
ALLOW_CLOUD_SYNC=false
ENABLE_TRANSLATION=true
ENABLE_ENTITY_EXTRACTION=true
ENABLE_TRIAGE_AGENT=true
ENABLE_MEDICAL_QA=true
ENABLE_CLOUD_SYNC=false
```

**Full Configuration (Hybrid Mode with Cloud):**
```bash
# .env.swahili-ai
GOOGLE_CLOUD_PROJECT=iluminara-kenya
GOOGLE_CLOUD_REGION=africa-south1
GOOGLE_APPLICATION_CREDENTIALS=/opt/iluminara/secrets/gcp-key.json
DIALOGFLOW_AGENT_ID=<your-agent-id>
VERTEX_AI_ENDPOINT=<your-endpoint-id>
GEMINI_API_KEY=<your-api-key>
GCS_SYNC_BUCKET=iluminara-kenya-sync
JURISDICTION=KDPA_KE
ALLOW_CLOUD_SYNC=true
```

### Step 5: Run Tests

```bash
# Verify installation
python run_tests.py

# Expected output:
# ✅ ALL TESTS PASSED
# 6/6 test suites successful
```

### Step 6: Start Services

#### Option A: Direct Python Execution

```bash
# Start demo
python swahili_ai_demo.py

# Or use agents programmatically
python -c "
from edge_node.ai_agents import SwahiliMedicalTranslator
translator = SwahiliMedicalTranslator('iluminara-kenya', 'africa-south1')
print(translator.translate('homa'))  # Should print: fever
"
```

#### Option B: Systemd Service (Recommended for Production)

Create service file:
```bash
sudo nano /etc/systemd/system/iluminara-swahili-ai.service
```

```ini
[Unit]
Description=iLuminara Swahili AI Agents
After=network.target

[Service]
Type=simple
User=jetson
WorkingDirectory=/opt/iluminara/iLuminara-Core
Environment="PATH=/opt/iluminara/iLuminara-Core/.venv/bin"
EnvironmentFile=/opt/iluminara/iLuminara-Core/.env.swahili-ai
ExecStart=/opt/iluminara/iLuminara-Core/.venv/bin/python swahili_ai_demo.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable iluminara-swahili-ai
sudo systemctl start iluminara-swahili-ai
sudo systemctl status iluminara-swahili-ai
```

---

## 🐳 Docker Deployment (Alternative)

### Create Dockerfile for ARM64

```bash
nano Dockerfile.jetson
```

```dockerfile
# Dockerfile.jetson
FROM nvcr.io/nvidia/l4t-base:r35.2.1

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy application files
COPY . /app/

# Install Python dependencies
RUN python3 -m pip install --no-cache-dir -r requirements-swahili-ai.txt

# Set environment
ENV PYTHONUNBUFFERED=1
ENV JURISDICTION=KDPA_KE
ENV ALLOW_CLOUD_SYNC=false

# Run tests on build
RUN python3 run_tests.py

# Default command
CMD ["python3", "swahili_ai_demo.py"]
```

### Build and Run

```bash
# Build image
docker build -f Dockerfile.jetson -t iluminara-swahili-ai:jetson .

# Run container
docker run -d \
  --name iluminara-swahili-ai \
  --restart unless-stopped \
  -v /opt/iluminara/data:/app/data \
  -v /opt/iluminara/secrets:/app/secrets:ro \
  iluminara-swahili-ai:jetson
```

---

## 📊 Performance Optimization

### Enable CUDA Acceleration (Future Enhancement)

```python
# For future Vertex AI model deployment
import torch
print(f"CUDA Available: {torch.cuda.is_available()}")
print(f"CUDA Device: {torch.cuda.get_device_name(0)}")
```

### Resource Monitoring

```bash
# Monitor Jetson resources
sudo tegrastats

# Monitor application
htop

# Check service logs
sudo journalctl -u iluminara-swahili-ai -f
```

---

## 🔒 Security Configuration

### Firewall Setup

```bash
# Enable firewall
sudo ufw enable

# Allow SSH (for remote management)
sudo ufw allow 22/tcp

# Deny all other incoming by default
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

### Secrets Management

```bash
# Create secrets directory
sudo mkdir -p /opt/iluminara/secrets
sudo chmod 700 /opt/iluminara/secrets

# Store Google Cloud credentials (if using cloud features)
sudo nano /opt/iluminara/secrets/gcp-key.json
sudo chmod 600 /opt/iluminara/secrets/gcp-key.json
```

---

## 🧪 Validation

### Smoke Tests

```bash
# Test translation (offline)
python -c "
from edge_node.ai_agents import SwahiliMedicalTranslator
t = SwahiliMedicalTranslator('test', 'africa-south1')
assert t.translate('homa', use_cache=True) == 'fever'
print('✅ Translation working')
"

# Test entity extraction
python -c "
from edge_node.ai_agents import SwahiliMedicalEntityExtractor
e = SwahiliMedicalEntityExtractor()
entities = e.extract_entities('Nina homa na malaria')
assert 'homa' in entities['symptoms']
assert 'malaria' in entities['diseases']
print('✅ Entity extraction working')
"

# Test triage
python -c "
from edge_node.ai_agents import SwahiliTriageAgent
t = SwahiliTriageAgent('test')
result = t.triage_symptom('kukosa pumzi', log_to_cbs=False)
assert 'DHARURA' in result or 'EMERGENCY' in result
print('✅ Triage working')
"
```

---

## 📈 Monitoring & Maintenance

### Log Files

```bash
# Application logs
tail -f /var/log/syslog | grep iluminara

# Service logs
sudo journalctl -u iluminara-swahili-ai -f
```

### Health Checks

```bash
# Create health check script
cat > /opt/iluminara/health_check.sh << 'EOF'
#!/bin/bash
source /opt/iluminara/iLuminara-Core/.venv/bin/activate
cd /opt/iluminara/iLuminara-Core
python run_tests.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Health check passed"
    exit 0
else
    echo "❌ Health check failed"
    exit 1
fi
EOF

chmod +x /opt/iluminara/health_check.sh

# Schedule health checks (every hour)
(crontab -l 2>/dev/null; echo "0 * * * * /opt/iluminara/health_check.sh") | crontab -
```

---

## 🔄 Updates & Rollbacks

### Update Application

```bash
cd /opt/iluminara/iLuminara-Core
git pull origin main
source .venv/bin/activate
pip install -r requirements-swahili-ai.txt
python run_tests.py
sudo systemctl restart iluminara-swahili-ai
```

### Rollback

```bash
cd /opt/iluminara/iLuminara-Core
git log --oneline -5  # Find previous commit
git checkout <commit-hash>
sudo systemctl restart iluminara-swahili-ai
```

---

## 🆘 Troubleshooting

### Issue: Service Won't Start

```bash
# Check logs
sudo journalctl -u iluminara-swahili-ai -n 50

# Check permissions
ls -la /opt/iluminara/iLuminara-Core

# Verify Python environment
source /opt/iluminara/iLuminara-Core/.venv/bin/activate
python --version
python -c "import edge_node.ai_agents"
```

### Issue: Out of Memory

```bash
# Check memory usage
free -h

# Reduce concurrent processes
# Edit service file to limit memory
sudo nano /etc/systemd/system/iluminara-swahili-ai.service

# Add under [Service]:
MemoryLimit=4G
```

### Issue: Offline Mode Not Working

```bash
# Verify offline cache is populated
python -c "
from edge_node.ai_agents import SwahiliMedicalTranslator
t = SwahiliMedicalTranslator('test', 'africa-south1')
print(len(t.translation_cache), 'terms in cache')
"

# Should show 20+ terms
```

---

## 📊 Production Checklist

- [ ] Jetson device updated to latest JetPack
- [ ] Python environment created and activated
- [ ] Dependencies installed
- [ ] Environment variables configured
- [ ] Tests passing (100%)
- [ ] Systemd service configured and enabled
- [ ] Firewall configured
- [ ] Secrets properly secured (600 permissions)
- [ ] Health checks scheduled
- [ ] Logs rotation configured
- [ ] Monitoring alerts set up
- [ ] Backup strategy in place
- [ ] Documentation reviewed by team
- [ ] Pilot testing with 10 patients completed

---

## 📞 Support

**Hardware Issues:** NVIDIA Jetson Forums  
**Software Issues:** GitHub Issues (VISENDI56/iLuminara-Core)  
**Deployment Support:** deployment@iluminara.org

---

**Deployment Guide Version:** 1.0  
**Last Updated:** December 19, 2025  
**Tested On:** Jetson Orin Nano 8GB, JetPack 5.1.1  
**Status:** ✅ Production-Ready
