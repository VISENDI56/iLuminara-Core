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

#!/usr/bin/env python3
"""
Swahili AI Agents Demo
═════════════════════════════════════════════════════════════════════════════

Demonstration of all Swahili AI agents integrated into iLuminara-Core.

Usage:
    python swahili_ai_demo.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edge_node.ai_agents import (
    SwahiliMedicalTranslator,
    SwahiliMedicalEntityExtractor,
    SwahiliTriageAgent,
    SwahiliMedicalQA,
    HybridSyncManager
)
from edge_node.ai_agents.config import SwahiliAIConfig


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def demo_translator():
    """Demonstrate Swahili medical translation."""
    print_section("1. Swahili Medical Translator")
    
    config = SwahiliAIConfig()
    translator = SwahiliMedicalTranslator(
        project_id=config.google_cloud_project,
        location=config.google_cloud_region
    )
    
    # Test translation (uses offline cache)
    swahili_texts = [
        "Nina homa na kichefuchefu",
        "Mgonjwa ana maumivu ya tumbo",
        "Daktari anasema ni malaria"
    ]
    
    print("📝 Translating Swahili to English (offline mode):\n")
    for swahili in swahili_texts:
        english = translator.translate(swahili, use_cache=True)
        print(f"  SW: {swahili}")
        print(f"  EN: {english}\n")


def demo_entity_extractor():
    """Demonstrate Swahili medical entity extraction."""
    print_section("2. Swahili Medical Entity Extractor")
    
    extractor = SwahiliMedicalEntityExtractor()
    
    # Test entity extraction
    swahili_text = "Mgonjwa ana homa kali na kichefuchefu. Tunamshuku ana malaria. Tumempa dawa za homa."
    
    print(f"📊 Extracting entities from:\n  '{swahili_text}'\n")
    entities = extractor.extract_entities(swahili_text)
    
    print("Entities found:")
    for entity_type, entity_list in entities.items():
        if entity_list:
            print(f"  {entity_type.upper()}: {', '.join(entity_list)}")


def demo_triage_agent():
    """Demonstrate Swahili medical triage agent."""
    print_section("3. Swahili Medical Triage Agent")
    
    config = SwahiliAIConfig()
    agent = SwahiliTriageAgent(
        project_id=config.google_cloud_project,
        location=config.google_cloud_region
    )
    
    # Test triage with different symptoms
    symptoms = [
        "homa na kichefuchefu",
        "kukosa pumzi",
        "maumivu ya kichwa"
    ]
    
    print("🏥 Triaging symptoms:\n")
    for symptom in symptoms:
        advice = agent.triage_symptom(symptom, log_to_cbs=False)
        print(f"  Symptom: {symptom}")
        print(f"  Advice: {advice}\n")


def demo_medical_qa():
    """Demonstrate Swahili medical Q&A."""
    print_section("4. Swahili Medical Q&A System")
    
    config = SwahiliAIConfig()
    qa_system = SwahiliMedicalQA(api_key=config.gemini_api_key)
    
    # Test Q&A
    questions = [
        "Je, dalili za malaria ni zipi?",
        "Ni dawa gani bora kwa homa?",
        "Jinsi ya kuzuia malaria?"
    ]
    
    print("❓ Answering medical questions:\n")
    for question in questions:
        result = qa_system.ask(question)
        print(f"  Q: {question}")
        print(f"  A: {result['answer'][:100]}...")
        print(f"  Sources: {', '.join(result['sources'])}")
        print(f"  Safety Notice: {result['safety_notice']}\n")


def demo_sync_manager():
    """Demonstrate hybrid edge-cloud sync."""
    print_section("5. Hybrid Edge-Cloud Sync Manager")
    
    config = SwahiliAIConfig()
    sync_manager = HybridSyncManager(
        bucket_name=config.gcs_sync_bucket,
        location=config.google_cloud_region
    )
    
    # Test sync status
    status = sync_manager.get_sync_status()
    print("☁️  Sync Status:")
    print(f"  Cloud Available: {status['cloud_available']}")
    print(f"  Queued Items: {status['queued_items']}")
    print(f"  Bucket: {status['bucket']}")
    print(f"  Region: {status['location']}\n")
    
    # Test query sync (offline mode)
    sample_queries = [
        {
            "query": "Nina homa",
            "timestamp": "2025-12-19T10:00:00Z",
            "location_region": "Nairobi",
            "has_phi": False
        }
    ]
    
    print("📤 Syncing sample queries...")
    success = sync_manager.sync_swahili_queries(sample_queries)
    print(f"  Sync {'successful' if success else 'failed'}")


def demo_integrated_workflow():
    """Demonstrate integrated workflow using multiple agents."""
    print_section("6. Integrated Workflow Example")
    
    config = SwahiliAIConfig()
    
    # Initialize agents
    translator = SwahiliMedicalTranslator(
        project_id=config.google_cloud_project,
        location=config.google_cloud_region
    )
    extractor = SwahiliMedicalEntityExtractor()
    triage = SwahiliTriageAgent(
        project_id=config.google_cloud_project
    )
    
    # Simulated patient report
    patient_report = "Nina homa kali, kichefuchefu, na maumivu ya kichwa. Nina hofu ni malaria."
    
    print("🔄 Integrated Workflow:\n")
    print(f"1. Patient Report (Swahili):\n   '{patient_report}'\n")
    
    # Step 1: Extract entities
    entities = extractor.extract_entities(patient_report)
    print(f"2. Extracted Entities:")
    for entity_type, entity_list in entities.items():
        if entity_list:
            print(f"   - {entity_type}: {', '.join(entity_list)}")
    
    # Step 2: Translate to English
    english_report = translator.translate(patient_report, use_cache=True)
    print(f"\n3. Translated to English:\n   '{english_report}'\n")
    
    # Step 3: Triage
    primary_symptom = entities['symptoms'][0] if entities['symptoms'] else "homa"
    triage_result = triage.detect_intent(f"Nina {primary_symptom}")
    print(f"4. Triage Result:")
    print(f"   Priority: {triage_result.get('priority', 'N/A')}")
    print(f"   Response: {triage_result['response_text'][:100]}...")
    
    print("\n✅ Workflow complete!")


def main():
    """Run all demos."""
    print("\n" + "="*70)
    print("  iLuminara Swahili AI Agents - Demonstration")
    print("  Sovereignty-First Medical AI for East Africa")
    print("="*70)
    
    # Load and validate configuration
    config = SwahiliAIConfig()
    print(config)
    
    if not config.validate():
        print("⚠️  Configuration validation failed. Some features may not work.")
        print("   Set environment variables or edit .env.swahili-ai.example\n")
    
    # Run demos
    try:
        demo_translator()
        demo_entity_extractor()
        demo_triage_agent()
        demo_medical_qa()
        demo_sync_manager()
        demo_integrated_workflow()
        
        print("\n" + "="*70)
        print("  ✅ All demos completed successfully!")
        print("  📚 See docs/swahili_ai_integration_guide.md for more details")
        print("="*70 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo error: {e}")
        print("   Check that dependencies are installed: pip install -r requirements-swahili-ai.txt")


if __name__ == "__main__":
    main()
