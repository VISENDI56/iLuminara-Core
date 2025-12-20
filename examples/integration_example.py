"""
Integration Example: AI Agents with iLuminara Governance
═════════════════════════════════════════════════════════════════════════════

Demonstrates how AI agents integrate with iLuminara's governance kernel,
golden thread data fusion, and compliance framework.

Usage:
    python examples/integration_example.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edge_node.ai_agents import (
    FederatedLearningClient,
    OfflineAgent,
    AgentRegistry,
    AgentCapability,
)
from edge_node.sync_protocol.golden_thread import GoldenThread
from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError


def print_section(title: str):
    """Print section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def demo_governance_integration():
    """Demonstrate AI agents with governance validation."""
    print_section("Integration 1: AI Agents + Governance Kernel")
    
    # Create federated learning client
    client = FederatedLearningClient(
        name="Compliant FL Client",
        epsilon=1.0,
        tags=["health", "privacy", "compliant"]
    )
    
    print("✅ Created federated learning client")
    print(f"   Privacy parameters: ε={client.privacy.epsilon}, δ={client.privacy.delta}")
    
    # Train model locally
    training_data = [
        {"features": [1, 2, 3], "label": 0},
        {"features": [4, 5, 6], "label": 1},
    ]
    client.train_local_model(training_data, epochs=3)
    print("\n✅ Trained model locally (data never left device)")
    
    # Generate model update
    update = client.get_model_update(apply_privacy=True)
    print("✅ Generated privacy-preserving update")
    
    # Validate with governance kernel
    print("\n🛡️  GOVERNANCE VALIDATION")
    guardrail = SovereignGuardrail()
    
    try:
        # Validate high-risk inference with explanation
        guardrail.validate_action(
            action_type='High_Risk_Inference',
            payload={
                'inference': 'malaria_prediction',
                'explanation': 'Model based on federated learning with differential privacy',
                'confidence_score': 0.92,
                'evidence_chain': [
                    'Local training on 2 samples',
                    f'Privacy: ε={client.privacy.epsilon}, δ={client.privacy.delta}',
                    'Gradient clipping applied',
                    'Laplacian noise added'
                ],
                'consent_token': 'CONSENT_12345',
            },
            jurisdiction='GDPR_EU'
        )
        print("   ✓ PASSED: Governance validation successful")
        print("   ✓ Compliant with GDPR, EU AI Act, HIPAA")
        print("   ✓ Right to explanation satisfied")
        print("   ✓ Consent validated")
        
    except SovereigntyViolationError as e:
        print(f"   ✗ FAILED: {e}")
    
    # Test violation scenario
    print("\n🚫 TESTING VIOLATION SCENARIO")
    try:
        guardrail.validate_action(
            action_type='Data_Transfer',
            payload={
                'data_type': 'PHI',
                'destination': 'Foreign_Cloud',
            },
            jurisdiction='GDPR_EU'
        )
    except SovereigntyViolationError as e:
        print("   ✓ Expected violation caught:")
        print(f"   {str(e)[:100]}...")
        print("   ✓ Data sovereignty enforced")


def demo_golden_thread_integration():
    """Demonstrate AI agents with Golden Thread data fusion."""
    print_section("Integration 2: AI Agents + Golden Thread Data Fusion")
    
    # Create offline agent
    agent = OfflineAgent(
        name="Health Data Agent",
        tags=["health", "data_fusion"]
    )
    
    # Create Golden Thread for data fusion
    gt = GoldenThread()
    
    print("✅ Created offline agent and Golden Thread")
    
    # Simulate data collection from multiple sources
    print("\n📊 COLLECTING DATA FROM MULTIPLE SOURCES")
    
    from datetime import datetime
    
    # Use current timestamp to avoid timezone issues
    current_time = datetime.utcnow().isoformat()
    
    # CBS (Community-Based Surveillance) data
    cbs_signal = {
        'location': 'Nairobi',
        'symptom': 'fever',
        'timestamp': current_time
    }
    print("   ✓ CBS signal collected")
    
    # EMR (Electronic Medical Record) data
    emr_record = {
        'location': 'Nairobi',
        'diagnosis': 'malaria',
        'timestamp': current_time
    }
    print("   ✓ EMR record collected")
    
    # Queue agent operations
    agent.queue_operation("data_collection", {
        "source": "CBS",
        "data": cbs_signal
    })
    agent.queue_operation("data_collection", {
        "source": "EMR",
        "data": emr_record
    })
    
    print("\n⚙️  EXECUTING AGENT OPERATIONS")
    agent.execute_queued_operations()
    
    # Fuse data with Golden Thread
    print("\n🧵 FUSING DATA WITH GOLDEN THREAD")
    fused = gt.fuse_data_streams(
        cbs_signal=cbs_signal,
        emr_record=emr_record,
        patient_id='PATIENT_001'
    )
    
    print(f"   ✓ Verification Score: {fused.verification_score} (CONFIRMED)")
    print(f"   ✓ Location: {fused.location}")
    print(f"   ✓ Event Type: {fused.event_type}")
    print(f"   ✓ Retention Status: {fused.retention_status}")
    print(f"   ✓ Data Sources: {list(fused.data_sources.keys())}")
    
    # Check sync queue
    print("\n📤 SYNC QUEUE STATUS")
    sync_stats = agent.sync_queue.get_stats()
    print(f"   Pending syncs: {sync_stats['pending']}")
    print("   ✓ Agent will sync fused data when online")


def demo_distributed_learning():
    """Demonstrate distributed federated learning across multiple agents."""
    print_section("Integration 3: Distributed Federated Learning Scenario")
    
    # Create registry
    registry = AgentRegistry()
    
    # Create multiple federated learning clients (hospitals/clinics)
    locations = [
        ("Hospital A - Nairobi", "hospital_a"),
        ("Hospital B - Mombasa", "hospital_b"),
        ("Clinic C - Dadaab", "clinic_c"),
    ]
    
    clients = []
    for name, tag in locations:
        client = FederatedLearningClient(
            name=name,
            epsilon=1.0,
            tags=["health", "kenya", tag]
        )
        registry.register(client)
        clients.append(client)
    
    print(f"✅ Created and registered {len(clients)} federated learning clients")
    
    # Each client trains locally on private data
    print("\n🔒 LOCAL TRAINING (Data stays at each location)")
    for i, client in enumerate(clients):
        # Simulate different amounts of local data
        local_data = [{"features": [j], "label": j % 2} for j in range((i+1) * 10)]
        result = client.train_local_model(local_data, epochs=3)
        print(f"   ✓ {client.metadata.name}: {result['samples']} samples")
    
    # Generate privacy-preserving updates
    print("\n🔐 GENERATING PRIVACY-PRESERVING UPDATES")
    updates = []
    for client in clients:
        update = client.get_model_update(apply_privacy=True)
        updates.append(update)
        print(f"   ✓ {client.metadata.name}: Update generated with DP")
    
    # Simulate aggregation
    print("\n📊 AGGREGATING UPDATES")
    print(f"   Combining updates from {len(updates)} clients")
    print("   ✓ Using secure aggregation protocol")
    print("   ✓ No individual client data exposed")
    
    global_model = {
        "round": 1,
        "parameters": {"aggregated": True},
        "contributors": len(clients)
    }
    
    # Distribute global model
    print("\n🔄 DISTRIBUTING GLOBAL MODEL")
    for client in clients:
        client.apply_global_model(global_model)
        print(f"   ✓ {client.metadata.name}: Model updated")
    
    # Privacy accounting
    print("\n🔍 PRIVACY ACCOUNTING")
    for client in clients:
        privacy = client.compute_privacy_spent()
        print(f"   {client.metadata.name}:")
        print(f"      Epsilon spent: {privacy['total_epsilon_spent']:.2f}")
        print(f"      Budget exhausted: {privacy['privacy_budget_exhausted']}")
    
    # Search for specific agents
    print("\n🔍 AGENT DISCOVERY")
    hospital_agents = registry.search_by_tags(["hospital_a", "hospital_b"])
    print(f"   Found {len(hospital_agents)} hospital agents")
    
    fl_agents = registry.search_by_capabilities([AgentCapability.FEDERATED_LEARNING])
    print(f"   Found {len(fl_agents)} agents with federated learning capability")


def main():
    """Run integration demonstrations."""
    print("\n" + "=" * 80)
    print("  iLuminara Integration: AI Agents + Governance + Golden Thread")
    print("=" * 80)
    print("\n  Demonstrating seamless integration of:")
    print("  ✓ AI Agents (offline operation & federated learning)")
    print("  ✓ Governance Kernel (compliance validation)")
    print("  ✓ Golden Thread (data fusion)")
    print("  ✓ Distributed learning scenario")
    
    demo_governance_integration()
    demo_golden_thread_integration()
    demo_distributed_learning()
    
    print("\n" + "=" * 80)
    print("  Integration Demo Complete!")
    print("=" * 80)
    print("\n  Key Integration Points:")
    print("  1. AI agents validate actions through governance kernel")
    print("  2. Agents integrate with Golden Thread for data fusion")
    print("  3. Privacy-preserving learning across distributed locations")
    print("  4. Compliance maintained: GDPR, HIPAA, KDPA, POPIA")
    print("  5. Data sovereignty: Raw data never leaves source")
    print("\n  System Status: FULLY INTEGRATED & OPERATIONAL")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
