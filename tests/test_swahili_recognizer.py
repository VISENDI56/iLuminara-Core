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
Tests for Swahili Speech Recognition Module
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, mock_open
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from edge_node.speech_recognition.swahili_recognizer import (
    SwahiliRecognizer,
    recognize_swahili_audio
)


class TestSwahiliRecognizer(unittest.TestCase):
    """Test cases for SwahiliRecognizer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.recognizer = SwahiliRecognizer()
    
    def test_initialization(self):
        """Test recognizer initialization"""
        self.assertEqual(self.recognizer.language_code, "sw-KE")
        self.assertIn("sw-TZ", self.recognizer.alternative_codes)
        self.assertTrue(self.recognizer.enable_automatic_punctuation)
    
    def test_initialization_custom_language(self):
        """Test initialization with custom language code"""
        recognizer = SwahiliRecognizer(language_code="sw-TZ")
        self.assertEqual(recognizer.language_code, "sw-TZ")
    
    def test_extract_health_keywords_fever(self):
        """Test extraction of fever keyword"""
        transcript = "Mgonjwa ana homa kali"
        keywords = self.recognizer.extract_health_keywords(transcript)
        
        self.assertEqual(len(keywords), 1)
        self.assertEqual(keywords[0]["swahili"], "homa")
        self.assertEqual(keywords[0]["english"], "fever")
    
    def test_extract_health_keywords_multiple(self):
        """Test extraction of multiple health keywords"""
        transcript = "Mgonjwa ana homa na kikohozi na kuhara"
        keywords = self.recognizer.extract_health_keywords(transcript)
        
        self.assertGreaterEqual(len(keywords), 3)
        
        swahili_words = [k["swahili"] for k in keywords]
        self.assertIn("homa", swahili_words)
        self.assertIn("kikohozi", swahili_words)
        self.assertIn("kuhara", swahili_words)
    
    def test_extract_health_keywords_case_insensitive(self):
        """Test that keyword extraction is case insensitive"""
        transcript_upper = "MGONJWA ANA HOMA"
        transcript_lower = "mgonjwa ana homa"
        
        keywords_upper = self.recognizer.extract_health_keywords(transcript_upper)
        keywords_lower = self.recognizer.extract_health_keywords(transcript_lower)
        
        self.assertEqual(len(keywords_upper), len(keywords_lower))
    
    def test_extract_health_keywords_no_match(self):
        """Test with transcript containing no health keywords"""
        transcript = "Habari yako leo"
        keywords = self.recognizer.extract_health_keywords(transcript)
        
        self.assertEqual(len(keywords), 0)
    
    @patch('edge_node.speech_recognition.swahili_recognizer.speech.SpeechClient')
    def test_transcribe_audio_mock(self, mock_client_class):
        """Test transcribe_audio with mocked Google Cloud client"""
        # Mock the response
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Create mock response
        mock_result = Mock()
        mock_alternative = Mock()
        mock_alternative.transcript = "Mgonjwa ana homa"
        mock_alternative.confidence = 0.95
        mock_alternative.words = []
        mock_result.alternatives = [mock_alternative]
        
        mock_response = Mock()
        mock_response.results = [mock_result]
        mock_client.recognize.return_value = mock_response
        
        # Create new recognizer to use mocked client
        recognizer = SwahiliRecognizer()
        recognizer.client = mock_client
        
        # Test transcription
        with patch('builtins.open', mock_open(read_data=b'fake audio')):
            result = recognizer.transcribe_audio("test.wav")
        
        self.assertEqual(result["transcript"], "Mgonjwa ana homa")
        self.assertEqual(result["confidence"], 0.95)
        self.assertEqual(result["language_code"], "sw-KE")
    
    @patch('edge_node.speech_recognition.swahili_recognizer.speech.SpeechClient')
    def test_transcribe_audio_no_speech(self, mock_client_class):
        """Test transcribe_audio when no speech is detected"""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Mock empty response
        mock_response = Mock()
        mock_response.results = []
        mock_client.recognize.return_value = mock_response
        
        recognizer = SwahiliRecognizer()
        recognizer.client = mock_client
        
        with patch('builtins.open', mock_open(read_data=b'fake audio')):
            result = recognizer.transcribe_audio("test.wav")
        
        self.assertEqual(result["transcript"], "")
        self.assertEqual(result["confidence"], 0.0)
        self.assertIn("error", result)


class TestHealthKeywordExtraction(unittest.TestCase):
    """Test cases specifically for health keyword extraction"""
    
    def setUp(self):
        self.recognizer = SwahiliRecognizer()
    
    def test_cholera_symptoms(self):
        """Test extraction of cholera-related symptoms"""
        transcript = "Mgonjwa ana kuhara na kutapika"
        keywords = self.recognizer.extract_health_keywords(transcript)
        
        swahili_words = [k["swahili"] for k in keywords]
        self.assertIn("kuhara", swahili_words)  # diarrhea
        self.assertIn("kutapika", swahili_words)  # vomiting
    
    def test_malaria_symptoms(self):
        """Test extraction of malaria-related symptoms"""
        transcript = "Ana homa na jasho na maumivu ya kichwa"
        keywords = self.recognizer.extract_health_keywords(transcript)
        
        swahili_words = [k["swahili"] for k in keywords]
        self.assertIn("homa", swahili_words)  # fever
        self.assertIn("jasho", swahili_words)  # sweating
        self.assertIn("kichwa", swahili_words)  # headache
    
    def test_respiratory_symptoms(self):
        """Test extraction of respiratory symptoms"""
        transcript = "Mgonjwa ana kikohozi na maumivu ya kifua"
        keywords = self.recognizer.extract_health_keywords(transcript)
        
        swahili_words = [k["swahili"] for k in keywords]
        self.assertIn("kikohozi", swahili_words)  # cough
        self.assertIn("kifua", swahili_words)  # chest


if __name__ == "__main__":
    unittest.main()
