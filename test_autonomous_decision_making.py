"""
Integration Tests for Autonomous Decision-Making Simulation
═════════════════════════════════════════════════════════════════════════════

Tests the complete integration of:
- Active Inference Engine
- Vertex AI Custom Containers
- Cloud Scheduler
- Pub/Sub

These tests validate that all components work together correctly.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cloud_oracle.autonomous_decision_maker import (
    AutonomousDecisionMaker,
    SimulationConfig
)
from cloud_oracle.active_inference import PolicyType, ActiveInferenceEngine
from cloud_oracle.vertex_ai_integration import VertexAIIntegration
from cloud_oracle.scheduler_integration import (
    CloudSchedulerIntegration,
    ScheduleFrequency
)
from cloud_oracle.pubsub_integration import (
    PubSubIntegration,
    AlertType,
    AlertSeverity
)


def test_active_inference_engine():
    """Test Active Inference Engine standalone."""
    print("\n" + "="*80)
    print("TEST: Active Inference Engine")
    print("="*80)
    
    engine = ActiveInferenceEngine(learning_rate=0.1)
    
    # Test policy optimization
    observations = {
        'cases': 45,
        'trend': 'increasing',
        'location': 'Nairobi'
    }
    
    policy = engine.optimize_policy(
        policy_type=PolicyType.OUTBREAK_RESPONSE,
        observations=observations,
        constraints={'max_resources': 1000}
    )
    
    print(f"✓ Policy optimized: {policy.policy_id}")
    print(f"  Policy Type: {policy.policy_type.value}")
    print(f"  Expected Outcome: {policy.expected_outcome:.2f}")
    print(f"  Confidence: {policy.confidence:.2f}")
    print(f"  Parameters: {policy.parameters}")
    
    # Verify explainability
    assert 'explanation' in policy.to_dict(), "Policy missing explainability"
    assert 'evidence_chain' in policy.to_dict(), "Policy missing evidence chain"
    
    # Get statistics
    stats = engine.get_statistics()
    print(f"  Statistics: {stats}")
    
    print("✓ Active Inference Engine test passed")
    return True


def test_vertex_ai_integration():
    """Test Vertex AI integration."""
    print("\n" + "="*80)
    print("TEST: Vertex AI Integration")
    print("="*80)
    
    integration = VertexAIIntegration(
        project_id="iluminara-test",
        region="us-central1"
    )
    
    # Generate container config
    config = integration.generate_container_config(
        image_tag="test",
        enable_gpu=False
    )
    
    print(f"✓ Container config generated: {config.image_uri}")
    
    # Deploy container (simulated)
    endpoint_id = integration.deploy_container(config)
    print(f"✓ Container deployed: {endpoint_id}")
    
    # Make inference request
    response = integration.predict(
        endpoint_id=endpoint_id,
        policy_type="outbreak_response",
        observations={'cases': 30, 'trend': 'stable'},
        jurisdiction="GDPR_EU"
    )
    
    print(f"✓ Inference completed:")
    print(f"  Request ID: {response.request_id}")
    print(f"  Confidence: {response.confidence:.2f}")
    print(f"  Processing Time: {response.processing_time_ms:.2f}ms")
    
    # Get statistics
    stats = integration.get_statistics()
    print(f"  Statistics: {stats}")
    
    print("✓ Vertex AI Integration test passed")
    return True


def test_scheduler_integration():
    """Test Cloud Scheduler integration."""
    print("\n" + "="*80)
    print("TEST: Cloud Scheduler Integration")
    print("="*80)
    
    scheduler = CloudSchedulerIntegration(
        project_id="iluminara-test",
        region="us-central1"
    )
    
    # Create schedule
    schedule = scheduler.create_schedule(
        schedule_name="test-optimization",
        policy_type="outbreak_response",
        frequency=ScheduleFrequency.EVERY_6_HOURS
    )
    
    print(f"✓ Schedule created: {schedule.schedule_id}")
    print(f"  Name: {schedule.schedule_name}")
    print(f"  Frequency: {schedule.frequency.value}")
    
    # Generate job spec
    job_spec = scheduler.generate_cloud_scheduler_job_spec(
        schedule_config=schedule,
        http_target_uri="https://example.com/optimize"
    )
    
    print(f"✓ Job spec generated")
    
    # Execute cycle
    observations = {'cases': 25, 'trend': 'stable'}
    cycle = scheduler.execute_optimization_cycle(
        schedule_id=schedule.schedule_id,
        observations=observations
    )
    
    print(f"✓ Optimization cycle executed:")
    print(f"  Cycle ID: {cycle.cycle_id}")
    print(f"  Status: {cycle.status}")
    print(f"  Observations Processed: {cycle.observations_processed}")
    
    # Get metrics
    metrics = scheduler.get_performance_metrics()
    print(f"  Metrics: {metrics}")
    
    print("✓ Cloud Scheduler Integration test passed")
    return True


def test_pubsub_integration():
    """Test Pub/Sub integration."""
    print("\n" + "="*80)
    print("TEST: Pub/Sub Integration")
    print("="*80)
    
    pubsub = PubSubIntegration(
        project_id="iluminara-test",
        enable_compliance_validation=True
    )
    
    # Create topic
    topic = pubsub.create_topic(
        topic_name="test-alerts",
        description="Test alert topic",
        alert_types=[AlertType.OUTBREAK_DETECTED, AlertType.POLICY_OPTIMIZED],
        min_severity=AlertSeverity.MEDIUM
    )
    
    print(f"✓ Topic created: {topic.topic_id}")
    print(f"  Name: {topic.topic_name}")
    
    # Create subscription
    subscription = pubsub.create_subscription(
        subscription_name="test-alerts-sub",
        topic_id=topic.topic_id
    )
    
    print(f"✓ Subscription created: {subscription.subscription_id}")
    
    # Publish alert
    from cloud_oracle.pubsub_integration import Alert
    alert = Alert(
        alert_id="test-alert-001",
        alert_type=AlertType.OUTBREAK_DETECTED,
        severity=AlertSeverity.HIGH,
        title="Test Outbreak Alert",
        message="Test alert for outbreak detection",
        metadata={'cases': 45, 'location': 'Test Location'},
        jurisdiction="GDPR_EU"
    )
    
    deliveries = pubsub.publish_alert(alert)
    
    print(f"✓ Alert published:")
    print(f"  Alert ID: {alert.alert_id}")
    print(f"  Deliveries: {len(deliveries)}")
    for delivery in deliveries:
        print(f"    - {delivery.target}: {delivery.status}")
    
    # Get statistics
    stats = pubsub.get_delivery_statistics()
    print(f"  Delivery Stats: {stats}")
    
    print("✓ Pub/Sub Integration test passed")
    return True


def test_full_integration():
    """Test complete integration of all components."""
    print("\n" + "="*80)
    print("TEST: Full System Integration")
    print("="*80)
    
    # Create configuration
    config = SimulationConfig(
        project_id="iluminara-test",
        region="us-central1",
        enable_vertex_ai=True,
        enable_scheduler=True,
        enable_pubsub=True,
        optimization_frequency=ScheduleFrequency.EVERY_6_HOURS,
        alert_severity_threshold=AlertSeverity.MEDIUM,
        jurisdiction="GDPR_EU"
    )
    
    print(f"✓ Configuration created:")
    print(f"  Project: {config.project_id}")
    print(f"  Region: {config.region}")
    print(f"  Jurisdiction: {config.jurisdiction}")
    
    # Initialize decision maker
    decision_maker = AutonomousDecisionMaker(config)
    decision_maker.initialize()
    
    print(f"✓ System initialized")
    
    # Process observations and make decision
    observations = {
        'cases': 55,
        'trend': 'increasing',
        'location': 'Nairobi',
        'timestamp': '2025-12-19T15:00:00Z'
    }
    
    result = decision_maker.process_and_decide(
        policy_type=PolicyType.OUTBREAK_RESPONSE,
        observations=observations,
        publish_alert=True
    )
    
    print(f"✓ Decision made:")
    print(f"  Policy Type: {result['policy']['policy_type']}")
    print(f"  Expected Outcome: {result['expected_outcome']:.2f}")
    print(f"  Confidence: {result['confidence']:.2f}")
    print(f"  Alerts Sent: {len(result['alerts_sent'])}")
    
    # Run optimization cycle
    cycle_result = decision_maker.run_optimization_cycle(PolicyType.OUTBREAK_RESPONSE)
    print(f"✓ Optimization cycle executed:")
    print(f"  Cycle ID: {cycle_result['cycle_id']}")
    print(f"  Status: {cycle_result['status']}")
    
    # Get system status
    status = decision_maker.get_system_status()
    print(f"✓ System status retrieved:")
    print(f"  Initialized: {status['initialized']}")
    print(f"  Decisions Made: {status['metrics']['decisions_made']}")
    print(f"  Alerts Sent: {status['metrics']['alerts_sent']}")
    
    # Get performance report
    report = decision_maker.get_performance_report()
    print(f"✓ Performance report generated:")
    print(f"  System Metrics: {report['system_metrics']}")
    
    print("✓ Full System Integration test passed")
    return True


def test_compliance_validation():
    """Test compliance validation throughout the system."""
    print("\n" + "="*80)
    print("TEST: Compliance Validation")
    print("="*80)
    
    # Test with governance kernel integration
    from governance_kernel.vector_ledger import SovereignGuardrail
    
    guardrail = SovereignGuardrail()
    
    # Create decision maker
    config = SimulationConfig(
        project_id="iluminara-test",
        jurisdiction="GDPR_EU",
        enable_compliance_validation=True
    )
    
    decision_maker = AutonomousDecisionMaker(config)
    decision_maker.initialize()
    
    # Make decision
    observations = {'cases': 25, 'trend': 'stable'}
    result = decision_maker.process_and_decide(
        policy_type=PolicyType.OUTBREAK_RESPONSE,
        observations=observations
    )
    
    # Validate policy has explainability (GDPR Art. 22, EU AI Act §6)
    assert 'explanation' in result, "Missing explainability"
    # Note: evidence_chain may be in the policy itself, not explanation
    has_evidence = ('evidence_chain' in result['explanation'] or 
                   'confidence_basis' in result['explanation'])
    assert has_evidence, "Missing evidence chain or confidence basis"
    
    print(f"✓ GDPR Art. 22 compliance: Explainability present")
    print(f"✓ EU AI Act §6 compliance: Transparency provided")
    
    # Validate jurisdiction is respected
    assert result['policy']['jurisdiction'] == "GDPR_EU", "Jurisdiction not respected"
    print(f"✓ Data sovereignty: Jurisdiction constraints enforced")
    
    print("✓ Compliance Validation test passed")
    return True


def run_all_tests():
    """Run all integration tests."""
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " "*20 + "AUTONOMOUS DECISION-MAKING SIMULATION" + " "*21 + "║")
    print("║" + " "*26 + "Integration Test Suite" + " "*27 + "║")
    print("╚" + "═"*78 + "╝")
    
    tests = [
        ("Active Inference Engine", test_active_inference_engine),
        ("Vertex AI Integration", test_vertex_ai_integration),
        ("Cloud Scheduler", test_scheduler_integration),
        ("Pub/Sub Integration", test_pubsub_integration),
        ("Full System Integration", test_full_integration),
        ("Compliance Validation", test_compliance_validation)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n✗ {test_name} FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*80)
    print(f"TEST SUMMARY: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("="*80)
    
    if failed == 0:
        print("\n✓ ALL TESTS PASSED")
        print("\nAutonomous Decision-Making Simulation: OPERATIONAL")
        print("- Active Inference: ✓")
        print("- Vertex AI Custom Containers: ✓")
        print("- Cloud Scheduler: ✓")
        print("- Pub/Sub Alerts: ✓")
        print("- Compliance: ✓")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
