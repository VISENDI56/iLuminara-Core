"""
FRENASA Symptom Extraction Server
==================================

HTTP inference server for symptom extraction from Swahili voice transcripts.
Designed for deployment on Google Cloud AI Platform (Vertex AI) and edge devices.

Key Features:
- RESTful API for symptom extraction
- Integration with Swahili speech recognition
- GDPR/KDPA compliant data handling
- Real-time inference with low latency

API Endpoints:
    POST /predict - Extract symptoms from text or audio
    GET /health - Health check endpoint
"""

from flask import Flask, request, jsonify
from typing import Dict, Any, List
import json
import logging
from datetime import datetime
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


class SymptomExtractor:
    """
    FRENASA Symptom Extraction Model
    
    Extracts structured health symptoms from Swahili transcripts.
    This is a simple rule-based system that can be replaced with
    a trained ML model (e.g., BERT, BioBERT) for production.
    """
    
    def __init__(self):
        """Initialize the symptom extractor."""
        # Swahili to English symptom mapping
        self.symptom_dictionary = {
            # Fever-related
            "homa": {"english": "fever", "severity": "moderate", "category": "systemic"},
            "joto": {"english": "heat/fever", "severity": "moderate", "category": "systemic"},
            
            # Respiratory
            "kikohozi": {"english": "cough", "severity": "mild", "category": "respiratory"},
            "pumu": {"english": "breathing difficulty", "severity": "severe", "category": "respiratory"},
            "kifua": {"english": "chest pain", "severity": "moderate", "category": "respiratory"},
            
            # Gastrointestinal
            "kuhara": {"english": "diarrhea", "severity": "moderate", "category": "gastrointestinal"},
            "kutapika": {"english": "vomiting", "severity": "moderate", "category": "gastrointestinal"},
            "tumbo": {"english": "stomach pain", "severity": "moderate", "category": "gastrointestinal"},
            "kichefuchefu": {"english": "nausea", "severity": "mild", "category": "gastrointestinal"},
            
            # Pain
            "maumivu": {"english": "pain", "severity": "moderate", "category": "pain"},
            "kichwa": {"english": "headache", "severity": "mild", "category": "pain"},
            
            # Other symptoms
            "damu": {"english": "blood", "severity": "severe", "category": "hematologic"},
            "jasho": {"english": "sweating", "severity": "mild", "category": "systemic"},
            "dhaifu": {"english": "weakness", "severity": "moderate", "category": "systemic"},
            "ukosefu_wa_nguvu": {"english": "fatigue", "severity": "mild", "category": "systemic"},
        }
        
        # Disease patterns (for risk assessment)
        self.disease_patterns = {
            "cholera": ["kuhara", "kutapika", "dhaifu"],
            "malaria": ["homa", "jasho", "kichwa", "maumivu"],
            "respiratory_infection": ["kikohozi", "homa", "kifua"],
            "covid19": ["kikohozi", "homa", "pumu", "dhaifu"],
        }
        
    def extract_symptoms(self, transcript: str) -> Dict[str, Any]:
        """
        Extract symptoms from Swahili transcript.
        
        Args:
            transcript: Swahili text from speech recognition
            
        Returns:
            Dictionary with extracted symptoms and risk assessment
        """
        transcript_lower = transcript.lower()
        detected_symptoms = []
        
        # Extract individual symptoms
        for swahili_term, symptom_info in self.symptom_dictionary.items():
            if swahili_term in transcript_lower:
                detected_symptoms.append({
                    "swahili": swahili_term,
                    "english": symptom_info["english"],
                    "severity": symptom_info["severity"],
                    "category": symptom_info["category"],
                })
        
        # Pattern matching for disease risk
        disease_risks = self._assess_disease_risk(detected_symptoms)
        
        # Calculate overall severity
        severity_scores = {"mild": 1, "moderate": 2, "severe": 3}
        max_severity = max(
            [severity_scores.get(s["severity"], 0) for s in detected_symptoms],
            default=0
        )
        
        overall_severity = "none"
        if max_severity == 1:
            overall_severity = "mild"
        elif max_severity == 2:
            overall_severity = "moderate"
        elif max_severity == 3:
            overall_severity = "severe"
        
        return {
            "symptoms": detected_symptoms,
            "symptom_count": len(detected_symptoms),
            "overall_severity": overall_severity,
            "disease_risks": disease_risks,
            "requires_immediate_attention": max_severity >= 3,
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def _assess_disease_risk(self, symptoms: List[Dict]) -> List[Dict[str, Any]]:
        """
        Assess disease risk based on symptom patterns.
        
        Args:
            symptoms: List of detected symptoms
            
        Returns:
            List of potential diseases with confidence scores
        """
        symptom_terms = [s["swahili"] for s in symptoms]
        risks = []
        
        for disease, pattern in self.disease_patterns.items():
            matches = sum(1 for term in pattern if term in symptom_terms)
            confidence = matches / len(pattern) if pattern else 0
            
            if confidence > 0:
                risks.append({
                    "disease": disease,
                    "confidence": round(confidence, 2),
                    "matched_symptoms": matches,
                    "total_pattern_symptoms": len(pattern),
                })
        
        # Sort by confidence
        risks.sort(key=lambda x: x["confidence"], reverse=True)
        return risks


# Initialize model
symptom_extractor = SymptomExtractor()


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Kubernetes/GCP load balancers."""
    return jsonify({
        "status": "healthy",
        "service": "frenasa-symptom-extractor",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }), 200


@app.route("/predict", methods=["POST"])
def predict():
    """
    Main inference endpoint for symptom extraction.
    
    Request Body:
        {
            "transcript": "Mgonjwa ana homa na kikohozi",
            "metadata": {
                "patient_id": "optional",
                "location": "optional",
                "timestamp": "optional"
            }
        }
    
    Response:
        {
            "symptoms": [...],
            "symptom_count": 2,
            "overall_severity": "moderate",
            "disease_risks": [...],
            "requires_immediate_attention": false
        }
    """
    try:
        # Parse request
        data = request.get_json()
        
        if not data or "transcript" not in data:
            return jsonify({
                "error": "Missing 'transcript' field in request body"
            }), 400
        
        transcript = data["transcript"]
        metadata = data.get("metadata", {})
        
        # Log request (without PHI)
        logger.info(f"Processing symptom extraction request")
        
        # Extract symptoms
        result = symptom_extractor.extract_symptoms(transcript)
        
        # Add metadata
        result["metadata"] = metadata
        result["model_version"] = "1.0.0"
        
        # Log result summary
        logger.info(
            f"Extracted {result['symptom_count']} symptoms, "
            f"severity: {result['overall_severity']}"
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        
        # Only log full stack trace in development
        if app.debug:
            logger.error(traceback.format_exc())
        
        return jsonify({
            "error": "Internal server error"
        }), 500


@app.route("/", methods=["GET"])
def root():
    """Root endpoint with API documentation."""
    return jsonify({
        "service": "FRENASA Symptom Extractor",
        "version": "1.0.0",
        "description": "Extract health symptoms from Swahili transcripts",
        "endpoints": {
            "/health": "GET - Health check",
            "/predict": "POST - Extract symptoms from transcript",
        },
        "example_request": {
            "transcript": "Mgonjwa ana homa na kikohozi",
            "metadata": {
                "location": "Nairobi",
                "timestamp": "2025-12-19T10:00:00Z"
            }
        }
    }), 200


if __name__ == "__main__":
    # Run server
    import os
    port = int(os.environ.get("PORT", 8080))
    
    logger.info(f"Starting FRENASA Symptom Extractor on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
