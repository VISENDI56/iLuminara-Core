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
PubSub Alerts Testing Script
═════════════════════════════════════════════════════════════════════════════

Demonstrates monitoring real-time alerts from the iLuminara system.

Simulates the command:
  gcloud pubsub subscriptions pull luminara-alerts-subscription --limit=5
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cloud_oracle.pubsub_alerts import AlertSubscriber, AlertPublisher


def test_pubsub_monitoring():
    """Test PubSub alert monitoring (pull-based)."""
    print("═" * 80)
    print("iLuminara PubSub Alert Monitoring Test")
    print("═" * 80)
    print("")
    
    # Initialize subscriber
    print("Initializing alert subscriber...")
    subscriber = AlertSubscriber()
    print(f"Subscription: {subscriber.subscription_path}")
    print("")
    
    # Pull alerts
    print("Pulling recent alerts (limit=5)...")
    print("-" * 80)
    
    alerts = subscriber.pull_alerts(max_messages=5)
    
    if not alerts:
        print("No alerts available.")
    else:
        print(f"Retrieved {len(alerts)} alert(s):")
        print("")
        
        for i, alert in enumerate(alerts, 1):
            print(f"Alert {i}:")
            print(f"  ID:        {alert.get('alert_id')}")
            print(f"  Type:      {alert.get('alert_type')}")
            print(f"  Severity:  {alert.get('severity')}")
            print(f"  Timestamp: {alert.get('timestamp')}")
            print(f"  Location:  {alert.get('location')}")
            
            if 'data' in alert:
                print(f"  Data:")
                for key, value in alert['data'].items():
                    print(f"    {key}: {value}")
            
            print("")
    
    print("-" * 80)
    print("")


def test_alert_publishing():
    """Test publishing alerts to PubSub."""
    print("═" * 80)
    print("iLuminara Alert Publishing Test")
    print("═" * 80)
    print("")
    
    # Initialize publisher
    print("Initializing alert publisher...")
    publisher = AlertPublisher()
    print(f"Topic: {publisher.topic_path}")
    print("")
    
    # Test 1: Outbreak alert
    print("Test 1: Publishing outbreak prediction alert...")
    print("-" * 80)
    
    outbreak_result = {
        "z_score": 3.2,
        "risk_level": "HIGH",
        "location": {"lat": 0.512, "lng": 40.3129},
        "disease_likelihood": [
            {"disease": "cholera", "confidence": 0.85}
        ],
        "bond_status": "ALERT",
        "population_at_risk": 125000,
        "recommendations": [
            "HIGH ALERT: Increase surveillance in affected area",
            "Pre-position medical supplies and personnel"
        ],
        "requires_immediate_action": False,
        "confidence_score": 0.78
    }
    
    message_id = publisher.publish_outbreak_alert(outbreak_result)
    print(f"✓ Published outbreak alert: {message_id}")
    print("")
    
    # Test 2: Voice alert
    print("Test 2: Publishing voice processing alert...")
    print("-" * 80)
    
    voice_result = {
        "alert_level": "CRITICAL",
        "location": {"lat": 0.512, "lng": 40.3129},
        "symptoms": ["diarrhea", "vomiting", "dehydration"],
        "severity": 9,
        "transcription": "Patient reporting severe watery diarrhea and vomiting",
        "language_detected": "swahili",
        "recommendations": [
            "IMMEDIATE: Suspected cholera. Start ORS immediately."
        ],
        "source": "CHV Voice Alert",
        "processing_time_ms": 4200
    }
    
    message_id = publisher.publish_voice_alert(voice_result)
    print(f"✓ Published voice alert: {message_id}")
    print("")
    
    # Test 3: Custom alert
    print("Test 3: Publishing custom alert...")
    print("-" * 80)
    
    message_id = publisher.publish_alert(
        alert_type="bond_trigger",
        severity="CRITICAL",
        location={"lat": 0.512, "lng": 40.3129},
        data={
            "z_score": 4.5,
            "threshold": 2.576,
            "bond_status": "PAYOUT_RELEASED",
            "estimated_payout": "$2,500,000"
        },
        metadata={
            "trigger_timestamp": datetime.utcnow().isoformat() + "Z",
            "node_id": "JOR-47"
        }
    )
    print(f"✓ Published bond trigger alert: {message_id}")
    print("")
    
    print("=" * 80)
    print("Alert Publishing Test Complete")
    print("=" * 80)
    print("")


def main():
    """Main test runner."""
    print("")
    print("iLuminara PubSub Testing")
    print("")
    
    # Check if running in simulation mode
    import cloud_oracle.pubsub_alerts as pubsub_module
    if not pubsub_module.PUBSUB_AVAILABLE:
        print("⚠ WARNING: google-cloud-pubsub not installed")
        print("  Running in SIMULATION MODE")
        print("  To enable real PubSub:")
        print("    pip install google-cloud-pubsub")
        print("    export GOOGLE_CLOUD_PROJECT=your-project-id")
        print("")
    
    # Run tests
    try:
        test_alert_publishing()
        print("")
        test_pubsub_monitoring()
        
        print("")
        print("✓ All tests completed successfully!")
        print("")
        print("To monitor alerts in production:")
        print("  gcloud pubsub subscriptions pull luminara-alerts-subscription --limit=5")
        print("")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
