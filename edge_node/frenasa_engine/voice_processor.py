"""
Voice Processing Module for FRENASA Engine
═════════════════════════════════════════════════════════════════════════════

Processes voice alerts from Community Health Volunteers (CHVs) and converts them
into structured JSON data for the Golden Thread fusion engine.

Simulates voice-to-text conversion and symptom extraction for demonstration purposes.
In production, this would integrate with actual speech recognition APIs.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceProcessor:
    """
    Voice processing engine that converts audio alerts into structured health data.
    
    Simulates the FRENASA AI engine's voice-to-JSON capability demonstrated
    in the 4.2-second alert transmission sequence.
    """
    
    def __init__(self):
        """Initialize the voice processor with symptom mapping."""
        self.symptom_keywords = {
            'diarrhea': ['diarrhea', 'watery stool', 'loose stool', 'kuharisha', 'kuhara', 'tumbo la kuhara'],
            'vomiting': ['vomiting', 'throwing up', 'kutapika', 'tapika'],
            'fever': ['fever', 'hot', 'temperature', 'homa', 'joto'],
            'cough': ['cough', 'coughing', 'kikohozi', 'kohozi'],
            'headache': ['headache', 'head pain', 'maumivu ya kichwa', 'kichwa kinaumwa'],
            'dehydration': ['dehydration', 'thirsty', 'dry mouth', 'ukame', 'kiu'],
            'body_ache': ['body ache', 'pain', 'maumivu', 'maumivu ya mwili']
        }
        
        self.language_support = ['english', 'swahili', 'somali']
    
    def process_audio(
        self, 
        audio_data: bytes,
        language: str = 'swahili',
        location: Optional[Dict[str, float]] = None,
        transcription_override: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process audio data and extract structured health information.
        
        Args:
            audio_data: Raw audio bytes (WAV format)
            language: Language of the audio (swahili, english, somali)
            location: Optional GPS coordinates {'lat': float, 'lng': float}
        
        Returns:
            Structured health alert with symptoms, location, and metadata
        """
        processing_start = datetime.utcnow()
        
        # Use provided transcription or simulate voice-to-text
        if transcription_override:
            transcription = transcription_override
        else:
            transcription = self._simulate_transcription(audio_data, language)
        
        # Extract symptoms from transcription
        symptoms = self._extract_symptoms(transcription)
        
        # Determine severity based on symptoms
        severity = self._assess_severity(symptoms)
        
        # Build structured response
        result = {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "processing_time_ms": (datetime.utcnow() - processing_start).total_seconds() * 1000,
            "transcription": transcription,
            "language_detected": language,
            "symptoms": symptoms,
            "severity": severity,
            "location": location or {"lat": 0.0512, "lng": 40.3129},  # Default: Dadaab
            "source": "CHV Voice Alert",
            "alert_level": "CRITICAL" if severity >= 8 else "ALERT" if severity >= 5 else "WATCH",
            "recommendations": self._generate_recommendations(symptoms, severity)
        }
        
        logger.info(f"Voice processing complete: {len(symptoms)} symptoms detected, severity {severity}/10")
        
        return result
    
    def _simulate_transcription(self, audio_data: bytes, language: str) -> str:
        """
        Simulate voice-to-text transcription.
        
        In production, this would call actual speech recognition APIs.
        For demo, we detect patterns in the audio data or use sample text.
        """
        # Sample transcriptions for different symptom patterns
        sample_transcriptions = {
            'cholera': "Patient reporting severe watery diarrhea and vomiting for 6 hours. Shows signs of dehydration.",
            'malaria': "Patient has high fever, body aches, and headache. Started 2 days ago.",
            'measles': "Child with fever, cough, and rash. Multiple cases in the area.",
            'default': "Patient reporting symptoms. Requires immediate assessment."
        }
        
        # For demo: detect based on audio size or return default
        # In production: use Google Speech-to-Text or similar
        audio_size = len(audio_data)
        
        if audio_size < 5000:
            return sample_transcriptions['default']
        elif audio_size < 15000:
            return sample_transcriptions['cholera']
        elif audio_size < 25000:
            return sample_transcriptions['malaria']
        else:
            return sample_transcriptions['measles']
    
    def _extract_symptoms(self, transcription: str) -> list:
        """
        Extract symptoms from transcribed text using keyword matching.
        
        Args:
            transcription: Transcribed text from voice alert
        
        Returns:
            List of detected symptoms
        """
        detected_symptoms = []
        transcription_lower = transcription.lower()
        
        for symptom, keywords in self.symptom_keywords.items():
            for keyword in keywords:
                if keyword in transcription_lower:
                    if symptom not in detected_symptoms:
                        detected_symptoms.append(symptom)
                    break
        
        return detected_symptoms
    
    def _assess_severity(self, symptoms: list) -> int:
        """
        Assess severity score based on symptoms.
        
        Args:
            symptoms: List of detected symptoms
        
        Returns:
            Severity score from 1-10
        """
        # High-risk symptoms get higher weights
        severity_weights = {
            'diarrhea': 3,
            'vomiting': 3,
            'dehydration': 4,
            'fever': 2,
            'cough': 1,
            'headache': 1,
            'body_ache': 1
        }
        
        total_severity = sum(severity_weights.get(s, 1) for s in symptoms)
        
        # Cap at 10
        return min(10, total_severity)
    
    def _generate_recommendations(self, symptoms: list, severity: int) -> list:
        """
        Generate clinical recommendations based on symptoms and severity.
        
        Args:
            symptoms: List of detected symptoms
            severity: Severity score
        
        Returns:
            List of recommended actions
        """
        recommendations = []
        
        # Critical symptoms requiring immediate action
        if 'diarrhea' in symptoms and 'vomiting' in symptoms:
            recommendations.append("IMMEDIATE: Suspected cholera. Start ORS immediately.")
            recommendations.append("Isolate patient to prevent spread")
            recommendations.append("Notify district health officer")
        
        if 'dehydration' in symptoms:
            recommendations.append("URGENT: Administer oral rehydration solution")
            recommendations.append("Monitor vital signs every 30 minutes")
        
        if 'fever' in symptoms:
            recommendations.append("Administer antipyretics if fever > 38.5°C")
            recommendations.append("Rule out malaria with rapid diagnostic test")
        
        # General recommendations based on severity
        if severity >= 8:
            recommendations.append("CRITICAL: Transfer to health facility immediately")
        elif severity >= 5:
            recommendations.append("ALERT: Clinical assessment required within 2 hours")
        else:
            recommendations.append("WATCH: Monitor symptoms and reassess in 4 hours")
        
        return recommendations


def process_voice_alert(audio_data: bytes, language: str = 'swahili', location: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """
    Convenience function to process a voice alert.
    
    Args:
        audio_data: Raw audio bytes
        language: Language of the audio
        location: GPS coordinates
    
    Returns:
        Structured health alert
    """
    processor = VoiceProcessor()
    return processor.process_audio(audio_data, language, location)
