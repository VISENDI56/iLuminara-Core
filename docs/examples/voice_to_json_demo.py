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
Example: Complete Voice-to-JSON Pipeline Demo
═════════════════════════════════════════════════════════════════════════════

This example demonstrates the complete end-to-end pipeline for transforming
Swahili voice notes into structured JSON data.

Pipeline Stages:
1. Audio Input (mock or real audio file)
2. Swahili Transcription (Cloud Speech-to-Text or mock)
3. Symptom Extraction (Vertex AI or rule-based)
4. Golden Thread Data Fusion
5. Sovereignty Validation

Requirements:
- Python 3.8+
- google-cloud-speech (optional, for Cloud Speech-to-Text)
- google-cloud-aiplatform (optional, for Vertex AI)
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from edge_node.frenasa_engine.voice_to_json import VoiceToJSONPipeline
from edge_node.frenasa_engine.voice_transcription import create_sample_audio


def demo_complete_pipeline():
    """Run complete pipeline demonstration."""
    print("=" * 80)
    print("COMPLETE VOICE-TO-JSON PIPELINE DEMO")
    print("=" * 80)
    
    # Configuration
    config = {
        "mode": "edge",  # Use "cloud" for Cloud Functions, "edge" for local
        "jurisdiction": "KDPA_KE",  # Kenya Data Protection Act
        "enable_logging": True
    }
    
    print("\n📋 Configuration:")
    for key, value in config.items():
        print(f"   {key}: {value}")
    
    # Create sample audio (3 seconds)
    print("\n📢 Creating sample Swahili voice note...")
    audio_data = create_sample_audio(duration_seconds=3.0)
    print(f"   Generated {len(audio_data)} bytes")
    
    # Patient metadata
    metadata = {
        "patient_id": "PATIENT_DEMO_001",
        "location": "Dadaab Refugee Complex, Ifo Camp",
        "chv_id": "CHV_AMINA_HASSAN",
        "consent_token": "DEMO_CONSENT_12345"
    }
    
    print("\n📋 Patient Metadata:")
    for key, value in metadata.items():
        print(f"   {key}: {value}")
    
    # Initialize pipeline
    print("\n🔧 Initializing pipeline...")
    pipeline = VoiceToJSONPipeline(**config)
    
    # Process voice note
    print("\n" + "=" * 80)
    print("PROCESSING VOICE NOTE")
    print("=" * 80)
    
    result = pipeline.process(
        audio_data=audio_data,
        patient_id=metadata["patient_id"],
        location=metadata["location"],
        chv_id=metadata["chv_id"],
        consent_token=metadata["consent_token"]
    )
    
    # Display results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    
    if result.success:
        print("\n✅ Pipeline completed successfully!\n")
        
        # Transcription results
        print("🎤 Transcription:")
        if result.transcription:
            print(f"   Text: {result.transcription.get('text', 'N/A')}")
            print(f"   Confidence: {result.transcription.get('confidence', 0):.2%}")
            print(f"   Time: {result.transcription_time_ms:.2f}ms")
        else:
            print("   No transcription available")
        
        # Symptom extraction results
        print("\n🔬 Extracted Symptoms:")
        if result.symptoms:
            symptoms = result.symptoms.get('symptoms', [])
            print(f"   Count: {len(symptoms)}")
            for symptom in symptoms:
                print(f"   - {symptom['symptom']} ({symptom['severity']})")
            print(f"   Urgency: {result.symptoms.get('urgency', 'N/A')}")
            print(f"   Disease Suspicion: {result.symptoms.get('disease_suspicion', 'None')}")
            print(f"   Time: {result.extraction_time_ms:.2f}ms")
        else:
            print("   No symptoms extracted")
        
        # Golden Thread fusion
        print("\n🧵 Golden Thread Record:")
        if result.golden_thread_record and isinstance(result.golden_thread_record, dict):
            gt = result.golden_thread_record
            print(f"   Record ID: {gt.get('record_id', 'N/A')}")
            print(f"   Verification Score: {gt.get('verification_score', 0):.2f}")
            print(f"   Retention Status: {gt.get('retention_status', 'N/A')}")
            print(f"   Time: {result.fusion_time_ms:.2f}ms")
        else:
            print("   No Golden Thread record available")
        
        # Governance
        print("\n🛡️  Governance:")
        print(f"   Status: {result.governance_status}")
        print(f"   Sovereignty Compliant: {result.sovereignty_compliant}")
        
        # Overall performance
        print(f"\n⏱️  Total Processing Time: {result.total_time_ms:.2f}ms")
        print(f"   Processing Mode: {result.processing_mode}")
        
    else:
        print(f"\n❌ Pipeline failed: {result.error_message}")
    
    # Save full JSON output
    output_file = "demo_output.json"
    result.save_to_file(output_file)
    
    print("\n" + "=" * 80)
    print(f"Full JSON output saved to: {output_file}")
    print("=" * 80)
    
    # Pipeline statistics
    stats = pipeline.get_statistics()
    print("\n📊 Pipeline Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    return result


if __name__ == "__main__":
    result = demo_complete_pipeline()
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)
    
    # Exit with appropriate code
    sys.exit(0 if result.success else 1)
