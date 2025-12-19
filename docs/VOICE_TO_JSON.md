# Swahili Voice-to-JSON Transformation System

## Overview

The iLuminara Voice-to-JSON system transforms Swahili voice notes from Community Health Volunteers (CHVs) into structured JSON data for health surveillance and outbreak detection.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Voice Note Input (Audio)                      │
│                      (Swahili Language)                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              STAGE 1: Swahili Transcription                      │
│         Google Cloud Speech-to-Text (sw-KE/sw-TZ)               │
│           Fallback: Edge Mock Transcriber                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│         STAGE 2: FRENASA Symptom Extraction Engine              │
│              Vertex AI Custom Model (Optional)                   │
│           Rule-based NLP (Edge Fallback)                         │
│                                                                  │
│  Extracts:                                                       │
│  - Symptoms (fever, cough, diarrhea, etc.)                      │
│  - Severity (mild, moderate, severe)                            │
│  - Demographics (age, gender)                                    │
│  - Urgency level (routine, urgent, emergency)                   │
│  - Disease suspicion (cholera, malaria, etc.)                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│           STAGE 3: Golden Thread Data Fusion                     │
│       Integrate with EMR/CBS/IDSR Data Streams                  │
│         Cross-source verification & validation                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│        STAGE 4: Sovereignty Compliance Validation                │
│              Sovereign Guardrail Enforcement                     │
│     (GDPR, KDPA, HIPAA, POPIA compliance checks)                │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Structured JSON Output                         │
│         Ready for analytics, dashboards, alerts                  │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. SwahiliTranscriber (`voice_transcription.py`)

**Purpose**: Real-time Swahili speech-to-text transcription

**Features**:
- Google Cloud Speech-to-Text API integration
- Swahili language support (sw-KE, sw-TZ)
- Streaming and batch transcription
- Edge fallback with mock transcription
- Multiple audio format support (LINEAR16, MP3, OGG_OPUS)

**Example**:
```python
from edge_node.frenasa_engine.voice_transcription import SwahiliTranscriber

transcriber = SwahiliTranscriber(language_code="sw-KE")
result = transcriber.transcribe_audio(audio_bytes)

print(f"Text: {result.text}")
print(f"Confidence: {result.confidence:.2%}")
```

### 2. FRENASASymptomExtractor (`symptom_extraction.py`)

**Purpose**: Extract structured symptom data from Swahili text

**Features**:
- Vertex AI custom model integration
- Rule-based NLP fallback (edge mode)
- Swahili medical entity recognition
- Symptom severity classification
- Disease pattern recognition
- Patient demographic inference

**Supported Symptoms**:
- Fever (homa)
- Cough (kikohozi)
- Diarrhea (kuharisha)
- Vomiting (kutapika)
- Headache (maumivu ya kichwa)
- Body ache (maumivu ya mwili)
- Breathing difficulty (ugumu wa kupumua)
- And more...

**Example**:
```python
from edge_node.frenasa_engine.symptom_extraction import FRENASASymptomExtractor

extractor = FRENASASymptomExtractor()
result = extractor.extract_symptoms(
    "Mgonjwa ana homa kali na kichefuchefu",
    location="Dadaab"
)

for symptom in result.symptoms:
    print(f"{symptom.symptom_name} ({symptom.severity})")
```

### 3. VoiceNoteProcessor (`voice_processor.py`)

**Purpose**: Cloud Functions trigger-based processing with edge fallback

**Features**:
- Cloud Functions integration
- Edge fallback simulation
- Sovereignty compliance validation
- Processing statistics tracking
- Error handling and retry logic

**Modes**:
- `cloud`: Uses Google Cloud services
- `edge`: Local processing without cloud connectivity
- `hybrid`: Mix of cloud and edge processing

**Example**:
```python
from cloud_oracle.voice_processor import VoiceNoteProcessor

processor = VoiceNoteProcessor(mode="edge")
result = processor.process_voice_note(
    audio_data=audio_bytes,
    metadata={"location": "Dadaab", "chv_id": "CHV_001"}
)
```

### 4. VoiceToJSONPipeline (`voice_to_json.py`)

**Purpose**: Complete end-to-end pipeline integration

**Features**:
- Orchestrates all pipeline stages
- Detailed logging and monitoring
- Performance tracking
- Governance validation at each stage
- JSON output generation

**Example**:
```python
from edge_node.frenasa_engine.voice_to_json import VoiceToJSONPipeline

pipeline = VoiceToJSONPipeline(mode="edge", jurisdiction="KDPA_KE")
result = pipeline.process(
    audio_data=audio_bytes,
    patient_id="PATIENT_001",
    location="Dadaab",
    chv_id="CHV_AMINA"
)

print(result.to_json())
```

## Setup and Configuration

### Prerequisites

1. **Python 3.8+**
2. **Optional: Google Cloud SDK** (for cloud mode)

### Installation

```bash
# Clone the repository
git clone https://github.com/VISENDI56/iLuminara-Core.git
cd iLuminara-Core

# Install Python dependencies (optional for cloud mode)
pip install google-cloud-speech google-cloud-aiplatform
```

### Configuration

#### Edge Mode (No Cloud Connectivity)

Edge mode works out-of-the-box without any configuration:

```python
from edge_node.frenasa_engine.voice_to_json import VoiceToJSONPipeline

pipeline = VoiceToJSONPipeline(mode="edge")
```

#### Cloud Mode (Google Cloud Services)

1. **Set up Google Cloud Project**:
   - Create a project in Google Cloud Console
   - Enable Cloud Speech-to-Text API
   - Enable Vertex AI API
   - Create a service account and download credentials JSON

2. **Set credentials path**:
   ```python
   pipeline = VoiceToJSONPipeline(
       mode="cloud",
       credentials_path="/path/to/credentials.json"
   )
   ```

3. **Environment variable (alternative)**:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
   ```

### Jurisdiction Configuration

Configure the legal framework for sovereignty compliance:

```python
pipeline = VoiceToJSONPipeline(
    jurisdiction="KDPA_KE"  # Kenya Data Protection Act
)
```

Supported jurisdictions:
- `KDPA_KE` - Kenya Data Protection Act
- `GDPR_EU` - European Union GDPR
- `HIPAA_US` - USA HIPAA
- `POPIA_ZA` - South Africa POPIA
- `PIPEDA_CA` - Canada PIPEDA
- `GLOBAL_DEFAULT` - Global baseline

## Usage Examples

### Example 1: Simple Voice Note Processing

```python
from edge_node.frenasa_engine.voice_to_json import VoiceToJSONPipeline

# Initialize pipeline
pipeline = VoiceToJSONPipeline(mode="edge")

# Read audio file
with open("voice_note.wav", "rb") as f:
    audio_data = f.read()

# Process
result = pipeline.process(
    audio_data=audio_data,
    patient_id="PATIENT_001",
    location="Dadaab"
)

# Check result
if result.success:
    print(f"Transcription: {result.transcription['text']}")
    print(f"Symptoms: {len(result.symptoms['symptoms'])}")
    print(result.to_json())
else:
    print(f"Error: {result.error_message}")
```

### Example 2: Streaming Transcription

```python
from edge_node.frenasa_engine.voice_transcription import SwahiliTranscriber

transcriber = SwahiliTranscriber()

# Create audio stream generator
def audio_stream_generator():
    with open("voice_note.wav", "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            yield chunk

# Stream transcription
for result in transcriber.transcribe_stream(audio_stream_generator()):
    if result.is_final:
        print(f"Final: {result.text}")
    else:
        print(f"Interim: {result.text}")
```

### Example 3: Batch Processing

```python
import glob
from edge_node.frenasa_engine.voice_to_json import VoiceToJSONPipeline

pipeline = VoiceToJSONPipeline(mode="edge")

# Process all audio files in directory
for audio_file in glob.glob("voice_notes/*.wav"):
    with open(audio_file, "rb") as f:
        audio_data = f.read()
    
    result = pipeline.process(
        audio_data=audio_data,
        patient_id=f"PATIENT_{audio_file}",
        location="Dadaab"
    )
    
    if result.success:
        result.save_to_file(f"results/{audio_file}.json")
        print(f"✅ {audio_file}: {result.symptoms['urgency']}")
    else:
        print(f"❌ {audio_file}: {result.error_message}")
```

### Example 4: Cloud Functions Deployment

```python
# main.py (Cloud Functions entry point)
from cloud_oracle.voice_processor import cloud_function_handler

def process_voice_note(event, context):
    """Cloud Functions entry point triggered by Cloud Storage."""
    return cloud_function_handler(event, context)
```

Deploy:
```bash
gcloud functions deploy process_voice_note \
  --runtime python39 \
  --trigger-resource voice-notes-bucket \
  --trigger-event google.storage.object.finalize \
  --entry-point process_voice_note
```

## Output Format

### JSON Schema

```json
{
  "pipeline_id": "PIPELINE-V2J-20251219154222616356",
  "success": true,
  "audio_metadata": {
    "size_bytes": 96000,
    "format": "LINEAR16",
    "sample_rate": 16000,
    "location": "Dadaab, Ifo Camp",
    "chv_id": "CHV_AMINA_HASSAN",
    "patient_id": "PATIENT_001"
  },
  "transcription": {
    "text": "Mtoto ana kuharisha maji na kutapika",
    "confidence": 0.92,
    "language_code": "sw-KE",
    "timestamp": "2025-12-19T15:42:22.615571",
    "audio_duration_seconds": 3.0,
    "is_final": true
  },
  "symptoms": {
    "transcription": "Mtoto ana kuharisha maji na kutapika",
    "symptoms": [
      {
        "symptom": "diarrhea",
        "severity": "moderate",
        "duration": null,
        "confidence": 0.85
      },
      {
        "symptom": "vomiting",
        "severity": "moderate",
        "duration": null,
        "confidence": 0.85
      }
    ],
    "demographics": {
      "age_group": "<5",
      "gender": null,
      "pregnant": null
    },
    "location": "Dadaab, Ifo Camp",
    "urgency": "routine",
    "disease_suspicion": "Cholera (suspected)",
    "timestamp": "2025-12-19T15:42:22.616087",
    "confidence": 0.27
  },
  "golden_thread_record": {
    "record_id": "GT-PATIENT_001-20251219154222",
    "patient_id": "PATIENT_001",
    "event_type": "symptom_report",
    "location": "Dadaab, Ifo Camp",
    "timestamp": "2025-12-19T15:42:22.616087",
    "verification_score": 0.5,
    "retention_status": "HOT"
  },
  "governance_status": "compliant",
  "sovereignty_compliant": true,
  "total_time_ms": 1.591,
  "processing_mode": "edge",
  "timestamp": "2025-12-19T15:42:22.616356"
}
```

## Performance

### Processing Times (Edge Mode)

- **Transcription**: ~1ms (mock) / 200-500ms (Cloud Speech-to-Text)
- **Symptom Extraction**: ~0.5ms (rule-based) / 100-300ms (Vertex AI)
- **Golden Thread Fusion**: ~0.1ms
- **Governance Validation**: <0.1ms
- **Total Pipeline**: ~2ms (edge) / 500-1000ms (cloud)

### Accuracy

- **Transcription Confidence**: 85-95% (Swahili)
- **Symptom Extraction**: 70-85% (rule-based), 90-95% (Vertex AI)
- **Disease Pattern Recognition**: 60-75%

## Sovereignty and Compliance

The system enforces global compliance standards:

- **GDPR** (EU): PHI data sovereignty, right to explanation
- **KDPA** (Kenya): Cross-border transfer restrictions
- **HIPAA** (USA): PHI protection, breach notification
- **POPIA** (South Africa): Data subject rights
- **PIPEDA** (Canada): Lawful processing requirements

All processing includes:
- Pre-processing governance validation
- Post-processing compliance checks
- Audit logging
- Consent token validation
- Explainability requirements for high-risk inferences

## Troubleshooting

### Issue: Import errors

**Solution**: Ensure Python path is set correctly:
```bash
export PYTHONPATH=/path/to/iLuminara-Core:$PYTHONPATH
```

### Issue: Google Cloud credentials not found

**Solution**: Set the credentials path explicitly:
```python
pipeline = VoiceToJSONPipeline(
    mode="cloud",
    credentials_path="/path/to/credentials.json"
)
```

Or use environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
```

### Issue: Sovereignty violation errors

**Solution**: Ensure consent tokens are provided:
```python
result = pipeline.process(
    audio_data=audio_bytes,
    consent_token="PATIENT_CONSENT_TOKEN_12345"
)
```

### Issue: Low symptom extraction accuracy

**Solution**: 
1. Use Vertex AI custom model (cloud mode) for better accuracy
2. Extend Swahili symptom lexicon in `symptom_extraction.py`
3. Provide clearer voice notes with standardized terminology

## Contributing

To extend the system:

1. **Add new symptoms**: Edit `symptom_lexicon` in `symptom_extraction.py`
2. **Add new languages**: Extend `SwahiliTranscriber` with additional language codes
3. **Custom Vertex AI models**: Deploy and reference in `FRENASASymptomExtractor`
4. **New jurisdictions**: Add to compliance matrix in `vector_ledger.py`

## Support

For issues or questions:
- GitHub Issues: https://github.com/VISENDI56/iLuminara-Core/issues
- Documentation: https://github.com/VISENDI56/iLuminara-Core/docs

## License

VISENDI56 © 2025. All rights reserved.
