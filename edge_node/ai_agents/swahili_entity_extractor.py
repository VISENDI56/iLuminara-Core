# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# COMPETITOR EXCLUSION: Commercial use by entities offering Sovereign/Health OS 
# solutions is STRICTLY PROHIBITED without a commercial license.
# 
# The Sovereign Immune System (Omni-Law) and JEPA-MPC Architecture are 
# proprietary inventions of iLuminara.
# ------------------------------------------------------------------------------

"""
Swahili Medical Entity Extractor
═════════════════════════════════════════════════════════════════════════════

Extract medical entities (symptoms, diseases, medications) from Swahili text
using custom-trained Vertex AI models.

Usage:
    extractor = SwahiliMedicalEntityExtractor(
        model_endpoint="projects/123/locations/europe-west4/endpoints/456"
    )
    
    entities = extractor.extract_entities("Mgonjwa ana homa na kichefuchefu")
"""

from typing import List, Dict
import json

try:
    from google.cloud import aiplatform
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False
    print("⚠️  google-cloud-aiplatform not installed. Install with: pip install google-cloud-aiplatform")


class SwahiliMedicalEntityExtractor:
    """
    Extract medical entities (symptoms, diseases, medications) from Swahili text.
    Uses custom-trained Vertex AI model.
    """
    
    def __init__(self, model_endpoint: str = None, location: str = "europe-west4"):
        """
        Initialize the entity extractor.
        
        Args:
            model_endpoint: Vertex AI model endpoint ID
            location: Google Cloud region
        """
        if not VERTEX_AI_AVAILABLE:
            print("⚠️  Vertex AI not available. Using rule-based extraction.")
            self.use_cloud = False
        else:
            self.use_cloud = model_endpoint is not None
            if self.use_cloud:
                self.model_endpoint = model_endpoint
                self.location = location
                aiplatform.init(location=location)
        
        # Rule-based entity patterns for offline mode
        self.entity_patterns = {
            "symptoms": [
                "homa", "homa kali", "kichefuchefu", "maumivu ya kichwa",
                "maumivu ya tumbo", "kukosa pumzi", "kuhara", "kutapika",
                "kikohozi", "uchovu", "kuharisha", "maumivu ya kifua"
            ],
            "diseases": [
                "malaria", "kifua kikuu", "ukimwi", "homa ya manjano",
                "kipindupindu", "polio", "tetanus", "hepatitis"
            ],
            "medications": [
                "dawa za malaria", "panadol", "penicillin", "ARV",
                "dawa za homa", "dawa za maumivu"
            ],
            "body_parts": [
                "kichwa", "tumbo", "moyo", "mapafu", "ini", "figo",
                "kifua", "mguu", "mkono", "jicho"
            ]
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract medical entities from Swahili clinical text.
        
        Args:
            text: Swahili medical text
        
        Returns:
            {
                "symptoms": ["homa", "kichefuchefu"],
                "diseases": ["malaria"],
                "medications": ["dawa za malaria"],
                "body_parts": ["tumbo", "kichwa"]
            }
        """
        
        if self.use_cloud:
            return self._extract_with_vertex_ai(text)
        else:
            return self._extract_with_rules(text)
    
    def _extract_with_vertex_ai(self, text: str) -> Dict[str, List[str]]:
        """Extract entities using Vertex AI model."""
        try:
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
            
        except Exception as e:
            print(f"⚠️  Vertex AI extraction failed: {e}. Falling back to rules.")
            return self._extract_with_rules(text)
    
    def _extract_with_rules(self, text: str) -> Dict[str, List[str]]:
        """Extract entities using rule-based pattern matching (offline mode)."""
        text_lower = text.lower()
        
        entities = {
            "symptoms": [],
            "diseases": [],
            "medications": [],
            "body_parts": []
        }
        
        # Pattern matching for each entity type
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    entities[entity_type].append(pattern)
        
        # Remove duplicates
        for entity_type in entities:
            entities[entity_type] = list(set(entities[entity_type]))
        
        return entities
    
    def extract_and_translate(self, text: str, translator=None) -> Dict[str, any]:
        """
        Extract entities and optionally translate them to English.
        
        Args:
            text: Swahili medical text
            translator: SwahiliMedicalTranslator instance (optional)
        
        Returns:
            {
                "swahili": {...},
                "english": {...}  # If translator provided
            }
        """
        swahili_entities = self.extract_entities(text)
        
        result = {"swahili": swahili_entities}
        
        if translator:
            english_entities = {}
            for entity_type, entity_list in swahili_entities.items():
                english_entities[entity_type] = [
                    translator.translate(entity) or entity
                    for entity in entity_list
                ]
            result["english"] = english_entities
        
        return result
