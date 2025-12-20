# iLuminara API Documentation

## Overview

The iLuminara API provides three core endpoints for health surveillance and outbreak prediction:

1. **Voice Processing** (`/process-voice`) - Convert voice alerts to structured health data
2. **Outbreak Prediction** (`/predict`) - Predict outbreak risk using Z-score analysis
3. **PubSub Monitoring** - Real-time alert system using Google Cloud Pub/Sub

## Getting Started

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API service
python api_service.py
```

The service will start on `http://localhost:8080` by default.

### Environment Variables

```bash
export API_HOST=0.0.0.0
export API_PORT=8080
export NODE_ID=JOR-47
export JURISDICTION=GLOBAL_DEFAULT
export GOOGLE_CLOUD_PROJECT=your-project-id  # For PubSub
```

## API Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check service health and get metadata.

**Example:**
```bash
curl -X GET http://localhost:8080/health
```

**Response:**
```json
{
  "status": "online",
  "service": "iluminara-api",
  "version": "1.0.0",
  "node_id": "JOR-47",
  "jurisdiction": "GLOBAL_DEFAULT",
  "timestamp": "2025-12-19T20:00:00.000Z",
  "endpoints": {
    "voice_processing": "/process-voice",
    "outbreak_prediction": "/predict",
    "health": "/health"
  }
}
```

### 2. Voice Processing

**Endpoint:** `POST /process-voice`

**Description:** Process voice alerts from Community Health Volunteers (CHVs) and convert them into structured health data.

**Headers:**
- `Content-Type: audio/wav` (or `multipart/form-data`)

**Query Parameters:**
- `language` (optional): Language of the audio (default: "swahili")
- `lat` (optional): Latitude coordinate
- `lng` (optional): Longitude coordinate

**Example:**
```bash
# With audio file
curl -X POST http://localhost:8080/process-voice \
  -H "Content-Type: audio/wav" \
  --data-binary @swahili-symptom.wav

# With location
curl -X POST "http://localhost:8080/process-voice?language=swahili&lat=0.0512&lng=40.3129" \
  -H "Content-Type: audio/wav" \
  --data-binary @swahili-symptom.wav
```

**Response:**
```json
{
  "status": "success",
  "timestamp": "2025-12-19T20:00:00.000Z",
  "processing_time_ms": 4200,
  "transcription": "Patient reporting severe watery diarrhea and vomiting",
  "language_detected": "swahili",
  "symptoms": ["diarrhea", "vomiting", "dehydration"],
  "severity": 9,
  "location": {
    "lat": 0.0512,
    "lng": 40.3129
  },
  "source": "CHV Voice Alert",
  "alert_level": "CRITICAL",
  "recommendations": [
    "IMMEDIATE: Suspected cholera. Start ORS immediately.",
    "Isolate patient to prevent spread",
    "Notify district health officer"
  ]
}
```

### 3. Outbreak Prediction

**Endpoint:** `POST /predict`

**Description:** Predict outbreak risk based on location and symptom data using Z-score analysis.

**Headers:**
- `Content-Type: application/json`

**Request Body:**
```json
{
  "location": {
    "lat": 0.4221,
    "lng": 40.2255
  },
  "symptoms": ["diarrhea", "vomiting"],
  "population": 125000,  // optional
  "historical_data": []  // optional
}
```

**Example:**
```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "location": {"lat": 0.4221, "lng": 40.2255},
    "symptoms": ["diarrhea", "vomiting"]
  }'
```

**Response:**
```json
{
  "status": "success",
  "timestamp": "2025-12-19T20:00:00.000Z",
  "processing_time_ms": 45,
  "location": {
    "lat": 0.4221,
    "lng": 40.2255
  },
  "location_name": "Near Dadaab, Kenya",
  "symptoms_analyzed": ["diarrhea", "vomiting"],
  "disease_likelihood": [
    {
      "disease": "cholera",
      "confidence": 0.85,
      "matching_symptoms": ["diarrhea", "vomiting"],
      "baseline_rate": 0.001
    }
  ],
  "z_score": 3.2,
  "risk_level": "HIGH",
  "bond_status": "ALERT",
  "alert_level": "YELLOW",
  "geographic_risk": {
    "in_known_outbreak_zone": false,
    "distance_to_high_risk_area_km": 15.3,
    "risk_factors": [
      "Limited water/sanitation",
      "Refugee camp proximity"
    ]
  },
  "population_at_risk": 125000,
  "recommendations": [
    "HIGH ALERT: Increase surveillance in affected area",
    "Pre-position medical supplies and personnel",
    "Conduct community health education",
    "Priority: Ensure safe water supply"
  ],
  "confidence_score": 0.78,
  "requires_immediate_action": false
}
```

## PubSub Alert Monitoring

### Setting Up PubSub

1. **Create Topic and Subscription:**
```bash
# Create topic
gcloud pubsub topics create luminara-alerts

# Create subscription
gcloud pubsub subscriptions create luminara-alerts-subscription \
  --topic=luminara-alerts
```

2. **Set Environment Variable:**
```bash
export GOOGLE_CLOUD_PROJECT=your-project-id
```

### Monitoring Alerts

**Using gcloud:**
```bash
# Pull recent alerts
gcloud pubsub subscriptions pull luminara-alerts-subscription --limit=5
```

**Using Python Script:**
```bash
python test_pubsub_alerts.py
```

**Alert Message Format:**
```json
{
  "alert_id": "ALERT-20251219200000123456",
  "alert_type": "outbreak_prediction",
  "severity": "HIGH",
  "timestamp": "2025-12-19T20:00:00.000Z",
  "location": {
    "lat": 0.0512,
    "lng": 40.3129
  },
  "data": {
    "z_score": 3.2,
    "disease_likelihood": [...],
    "bond_status": "ALERT",
    "population_at_risk": 125000,
    "recommendations": [...]
  },
  "metadata": {
    "requires_immediate_action": false,
    "confidence_score": 0.78
  },
  "source": "iluminara-core",
  "version": "1.0.0"
}
```

## Testing

### Quick Test

```bash
# Run comprehensive test suite
./test_api.sh
```

### Individual Tests

```bash
# Generate test audio file
python generate_test_audio.py

# Test voice processing
curl -X POST http://localhost:8080/process-voice \
  -H "Content-Type: audio/wav" \
  --data-binary @swahili-symptom.wav

# Test outbreak prediction
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"location": {"lat": 0.4221, "lng": 40.2255}, "symptoms": ["diarrhea", "vomiting"]}'

# Test PubSub
python test_pubsub_alerts.py
```

## Integration with Golden Thread

The API automatically integrates with iLuminara's Golden Thread data fusion engine:

```python
from edge_node.sync_protocol.golden_thread import GoldenThread
from cloud_oracle.pubsub_alerts import publish_outbreak_alert

# Voice alerts become CBS signals
gt = GoldenThread()
fused = gt.fuse_data_streams(
    cbs_signal={
        'location': voice_result['location'],
        'symptom': voice_result['symptoms'][0],
        'timestamp': voice_result['timestamp']
    },
    patient_id='PATIENT_AUTO_123'
)

# Outbreak predictions trigger alerts
if prediction['z_score'] >= 2.576:
    publish_outbreak_alert(prediction)
```

## Sovereignty & Compliance

All API endpoints enforce sovereignty constraints through the `SovereignGuardrail`:

- **Voice processing:** Data processed at edge (local node)
- **Outbreak prediction:** Analytics comply with GDPR, KDPA, HIPAA
- **Data transfers:** PHI never leaves sovereign territory

## Error Handling

### Error Response Format
```json
{
  "status": "error",
  "error": "error_code",
  "message": "Human-readable error message"
}
```

### Common Errors

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `no_audio_data` | 400 | No audio data in request |
| `missing_location` | 400 | Location required but not provided |
| `missing_symptoms` | 400 | Symptoms list required |
| `invalid_content_type` | 400 | Wrong Content-Type header |
| `sovereignty_violation` | 403 | Action violates compliance rules |
| `processing_failed` | 500 | Internal processing error |

## Performance

- **Voice Processing:** ~4.2s average (simulates real-time transcription)
- **Outbreak Prediction:** ~45ms average
- **PubSub Latency:** <100ms for alert delivery

## Deployment

### Cloud Run (Google Cloud)

```bash
# Build and deploy
gcloud run deploy frenasa-engine \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Get URL
gcloud run services describe frenasa-engine --format='value(status.url)'
```

### Docker

```bash
# Build
docker build -t iluminara-api:latest .

# Run
docker run -p 8080:8080 \
  -e GOOGLE_CLOUD_PROJECT=your-project-id \
  iluminara-api:latest
```

### NVIDIA Jetson Orin (Edge)

```bash
# Use docker-compose
docker-compose up -d
```

## Support

For issues or questions:
- GitHub Issues: https://github.com/VISENDI56/iLuminara-Core/issues
- Documentation: https://github.com/VISENDI56/iLuminara-Core/blob/main/README.md
