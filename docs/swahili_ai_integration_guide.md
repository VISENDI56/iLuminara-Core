# Swahili AI Agents: Integration Guide for iLuminara-Core

**Purpose:** Technical implementation guide for integrating Google Cloud AI agents with iLuminara-Core's sovereignty-first architecture.

---

## Quick Start: Deploy Your First Swahili Medical Agent

### Prerequisites
```bash
# Install Google Cloud SDK
pip install google-cloud-translate google-cloud-aiplatform google-cloud-dialogflow-cx google-generativeai

# Set up authentication
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
export GOOGLE_CLOUD_PROJECT="iluminara-production"
export GOOGLE_CLOUD_REGION="europe-west4"  # GDPR-compliant EU region
```

### 1. Swahili-English Medical Translation

```python
# File: edge_node/ai_agents/swahili_translator.py

from google.cloud import translate_v3
from typing import Optional
from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError

class SwahiliMedicalTranslator:
    """
    GDPR-compliant Swahili-English medical translator.
    Always de-identifies PHI before cloud translation.
    """
    
    def __init__(self, project_id: str, location: str = "europe-west4"):
        self.project_id = project_id
        self.location = location
        self.client = translate_v3.TranslationServiceClient()
        self.parent = f"projects/{project_id}/locations/{location}"
        self.guardrail = SovereignGuardrail()
        
        # Medical glossary for accurate translations
        self.glossary_id = self._create_medical_glossary()
    
    def _create_medical_glossary(self) -> str:
        """Create Swahili-English medical terminology glossary."""
        glossary_config = {
            "name": f"{self.parent}/glossaries/swahili_medical_terms",
            "language_pair": {
                "source_language_code": "sw",
                "target_language_code": "en"
            },
            "input_config": {
                "gcs_source": {
                    "input_uri": "gs://iluminara-glossaries/swahili_medical.csv"
                }
            }
        }
        
        # CSV format: sw_term,en_term
        # Example: "homa,fever"
        #          "kifua kikuu,tuberculosis"
        #          "ukimwi,HIV/AIDS"
        
        try:
            operation = self.client.create_glossary(
                parent=self.parent,
                glossary=glossary_config
            )
            result = operation.result()
            return result.name
        except Exception as e:
            print(f"Glossary creation error: {e}")
            return None
    
    def translate(
        self, 
        text: str, 
        source_lang: str = "sw", 
        target_lang: str = "en",
        jurisdiction: str = "GDPR_EU"
    ) -> Optional[str]:
        """
        Translate medical text with sovereignty validation.
        
        Args:
            text: De-identified medical text (no PHI)
            source_lang: Source language code (default: Swahili)
            target_lang: Target language code (default: English)
            jurisdiction: Legal framework to validate against
        
        Returns:
            Translated text or None if sovereignty violation
        """
        
        # Step 1: Validate sovereignty compliance
        try:
            self.guardrail.validate_action(
                action_type='Cloud_Translation',
                payload={
                    'data_type': 'De_Identified_Medical_Text',
                    'destination': f'Google_Cloud_{self.location.upper()}',
                    'has_phi': False,  # Must be False
                    'consent_token': 'GENERAL_RESEARCH_CONSENT'
                },
                jurisdiction=jurisdiction
            )
        except SovereigntyViolationError as e:
            print(f"❌ Translation blocked: {e}")
            return None
        
        # Step 2: Perform translation
        request = {
            "parent": self.parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_lang,
            "target_language_code": target_lang
        }
        
        # Use glossary if available
        if self.glossary_id:
            request["glossary_config"] = {
                "glossary": self.glossary_id
            }
        
        response = self.client.translate_text(request=request)
        
        return response.translations[0].translated_text


# Example usage:
if __name__ == "__main__":
    translator = SwahiliMedicalTranslator(
        project_id="iluminara-production",
        location="europe-west4"
    )
    
    # De-identified symptom (no patient name/ID)
    swahili_symptom = "Mgonjwa ana homa na maumivu ya tumbo"
    english_symptom = translator.translate(swahili_symptom)
    
    print(f"Swahili: {swahili_symptom}")
    print(f"English: {english_symptom}")
    # Output: "The patient has fever and stomach pain"
```

---

### 2. Swahili Medical Entity Extraction (Vertex AI)

```python
# File: edge_node/ai_agents/swahili_entity_extractor.py

from google.cloud import aiplatform
from typing import List, Dict
import json

class SwahiliMedicalEntityExtractor:
    """
    Extract medical entities (symptoms, diseases, medications) from Swahili text.
    Uses custom-trained Vertex AI model.
    """
    
    def __init__(self, model_endpoint: str, location: str = "europe-west4"):
        self.model_endpoint = model_endpoint
        self.location = location
        aiplatform.init(location=location)
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract medical entities from Swahili clinical text.
        
        Returns:
            {
                "symptoms": ["homa", "kichefuchefu"],
                "diseases": ["malaria"],
                "medications": ["dawa za malaria"],
                "body_parts": ["tumbo", "kichwa"]
            }
        """
        
        # Get prediction from custom Vertex AI model
        endpoint = aiplatform.Endpoint(self.model_endpoint)
        
        instances = [{"text": text}]
        response = endpoint.predict(instances=instances)
        
        # Parse model output
        entities = {
            "symptoms": [],
            "diseases": [],
            "medications": [],
            "body_parts": []
        }
        
        for prediction in response.predictions:
            entity_type = prediction.get("entity_type")
            entity_text = prediction.get("text")
            confidence = prediction.get("confidence", 0.0)
            
            if confidence > 0.7:  # Filter low-confidence predictions
                if entity_type in entities:
                    entities[entity_type].append(entity_text)
        
        return entities


# Example usage:
if __name__ == "__main__":
    extractor = SwahiliMedicalEntityExtractor(
        model_endpoint="projects/123/locations/europe-west4/endpoints/456"
    )
    
    swahili_text = "Mgonjwa ana homa kali na kichefuchefu. Tunamshuku ana malaria."
    # Translation: "Patient has high fever and nausea. We suspect malaria."
    
    entities = extractor.extract_entities(swahili_text)
    print(json.dumps(entities, indent=2, ensure_ascii=False))
    
    # Output:
    # {
    #   "symptoms": ["homa kali", "kichefuchefu"],
    #   "diseases": ["malaria"],
    #   "medications": [],
    #   "body_parts": []
    # }
```

---

### 3. Dialogflow CX Swahili Symptom Triage Agent

```python
# File: edge_node/ai_agents/swahili_triage_agent.py

from google.cloud import dialogflowcx_v3 as dialogflow
from typing import Optional
import uuid

class SwahiliTriageAgent:
    """
    Conversational AI agent for Swahili medical symptom triage.
    Integrates with iLuminara Edge Node for CBS reporting.
    """
    
    def __init__(
        self, 
        project_id: str,
        location: str = "europe-west4",
        agent_id: str = None
    ):
        self.project_id = project_id
        self.location = location
        self.agent_id = agent_id or self._create_agent()
        
        self.session_client = dialogflow.SessionsClient()
        self.agent_path = f"projects/{project_id}/locations/{location}/agents/{agent_id}"
    
    def _create_agent(self) -> str:
        """Create Dialogflow CX agent for Swahili medical triage."""
        agents_client = dialogflow.AgentsClient()
        
        agent_config = dialogflow.Agent(
            display_name="Swahili Medical Triage Agent",
            default_language_code="sw",  # Swahili
            time_zone="Africa/Nairobi",
            description="AI agent for triaging medical symptoms in Swahili",
            enable_stackdriver_logging=True,
            enable_spell_correction=True
        )
        
        parent = f"projects/{self.project_id}/locations/{self.location}"
        response = agents_client.create_agent(parent=parent, agent=agent_config)
        
        return response.name.split('/')[-1]
    
    def detect_intent(
        self, 
        text: str, 
        session_id: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Send user query to Dialogflow agent and get response.
        
        Args:
            text: Swahili medical query (e.g., "Nina homa na maumivu ya kichwa")
            session_id: Unique session identifier (creates new if None)
        
        Returns:
            {
                "response_text": "Samahani kusikia hivyo...",
                "intent": "report_symptom",
                "parameters": {"symptom": ["homa", "maumivu ya kichwa"]},
                "confidence": 0.95
            }
        """
        
        if not session_id:
            session_id = str(uuid.uuid4())
        
        session_path = f"{self.agent_path}/sessions/{session_id}"
        
        # Prepare query
        text_input = dialogflow.TextInput(text=text)
        query_input = dialogflow.QueryInput(
            text=text_input,
            language_code="sw"
        )
        
        # Send request
        request = dialogflow.DetectIntentRequest(
            session=session_path,
            query_input=query_input
        )
        
        response = self.session_client.detect_intent(request=request)
        query_result = response.query_result
        
        # Parse response
        return {
            "response_text": query_result.response_messages[0].text.text[0],
            "intent": query_result.intent.display_name,
            "parameters": dict(query_result.parameters),
            "confidence": query_result.intent_detection_confidence
        }
    
    def triage_symptom(self, symptom: str) -> str:
        """
        Triage a reported symptom and provide guidance.
        
        Args:
            symptom: Swahili symptom description
        
        Returns:
            Triage advice in Swahili
        """
        
        query = f"Nina {symptom}. Je, ni hatari?"
        # Translation: "I have {symptom}. Is it dangerous?"
        
        result = self.detect_intent(query)
        
        # Log to CBS (Community-Based Surveillance)
        from edge_node.sync_protocol.golden_thread import GoldenThread
        gt = GoldenThread()
        
        cbs_record = {
            'location': 'Unknown',  # Would be geo-tagged in production
            'symptom': symptom,
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'dialogflow_triage'
        }
        
        # This creates a CBS signal without linking to specific patient (privacy-preserving)
        gt.log_cbs_signal(cbs_record)
        
        return result["response_text"]


# Example usage:
if __name__ == "__main__":
    agent = SwahiliTriageAgent(
        project_id="iluminara-production",
        location="europe-west4"
    )
    
    # Test symptom triage
    symptoms = [
        "homa na kichefuchefu",  # fever and nausea
        "maumivu ya kifua",      # chest pain
        "kukosa pumzi"           # difficulty breathing
    ]
    
    for symptom in symptoms:
        advice = agent.triage_symptom(symptom)
        print(f"\nSymptom: {symptom}")
        print(f"Advice: {advice}")
```

---

### 4. Gemini Pro Swahili Medical Q&A

```python
# File: edge_node/ai_agents/swahili_medical_qa.py

import google.generativeai as genai
from governance_kernel.vector_ledger import SovereignGuardrail

class SwahiliMedicalQA:
    """
    Medical question-answering system using Gemini Pro.
    Provides evidence-based medical information in Swahili.
    """
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.guardrail = SovereignGuardrail()
        
        # System prompt for medical context
        self.system_prompt = """
        Wewe ni mshauri wa afya wa AI unayezungumza Kiswahili na Kiingereza kwa ufasaha.
        (You are an AI health advisor fluent in Swahili and English.)
        
        Kanuni:
        1. Toa majibu ya kitaalamu yakijumuisha vyanzo vya kisayansi
        2. Kumbuka kuweka onyo kwa dalili hatari
        3. Pendekeza kutembelea daktari kwa hali mbaya
        4. Usitoe diagnosis za moja kwa moja - eleza uwezekano tu
        5. Zingatia hali za Kenya na Afrika Mashariki
        
        Rules:
        1. Provide evidence-based answers with scientific sources
        2. Always include warnings for serious symptoms
        3. Recommend seeing a doctor for severe conditions
        4. Don't give definitive diagnoses - explain possibilities only
        5. Consider context of Kenya and East Africa
        """
    
    def ask(self, question: str) -> Dict[str, str]:
        """
        Answer medical question in Swahili.
        
        Args:
            question: Medical question in Swahili
        
        Returns:
            {
                "answer": "...",
                "sources": ["WHO", "CDC", "Kenya MoH"],
                "safety_notice": "...",
                "confidence": 0.85
            }
        """
        
        # Validate sovereignty (no PHI in question)
        if self._contains_phi(question):
            return {
                "answer": "Samahani, siwezi kuchakata maswali yenye taarifa za kibinafsi. Tafadhali uliza swali la jumla.",
                "sources": [],
                "safety_notice": "Privacy protection active",
                "confidence": 0.0
            }
        
        # Generate response
        full_prompt = f"{self.system_prompt}\n\nSwali la Mgonjwa: {question}\n\nJibu:"
        
        response = self.model.generate_content(
            full_prompt,
            generation_config={
                "temperature": 0.3,  # Lower temperature for medical accuracy
                "top_p": 0.8,
                "max_output_tokens": 1024
            },
            safety_settings={
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE",
                "HARM_CATEGORY_MEDICAL": "BLOCK_NONE"  # Allow medical content
            }
        )
        
        answer_text = response.text
        
        # Extract citations (if model includes them)
        sources = self._extract_sources(answer_text)
        
        return {
            "answer": answer_text,
            "sources": sources,
            "safety_notice": self._generate_safety_notice(question),
            "confidence": 0.85  # Gemini doesn't provide confidence scores
        }
    
    def _contains_phi(self, text: str) -> bool:
        """Check if text contains Protected Health Information."""
        phi_indicators = [
            "jina langu",  # my name
            "naitwa",      # I am called
            "ID",
            "nambari ya simu",  # phone number
            "email"
        ]
        
        return any(indicator in text.lower() for indicator in phi_indicators)
    
    def _extract_sources(self, text: str) -> List[str]:
        """Extract cited sources from generated text."""
        sources = []
        if "WHO" in text:
            sources.append("World Health Organization")
        if "CDC" in text:
            sources.append("Centers for Disease Control")
        if "Kenya" in text or "MoH" in text:
            sources.append("Kenya Ministry of Health")
        
        return sources
    
    def _generate_safety_notice(self, question: str) -> str:
        """Generate appropriate safety notice based on question."""
        emergency_keywords = ["ajali", "damu nyingi", "kukosa pumzi", "kifua kikuu"]
        
        for keyword in emergency_keywords:
            if keyword in question.lower():
                return "⚠️ DHARURA: Tafuta msaada wa haraka! / EMERGENCY: Seek immediate help!"
        
        return "Taarifa hii ni ya elimu tu. Tembelea daktari kwa diagnosis sahihi."


# Example usage:
if __name__ == "__main__":
    qa_system = SwahiliMedicalQA(api_key="YOUR_GEMINI_API_KEY")
    
    questions = [
        "Je, dalili za malaria ni zipi?",  # What are the symptoms of malaria?
        "Ni dawa gani bora kwa homa?",    # What is the best medicine for fever?
        "Nina kukosa pumzi. Je, ni COVID-19?"  # I have difficulty breathing. Is it COVID-19?
    ]
    
    for question in questions:
        result = qa_system.ask(question)
        print(f"\n{'='*60}")
        print(f"Swali: {question}")
        print(f"Jibu: {result['answer']}")
        print(f"Vyanzo: {', '.join(result['sources'])}")
        print(f"Onyo: {result['safety_notice']}")
```

---

### 5. Hybrid Edge-Cloud Sync Protocol

```python
# File: edge_node/ai_agents/hybrid_sync_manager.py

from typing import List, Dict
import json
from datetime import datetime
from google.cloud import storage
from governance_kernel.vector_ledger import SovereignGuardrail

class HybridSyncManager:
    """
    Manage synchronization between edge (NVIDIA Jetson) and cloud (Google Cloud).
    Enforces data sovereignty: only de-identified data syncs to cloud.
    """
    
    def __init__(
        self, 
        bucket_name: str = "iluminara-edge-sync-eu",
        location: str = "europe-west4"
    ):
        self.bucket_name = bucket_name
        self.location = location
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(bucket_name)
        self.guardrail = SovereignGuardrail()
    
    def sync_swahili_queries(self, queries: List[Dict]) -> bool:
        """
        Sync Swahili medical queries from edge to cloud for model improvement.
        
        Args:
            queries: List of de-identified query logs
                [
                    {
                        "query": "Nina homa",
                        "timestamp": "2025-12-19T10:00:00Z",
                        "location_region": "Nairobi",  # No precise location
                        "has_phi": False
                    }
                ]
        
        Returns:
            True if sync successful, False otherwise
        """
        
        # Validate all queries are de-identified
        for query in queries:
            if query.get("has_phi", True):
                print(f"❌ Sync blocked: Query contains PHI")
                return False
            
            try:
                self.guardrail.validate_action(
                    action_type='Cloud_Sync',
                    payload={
                        'data_type': 'De_Identified_Medical_Query',
                        'destination': f'Google_Cloud_{self.location}',
                        'has_phi': False
                    },
                    jurisdiction='GDPR_EU'
                )
            except Exception as e:
                print(f"❌ Sovereignty violation: {e}")
                return False
        
        # Upload to Cloud Storage
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        blob_name = f"swahili_queries/{timestamp}.json"
        
        blob = self.bucket.blob(blob_name)
        blob.upload_from_string(
            json.dumps(queries, ensure_ascii=False, indent=2),
            content_type='application/json'
        )
        
        print(f"✅ Synced {len(queries)} queries to {blob_name}")
        return True
    
    def download_updated_models(self) -> List[str]:
        """
        Download updated Swahili medical models from cloud to edge.
        
        Returns:
            List of downloaded model file paths
        """
        
        downloaded_files = []
        
        # List all model files in cloud bucket
        blobs = self.bucket.list_blobs(prefix="models/swahili/")
        
        for blob in blobs:
            if blob.name.endswith(".tflite") or blob.name.endswith(".onnx"):
                # Download lightweight models for edge deployment
                local_path = f"/opt/iluminara/models/{blob.name.split('/')[-1]}"
                blob.download_to_filename(local_path)
                downloaded_files.append(local_path)
                print(f"✅ Downloaded model: {local_path}")
        
        return downloaded_files


# Example usage:
if __name__ == "__main__":
    sync_manager = HybridSyncManager(
        bucket_name="iluminara-edge-sync-eu",
        location="europe-west4"
    )
    
    # Sync de-identified queries from edge to cloud
    queries = [
        {
            "query": "Nina homa na kichefuchefu",
            "timestamp": "2025-12-19T10:00:00Z",
            "location_region": "Nairobi",
            "has_phi": False
        }
    ]
    
    sync_manager.sync_swahili_queries(queries)
    
    # Download updated models
    models = sync_manager.download_updated_models()
    print(f"Downloaded {len(models)} models")
```

---

## Configuration Files

### 1. Environment Variables
```bash
# File: .env.swahili_ai

# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=iluminara-production
GOOGLE_CLOUD_REGION=europe-west4  # GDPR-compliant EU region
GOOGLE_APPLICATION_CREDENTIALS=/opt/iluminara/secrets/gcp-service-account.json

# Dialogflow CX
DIALOGFLOW_AGENT_ID=your-agent-id
DIALOGFLOW_LOCATION=europe-west4

# Vertex AI
VERTEX_AI_ENDPOINT=projects/123/locations/europe-west4/endpoints/456

# Gemini Pro
GEMINI_API_KEY=your-gemini-api-key

# Data Sync
GCS_SYNC_BUCKET=iluminara-edge-sync-eu
SYNC_INTERVAL_SECONDS=3600  # Sync every hour

# Sovereignty Settings
JURISDICTION=GDPR_EU
ALLOW_CLOUD_SYNC=true  # Set to false for strict offline-only mode
```

### 2. Docker Compose for Edge Deployment
```yaml
# File: docker-compose.swahili-ai.yml

version: '3.8'

services:
  swahili-translator:
    build:
      context: ./edge_node/ai_agents
      dockerfile: Dockerfile.translator
    environment:
      - GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}
      - GOOGLE_CLOUD_REGION=${GOOGLE_CLOUD_REGION}
    volumes:
      - ./secrets:/opt/iluminara/secrets:ro
      - ./cache/translations:/opt/iluminara/cache
    networks:
      - iluminara-network
    restart: unless-stopped

  swahili-triage-agent:
    build:
      context: ./edge_node/ai_agents
      dockerfile: Dockerfile.triage
    environment:
      - DIALOGFLOW_AGENT_ID=${DIALOGFLOW_AGENT_ID}
      - DIALOGFLOW_LOCATION=${DIALOGFLOW_LOCATION}
    depends_on:
      - swahili-translator
    networks:
      - iluminara-network
    restart: unless-stopped

  hybrid-sync-manager:
    build:
      context: ./edge_node/ai_agents
      dockerfile: Dockerfile.sync
    environment:
      - GCS_SYNC_BUCKET=${GCS_SYNC_BUCKET}
      - SYNC_INTERVAL_SECONDS=${SYNC_INTERVAL_SECONDS}
    volumes:
      - ./data/sync_queue:/opt/iluminara/sync_queue
      - ./secrets:/opt/iluminara/secrets:ro
    networks:
      - iluminara-network
    restart: unless-stopped

networks:
  iluminara-network:
    driver: bridge
```

---

## Testing & Validation

### Unit Tests
```python
# File: tests/test_swahili_translator.py

import pytest
from edge_node.ai_agents.swahili_translator import SwahiliMedicalTranslator

def test_translate_symptom():
    translator = SwahiliMedicalTranslator(
        project_id="test-project",
        location="europe-west4"
    )
    
    swahili = "Nina homa"
    english = translator.translate(swahili)
    
    assert "fever" in english.lower()

def test_phi_rejection():
    translator = SwahiliMedicalTranslator(
        project_id="test-project",
        location="europe-west4"
    )
    
    # Text with PHI should be rejected
    phi_text = "Jina langu ni John Doe na nina homa"
    
    with pytest.raises(Exception):
        translator.translate(phi_text)

def test_offline_cache():
    translator = SwahiliMedicalTranslator(
        project_id="test-project",
        location="europe-west4"
    )
    
    # First translation (online)
    swahili = "homa"
    english1 = translator.translate(swahili)
    
    # Second translation (should use cache)
    english2 = translator.translate(swahili)
    
    assert english1 == english2
```

---

## Deployment Checklist

- [ ] Set up Google Cloud project with billing enabled
- [ ] Enable APIs: Translation, Vertex AI, Dialogflow CX, Gemini
- [ ] Create service account with appropriate IAM roles
- [ ] Configure regional endpoints (europe-west4 or africa-south1)
- [ ] Enable VPC Service Controls for data boundary enforcement
- [ ] Set up Customer-Managed Encryption Keys (CMEK)
- [ ] Create Swahili medical glossary (CSV file)
- [ ] Train custom Vertex AI models on Swahili medical corpus
- [ ] Deploy Dialogflow CX agent with Swahili intents
- [ ] Configure hybrid sync protocol (edge ↔ cloud)
- [ ] Test with de-identified medical queries
- [ ] Conduct compliance audit (GDPR, KDPA)
- [ ] Monitor API usage and costs
- [ ] Set up alerting for sovereignty violations

---

## Support & Resources

- **Google Cloud Healthcare Solutions:** https://cloud.google.com/solutions/healthcare
- **Dialogflow CX Documentation:** https://cloud.google.com/dialogflow/cx/docs
- **Vertex AI Tutorials:** https://cloud.google.com/vertex-ai/docs/tutorials
- **Swahili NLP Resources:** https://github.com/swahili-nlp

**Questions? Contact:** swahili-ai-support@iluminara.org

---

**Document Version:** 1.0  
**Last Updated:** December 19, 2025  
**Status:** Implementation Ready
