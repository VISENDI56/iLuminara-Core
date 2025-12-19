"""
FRENASA Symptom Extraction Engine
═════════════════════════════════════════════════════════════════════════════

Custom Vertex AI model for extracting structured symptom data from Swahili
transcriptions. Identifies FRENASA-specific health indicators and formats them
as JSON for Golden Thread data fusion.

FRENASA: Fast Response Early Notification And Symptom Analysis

Features:
- Swahili medical entity recognition
- Symptom vector extraction (fever, cough, diarrhea, etc.)
- Patient demographic inference (age, gender)
- Severity classification
- JSON schema compliance

Philosophy: "Transform voice into actionable intelligence while preserving dignity."
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import re


@dataclass
class SymptomVector:
    """Structured symptom representation."""
    symptom_name: str
    severity: str  # "mild", "moderate", "severe"
    duration: Optional[str] = None  # e.g., "2 days", "1 week"
    confidence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "symptom": self.symptom_name,
            "severity": self.severity,
            "duration": self.duration,
            "confidence": self.confidence
        }


@dataclass
class PatientDemographics:
    """Inferred patient demographics from transcription."""
    age_group: Optional[str] = None  # "<5", "5-14", "15-49", "50+"
    gender: Optional[str] = None  # "male", "female", "unknown"
    pregnant: Optional[bool] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "age_group": self.age_group,
            "gender": self.gender,
            "pregnant": self.pregnant
        }


@dataclass
class ExtractedSymptoms:
    """Complete symptom extraction result."""
    transcription_text: str
    symptoms: List[SymptomVector] = field(default_factory=list)
    demographics: PatientDemographics = field(default_factory=PatientDemographics)
    location: Optional[str] = None
    urgency_level: str = "routine"  # "routine", "urgent", "emergency"
    disease_suspicion: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    confidence_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return {
            "transcription": self.transcription_text,
            "symptoms": [s.to_dict() for s in self.symptoms],
            "demographics": self.demographics.to_dict(),
            "location": self.location,
            "urgency": self.urgency_level,
            "disease_suspicion": self.disease_suspicion,
            "timestamp": self.timestamp.isoformat(),
            "confidence": self.confidence_score
        }
    
    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class FRENASASymptomExtractor:
    """
    FRENASA Symptom Extraction Engine powered by Vertex AI.
    
    Extracts structured symptom data from Swahili medical transcriptions
    for integration with the Golden Thread data fusion system.
    
    Usage:
        extractor = FRENASASymptomExtractor(
            project_id="your-project",
            location="us-central1",
            model_id="frenasa-symptom-v1"
        )
        
        result = extractor.extract_symptoms(
            "Mgonjwa ana homa kali na kichefuchefu"
        )
        print(result.to_json())
    """
    
    def __init__(
        self,
        project_id: Optional[str] = None,
        location: str = "us-central1",
        model_id: str = "frenasa-symptom-extractor-v1",
        credentials_path: Optional[str] = None,
    ):
        """
        Initialize FRENASA symptom extractor.
        
        Args:
            project_id: Google Cloud project ID
            location: Vertex AI location (e.g., "us-central1", "europe-west4")
            model_id: Custom model endpoint ID
            credentials_path: Path to service account credentials
        """
        self.project_id = project_id
        self.location = location
        self.model_id = model_id
        self.credentials_path = credentials_path
        self.client = None
        self._initialize_client()
        
        # Swahili symptom dictionary
        self.symptom_lexicon = self._build_symptom_lexicon()
        self.severity_keywords = self._build_severity_keywords()
        self.demographic_patterns = self._build_demographic_patterns()
    
    def _initialize_client(self):
        """
        Initialize Vertex AI client.
        
        Falls back to rule-based extraction if Vertex AI is unavailable.
        """
        try:
            from google.cloud import aiplatform
            import os
            
            if self.credentials_path:
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
            
            if self.project_id:
                aiplatform.init(project=self.project_id, location=self.location)
                self.client = aiplatform
                print(f"✅ Vertex AI client initialized (project: {self.project_id})")
            else:
                print("⚠️  No project_id provided. Using rule-based extraction.")
                self.client = None
                
        except ImportError:
            print("⚠️  google-cloud-aiplatform not installed. Using rule-based extraction.")
            self.client = None
        except Exception as e:
            print(f"⚠️  Failed to initialize Vertex AI client: {e}. Using rule-based extraction.")
            self.client = None
    
    def extract_symptoms(
        self,
        transcription_text: str,
        location: Optional[str] = None,
        use_vertex_ai: bool = True,
    ) -> ExtractedSymptoms:
        """
        Extract structured symptoms from Swahili transcription.
        
        Args:
            transcription_text: Transcribed Swahili text from voice note
            location: Geographic location (optional)
            use_vertex_ai: Whether to use Vertex AI model (falls back to rules if False)
        
        Returns:
            ExtractedSymptoms object with structured symptom data
        """
        if self.client and use_vertex_ai:
            return self._extract_with_vertex_ai(transcription_text, location)
        else:
            return self._extract_with_rules(transcription_text, location)
    
    def _extract_with_vertex_ai(
        self,
        transcription_text: str,
        location: Optional[str] = None,
    ) -> ExtractedSymptoms:
        """
        Extract symptoms using Vertex AI custom model.
        
        This method would call the deployed Vertex AI endpoint.
        For now, falls back to rule-based extraction.
        """
        try:
            # TODO: Implement actual Vertex AI endpoint call
            # endpoint = self.client.Endpoint(endpoint_name=self.model_id)
            # prediction = endpoint.predict(instances=[{"text": transcription_text}])
            # return self._parse_vertex_ai_response(prediction)
            
            print("⚠️  Vertex AI endpoint not yet deployed. Using rule-based extraction.")
            return self._extract_with_rules(transcription_text, location)
            
        except Exception as e:
            print(f"❌ Vertex AI extraction failed: {e}. Falling back to rules.")
            return self._extract_with_rules(transcription_text, location)
    
    def _extract_with_rules(
        self,
        transcription_text: str,
        location: Optional[str] = None,
    ) -> ExtractedSymptoms:
        """
        Extract symptoms using rule-based NLP (fallback/edge mode).
        
        Provides immediate functionality without requiring cloud connectivity.
        """
        text_lower = transcription_text.lower()
        
        # Extract symptoms
        symptoms = self._identify_symptoms(text_lower)
        
        # Extract demographics
        demographics = self._identify_demographics(text_lower)
        
        # Determine urgency
        urgency = self._classify_urgency(symptoms)
        
        # Infer disease suspicion
        disease_suspicion = self._infer_disease(symptoms, text_lower)
        
        # Calculate confidence
        confidence = self._calculate_confidence(symptoms, len(text_lower.split()))
        
        return ExtractedSymptoms(
            transcription_text=transcription_text,
            symptoms=symptoms,
            demographics=demographics,
            location=location,
            urgency_level=urgency,
            disease_suspicion=disease_suspicion,
            confidence_score=confidence,
            timestamp=datetime.utcnow()
        )
    
    def _identify_symptoms(self, text: str) -> List[SymptomVector]:
        """Identify symptoms from Swahili text using lexicon matching."""
        identified_symptoms = []
        
        for symptom_name, keywords in self.symptom_lexicon.items():
            for keyword in keywords:
                if keyword in text:
                    # Determine severity
                    severity = self._determine_severity(text, keyword)
                    
                    # Extract duration if present
                    duration = self._extract_duration(text)
                    
                    identified_symptoms.append(SymptomVector(
                        symptom_name=symptom_name,
                        severity=severity,
                        duration=duration,
                        confidence=0.85
                    ))
                    break  # Only count each symptom once
        
        return identified_symptoms
    
    def _determine_severity(self, text: str, symptom_keyword: str) -> str:
        """Determine severity from context around symptom keyword."""
        # Find symptom in text
        index = text.find(symptom_keyword)
        if index == -1:
            return "moderate"
        
        # Check surrounding words for severity indicators
        window = 30  # characters before and after
        context = text[max(0, index-window):index+len(symptom_keyword)+window]
        
        # Check for severity keywords
        if any(kw in context for kw in self.severity_keywords["severe"]):
            return "severe"
        elif any(kw in context for kw in self.severity_keywords["mild"]):
            return "mild"
        else:
            return "moderate"
    
    def _extract_duration(self, text: str) -> Optional[str]:
        """Extract temporal duration from text."""
        # Swahili duration patterns
        patterns = [
            r"siku (\w+)",  # "siku mbili" = two days
            r"wiki (\w+)",  # "wiki moja" = one week
            r"mwezi (\w+)",  # "mwezi mmoja" = one month
            r"(\d+)\s*siku",  # "2 siku" = 2 days
            r"(\d+)\s*wiki",  # "1 wiki" = 1 week
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return None
    
    def _identify_demographics(self, text: str) -> PatientDemographics:
        """Extract patient demographics from text."""
        demographics = PatientDemographics()
        
        # Age group patterns
        for age_group, patterns in self.demographic_patterns["age"].items():
            if any(pattern in text for pattern in patterns):
                demographics.age_group = age_group
                break
        
        # Gender patterns
        for gender, patterns in self.demographic_patterns["gender"].items():
            if any(pattern in text for pattern in patterns):
                demographics.gender = gender
                break
        
        # Pregnancy indicator
        if any(kw in text for kw in ["mjamzito", "mimba", "kujifungua"]):
            demographics.pregnant = True
        
        return demographics
    
    def _classify_urgency(self, symptoms: List[SymptomVector]) -> str:
        """Classify urgency level based on symptoms."""
        # Emergency indicators
        emergency_symptoms = {"breathing_difficulty", "severe_bleeding", "unconsciousness"}
        severe_count = sum(1 for s in symptoms if s.severity == "severe")
        
        for symptom in symptoms:
            if symptom.symptom_name in emergency_symptoms:
                return "emergency"
        
        if severe_count >= 2 or len(symptoms) >= 4:
            return "urgent"
        
        return "routine"
    
    def _infer_disease(self, symptoms: List[SymptomVector], text: str) -> Optional[str]:
        """Infer disease suspicion from symptom pattern."""
        symptom_names = {s.symptom_name for s in symptoms}
        
        # Cholera pattern
        if {"diarrhea", "vomiting", "dehydration"} <= symptom_names:
            return "Cholera (suspected)"
        
        # Malaria pattern
        if "fever" in symptom_names and ("chills" in text or "baridi" in text):
            return "Malaria (suspected)"
        
        # COVID-19 pattern
        if {"cough", "fever"} <= symptom_names and ("kupumua" in text or "breathing" in text):
            return "COVID-19 (suspected)"
        
        # Typhoid pattern
        if "fever" in symptom_names and "headache" in symptom_names:
            return "Typhoid (suspected)"
        
        return None
    
    def _calculate_confidence(self, symptoms: List[SymptomVector], word_count: int) -> float:
        """Calculate overall extraction confidence."""
        if not symptoms:
            return 0.3
        
        # Base confidence on number of symptoms and text length
        symptom_confidence = min(len(symptoms) * 0.2 + 0.5, 0.95)
        length_factor = min(word_count / 20, 1.0)  # Longer texts = higher confidence
        
        return symptom_confidence * length_factor
    
    def _build_symptom_lexicon(self) -> Dict[str, List[str]]:
        """Build Swahili-to-symptom mapping."""
        return {
            "fever": ["homa", "joto", "moto wa mwili"],
            "cough": ["kikohozi", "kohozi"],
            "diarrhea": ["kuharisha", "kuharisha maji", "tumbo la homa"],
            "vomiting": ["kutapika", "tapika", "kichefuchefu"],
            "headache": ["maumivu ya kichwa", "kichwa kinaumwa"],
            "body_ache": ["maumivu ya mwili", "mwili unaumwa"],
            "dehydration": ["ukosefu wa maji", "kauka"],
            "breathing_difficulty": ["ugumu wa kupumua", "shida ya kupumua"],
            "chills": ["kutetemeka", "baridi"],
            "fatigue": ["uchovu", "udhaifu"],
            "sore_throat": ["koo kunaumwa", "maumivu ya koo"],
            "abdominal_pain": ["maumivu ya tumbo", "tumbo linaumwa"],
        }
    
    def _build_severity_keywords(self) -> Dict[str, List[str]]:
        """Build severity indicator keywords."""
        return {
            "severe": ["kali", "sana", "vibaya", "hatari", "mbaya"],
            "mild": ["kidogo", "rahisi", "ndogo", "pekee"],
        }
    
    def _build_demographic_patterns(self) -> Dict[str, Dict[str, List[str]]]:
        """Build demographic pattern matchers."""
        return {
            "age": {
                "<5": ["mtoto", "mchanga", "mtoto mdogo", "miezi"],
                "5-14": ["mtoto", "msichana", "mvulana"],
                "15-49": ["kijana", "mtu mzima", "mama", "baba"],
                "50+": ["mzee", "mwanamke mzima", "mwanamume mzima"],
            },
            "gender": {
                "male": ["mvulana", "mwanamume", "baba"],
                "female": ["msichana", "mwanamke", "mama", "mjamzito"],
            }
        }


# ═════════════════════════════════════════════════════════════════════════════
# Example Usage
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("═" * 80)
    print("FRENASA Symptom Extraction Engine - Test Module")
    print("═" * 80)
    
    # Initialize extractor (will use rule-based mode if Vertex AI unavailable)
    extractor = FRENASASymptomExtractor()
    
    # Test transcriptions
    test_cases = [
        "Mgonjwa ana homa kali na kichefuchefu tangu siku tatu",
        "Mtoto mdogo ana kuharisha maji na kutapika sana",
        "Mwanamke mjamzito ana maumivu makali ya tumbo",
        "Mzee ana kikohozi kikali na ugumu wa kupumua",
        "Familia nne wanaonyesha dalili za homa ya malaria",
    ]
    
    print("\n🔬 Testing Symptom Extraction...\n")
    
    for i, transcription in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"   Input: {transcription}")
        
        result = extractor.extract_symptoms(transcription, location="Dadaab")
        
        print(f"   Symptoms: {len(result.symptoms)} identified")
        for symptom in result.symptoms:
            print(f"      - {symptom.symptom_name} ({symptom.severity})")
        
        print(f"   Demographics: Age={result.demographics.age_group}, Gender={result.demographics.gender}")
        print(f"   Urgency: {result.urgency_level}")
        print(f"   Disease Suspicion: {result.disease_suspicion or 'None'}")
        print(f"   Confidence: {result.confidence_score:.2%}")
        print()
    
    # Show full JSON output for last case
    print("=" * 80)
    print("Full JSON Output (Last Case):")
    print("=" * 80)
    print(result.to_json())
    
    print("\n" + "═" * 80)
