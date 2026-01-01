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
Dadaab Test Scenario - CHV Voice Alert Processing
═════════════════════════════════════════════════════════════════════════════

Tests the voice processing endpoint with a realistic Dadaab scenario:
- Swahili language input
- Multiple children with diarrhea
- Specific water point location
- GPS coordinates

Scenario: "watero watatu, tumbo la kuhara, eneo la maji W-B12"
Translation: "three children, diarrhea, water point W-B12"
Location: 0.4221°N, 40.2255°E
Time: 10:23 AM
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from edge_node.frenasa_engine.voice_processor import VoiceProcessor
from cloud_oracle.outbreak_predictor import OutbreakPredictor
from cloud_oracle.pubsub_alerts import AlertPublisher


def test_dadaab_scenario():
    """Test the Dadaab CHV scenario."""
    print("═" * 80)
    print("Dadaab Test Scenario - CHV Voice Alert Processing")
    print("═" * 80)
    print("")
    
    # Scenario details
    scenario = {
        "transcription": "watero watatu, tumbo la kuhara, eneo la maji W-B12",
        "translation": "three children, diarrhea, water point W-B12",
        "location": {
            "lat": 0.4221,
            "lng": 40.2255
        },
        "time": "10:23 AM",
        "language": "swahili"
    }
    
    print("📋 Scenario Details:")
    print(f"  Original (Swahili): {scenario['transcription']}")
    print(f"  Translation: {scenario['translation']}")
    print(f"  Location: {scenario['location']['lat']}°N, {scenario['location']['lng']}°E")
    print(f"  Time: {scenario['time']}")
    print("")
    
    # Initialize components
    voice_processor = VoiceProcessor()
    outbreak_predictor = OutbreakPredictor()
    alert_publisher = AlertPublisher()
    
    # Step 1: Process voice alert
    print("Step 1: Voice Processing")
    print("-" * 80)
    
    # Simulate audio data
    simulated_audio = b"SIMULATED_AUDIO_DATA" * 100  # Simulate audio bytes
    
    voice_result = voice_processor.process_audio(
        audio_data=simulated_audio,
        language=scenario['language'],
        location=scenario['location'],
        transcription_override=scenario['transcription']
    )
    
    print(f"✓ Status: {voice_result['status']}")
    print(f"✓ Symptoms detected: {voice_result['symptoms']}")
    print(f"✓ Severity: {voice_result['severity']}/10")
    print(f"✓ Alert level: {voice_result['alert_level']}")
    print(f"✓ Processing time: {voice_result['processing_time_ms']:.2f}ms")
    print("")
    print("Recommendations:")
    for i, rec in enumerate(voice_result['recommendations'], 1):
        print(f"  {i}. {rec}")
    print("")
    
    # Step 2: Outbreak prediction
    print("Step 2: Outbreak Risk Assessment")
    print("-" * 80)
    
    prediction_result = outbreak_predictor.predict(
        location=scenario['location'],
        symptoms=voice_result['symptoms'],
        population=None  # Will use estimated population
    )
    
    print(f"✓ Z-score: {prediction_result['z_score']:.2f}")
    print(f"✓ Risk level: {prediction_result['risk_level']}")
    print(f"✓ Bond status: {prediction_result['bond_status']}")
    print(f"✓ Alert level: {prediction_result['alert_level']}")
    print(f"✓ Location: {prediction_result['location_name']}")
    print(f"✓ Population at risk: {prediction_result['population_at_risk']:,}")
    print("")
    
    if prediction_result['disease_likelihood']:
        print("Disease Likelihood:")
        for disease in prediction_result['disease_likelihood'][:3]:
            print(f"  • {disease['disease'].capitalize()}: {disease['confidence']:.1%} confidence")
            print(f"    Matching symptoms: {', '.join(disease['matching_symptoms'])}")
        print("")
    
    # Step 3: Geographic risk analysis
    print("Step 3: Geographic Risk Analysis")
    print("-" * 80)
    
    geo_risk = prediction_result['geographic_risk']
    print(f"✓ Distance to high-risk area: {geo_risk['distance_to_high_risk_area_km']:.1f} km")
    print(f"✓ In outbreak zone: {geo_risk['in_known_outbreak_zone']}")
    print("")
    print("Risk factors:")
    for factor in geo_risk['risk_factors']:
        if factor:
            print(f"  • {factor}")
    print("")
    
    # Step 4: Extract urgency indicators
    print("Step 4: Urgency Assessment")
    print("-" * 80)
    
    urgency_indicators = {
        "multiple_patients": "watero watatu" in scenario['transcription'],  # three children
        "acute_symptoms": "tumbo la kuhara" in scenario['transcription'],  # diarrhea
        "water_point_reference": "eneo la maji" in scenario['transcription'],  # water point
        "high_severity": voice_result['severity'] >= 7,
        "critical_alert": voice_result['alert_level'] in ['CRITICAL', 'ALERT'],
        "requires_immediate_action": prediction_result['requires_immediate_action']
    }
    
    urgency_score = sum(urgency_indicators.values())
    urgency_level = (
        "CRITICAL" if urgency_score >= 5 else
        "HIGH" if urgency_score >= 3 else
        "MEDIUM" if urgency_score >= 2 else
        "LOW"
    )
    
    print(f"✓ Urgency level: {urgency_level} ({urgency_score}/6 indicators)")
    print("")
    print("Urgency indicators:")
    for indicator, present in urgency_indicators.items():
        status = "✓" if present else "✗"
        print(f"  {status} {indicator.replace('_', ' ').title()}")
    print("")
    
    # Step 5: Response protocol
    print("Step 5: Response Protocol Activation")
    print("-" * 80)
    
    protocols = []
    
    if urgency_indicators['multiple_patients']:
        protocols.append("CLUSTER INVESTIGATION: Multiple patients detected")
    
    if urgency_indicators['water_point_reference']:
        protocols.append("WATER SAFETY: Water point W-B12 requires immediate testing")
    
    if "diarrhea" in voice_result['symptoms']:
        protocols.append("CHOLERA PROTOCOL: ORS distribution and isolation facilities")
    
    if prediction_result['risk_level'] in ['HIGH', 'CRITICAL']:
        protocols.append("OUTBREAK RESPONSE: Activate rapid response team")
    
    if urgency_level in ['CRITICAL', 'HIGH']:
        protocols.append("NOTIFICATION: Alert district health officer immediately")
    
    print("Activated protocols:")
    for i, protocol in enumerate(protocols, 1):
        print(f"  {i}. {protocol}")
    print("")
    
    # Step 6: Alert publishing
    print("Step 6: Alert Publishing")
    print("-" * 80)
    
    if voice_result['alert_level'] in ['CRITICAL', 'ALERT']:
        voice_alert_id = alert_publisher.publish_voice_alert(voice_result)
        print(f"✓ Voice alert published: {voice_alert_id}")
    
    if prediction_result['risk_level'] in ['HIGH', 'CRITICAL']:
        outbreak_alert_id = alert_publisher.publish_outbreak_alert(prediction_result)
        print(f"✓ Outbreak alert published: {outbreak_alert_id}")
    
    print("")
    
    # Summary
    print("=" * 80)
    print("Test Summary")
    print("=" * 80)
    print("")
    print(f"✓ Scenario: Dadaab CHV report - {scenario['translation']}")
    print(f"✓ Symptoms extracted: {', '.join(voice_result['symptoms'])}")
    print(f"✓ Urgency level: {urgency_level}")
    print(f"✓ Risk level: {prediction_result['risk_level']}")
    print(f"✓ Response protocols: {len(protocols)} activated")
    print(f"✓ Processing time: Voice {voice_result['processing_time_ms']:.2f}ms + Prediction {prediction_result['processing_time_ms']:.2f}ms")
    print("")
    print("✅ Test scenario completed successfully!")
    print("")
    
    # Return results for further processing
    return {
        "voice_result": voice_result,
        "prediction_result": prediction_result,
        "urgency_level": urgency_level,
        "protocols": protocols,
        "scenario": scenario
    }


if __name__ == "__main__":
    print("")
    try:
        results = test_dadaab_scenario()
        sys.exit(0)
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
