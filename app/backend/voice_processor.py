"""
Voice Processor: Sentry Mode
══════════════════════════════════════════════════════════════════════════════

Processes voice reports from field health workers using Google Cloud Speech-to-Text.
Converts audio to structured JSON for downstream analysis.

For local demo: Uses MockGCP to simulate Speech-to-Text API.
For production: Integrates with real Google Cloud Speech-to-Text.
"""

from typing import Dict, Any, Optional
import json
from datetime import datetime
from .mock_gcp import MockGCP


class VoiceProcessor:
    """
    Processes voice reports from health workers in the field.
    Implements "Sentry Mode" - the first line of outbreak intelligence.
    """
    
    def __init__(self, use_mock: bool = True):
        """
        Initialize voice processor.
        
        Args:
            use_mock: If True, uses mock GCP services. Set to False in production.
        """
        self.use_mock = use_mock
        if use_mock:
            self.speech_client = MockGCP().get_speech_client()
        else:
            # Real GCP implementation would go here
            from google.cloud import speech
            self.speech_client = speech.SpeechClient()
    
    def process_audio(self, audio_data: bytes, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process audio input and convert to structured JSON.
        
        Args:
            audio_data: Raw audio bytes
            metadata: Optional metadata (location, worker_id, etc.)
        
        Returns:
            Structured voice report with transcript and extracted entities
        """
        # Transcribe audio
        if self.use_mock:
            transcription_result = self.speech_client.transcribe(audio_data)
        else:
            # Real GCP Speech-to-Text call
            config = {
                "language_code": "en-US",
                "enable_automatic_punctuation": True,
            }
            audio = {"content": audio_data}
            response = self.speech_client.recognize(config=config, audio=audio)
            transcription_result = self._parse_gcp_response(response)
        
        # Extract structured information
        structured_report = self._extract_entities(transcription_result, metadata)
        
        return structured_report
    
    def process_audio_file(self, file_path: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process an uploaded audio file.
        
        Args:
            file_path: Path to audio file
            metadata: Optional metadata
        
        Returns:
            Structured voice report
        """
        if self.use_mock:
            transcription_result = self.speech_client.process_audio_file(file_path)
        else:
            # Read audio file and process
            with open(file_path, 'rb') as f:
                audio_data = f.read()
            return self.process_audio(audio_data, metadata)
        
        # Extract structured information
        structured_report = self._extract_entities(transcription_result, metadata)
        
        return structured_report
    
    def _extract_entities(self, transcription: Dict, metadata: Optional[Dict]) -> Dict[str, Any]:
        """
        Extract structured entities from transcription.
        
        Simple keyword-based extraction for demo.
        In production, would use NLP/LLM for entity recognition.
        """
        transcript = transcription.get("transcript", "")
        
        # Extract key entities (simple keyword matching for demo)
        entities = {
            "symptoms": self._extract_symptoms(transcript),
            "case_count": self._extract_case_count(transcript),
            "urgency": self._assess_urgency(transcript),
            "location_mentioned": self._extract_location(transcript)
        }
        
        # Build structured report
        report = {
            "report_id": f"VOICE_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "transcription": {
                "text": transcript,
                "confidence": transcription.get("confidence", 0.0),
                "language": transcription.get("language_code", "en-US")
            },
            "entities": entities,
            "metadata": metadata or {},
            "status": "PROCESSED",
            "sentry_mode": "ACTIVE"
        }
        
        return report
    
    def _extract_symptoms(self, text: str) -> list:
        """Extract mentioned symptoms."""
        symptoms_keywords = ["fever", "headache", "cough", "diarrhea", "vomiting", 
                            "respiratory", "gastroenteritis", "rash"]
        found_symptoms = [s for s in symptoms_keywords if s.lower() in text.lower()]
        return found_symptoms
    
    def _extract_case_count(self, text: str) -> Optional[int]:
        """Extract number of cases mentioned."""
        import re
        # Simple regex to find numbers
        numbers = re.findall(r'\b\d+\b', text)
        if numbers:
            return int(numbers[0])
        return None
    
    def _assess_urgency(self, text: str) -> str:
        """Assess urgency level from transcript."""
        urgent_keywords = ["emergency", "urgent", "immediate", "critical", "outbreak"]
        text_lower = text.lower()
        
        for keyword in urgent_keywords:
            if keyword in text_lower:
                return "HIGH"
        
        return "MEDIUM"
    
    def _extract_location(self, text: str) -> Optional[str]:
        """Extract location mentions."""
        locations = ["Dadaab", "Nairobi", "Mombasa", "eastern district", "western district"]
        text_lower = text.lower()
        
        for location in locations:
            if location.lower() in text_lower:
                return location
        
        return None
    
    def _parse_gcp_response(self, response) -> Dict[str, Any]:
        """Parse real GCP Speech-to-Text response."""
        # This would parse the actual GCP response structure
        # Placeholder for production implementation
        return {
            "transcript": "",
            "confidence": 0.0,
            "language_code": "en-US"
        }
