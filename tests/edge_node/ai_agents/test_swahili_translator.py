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
Unit tests for SwahiliMedicalTranslator
═════════════════════════════════════════════════════════════════════════════

Tests translation functionality, offline cache, and sovereignty validation.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from edge_node.ai_agents.swahili_translator import SwahiliMedicalTranslator


class TestSwahiliMedicalTranslator:
    """Test cases for Swahili Medical Translator."""
    
    def test_translator_initialization(self):
        """Test translator can be initialized."""
        # Should work even without Google Cloud credentials
        translator = SwahiliMedicalTranslator(
            project_id="test-project",
            location="europe-west4"
        )
        assert translator.project_id == "test-project"
        assert translator.location == "europe-west4"
    
    def test_offline_cache_loading(self):
        """Test offline translation cache is loaded."""
        translator = SwahiliMedicalTranslator(
            project_id="test-project",
            location="europe-west4"
        )
        cache = translator.translation_cache
        
        # Verify common medical terms are cached
        assert "homa" in cache
        assert cache["homa"] == "fever"
        assert "malaria" in cache
        assert "kifua kikuu" in cache
        assert cache["kifua kikuu"] == "tuberculosis"
    
    def test_translate_offline_cache_hit(self):
        """Test translation using offline cache."""
        translator = SwahiliMedicalTranslator(
            project_id="test-project",
            location="europe-west4"
        )
        
        # Test cached translations
        assert translator.translate("homa", use_cache=True) == "fever"
        assert translator.translate("malaria", use_cache=True) == "malaria"
        assert translator.translate("kichefuchefu", use_cache=True) == "nausea"
    
    def test_batch_translate(self):
        """Test batch translation."""
        translator = SwahiliMedicalTranslator(
            project_id="test-project",
            location="europe-west4"
        )
        
        swahili_texts = ["homa", "malaria", "kichefuchefu"]
        english_texts = translator.batch_translate(swahili_texts, use_cache=True)
        
        assert len(english_texts) == 3
        assert english_texts[0] == "fever"
        assert english_texts[1] == "malaria"
        assert english_texts[2] == "nausea"
    
    def test_cache_contains_body_parts(self):
        """Test cache includes body part terminology."""
        translator = SwahiliMedicalTranslator(
            project_id="test-project",
            location="europe-west4"
        )
        cache = translator.translation_cache
        
        assert "kichwa" in cache and cache["kichwa"] == "head"
        assert "tumbo" in cache and cache["tumbo"] == "stomach"
        assert "moyo" in cache and cache["moyo"] == "heart"
    
    def test_cache_contains_common_phrases(self):
        """Test cache includes common medical phrases."""
        translator = SwahiliMedicalTranslator(
            project_id="test-project",
            location="europe-west4"
        )
        cache = translator.translation_cache
        
        assert "nina" in cache and cache["nina"] == "I have"
        assert "daktari" in cache and cache["daktari"] == "doctor"
        assert "dawa" in cache and cache["dawa"] == "medicine"
    
    def test_sovereignty_validation_jurisdiction(self):
        """Test that translator accepts jurisdiction parameter."""
        translator = SwahiliMedicalTranslator(
            project_id="test-project",
            location="europe-west4"
        )
        
        # Should not raise error with valid jurisdiction
        result = translator.translate(
            "homa",
            jurisdiction="GDPR_EU",
            use_cache=True
        )
        assert result == "fever"
    
    def test_multiple_locations_supported(self):
        """Test translator supports different regions."""
        translator_eu = SwahiliMedicalTranslator(
            project_id="test-project",
            location="europe-west4"
        )
        translator_africa = SwahiliMedicalTranslator(
            project_id="test-project",
            location="africa-south1"
        )
        
        assert translator_eu.location == "europe-west4"
        assert translator_africa.location == "africa-south1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
