"""
Unit tests for SwahiliMedicalQA
═════════════════════════════════════════════════════════════════════════════

Tests medical Q&A functionality with offline knowledge base.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from edge_node.ai_agents.swahili_medical_qa import SwahiliMedicalQA


class TestSwahiliMedicalQA:
    """Test cases for Swahili Medical Q&A."""
    
    def test_qa_initialization_offline_mode(self):
        """Test Q&A initializes in offline mode."""
        qa = SwahiliMedicalQA()
        assert qa.use_gemini == False
    
    def test_malaria_question(self):
        """Test answering question about malaria."""
        qa = SwahiliMedicalQA()
        
        result = qa.ask("Je, dalili za malaria ni zipi?")
        
        assert "malaria" in result["answer"].lower()
        assert len(result["sources"]) > 0
        assert result["confidence"] > 0
    
    def test_fever_advice(self):
        """Test answering question about fever."""
        qa = SwahiliMedicalQA()
        
        result = qa.ask("Nina homa. Je, nifanye nini?")
        
        assert "answer" in result
        assert len(result["answer"]) > 0
    
    def test_tuberculosis_question(self):
        """Test answering question about tuberculosis."""
        qa = SwahiliMedicalQA()
        
        result = qa.ask("Je, kifua kikuu ni nini?")
        
        assert "answer" in result
        assert result.get("safety_notice")
    
    def test_phi_detection(self):
        """Test that PHI is detected and blocked."""
        qa = SwahiliMedicalQA()
        
        result = qa.ask("Jina langu ni John na nina homa")
        
        assert "kibinafsi" in result["answer"].lower() or "binafsi" in result["answer"].lower()
        assert result["confidence"] == 0.0
    
    def test_emergency_safety_notice(self):
        """Test that emergency questions get safety notices."""
        qa = SwahiliMedicalQA()
        
        result = qa.ask("Nina kukosa pumzi sana. Je, ni hatari?")
        
        assert "DHARURA" in result["safety_notice"] or "EMERGENCY" in result["safety_notice"]
    
    def test_regular_safety_notice(self):
        """Test that regular questions get standard safety notice."""
        qa = SwahiliMedicalQA()
        
        result = qa.ask("Je, dalili za malaria ni zipi?")
        
        assert "daktari" in result["safety_notice"].lower()
    
    def test_unknown_topic_handling(self):
        """Test handling of unknown topics."""
        qa = SwahiliMedicalQA()
        
        result = qa.ask("Je, nini kinaendelea na hali ya hewa?")
        
        assert "answer" in result
        assert "samahani" in result["answer"].lower() or "sorry" in result["answer"].lower()
    
    def test_knowledge_base_has_malaria(self):
        """Test knowledge base contains malaria information."""
        qa = SwahiliMedicalQA()
        
        assert "malaria" in qa.knowledge_base
        assert "symptoms" in qa.knowledge_base["malaria"]
    
    def test_knowledge_base_has_fever(self):
        """Test knowledge base contains fever information."""
        qa = SwahiliMedicalQA()
        
        assert "homa" in qa.knowledge_base
        assert "advice" in qa.knowledge_base["homa"]
    
    def test_knowledge_base_has_tuberculosis(self):
        """Test knowledge base contains tuberculosis information."""
        qa = SwahiliMedicalQA()
        
        assert "kifua kikuu" in qa.knowledge_base
        assert "symptoms" in qa.knowledge_base["kifua kikuu"]
    
    def test_response_structure(self):
        """Test that response has expected structure."""
        qa = SwahiliMedicalQA()
        
        result = qa.ask("Je, dalili za malaria ni zipi?")
        
        assert "answer" in result
        assert "sources" in result
        assert "safety_notice" in result
        assert "confidence" in result
        
        assert isinstance(result["answer"], str)
        assert isinstance(result["sources"], list)
        assert isinstance(result["safety_notice"], str)
        assert isinstance(result["confidence"], (int, float))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
