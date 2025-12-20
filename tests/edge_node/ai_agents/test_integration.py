"""
Integration tests for Swahili AI Agents
═════════════════════════════════════════════════════════════════════════════

Tests integrated workflows using multiple AI agents together.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from edge_node.ai_agents import (
    SwahiliMedicalTranslator,
    SwahiliMedicalEntityExtractor,
    SwahiliTriageAgent,
    SwahiliMedicalQA,
    HybridSyncManager
)


class TestIntegration:
    """Integration tests for AI agents working together."""
    
    def test_translation_and_entity_extraction(self):
        """Test translation followed by entity extraction."""
        translator = SwahiliMedicalTranslator("test", "europe-west4")
        extractor = SwahiliMedicalEntityExtractor()
        
        swahili_text = "Nina homa na kichefuchefu"
        
        # Translate
        english_text = translator.translate(swahili_text, use_cache=True)
        
        # Extract entities
        entities = extractor.extract_entities(swahili_text)
        
        assert english_text is not None
        assert len(entities["symptoms"]) > 0
    
    def test_entity_extraction_and_triage(self):
        """Test entity extraction followed by triage."""
        extractor = SwahiliMedicalEntityExtractor()
        triage = SwahiliTriageAgent("test")
        
        text = "Nina homa kali na kukosa pumzi"
        
        # Extract entities
        entities = extractor.extract_entities(text)
        
        # Triage primary symptom
        if entities["symptoms"]:
            primary_symptom = entities["symptoms"][0]
            advice = triage.triage_symptom(primary_symptom, log_to_cbs=False)
            
            assert advice is not None
            assert len(advice) > 0
    
    def test_qa_and_translation(self):
        """Test Q&A followed by translation."""
        qa = SwahiliMedicalQA()
        translator = SwahiliMedicalTranslator("test", "europe-west4")
        
        # Ask question in Swahili
        result = qa.ask("Je, dalili za malaria ni zipi?")
        
        assert result["answer"] is not None
        assert len(result["sources"]) > 0
    
    def test_full_workflow(self):
        """Test complete workflow: extract, translate, triage, sync."""
        extractor = SwahiliMedicalEntityExtractor()
        translator = SwahiliMedicalTranslator("test", "europe-west4")
        triage = SwahiliTriageAgent("test")
        sync = HybridSyncManager()
        
        # Patient report
        report = "Nina homa kali na kichefuchefu"
        
        # Step 1: Extract entities
        entities = extractor.extract_entities(report)
        assert len(entities["symptoms"]) > 0
        
        # Step 2: Translate
        english = translator.translate(report, use_cache=True)
        assert english is not None
        
        # Step 3: Triage
        triage_result = triage.detect_intent(f"Nina {entities['symptoms'][0]}")
        assert "response_text" in triage_result
        
        # Step 4: Sync de-identified data
        queries = [{
            "query": report,
            "has_phi": False,
            "timestamp": "2025-12-19T10:00:00Z"
        }]
        sync_result = sync.sync_swahili_queries(queries)
        assert sync_result == True
    
    def test_multiple_agents_initialization(self):
        """Test that all agents can be initialized together."""
        translator = SwahiliMedicalTranslator("test", "europe-west4")
        extractor = SwahiliMedicalEntityExtractor()
        triage = SwahiliTriageAgent("test")
        qa = SwahiliMedicalQA()
        sync = HybridSyncManager()
        
        # All should initialize successfully
        assert translator is not None
        assert extractor is not None
        assert triage is not None
        assert qa is not None
        assert sync is not None
    
    def test_offline_resilience(self):
        """Test that all agents work in offline mode."""
        translator = SwahiliMedicalTranslator("test", "europe-west4")
        extractor = SwahiliMedicalEntityExtractor()
        triage = SwahiliTriageAgent("test")
        qa = SwahiliMedicalQA()
        
        # All should work offline
        assert translator.translate("homa", use_cache=True) == "fever"
        assert len(extractor.extract_entities("Nina homa")["symptoms"]) > 0
        assert len(triage.triage_symptom("homa", log_to_cbs=False)) > 0
        assert qa.ask("Je, dalili za malaria ni zipi?")["answer"] is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
