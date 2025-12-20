"""
AI Agents Example: Offline Operation with Federated Learning
═════════════════════════════════════════════════════════════════════════════

Demonstrates AI agents designed for offline operation, intermittent connectivity,
and edge-to-cloud synchronization with privacy-preserving federated learning.

Usage:
    python examples/offline_agents_demo.py
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edge_node.ai_agents import (
    OfflineAgent,
    FederatedLearningClient,
    AgentRegistry,
    AgentCapability,
)


def print_section(title: str):
    """Print section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def demo_offline_agent():
    """Demonstrate offline agent capabilities."""
    print_section("DEMO 1: Offline Agent with Intermittent Connectivity")
    
    # Create offline agent
    agent = OfflineAgent(
        name="Health Surveillance Agent",
        capabilities=[
            AgentCapability.OFFLINE_OPERATION,
            AgentCapability.AUTONOMOUS_INFERENCE,
        ],
        tags=["health", "surveillance", "edge"],
        description="Autonomous agent for health surveillance in remote areas",
    )
    
    print("✅ Created offline agent")
    print(f"   Name: {agent.metadata.name}")
    print(f"   Status: {agent.status.value}")
    print(f"   Capabilities: {[c.value for c in agent.get_capabilities()]}")
    
    # Simulate offline operations
    print("\n📡 OFFLINE MODE: Queuing operations...")
    
    # Queue inference operations
    agent.queue_operation("inference", {
        "patient_id": "P001",
        "symptoms": ["fever", "cough", "fatigue"],
        "temperature": 38.5,
    })
    
    agent.queue_operation("inference", {
        "patient_id": "P002",
        "symptoms": ["headache", "nausea"],
        "temperature": 37.8,
    })
    
    agent.queue_operation("data_collection", {
        "sensor_type": "temperature",
        "location": "Dadaab Refugee Camp",
        "readings": [37.2, 37.5, 38.1, 37.9],
    })
    
    print(f"   Queued operations: {len(agent.operation_queue)}")
    
    # Execute operations offline
    print("\n⚙️  Executing queued operations (offline)...")
    results = agent.execute_queued_operations()
    print(f"   ✓ Successful: {results['successful']}")
    print(f"   ✗ Failed: {results['failed']}")
    
    # Check sync queue
    sync_stats = agent.sync_queue.get_stats()
    print(f"\n📊 Sync Queue Status:")
    print(f"   Pending syncs: {sync_stats['pending']}")
    print(f"   Completed syncs: {sync_stats['completed']}")
    
    # Simulate connectivity becomes available
    print("\n🌐 CONNECTIVITY RESTORED")
    agent.connectivity.set_connectivity(True)
    print("   Status: ONLINE")
    
    # Sync to cloud
    print("\n☁️  Syncing to cloud...")
    sync_result = agent.sync_to_cloud()
    print(f"   Status: {sync_result['status']}")
    print(f"   Synced items: {sync_result['synced']}")
    print(f"   Failed items: {sync_result['failed']}")
    
    # Show final status
    print("\n📈 Final Status:")
    status = agent.get_status()
    print(f"   Agent status: {status['status']}")
    print(f"   Queued operations: {status['queued_operations']}")
    print(f"   Local state size: {status['local_state_size']}")


def demo_federated_learning():
    """Demonstrate federated learning client."""
    print_section("DEMO 2: Privacy-Preserving Federated Learning")
    
    # Create federated learning clients
    client1 = FederatedLearningClient(
        name="FL Client - Hospital A",
        epsilon=1.0,
        delta=1e-5,
        tags=["health", "hospital", "kenya"],
        description="Federated learning client at Hospital A",
    )
    
    client2 = FederatedLearningClient(
        name="FL Client - Clinic B",
        epsilon=1.0,
        delta=1e-5,
        tags=["health", "clinic", "kenya"],
        description="Federated learning client at Clinic B",
    )
    
    print("✅ Created 2 federated learning clients")
    print(f"   Client 1: {client1.metadata.name}")
    print(f"   Client 2: {client2.metadata.name}")
    
    # Simulate local training (data never leaves the device)
    print("\n🔒 LOCAL TRAINING (Data stays on device)")
    
    # Client 1 trains on local data
    print("\n   Client 1: Training on local data...")
    training_data_1 = [
        {"features": [1.2, 2.3, 3.1], "label": 0},
        {"features": [4.5, 5.2, 6.1], "label": 1},
        {"features": [2.1, 3.4, 4.2], "label": 0},
    ]
    result1 = client1.train_local_model(training_data_1, epochs=5)
    print(f"      Samples: {result1['samples']}")
    print(f"      Loss: {result1['metrics']['loss']:.3f}")
    print(f"      Accuracy: {result1['metrics']['accuracy']:.3f}")
    
    # Client 2 trains on local data
    print("\n   Client 2: Training on local data...")
    training_data_2 = [
        {"features": [1.8, 2.9, 3.5], "label": 0},
        {"features": [5.1, 6.2, 7.0], "label": 1},
    ]
    result2 = client2.train_local_model(training_data_2, epochs=5)
    print(f"      Samples: {result2['samples']}")
    print(f"      Loss: {result2['metrics']['loss']:.3f}")
    print(f"      Accuracy: {result2['metrics']['accuracy']:.3f}")
    
    # Generate privacy-preserving model updates
    print("\n🔐 GENERATING PRIVACY-PRESERVING UPDATES")
    print("   (Only gradients shared, NOT raw data)")
    
    update1 = client1.get_model_update(apply_privacy=True)
    print(f"\n   Client 1 Update:")
    print(f"      Privacy applied: {update1['privacy_applied']}")
    print(f"      Epsilon: {update1['privacy_params']['epsilon']}")
    print(f"      Delta: {update1['privacy_params']['delta']}")
    print(f"      Gradients (with noise): {update1['gradients'][:3]}...")
    
    update2 = client2.get_model_update(apply_privacy=True)
    print(f"\n   Client 2 Update:")
    print(f"      Privacy applied: {update2['privacy_applied']}")
    print(f"      Gradients (with noise): {update2['gradients'][:3]}...")
    
    # Simulate aggregation server combining updates
    print("\n📊 AGGREGATING UPDATES (Simulated)")
    print("   In production: Secure multi-party computation")
    
    # Create aggregated model
    global_model = {
        "round": 1,
        "parameters": {
            "layer1_weights": [0.25, -0.15, 0.35],
            "layer2_weights": [0.12, 0.28, -0.08],
        },
        "contributors": 2,
    }
    
    # Apply global model to clients
    print("\n🔄 APPLYING GLOBAL MODEL")
    client1.apply_global_model(global_model)
    client2.apply_global_model(global_model)
    print("   ✓ Both clients updated with aggregated model")
    
    # Privacy accounting
    print("\n🔍 PRIVACY ACCOUNTING")
    privacy1 = client1.compute_privacy_spent()
    print(f"   Client 1:")
    print(f"      Training rounds: {privacy1['total_rounds']}")
    print(f"      Total epsilon spent: {privacy1['total_epsilon_spent']:.2f}")
    print(f"      Budget exhausted: {privacy1['privacy_budget_exhausted']}")
    
    privacy2 = client2.compute_privacy_spent()
    print(f"   Client 2:")
    print(f"      Training rounds: {privacy2['total_rounds']}")
    print(f"      Total epsilon spent: {privacy2['total_epsilon_spent']:.2f}")
    
    print("\n✅ Federated learning complete!")
    print("   - Raw data stayed on devices")
    print("   - Privacy guarantees maintained")
    print("   - Model improved through collaboration")


def demo_agent_registry():
    """Demonstrate agent registry and search."""
    print_section("DEMO 3: Agent Registry & Discovery")
    
    # Create registry
    registry = AgentRegistry()
    print("✅ Created agent registry")
    
    # Create diverse agents
    agent1 = OfflineAgent(
        name="Edge Surveillance Agent",
        capabilities=[
            AgentCapability.OFFLINE_OPERATION,
            AgentCapability.AUTONOMOUS_INFERENCE,
        ],
        tags=["surveillance", "edge", "remote"],
    )
    
    agent2 = FederatedLearningClient(
        name="Hospital ML Agent",
        tags=["hospital", "ml", "privacy"],
    )
    
    agent3 = OfflineAgent(
        name="Field Data Collector",
        capabilities=[
            AgentCapability.OFFLINE_OPERATION,
            AgentCapability.LOCAL_STORAGE,
        ],
        tags=["data", "field", "remote"],
    )
    
    # Register agents
    print("\n📝 Registering agents...")
    registry.register(agent1)
    registry.register(agent2)
    registry.register(agent3)
    
    # Search by capabilities
    print("\n🔍 SEARCH BY CAPABILITIES")
    print("\n   Query: Agents with OFFLINE_OPERATION capability")
    results = registry.search_by_capabilities([AgentCapability.OFFLINE_OPERATION])
    print(f"   Found {len(results)} agents:")
    for agent in results:
        print(f"      - {agent.metadata.name}")
    
    print("\n   Query: Agents with FEDERATED_LEARNING capability")
    results = registry.search_by_capabilities([AgentCapability.FEDERATED_LEARNING])
    print(f"   Found {len(results)} agents:")
    for agent in results:
        print(f"      - {agent.metadata.name}")
    
    # Search by tags
    print("\n🏷️  SEARCH BY TAGS")
    print("\n   Query: Agents tagged with 'remote'")
    results = registry.search_by_tags(["remote"])
    print(f"   Found {len(results)} agents:")
    for agent in results:
        print(f"      - {agent.metadata.name}")
    
    # Advanced search
    print("\n🎯 ADVANCED SEARCH")
    print("\n   Query: Offline agents for remote deployment")
    results = registry.advanced_search(
        capabilities=[AgentCapability.OFFLINE_OPERATION],
        tags=["remote"],
    )
    print(f"   Found {len(results)} agents:")
    for agent in results:
        print(f"      - {agent.metadata.name}")
        print(f"        Capabilities: {len(agent.get_capabilities())}")
        print(f"        Tags: {', '.join(agent.metadata.tags)}")
    
    # Registry summary
    print("\n📊 REGISTRY SUMMARY")
    summary = registry.get_registry_summary()
    print(f"   Total agents: {summary['total_agents']}")
    print(f"\n   Capability distribution:")
    for cap, count in summary['capability_distribution'].items():
        print(f"      {cap}: {count}")
    print(f"\n   Status distribution:")
    for status, count in summary['status_distribution'].items():
        print(f"      {status}: {count}")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 80)
    print("  iLuminara AI Agents: Offline Operation & Federated Learning Demo")
    print("=" * 80)
    print("\n  Demonstrating AI agents designed for:")
    print("  ✓ Offline operation")
    print("  ✓ Intermittent connectivity")
    print("  ✓ Edge-to-cloud synchronization")
    print("  ✓ Privacy-preserving federated learning")
    print("  ✓ Agent discovery and matching")
    
    # Run demonstrations
    demo_offline_agent()
    time.sleep(1)
    
    demo_federated_learning()
    time.sleep(1)
    
    demo_agent_registry()
    
    # Final message
    print("\n" + "=" * 80)
    print("  Demo Complete!")
    print("=" * 80)
    print("\n  Key Features Demonstrated:")
    print("  1. Offline agents continue operating without connectivity")
    print("  2. Operations queue and sync when connectivity returns")
    print("  3. Federated learning enables collaborative model training")
    print("  4. Privacy guarantees protect individual data")
    print("  5. Agent registry enables capability-based discovery")
    print("\n  Philosophy: 'Sovereign agents operate with dignity even in digital darkness.'")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
