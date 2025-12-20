"""
Unit tests for SwahiliMedicalEntityExtractor
═════════════════════════════════════════════════════════════════════════════

Tests entity extraction with rule-based and Vertex AI modes.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from edge_node.ai_agents.swahili_entity_extractor import SwahiliMedicalEntityExtractor


class TestSwahiliMedicalEntityExtractor:
    """Test cases for Swahili Medical Entity Extractor."""
    
    def test_extractor_initialization_offline_mode(self):
        """Test extractor initializes in offline mode."""
        extractor = SwahiliMedicalEntityExtractor()
        assert extractor.use_cloud == False
    
    def test_rule_based_extraction_symptoms(self):
        """Test extraction of symptoms using rule-based patterns."""
        extractor = SwahiliMedicalEntityExtractor()
        
        text = "Mgonjwa ana homa na kichefuchefu"
        entities = extractor.extract_entities(text)
        
        assert "symptoms" in entities
        assert "homa" in entities["symptoms"]
        assert "kichefuchefu" in entities["symptoms"]
    
    def test_rule_based_extraction_diseases(self):
        """Test extraction of diseases."""
        extractor = SwahiliMedicalEntityExtractor()
        
        text = "Tunamshuku ana malaria au kifua kikuu"
        entities = extractor.extract_entities(text)
        
        assert "diseases" in entities
        assert "malaria" in entities["diseases"]
        assert "kifua kikuu" in entities["diseases"]
    
    def test_rule_based_extraction_medications(self):
        """Test extraction of medications."""
        extractor = SwahiliMedicalEntityExtractor()
        
        text = "Tumempa dawa za malaria na panadol"
        entities = extractor.extract_entities(text)
        
        assert "medications" in entities
        assert "dawa za malaria" in entities["medications"]
        assert "panadol" in entities["medications"]
    
    def test_rule_based_extraction_body_parts(self):
        """Test extraction of body parts."""
        extractor = SwahiliMedicalEntityExtractor()
        
        text = "Ana maumivu ya kichwa na tumbo"
        entities = extractor.extract_entities(text)
        
        assert "body_parts" in entities
        assert "kichwa" in entities["body_parts"]
        assert "tumbo" in entities["body_parts"]
    
    def test_mixed_entity_extraction(self):
        """Test extraction of multiple entity types."""
        extractor = SwahiliMedicalEntityExtractor()
        
        text = "Mgonjwa ana homa kali na maumivu ya tumbo. Tunamshuku ana malaria. Tumempa dawa za malaria."
        entities = extractor.extract_entities(text)
        
        assert len(entities["symptoms"]) > 0
        assert len(entities["diseases"]) > 0
        assert len(entities["medications"]) > 0
        assert len(entities["body_parts"]) > 0
    
    def test_empty_text_returns_empty_entities(self):
        """Test extraction with empty text."""
        extractor = SwahiliMedicalEntityExtractor()
        
        text = ""
        entities = extractor.extract_entities(text)
        
        assert all(len(v) == 0 for v in entities.values())
    
    def test_no_entities_found(self):
        """Test extraction when no entities present."""
        extractor = SwahiliMedicalEntityExtractor()
        
        text = "Habari yako"  # "How are you" - no medical entities
        entities = extractor.extract_entities(text)
        
        assert all(len(v) == 0 for v in entities.values())
    
    def test_case_insensitive_extraction(self):
        """Test extraction is case insensitive."""
        extractor = SwahiliMedicalEntityExtractor()
        
        text_lower = "nina homa"
        text_upper = "Nina Homa"
        
        entities_lower = extractor.extract_entities(text_lower)
        entities_upper = extractor.extract_entities(text_upper)
        
        assert entities_lower["symptoms"] == entities_upper["symptoms"]
    
    def test_duplicate_removal(self):
        """Test that duplicate entities are removed."""
        extractor = SwahiliMedicalEntityExtractor()
        
        text = "Nina homa. Nina homa kali. Homa yangu ni kali."
        entities = extractor.extract_entities(text)
        
        # Should only contain "homa" once, not three times
        assert "homa" in entities["symptoms"]
        assert entities["symptoms"].count("homa") == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
