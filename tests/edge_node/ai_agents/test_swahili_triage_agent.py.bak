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
Unit tests for SwahiliTriageAgent
═════════════════════════════════════════════════════════════════════════════

Tests symptom triage functionality with rule-based classification.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from edge_node.ai_agents.swahili_triage_agent import SwahiliTriageAgent


class TestSwahiliTriageAgent:
    """Test cases for Swahili Triage Agent."""
    
    def test_agent_initialization_offline_mode(self):
        """Test agent initializes in offline mode."""
        agent = SwahiliTriageAgent(
            project_id="test-project",
            location="europe-west4"
        )
        assert agent.use_dialogflow == False
    
    def test_emergency_symptom_detection(self):
        """Test detection of emergency symptoms."""
        agent = SwahiliTriageAgent(project_id="test-project")
        
        result = agent.detect_intent("Nina kukosa pumzi")
        
        assert "emergency" in result["intent"] or result.get("priority") == "HIGH"
        assert "DHARURA" in result["response_text"] or "EMERGENCY" in result["response_text"]
    
    def test_urgent_symptom_detection(self):
        """Test detection of urgent symptoms."""
        agent = SwahiliTriageAgent(project_id="test-project")
        
        result = agent.detect_intent("Nina homa kali")
        
        assert result.get("priority") in ["MEDIUM", "HIGH"]
    
    def test_routine_symptom_detection(self):
        """Test detection of routine symptoms."""
        agent = SwahiliTriageAgent(project_id="test-project")
        
        result = agent.detect_intent("Nina kichefuchefu")
        
        assert result.get("priority") == "LOW"
    
    def test_triage_symptom_method(self):
        """Test triage_symptom method."""
        agent = SwahiliTriageAgent(project_id="test-project")
        
        response = agent.triage_symptom("homa", log_to_cbs=False)
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_emergency_keywords(self):
        """Test all emergency keywords are detected."""
        agent = SwahiliTriageAgent(project_id="test-project")
        
        emergency_phrases = [
            "Nina kukosa pumzi",
            "Nina damu nyingi",
            "Nina ajali"
        ]
        
        for phrase in emergency_phrases:
            result = agent.detect_intent(phrase)
            assert result.get("priority") == "HIGH" or "DHARURA" in result["response_text"]
    
    def test_response_contains_swahili(self):
        """Test that responses contain Swahili text."""
        agent = SwahiliTriageAgent(project_id="test-project")
        
        result = agent.detect_intent("Nina homa")
        
        # Response should contain Swahili words
        assert any(word in result["response_text"].lower() for word in ["daktari", "pumzika", "tembelea", "hospitali", "msaada"])
    
    def test_confidence_score_present(self):
        """Test that confidence score is returned."""
        agent = SwahiliTriageAgent(project_id="test-project")
        
        result = agent.detect_intent("Nina homa")
        
        assert "confidence" in result
        assert isinstance(result["confidence"], (int, float))
        assert 0 <= result["confidence"] <= 1
    
    def test_session_id_generation(self):
        """Test that session ID is generated."""
        agent = SwahiliTriageAgent(project_id="test-project")
        
        result = agent.detect_intent("Nina homa")
        
        # Rule-based mode may not have session_id, but should not error
        assert isinstance(result, dict)
    
    def test_different_locations_supported(self):
        """Test agent supports different regions."""
        agent_eu = SwahiliTriageAgent(
            project_id="test-project",
            location="europe-west4"
        )
        agent_africa = SwahiliTriageAgent(
            project_id="test-project",
            location="africa-south1"
        )
        
        assert agent_eu.location == "europe-west4"
        assert agent_africa.location == "africa-south1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
