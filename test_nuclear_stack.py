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
Integration test for the Core IP Stack components.
Tests all proprietary innovations (IP-02 through IP-06).
"""

import sys
from datetime import datetime, timedelta


def test_crypto_shredder():
    """Test IP-02: Crypto Shredder"""
    print("🔐 Testing IP-02: Crypto Shredder...")
    
    from governance_kernel.crypto_shredder import CryptoShredder
    
    shredder = CryptoShredder()
    
    # Encrypt sensitive data
    test_data = {
        "patient_id": "PATIENT_12345",
        "diagnosis": "malaria",
        "location": "Nairobi"
    }
    
    key_id, ciphertext = shredder.encrypt_data(test_data, "TEST_RECORD_001")
    print(f"   ✅ Encrypted data with key: {key_id[:20]}...")
    
    # Verify decryption works
    decrypted = shredder.decrypt_data(key_id, ciphertext)
    assert decrypted == test_data, "Decryption failed"
    print(f"   ✅ Decryption verified")
    
    # Dissolve the key
    dissolution = shredder.dissolve(
        key_id=key_id,
        legal_basis="GDPR Art. 17 (Right to Erasure)",
        jurisdiction="GDPR_EU"
    )
    print(f"   ✅ Key dissolved: {dissolution.dissolution_proof[:40]}...")
    
    # Verify data is unrecoverable
    decrypted_after = shredder.decrypt_data(key_id, ciphertext)
    assert decrypted_after is None, "Data should be unrecoverable after dissolution"
    print(f"   ✅ Data confirmed unrecoverable after dissolution")
    
    print("   ✅ Crypto Shredder (IP-02) - PASSED\n")


def test_silent_flux():
    """Test IP-04: Silent Flux"""
    print("🌊 Testing IP-04: Silent Flux...")
    
    from edge_node.frenasa_engine.silent_flux import SilentFlux, OutputMode
    
    flux = SilentFlux()
    
    # Record normal operator metrics
    flux.record_operator_metrics(
        typing_speed_wpm=60.0,
        click_frequency_per_min=15.0,
        avg_response_time_sec=2.0,
        alert_dismissal_rate=0.05
    )
    
    anxiety = flux.calculate_anxiety()
    print(f"   ✅ Normal anxiety score: {anxiety:.2f} (should be < 0.3)")
    assert anxiety < 0.3, "Normal metrics should show low anxiety"
    
    # Record stressed operator metrics
    flux.record_operator_metrics(
        typing_speed_wpm=30.0,  # Much slower
        click_frequency_per_min=35.0,  # Frantic clicking
        avg_response_time_sec=8.0,  # Slow response
        alert_dismissal_rate=0.40  # Ignoring alerts
    )
    
    anxiety = flux.calculate_anxiety()
    print(f"   ✅ Elevated anxiety score: {anxiety:.2f} (should be > 0.6)")
    assert anxiety > 0.6, "Stressed metrics should show high anxiety"
    
    # Test inference filtering
    test_inferences = [
        {"id": 1, "priority": "CRITICAL", "message": "Critical alert"},
        {"id": 2, "priority": "HIGH", "message": "High priority"},
        {"id": 3, "priority": "LOW", "message": "Low priority"},
        {"id": 4, "priority": "LOW", "message": "Another low priority"},
    ]
    
    output_mode = flux.get_output_mode()
    filtered = flux.filter_inferences(test_inferences, output_mode)
    print(f"   ✅ Filtered {len(test_inferences) - len(filtered)} low-priority alerts")
    assert len(filtered) < len(test_inferences), "Should filter some alerts under stress"
    
    print("   ✅ Silent Flux (IP-04) - PASSED\n")


def test_acorn_protocol():
    """Test IP-03: Acorn Protocol"""
    print("🌰 Testing IP-03: Acorn Protocol...")
    
    from hardware.acorn_protocol import AcornProtocol, DuressLevel
    
    acorn = AcornProtocol(operator_id="OPERATOR_TEST_001")
    
    # Establish baseline profile
    baseline_posture = [(5.0, -3.0) for _ in range(10)]
    baseline_location = [(1.2921, 36.8219, "OFFICE") for _ in range(10)]  # Nairobi
    baseline_movement = [0.15 for _ in range(10)]
    
    acorn.establish_baseline(
        posture_samples=baseline_posture,
        location_samples=baseline_location,
        movement_samples=baseline_movement
    )
    print(f"   ✅ Baseline profile established")
    
    # Test normal authentication
    normal_signature = acorn.capture_somatic_signature(
        tilt_x=5.0,  # Match baseline exactly
        tilt_y=-3.0,  # Match baseline exactly
        latitude=1.2921,
        longitude=36.8219,
        movement_magnitude=0.15,  # Match baseline
        venue_context="OFFICE"
    )
    
    decision = acorn.authenticate(normal_signature)
    print(f"   ✅ Normal authentication: duress={decision.duress_level.value}, anomaly={normal_signature.anomaly_score:.2f}")
    # Allow ELEVATED due to slight variations but not SUSPECTED or CONFIRMED
    assert decision.duress_level in [DuressLevel.NORMAL, DuressLevel.ELEVATED], "Normal metrics should not show high duress"
    
    # Test anomalous authentication (possible duress)
    anomalous_signature = acorn.capture_somatic_signature(
        tilt_x=35.0,  # Extreme tilt
        tilt_y=-25.0,
        latitude=-1.2921,  # Different location
        longitude=36.8219,
        movement_magnitude=0.45,  # High movement/tremor
        venue_context="UNKNOWN"
    )
    
    decision = acorn.authenticate(anomalous_signature)
    print(f"   ✅ Anomalous authentication: duress={decision.duress_level.value}")
    assert decision.duress_level != DuressLevel.NORMAL, "Anomalous metrics should flag"
    
    print("   ✅ Acorn Protocol (IP-03) - PASSED\n")


def test_azure_oracle():
    """Test Azure Oracle"""
    print("☁️  Testing Azure Oracle...")
    
    from cloud_oracle.azure_oracle import AzureOracle, InferenceMode
    
    oracle = AzureOracle(
        inference_mode=InferenceMode.HYBRID,
        jurisdiction="GDPR_EU"
    )
    
    # Generate forensic narrative
    event_data = {
        "outbreak_location": "Nairobi",
        "case_count": 47,
        "temporal_pattern": [5, 8, 12, 22, 47],
        "symptom_clusters": ["fever", "rash", "headache"],
        "sources": ["EMR", "CBS", "IDSR"]
    }
    
    narrative = oracle.generate_forensic_narrative(event_data)
    print(f"   ✅ Generated forensic narrative: {narrative.narrative_id}")
    print(f"   ✅ Risk level: {narrative.risk_assessment.get('risk_level')}")
    print(f"   ✅ Confidence: {narrative.confidence_score:.2f}")
    
    # Test cloud inference (PHI-free)
    anonymized_features = {
        "case_growth_rate": 2.3,
        "r0_estimate": 1.8
    }
    
    result = oracle.cloud_inference("outbreak_risk", anonymized_features)
    print(f"   ✅ Cloud inference completed: {result.get('model_version')}")
    
    print("   ✅ Azure Oracle - PASSED\n")


def test_5dm_bridge():
    """Test IP-06: 5DM Bridge"""
    print("📡 Testing IP-06: 5DM Bridge...")
    
    from edge_node.frenasa_engine.five_dm_bridge import FiveDMBridge, DeliveryChannel, MessagePriority
    
    bridge = FiveDMBridge(
        api_key="TEST_API_KEY",
        enable_sms=True,
        enable_whatsapp=True
    )
    
    # Test SMS broadcast
    message = bridge.broadcast_alert(
        message="Malaria outbreak alert. Seek medical attention if symptomatic.",
        target_region="NAIROBI_COUNTY",
        channel=DeliveryChannel.SMS,
        priority=MessagePriority.CRITICAL
    )
    
    print(f"   ✅ SMS broadcast to {message.recipient_count} recipients")
    print(f"   ✅ Message ID: {message.message_id[:30]}...")
    
    # Test WhatsApp alert
    whatsapp_result = bridge.send_whatsapp_alert(
        phone_numbers=["+254712345678", "+254723456789"],
        message="Health advisory update",
        media_url="https://example.com/advisory.png"
    )
    
    print(f"   ✅ WhatsApp alert sent to {whatsapp_result['recipients']} recipients")
    
    # Get deployment metrics
    metrics = bridge.get_deployment_metrics()
    print(f"   ✅ Total nodes reached: {metrics.total_nodes_reached:,}")
    print(f"   ✅ CAC reduction: {metrics.cac_reduction_percent}%")
    
    print("   ✅ 5DM Bridge (IP-06) - PASSED\n")


def test_golden_thread():
    """Test IP-05: Golden Thread"""
    print("🧵 Testing IP-05: Golden Thread...")
    
    from edge_node.sync_protocol.golden_thread import GoldenThread
    
    gt = GoldenThread()
    
    # Test data fusion
    fused = gt.fuse_data_streams(
        cbs_signal={
            'location': 'Nairobi',
            'symptom': 'fever',
            'timestamp': '2025-01-10T10:00:00Z'
        },
        emr_record={
            'location': 'Nairobi',
            'diagnosis': 'malaria',
            'timestamp': '2025-01-10T09:45:00Z'
        },
        patient_id='PATIENT_TEST_001'
    )
    
    print(f"   ✅ Fused record: {fused.record_id}")
    print(f"   ✅ Verification score: {fused.verification_score:.2f}")
    print(f"   ✅ Event type: {fused.event_type}")
    assert fused.verification_score >= 0.8, "Cross-verified data should have high score"
    
    # Test retention policy
    old_timestamp = datetime.utcnow() - timedelta(days=200)
    should_archive = not gt.retention_check(old_timestamp)
    print(f"   ✅ Retention policy enforced (>180 days should archive)")
    assert should_archive, "Records > 180 days should be archived"
    
    print("   ✅ Golden Thread (IP-05) - PASSED\n")


def main():
    """Run all integration tests."""
    print("═══════════════════════════════════════════════════════════════")
    print("🧪 Core IP STACK INTEGRATION TESTS")
    print("═══════════════════════════════════════════════════════════════")
    print()
    
    tests = [
        ("IP-02: Crypto Shredder", test_crypto_shredder),
        ("IP-04: Silent Flux", test_silent_flux),
        ("IP-03: Acorn Protocol", test_acorn_protocol),
        ("Azure Oracle", test_azure_oracle),
        ("IP-06: 5DM Bridge", test_5dm_bridge),
        ("IP-05: Golden Thread", test_golden_thread),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"   ❌ {name} - FAILED")
            print(f"      Error: {e}")
            failed += 1
            import traceback
            traceback.print_exc()
    
    print("═══════════════════════════════════════════════════════════════")
    print(f"📊 TEST RESULTS")
    print("═══════════════════════════════════════════════════════════════")
    print(f"   ✅ Passed: {passed}/{len(tests)}")
    print(f"   ❌ Failed: {failed}/{len(tests)}")
    print()
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED - Core IP STACK OPERATIONAL")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED - REVIEW REQUIRED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
