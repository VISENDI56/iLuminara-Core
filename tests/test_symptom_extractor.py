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
Tests for FRENASA Symptom Extractor Server
"""

import unittest
import json
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from edge_node.frenasa_engine.symptom_extractor_server import (
    app,
    SymptomExtractor,
    symptom_extractor
)


class TestSymptomExtractor(unittest.TestCase):
    """Test cases for SymptomExtractor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.extractor = SymptomExtractor()
    
    def test_initialization(self):
        """Test extractor initialization"""
        self.assertIsNotNone(self.extractor.symptom_dictionary)
        self.assertIsNotNone(self.extractor.disease_patterns)
        self.assertIn("homa", self.extractor.symptom_dictionary)
    
    def test_extract_symptoms_single(self):
        """Test extraction of single symptom"""
        transcript = "Mgonjwa ana homa"
        result = self.extractor.extract_symptoms(transcript)
        
        self.assertEqual(result["symptom_count"], 1)
        self.assertEqual(result["symptoms"][0]["swahili"], "homa")
        self.assertEqual(result["symptoms"][0]["english"], "fever")
        self.assertIn("overall_severity", result)
    
    def test_extract_symptoms_multiple(self):
        """Test extraction of multiple symptoms"""
        transcript = "Mgonjwa ana homa na kikohozi na kuhara"
        result = self.extractor.extract_symptoms(transcript)
        
        self.assertGreaterEqual(result["symptom_count"], 3)
        symptom_names = [s["swahili"] for s in result["symptoms"]]
        self.assertIn("homa", symptom_names)
        self.assertIn("kikohozi", symptom_names)
        self.assertIn("kuhara", symptom_names)
    
    def test_extract_symptoms_severity(self):
        """Test severity classification"""
        # Mild symptom
        transcript_mild = "Ana kikohozi"
        result_mild = self.extractor.extract_symptoms(transcript_mild)
        self.assertIn(result_mild["overall_severity"], ["mild", "moderate"])
        
        # Severe symptom
        transcript_severe = "Ana damu"
        result_severe = self.extractor.extract_symptoms(transcript_severe)
        self.assertEqual(result_severe["overall_severity"], "severe")
        self.assertTrue(result_severe["requires_immediate_attention"])
    
    def test_disease_risk_cholera(self):
        """Test cholera disease risk assessment"""
        transcript = "Mgonjwa ana kuhara na kutapika na dhaifu"
        result = self.extractor.extract_symptoms(transcript)
        
        self.assertGreater(len(result["disease_risks"]), 0)
        
        # Check if cholera is in risks
        disease_names = [r["disease"] for r in result["disease_risks"]]
        self.assertIn("cholera", disease_names)
        
        # Find cholera risk
        cholera_risk = next(r for r in result["disease_risks"] if r["disease"] == "cholera")
        self.assertGreater(cholera_risk["confidence"], 0)
    
    def test_disease_risk_malaria(self):
        """Test malaria disease risk assessment"""
        transcript = "Ana homa na jasho na kichwa na maumivu"
        result = self.extractor.extract_symptoms(transcript)
        
        disease_names = [r["disease"] for r in result["disease_risks"]]
        self.assertIn("malaria", disease_names)
    
    def test_no_symptoms(self):
        """Test with transcript containing no symptoms"""
        transcript = "Habari yako leo"
        result = self.extractor.extract_symptoms(transcript)
        
        self.assertEqual(result["symptom_count"], 0)
        self.assertEqual(result["overall_severity"], "none")
        self.assertFalse(result["requires_immediate_attention"])


class TestSymptomExtractorAPI(unittest.TestCase):
    """Test cases for Flask API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "frenasa-symptom-extractor")
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = self.app.get('/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("service", data)
        self.assertIn("endpoints", data)
    
    def test_predict_endpoint_success(self):
        """Test predict endpoint with valid input"""
        payload = {
            "transcript": "Mgonjwa ana homa na kikohozi",
            "metadata": {
                "location": "Nairobi",
                "patient_id": "P12345"
            }
        }
        
        response = self.app.post(
            '/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertIn("symptoms", data)
        self.assertIn("symptom_count", data)
        self.assertIn("overall_severity", data)
        self.assertIn("disease_risks", data)
        self.assertIn("metadata", data)
        
        self.assertEqual(data["metadata"]["location"], "Nairobi")
        self.assertGreater(data["symptom_count"], 0)
    
    def test_predict_endpoint_missing_transcript(self):
        """Test predict endpoint with missing transcript"""
        payload = {
            "metadata": {"location": "Nairobi"}
        }
        
        response = self.app.post(
            '/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)
    
    def test_predict_endpoint_empty_transcript(self):
        """Test predict endpoint with empty transcript"""
        payload = {
            "transcript": ""
        }
        
        response = self.app.post(
            '/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["symptom_count"], 0)
    
    def test_predict_endpoint_complex_case(self):
        """Test predict endpoint with complex symptom case"""
        payload = {
            "transcript": "Mgonjwa ana homa kali, kuhara maji, kutapika, dhaifu sana, na jasho nyingi"
        }
        
        response = self.app.post(
            '/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Should detect multiple symptoms
        self.assertGreaterEqual(data["symptom_count"], 3)
        
        # Should have disease risk assessment
        self.assertGreater(len(data["disease_risks"]), 0)


class TestDiseasePatternMatching(unittest.TestCase):
    """Test cases for disease pattern matching"""
    
    def setUp(self):
        self.extractor = SymptomExtractor()
    
    def test_cholera_pattern_full_match(self):
        """Test full cholera pattern match"""
        transcript = "Ana kuhara kutapika dhaifu"
        result = self.extractor.extract_symptoms(transcript)
        
        cholera_risk = next(
            (r for r in result["disease_risks"] if r["disease"] == "cholera"),
            None
        )
        
        self.assertIsNotNone(cholera_risk)
        self.assertGreater(cholera_risk["confidence"], 0.5)
    
    def test_malaria_pattern_partial_match(self):
        """Test partial malaria pattern match"""
        transcript = "Ana homa na jasho"
        result = self.extractor.extract_symptoms(transcript)
        
        malaria_risk = next(
            (r for r in result["disease_risks"] if r["disease"] == "malaria"),
            None
        )
        
        self.assertIsNotNone(malaria_risk)
        self.assertGreater(malaria_risk["confidence"], 0)
    
    def test_respiratory_infection_pattern(self):
        """Test respiratory infection pattern"""
        transcript = "Ana kikohozi na homa na kifua"
        result = self.extractor.extract_symptoms(transcript)
        
        respiratory_risk = next(
            (r for r in result["disease_risks"] if r["disease"] == "respiratory_infection"),
            None
        )
        
        self.assertIsNotNone(respiratory_risk)


if __name__ == "__main__":
    unittest.main()
