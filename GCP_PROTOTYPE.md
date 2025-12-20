# iLuminara GCP Prototype

This directory contains the Google Cloud Platform prototype of iLuminara - a complete, production-ready implementation with FastAPI backend, Streamlit dashboard, and GCP service integration.

## 🏗️ Architecture

```
iLuminara-Core/
├── app/
│   ├── backend/              # FastAPI Microservices
│   │   ├── main.py          # API entry point
│   │   ├── voice_processor.py   # Speech-to-Text integration
│   │   ├── hstpu_forecast.py    # BigQuery/Vertex AI forecasting
│   │   ├── ethical_engine.py    # Humanitarian protocols
│   │   └── mock_gcp.py          # Mock GCP services for local dev
│   └── frontend/            # Streamlit Dashboard
│       └── main.py          # Compassionate UI
├── gcp_scripts/            # GCP Deployment
│   ├── deploy.sh          # Full deployment script
│   └── setup.sh           # Initial GCP setup
└── requirements.txt       # Python dependencies
```

## 🚀 Quick Start (Local Demo)

Run the complete stack locally with mock GCP services:

```bash
# One-command launch
./run_demo.sh
```

This will:
1. Create/activate virtual environment
2. Install dependencies
3. Start FastAPI backend on `localhost:8000`
4. Launch Streamlit dashboard on `localhost:8501`

**Access Points:**
- 📊 Dashboard: http://localhost:8501
- 🔌 API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

## 🎯 Dashboard Features

### Tab 1: Sentry Mode 🎤
Voice-to-JSON processing simulation
- Upload or simulate voice reports
- Real-time transcription
- Entity extraction (symptoms, locations, case counts)
- Urgency assessment

### Tab 2: HSTPU Map 🗺️
Hierarchical Spatiotemporal outbreak visualization
- Interactive 3D map with PyDeck
- Real-time hotspot identification
- Z-score risk metrics
- Population at risk analysis

### Tab 3: Ethical Audit ⚖️
Active Inference decision logging
- Test ethical decisions
- Humanitarian constraint validation
- Legal compliance checking (GDPR, HIPAA, etc.)
- Complete audit trail

## 🌩️ Deploy to Google Cloud

### Prerequisites
- Google Cloud account with billing enabled
- `gcloud` CLI installed and authenticated
- Project with necessary APIs enabled

### Setup

1. **Configure GCP Project:**
```bash
export GCP_PROJECT_ID="your-project-id"
export GCP_REGION="us-central1"  # Optional, defaults to us-central1

# Initial setup (authenticate and configure)
./gcp_scripts/setup.sh
```

2. **Deploy to Cloud Run:**
```bash
# Deploy both backend and frontend
./gcp_scripts/deploy.sh
```

The script will:
- Enable required GCP APIs (Cloud Run, Vertex AI, BigQuery, Speech-to-Text)
- Build and deploy backend service
- Build and deploy frontend service
- Create BigQuery dataset
- Output deployment URLs

### GCP Services Used

| Service | Purpose |
|---------|---------|
| **Cloud Run** | Serverless container deployment |
| **Vertex AI** | ML outbreak forecasting |
| **BigQuery** | Health data analytics |
| **Speech-to-Text** | Voice report transcription |
| **Cloud Build** | Automated container builds |

## 🔧 Development

### Backend API Development

Start backend only:
```bash
source .venv/bin/activate
uvicorn app.backend.main:app --reload --port 8000
```

API Endpoints:
- `GET /health` - Health check
- `POST /voice/process` - Process audio file
- `POST /voice/simulate` - Simulate voice report
- `GET /hstpu/map` - Get outbreak map data
- `POST /hstpu/forecast` - Generate forecast
- `GET /hstpu/hotspots` - Get active hotspots
- `POST /ethics/evaluate` - Evaluate action
- `GET /ethics/log` - Get decision log

### Frontend Development

Start frontend only:
```bash
source .venv/bin/activate
streamlit run app/frontend/main.py
```

### Mock vs Real GCP

**Local Development (Mock):**
- Backend uses `MockGCP` class
- No GCP credentials required
- Instant startup
- Synthetic data generation

**Production (Real GCP):**
- Set `use_mock=False` in service initializers
- Configure GCP credentials
- Connect to real BigQuery/Vertex AI endpoints
- Set environment variables:
  ```bash
  export USE_MOCK_GCP=false
  export GCP_PROJECT_ID=your-project
  ```

## 📦 Dependencies

Key packages:
- `fastapi` - Modern async API framework
- `streamlit` - Interactive dashboard
- `pydeck` - 3D geospatial visualization
- `google-cloud-aiplatform` - Vertex AI integration
- `google-cloud-bigquery` - BigQuery client
- `google-cloud-speech` - Speech-to-Text

See `requirements.txt` for complete list.

## 🛡️ Compliance Integration

The ethical engine integrates with the existing `governance_kernel`:
- Validates all actions against 14 legal frameworks
- Applies humanitarian constraints
- Generates audit logs for SOC 2 compliance
- Implements "Right to Explanation" (GDPR Art. 22)

## 🧪 Testing

Run backend tests:
```bash
pytest app/backend/tests/ -v
```

Test specific endpoints:
```bash
# Health check
curl http://localhost:8000/health

# Simulate voice report
curl -X POST http://localhost:8000/voice/simulate

# Get HSTPU map
curl http://localhost:8000/hstpu/map
```

## 📊 Monitoring

When deployed to GCP, use:
- **Cloud Logging** for application logs
- **Cloud Monitoring** for metrics and alerts
- **Cloud Trace** for performance profiling

## 🔐 Security

- All APIs support CORS for frontend integration
- Authentication can be added via Cloud IAM
- Secrets managed through Secret Manager
- Network policies via VPC

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Cloud Run](https://cloud.google.com/run/docs)
- [Vertex AI](https://cloud.google.com/vertex-ai/docs)

## 🤝 Contributing

When adding features:
1. Update mock services in `mock_gcp.py`
2. Add corresponding API endpoints in `backend/main.py`
3. Update dashboard UI in `frontend/main.py`
4. Update this README

## 📄 License

VISENDI56 © 2025. All rights reserved.

---

**Status:** ✅ Production-Ready for GCP Deployment  
**Mode:** Local Demo with Mock GCP Services  
**Version:** 1.0.0
