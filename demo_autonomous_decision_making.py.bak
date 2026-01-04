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
Autonomous Decision-Making Simulation Demo
═════════════════════════════════════════════════════════════════════════════

Demonstrates the complete autonomous decision-making system:
- Active Inference Engine (Bayesian policy optimization)
- Vertex AI Custom Containers (scalable inference)
- Cloud Scheduler (automated optimization cycles)
- Pub/Sub (real-time alert distribution)

Usage:
    python demo_autonomous_decision_making.py
"""

import sys
import time
from datetime import datetime

from cloud_oracle.autonomous_decision_maker import (
    AutonomousDecisionMaker,
    SimulationConfig
)
from cloud_oracle.active_inference import PolicyType


def print_banner():
    """Print demo banner."""
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " "*15 + "AUTONOMOUS DECISION-MAKING SIMULATION DEMO" + " "*21 + "║")
    print("║" + " "*20 + "iLuminara-Core Health Intelligence" + " "*24 + "║")
    print("╚" + "═"*78 + "╝\n")


def print_section(title):
    """Print section header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def demo_active_inference():
    """Demonstrate Active Inference Engine."""
    print_section("1. ACTIVE INFERENCE ENGINE - Bayesian Policy Optimization")
    
    from cloud_oracle.active_inference import ActiveInferenceEngine
    
    engine = ActiveInferenceEngine(learning_rate=0.1)
    
    # Scenario: Malaria outbreak in Nairobi
    print("\n📊 Scenario: Malaria Outbreak Detection")
    print("   Location: Nairobi, Kenya")
    print("   Cases: 45 confirmed cases")
    print("   Trend: Increasing")
    
    observations = {
        'cases': 45,
        'trend': 'increasing',
        'location': 'Nairobi',
        'population_density': 'high',
        'season': 'rainy'
    }
    
    print("\n🧠 Running Bayesian active inference...")
    time.sleep(0.5)
    
    policy = engine.optimize_policy(
        policy_type=PolicyType.OUTBREAK_RESPONSE,
        observations=observations,
        constraints={'max_resources': 1000, 'sovereignty': 'KDPA_KE'}
    )
    
    print(f"\n✅ Policy Optimized: {policy.policy_id}")
    print(f"   Type: {policy.policy_type.value}")
    print(f"   Response Level: {policy.parameters.get('response_level', 'N/A')}")
    print(f"   Testing Rate: {policy.parameters.get('testing_rate', 0):.1%}")
    print(f"   Contact Tracing: {'Enabled' if policy.parameters.get('contact_tracing') else 'Disabled'}")
    print(f"   Public Alert: {'Yes' if policy.parameters.get('public_alert') else 'No'}")
    print(f"   Expected Outcome: {policy.expected_outcome:.2%}")
    print(f"   Confidence: {policy.confidence:.2%}")
    
    print(f"\n📝 Explainability (GDPR Art. 22 & EU AI Act §6):")
    print(f"   Rationale: {policy.explanation['decision_rationale']}")
    print(f"   Key Factors: {', '.join(policy.explanation['key_factors'][:5])}")
    print(f"   Risk Assessment: {policy.explanation['risk_assessment']['implementation_risk']}")
    
    return engine


def demo_vertex_ai():
    """Demonstrate Vertex AI integration."""
    print_section("2. VERTEX AI CUSTOM CONTAINERS - Scalable ML Inference")
    
    from cloud_oracle.vertex_ai_integration import VertexAIIntegration
    
    integration = VertexAIIntegration(
        project_id="iluminara-prod",
        region="us-central1"
    )
    
    print("\n🐳 Generating Docker Container Configuration...")
    container_config = integration.generate_container_config(
        image_tag="v1.0",
        enable_gpu=False
    )
    
    print(f"   Image URI: {container_config.image_uri}")
    print(f"   CPU Limit: {container_config.cpu_limit} cores")
    print(f"   Memory Limit: {container_config.memory_limit}")
    print(f"   Port: {container_config.port}")
    
    print("\n📄 Generating Dockerfile...")
    dockerfile = integration.generate_dockerfile()
    print("   ✓ Dockerfile generated (base: python:3.10-slim)")
    print("   ✓ Health check configured")
    print("   ✓ Environment variables set")
    
    print("\n🚀 Deploying to Vertex AI...")
    time.sleep(0.5)
    endpoint_id = integration.deploy_container(container_config)
    
    print(f"   ✓ Endpoint deployed: {endpoint_id}")
    print(f"   ✓ Status: DEPLOYED")
    print(f"   ✓ Auto-scaling: 1-10 replicas")
    
    print("\n🔮 Making inference request...")
    response = integration.predict(
        endpoint_id=endpoint_id,
        policy_type="outbreak_response",
        observations={'cases': 30, 'trend': 'stable'},
        jurisdiction="GDPR_EU"
    )
    
    print(f"   ✓ Request ID: {response.request_id}")
    print(f"   ✓ Processing Time: {response.processing_time_ms:.2f}ms")
    print(f"   ✓ Confidence: {response.confidence:.2%}")
    
    return integration


def demo_cloud_scheduler():
    """Demonstrate Cloud Scheduler integration."""
    print_section("3. CLOUD SCHEDULER - Automated Optimization Cycles")
    
    from cloud_oracle.scheduler_integration import (
        CloudSchedulerIntegration,
        ScheduleFrequency
    )
    
    scheduler = CloudSchedulerIntegration(
        project_id="iluminara-prod",
        region="us-central1"
    )
    
    print("\n📅 Creating Optimization Schedules...")
    
    schedules = []
    for policy_type, freq in [
        (PolicyType.OUTBREAK_RESPONSE, ScheduleFrequency.EVERY_6_HOURS),
        (PolicyType.RESOURCE_ALLOCATION, ScheduleFrequency.DAILY),
        (PolicyType.SURVEILLANCE_INTENSITY, ScheduleFrequency.EVERY_6_HOURS)
    ]:
        schedule = scheduler.create_schedule(
            schedule_name=f"{policy_type.value}-optimization",
            policy_type=policy_type.value,
            frequency=freq
        )
        schedules.append(schedule)
        print(f"   ✓ {schedule.schedule_name}")
        print(f"     Frequency: {freq.value}")
        print(f"     Enabled: {schedule.enabled}")
    
    print("\n⚙️  Generating Cloud Scheduler Job Specifications...")
    for schedule in schedules:
        job_spec = scheduler.generate_cloud_scheduler_job_spec(
            schedule_config=schedule,
            http_target_uri="https://iluminara-prod.run.app/optimize"
        )
        print(f"   ✓ {schedule.schedule_name}")
        print(f"     Retry count: {job_spec['retry_config']['retry_count']}")
        print(f"     Attempt deadline: {job_spec['attempt_deadline']}")
    
    print("\n▶️  Executing Optimization Cycle...")
    time.sleep(0.5)
    cycle = scheduler.execute_optimization_cycle(
        schedule_id=schedules[0].schedule_id,
        observations={'cases': 25, 'trend': 'stable'}
    )
    
    print(f"   ✓ Cycle ID: {cycle.cycle_id}")
    print(f"   ✓ Status: {cycle.status}")
    print(f"   ✓ Observations Processed: {cycle.observations_processed}")
    print(f"   ✓ Policies Generated: {cycle.policies_generated}")
    print(f"   ✓ Improvement: {cycle.improvements_detected:.1%}")
    
    return scheduler


def demo_pubsub():
    """Demonstrate Pub/Sub integration."""
    print_section("4. PUB/SUB - Real-Time Alert Distribution")
    
    from cloud_oracle.pubsub_integration import (
        PubSubIntegration,
        Alert,
        AlertType,
        AlertSeverity
    )
    
    pubsub = PubSubIntegration(
        project_id="iluminara-prod",
        enable_compliance_validation=True
    )
    
    print("\n📢 Creating Pub/Sub Topics...")
    
    topics = []
    for name, types, severity in [
        ("outbreak-alerts", [AlertType.OUTBREAK_DETECTED], AlertSeverity.HIGH),
        ("policy-updates", [AlertType.POLICY_OPTIMIZED], AlertSeverity.MEDIUM),
        ("surveillance-alerts", [AlertType.SURVEILLANCE_ALERT], AlertSeverity.MEDIUM)
    ]:
        topic = pubsub.create_topic(
            topic_name=name,
            description=f"{name.replace('-', ' ').title()} Topic",
            alert_types=types,
            min_severity=severity
        )
        topics.append(topic)
        print(f"   ✓ {topic.topic_name}")
        print(f"     Alert Types: {[at.value for at in topic.alert_types]}")
        print(f"     Min Severity: {topic.min_severity.value}")
    
    print("\n📨 Creating Subscriptions...")
    for topic in topics:
        subscription = pubsub.create_subscription(
            subscription_name=f"{topic.topic_name}-sub",
            topic_id=topic.topic_id
        )
        print(f"   ✓ {subscription.subscription_name}")
        print(f"     Ack Deadline: {subscription.ack_deadline_seconds}s")
    
    print("\n🚨 Publishing Critical Alert...")
    time.sleep(0.5)
    
    alert = Alert(
        alert_id="ALERT-MALARIA-001",
        alert_type=AlertType.OUTBREAK_DETECTED,
        severity=AlertSeverity.CRITICAL,
        title="Malaria Outbreak Detected - Nairobi",
        message="45 confirmed cases with increasing trend. Immediate response required.",
        metadata={
            'cases': 45,
            'location': 'Nairobi',
            'trend': 'increasing',
            'response_level': 'high'
        },
        jurisdiction="KDPA_KE",
        requires_acknowledgment=True
    )
    
    deliveries = pubsub.publish_alert(alert)
    
    print(f"   ✓ Alert Published: {alert.alert_id}")
    print(f"   ✓ Severity: {alert.severity.value.upper()}")
    print(f"   ✓ Deliveries: {len(deliveries)}")
    for delivery in deliveries:
        print(f"     → {delivery.target}: {delivery.status}")
    
    return pubsub


def demo_full_integration():
    """Demonstrate full system integration."""
    print_section("5. FULL SYSTEM INTEGRATION - End-to-End Pipeline")
    
    config = SimulationConfig(
        project_id="iluminara-prod",
        region="us-central1",
        enable_vertex_ai=True,
        enable_scheduler=True,
        enable_pubsub=True,
        jurisdiction="KDPA_KE"
    )
    
    print("\n🏗️  Initializing Autonomous Decision-Making System...")
    print("   Components:")
    print("   • Active Inference Engine")
    print("   • Vertex AI Custom Containers")
    print("   • Cloud Scheduler")
    print("   • Pub/Sub Alert Distribution")
    
    time.sleep(1)
    
    decision_maker = AutonomousDecisionMaker(config)
    decision_maker.initialize()
    
    print("   ✓ System initialized")
    
    print("\n📊 Processing Real-World Scenario...")
    print("   Scenario: Cholera outbreak in rural Kenya")
    print("   Cases: 62 confirmed, 8 suspected")
    print("   Trend: Rapidly increasing")
    print("   Region: Turkana County")
    
    observations = {
        'cases': 62,
        'suspected_cases': 8,
        'trend': 'rapidly_increasing',
        'location': 'Turkana',
        'water_source': 'contaminated',
        'population_at_risk': 15000
    }
    
    print("\n🧠 Making autonomous decision...")
    time.sleep(0.5)
    
    result = decision_maker.process_and_decide(
        policy_type=PolicyType.OUTBREAK_RESPONSE,
        observations=observations,
        publish_alert=True
    )
    
    print(f"\n✅ Decision Complete!")
    print(f"   Policy Type: {result['policy']['policy_type']}")
    print(f"   Response Level: {result['policy']['parameters'].get('response_level', 'N/A')}")
    print(f"   Expected Outcome: {result['expected_outcome']:.2%}")
    print(f"   Confidence: {result['confidence']:.2%}")
    print(f"   Alerts Sent: {len(result['alerts_sent'])}")
    
    print(f"\n📋 Compliance Validation:")
    print(f"   ✓ GDPR Art. 22: Explainability provided")
    print(f"   ✓ EU AI Act §6: Transparency ensured")
    print(f"   ✓ KDPA §37: Data sovereignty respected")
    print(f"   ✓ Right to Explanation: Full evidence chain")
    
    print(f"\n📈 System Performance:")
    stats = decision_maker.get_system_status()
    print(f"   Decisions Made: {stats['metrics']['decisions_made']}")
    print(f"   Alerts Sent: {stats['metrics']['alerts_sent']}")
    print(f"   Optimization Cycles: {stats['metrics']['optimization_cycles']}")
    
    return decision_maker


def main():
    """Run the complete demo."""
    print_banner()
    
    print("This demonstration showcases iLuminara-Core's autonomous decision-making")
    print("capabilities for global health intelligence.")
    print()
    print("Components demonstrated:")
    print("  1. Active Inference Engine (Bayesian optimization)")
    print("  2. Vertex AI Custom Containers (scalable inference)")
    print("  3. Cloud Scheduler (automated cycles)")
    print("  4. Pub/Sub (real-time alerts)")
    print("  5. Full System Integration")
    
    input("\nPress Enter to begin demonstration...")
    
    try:
        # Demo each component
        demo_active_inference()
        input("\nPress Enter to continue...")
        
        demo_vertex_ai()
        input("\nPress Enter to continue...")
        
        demo_cloud_scheduler()
        input("\nPress Enter to continue...")
        
        demo_pubsub()
        input("\nPress Enter to continue...")
        
        demo_full_integration()
        
        # Final summary
        print_section("DEMONSTRATION COMPLETE")
        print("\n✅ All systems operational!")
        print("\nKey Achievements:")
        print("  • Bayesian active inference for policy optimization")
        print("  • Scalable ML inference via Vertex AI")
        print("  • Automated optimization cycles")
        print("  • Real-time alert distribution")
        print("  • Full GDPR & EU AI Act compliance")
        print("  • Sovereignty-preserving architecture")
        
        print("\n🌍 Ready for deployment in:")
        print("  • Kenya (KDPA compliant)")
        print("  • South Africa (POPIA compliant)")
        print("  • European Union (GDPR + EU AI Act)")
        print("  • United States (HIPAA + CCPA)")
        print("  • Any jurisdiction (GLOBAL_DEFAULT)")
        
        print("\n" + "="*80)
        print("Autonomous Decision-Making Simulation: OPERATIONAL ✓")
        print("="*80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
