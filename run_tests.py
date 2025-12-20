#!/usr/bin/env python3
"""
Simple Test Runner for Swahili AI Agents
═════════════════════════════════════════════════════════════════════════════

Runs tests without pytest dependency for offline validation.

Usage:
    python run_tests.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from edge_node.ai_agents import (
    SwahiliMedicalTranslator,
    SwahiliMedicalEntityExtractor,
    SwahiliTriageAgent,
    SwahiliMedicalQA,
    HybridSyncManager
)


def print_test(test_name):
    """Print test header."""
    print(f"\n{'='*70}")
    print(f"  {test_name}")
    print(f"{'='*70}")


def test_translator():
    """Test Swahili Medical Translator."""
    print_test("Testing SwahiliMedicalTranslator")
    
    translator = SwahiliMedicalTranslator("test-project", "europe-west4")
    
    # Test offline cache
    assert translator.translate("homa", use_cache=True) == "fever", "Translation failed"
    assert translator.translate("malaria", use_cache=True) == "malaria", "Translation failed"
    
    # Test batch translation
    results = translator.batch_translate(["homa", "kichefuchefu"], use_cache=True)
    assert len(results) == 2, "Batch translation failed"
    
    print("✅ All translator tests passed")


def test_entity_extractor():
    """Test Swahili Medical Entity Extractor."""
    print_test("Testing SwahiliMedicalEntityExtractor")
    
    extractor = SwahiliMedicalEntityExtractor()
    
    # Test entity extraction
    entities = extractor.extract_entities("Nina homa na malaria")
    assert "homa" in entities["symptoms"], "Symptom extraction failed"
    assert "malaria" in entities["diseases"], "Disease extraction failed"
    
    print("✅ All entity extractor tests passed")


def test_triage_agent():
    """Test Swahili Triage Agent."""
    print_test("Testing SwahiliTriageAgent")
    
    agent = SwahiliTriageAgent("test-project")
    
    # Test triage
    result = agent.detect_intent("Nina kukosa pumzi")
    assert result.get("priority") == "HIGH", "Emergency detection failed"
    
    result = agent.detect_intent("Nina homa")
    assert "response_text" in result, "Triage response failed"
    
    print("✅ All triage agent tests passed")


def test_medical_qa():
    """Test Swahili Medical Q&A."""
    print_test("Testing SwahiliMedicalQA")
    
    qa = SwahiliMedicalQA()
    
    # Test Q&A
    result = qa.ask("Je, dalili za malaria ni zipi?")
    assert "malaria" in result["answer"].lower(), "Q&A failed"
    assert len(result["sources"]) > 0, "Sources not provided"
    
    # Test PHI detection
    result = qa.ask("Jina langu ni John")
    assert result["confidence"] == 0.0, "PHI detection failed"
    
    print("✅ All medical Q&A tests passed")


def test_sync_manager():
    """Test Hybrid Sync Manager."""
    print_test("Testing HybridSyncManager")
    
    sync = HybridSyncManager()
    
    # Test sync status
    status = sync.get_sync_status()
    assert "cloud_available" in status, "Status check failed"
    
    # Test query sync with proper consent
    queries = [{
        "query": "Nina homa",
        "has_phi": False,
        "consent_token": "GENERAL_RESEARCH_CONSENT",
        "timestamp": "2025-12-19T10:00:00Z"
    }]
    result = sync.sync_swahili_queries(queries)
    assert result == True, "Query sync failed"
    
    # Test PHI blocking
    queries = [{"query": "Test", "has_phi": True}]
    result = sync.sync_swahili_queries(queries)
    assert result == False, "PHI blocking failed"
    
    print("✅ All sync manager tests passed")


def test_integration():
    """Test integrated workflow."""
    print_test("Testing Integration Workflow")
    
    translator = SwahiliMedicalTranslator("test", "europe-west4")
    extractor = SwahiliMedicalEntityExtractor()
    triage = SwahiliTriageAgent("test")
    
    # Patient report using cached terms
    report = "Nina homa"  # Use simple cached term
    
    # Extract
    entities = extractor.extract_entities(report)
    assert len(entities["symptoms"]) > 0, "Integration: extraction failed"
    
    # Translate
    english = translator.translate("homa", use_cache=True)  # Translate individual term
    assert english is not None, "Integration: translation failed"
    
    # Triage
    result = triage.triage_symptom("homa", log_to_cbs=False)
    assert len(result) > 0, "Integration: triage failed"
    
    print("✅ All integration tests passed")


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("  iLuminara Swahili AI Agents - Test Suite")
    print("  Running offline validation tests")
    print("="*70)
    
    try:
        test_translator()
        test_entity_extractor()
        test_triage_agent()
        test_medical_qa()
        test_sync_manager()
        test_integration()
        
        print("\n" + "="*70)
        print("  ✅ ALL TESTS PASSED")
        print("  6/6 test suites successful")
        print("="*70 + "\n")
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
