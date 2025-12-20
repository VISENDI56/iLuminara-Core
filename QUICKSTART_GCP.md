# iLuminara GCP Prototype - Quickstart Guide

## 🚀 Run the Demo in 30 Seconds

```bash
# 1. Clone the repository (if not already cloned)
git clone https://github.com/VISENDI56/iLuminara-Core.git
cd iLuminara-Core

# 2. Run the demo
./run_demo.sh
```

That's it! The script will:
- Create a virtual environment
- Install all dependencies
- Start the backend API (port 8000)
- Launch the dashboard (port 8501)

## 📊 What You'll See

### Dashboard (http://localhost:8501)

The **Compassionate UI** features three main tabs:

#### 🎤 Tab 1: Sentry Mode
- **Purpose**: Voice-to-JSON intelligence processing
- **Demo**: Click "Process Voice Report" to see simulated field reports
- **Features**:
  - Real-time transcription simulation
  - Entity extraction (symptoms, locations, urgency)
  - Confidence scoring

#### 🗺️ Tab 2: HSTPU Map
- **Purpose**: Hierarchical spatiotemporal outbreak visualization
- **Demo**: Interactive 3D map with outbreak hotspots
- **Features**:
  - Real-time Z-score risk metrics
  - Population at risk calculations
  - Geographic hotspot identification
  - Time series trend analysis

#### ⚖️ Tab 3: Ethical Audit
- **Purpose**: Active Inference decision validation
- **Demo**: Test ethical decisions and see approval/rejection
- **Features**:
  - Humanitarian constraint checking
  - Legal compliance validation (GDPR, HIPAA, etc.)
  - Complete audit trail
  - Decision statistics

### API Endpoints (http://localhost:8000)

Interactive API documentation at: http://localhost:8000/docs

Key endpoints:
- `POST /voice/simulate` - Generate voice report
- `GET /hstpu/map` - Get outbreak map data
- `GET /hstpu/hotspots` - Get active hotspots
- `POST /ethics/evaluate` - Validate ethical decision

## 🧪 Running Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run integration tests
python test_integration.py
```

Expected output: **All tests passed! (9/9)** ✓

## 🔧 Manual Setup (Alternative)

If you prefer manual control:

### 1. Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Start Backend
```bash
uvicorn app.backend.main:app --host 0.0.0.0 --port 8000
```

### 3. Start Frontend (in another terminal)
```bash
source .venv/bin/activate
streamlit run app/frontend/main.py
```

## 🌩️ Deploy to Google Cloud

See [GCP_PROTOTYPE.md](GCP_PROTOTYPE.md) for detailed deployment instructions.

Quick deploy:
```bash
export GCP_PROJECT_ID="your-project-id"
./gcp_scripts/setup.sh
./gcp_scripts/deploy.sh
```

## 📋 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Disk**: 500MB for dependencies
- **OS**: Linux, macOS, or Windows (WSL)

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Backend (8000)
lsof -ti:8000 | xargs kill

# Frontend (8501)
lsof -ti:8501 | xargs kill
```

### Dependencies Failed to Install
```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v
```

### Backend Not Starting
Check logs:
```bash
# Start with debugging
uvicorn app.backend.main:app --host 0.0.0.0 --port 8000 --log-level debug
```

### Frontend Error: "Backend not running"
Ensure backend is running on port 8000:
```bash
curl http://localhost:8000/health
```

## 🎯 Next Steps

1. **Explore the Dashboard**: Navigate through all three tabs
2. **Test API Endpoints**: Use http://localhost:8000/docs
3. **Run Integration Tests**: `python test_integration.py`
4. **Deploy to GCP**: Follow [GCP_PROTOTYPE.md](GCP_PROTOTYPE.md)
5. **Customize**: Modify code in `app/backend/` and `app/frontend/`

## 📚 Additional Resources

- [Full Documentation](GCP_PROTOTYPE.md)
- [Architecture Overview](README.md)
- [Deployment Guide](gcp_scripts/deploy.sh)
- [API Reference](http://localhost:8000/docs)

## 💡 Key Features

✅ **Mock GCP Services**: Works without GCP credentials  
✅ **Dark Mode UI**: Industrial Cyberpunk aesthetic  
✅ **Ethical Validation**: Built-in humanitarian constraints  
✅ **Real-time Visualization**: Interactive maps and charts  
✅ **Complete API**: RESTful endpoints for all services  
✅ **Production Ready**: Deploy to GCP with one command  

## 🔐 Security & Compliance

The system integrates with the existing `governance_kernel` for:
- GDPR, HIPAA, KDPA compliance validation
- Sovereign data guardrails
- Audit trail generation
- Explainability requirements

## 🤝 Support

Having issues? Check:
1. [Troubleshooting section](#troubleshooting) above
2. [GitHub Issues](https://github.com/VISENDI56/iLuminara-Core/issues)
3. [GCP_PROTOTYPE.md](GCP_PROTOTYPE.md) for detailed docs

---

**Status**: ✅ Ready for Demo  
**Mode**: Local with Mock GCP Services  
**Version**: 1.0.0

*"Transform preventable suffering from statistical inevitability to historical anomaly."*
