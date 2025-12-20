"""
Tests for AI Agents Module
═════════════════════════════════════════════════════════════════════════════

Comprehensive tests for offline AI agents with federated learning capabilities.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edge_node.ai_agents import (
    BaseAgent,
    AgentCapability,
    AgentStatus,
    OfflineAgent,
    FederatedLearningClient,
    AgentRegistry,
)


class TestBaseAgent(unittest.TestCase):
    """Tests for BaseAgent base class."""
    
    def setUp(self):
        """Set up test agent."""
        class TestAgent(BaseAgent):
            def _execute_operation(self, operation):
                return {"result": "test_success"}
        
        self.TestAgent = TestAgent
        self.agent = TestAgent(
            name="Test Agent",
            capabilities=[AgentCapability.OFFLINE_OPERATION],
        )
    
    def test_agent_initialization(self):
        """Test agent initialization."""
        self.assertEqual(self.agent.metadata.name, "Test Agent")
        self.assertEqual(self.agent.status, AgentStatus.OFFLINE)
        self.assertIn(AgentCapability.OFFLINE_OPERATION, self.agent.get_capabilities())
    
    def test_queue_operation(self):
        """Test operation queuing."""
        op_id = self.agent.queue_operation("test_op", {"data": "test"})
        self.assertIsNotNone(op_id)
        self.assertEqual(len(self.agent.operation_queue), 1)
    
    def test_execute_queued_operations(self):
        """Test executing queued operations."""
        self.agent.queue_operation("test_op", {"data": "test1"})
        self.agent.queue_operation("test_op", {"data": "test2"})
        
        results = self.agent.execute_queued_operations()
        self.assertEqual(results["successful"], 2)
        self.assertEqual(results["failed"], 0)
    
    def test_local_state_management(self):
        """Test local state save/load."""
        self.agent.save_local_state("key1", "value1")
        loaded = self.agent.load_local_state("key1")
        self.assertEqual(loaded, "value1")
    
    def test_capability_check(self):
        """Test capability checking."""
        self.assertTrue(
            self.agent.has_capability(AgentCapability.OFFLINE_OPERATION)
        )
        self.assertFalse(
            self.agent.has_capability(AgentCapability.FEDERATED_LEARNING)
        )


class TestOfflineAgent(unittest.TestCase):
    """Tests for OfflineAgent."""
    
    def setUp(self):
        """Set up test offline agent."""
        self.agent = OfflineAgent(
            name="Offline Test Agent",
            capabilities=[
                AgentCapability.OFFLINE_OPERATION,
                AgentCapability.AUTONOMOUS_INFERENCE,
            ],
        )
    
    def test_offline_initialization(self):
        """Test offline agent initialization."""
        self.assertEqual(self.agent.status, AgentStatus.OFFLINE)
        self.assertIsNotNone(self.agent.connectivity)
        self.assertIsNotNone(self.agent.sync_queue)
    
    def test_inference_operation(self):
        """Test inference operation."""
        self.agent.queue_operation("inference", {
            "patient_id": "123",
            "symptoms": ["fever", "cough"],
        })
        
        results = self.agent.execute_queued_operations()
        self.assertEqual(results["successful"], 1)
        
        # Check sync queue
        self.assertEqual(self.agent.sync_queue.get_stats()["pending"], 1)
    
    def test_data_collection(self):
        """Test data collection operation."""
        self.agent.queue_operation("data_collection", {
            "sensor": "temperature",
            "value": 37.5,
        })
        
        results = self.agent.execute_queued_operations()
        self.assertEqual(results["successful"], 1)
    
    def test_connectivity_handling(self):
        """Test connectivity management."""
        # Start offline
        self.assertFalse(self.agent.connectivity.is_connected)
        
        # Go online
        self.agent.connectivity.set_connectivity(True)
        self.assertTrue(self.agent.connectivity.is_connected)
        
        # Sync to cloud
        self.agent.queue_operation("inference", {"data": "test"})
        self.agent.execute_queued_operations()
        
        sync_result = self.agent.sync_to_cloud()
        self.assertEqual(sync_result["status"], "completed")
        self.assertGreater(sync_result["synced"], 0)
    
    def test_offline_to_online_transition(self):
        """Test offline to online transition."""
        # Queue operations while offline
        self.agent.queue_operation("inference", {"id": "1"})
        self.agent.queue_operation("inference", {"id": "2"})
        self.agent.execute_queued_operations()
        
        # Verify operations queued for sync
        self.assertGreater(self.agent.sync_queue.get_stats()["pending"], 0)
        
        # Go online and sync
        self.agent.connectivity.set_connectivity(True)
        sync_result = self.agent.sync_to_cloud()
        
        self.assertEqual(sync_result["status"], "completed")
        self.assertEqual(self.agent.sync_queue.get_stats()["completed"], 2)


class TestFederatedLearningClient(unittest.TestCase):
    """Tests for FederatedLearningClient."""
    
    def setUp(self):
        """Set up test federated learning client."""
        self.client = FederatedLearningClient(
            name="FL Test Client",
            epsilon=1.0,
            delta=1e-5,
        )
    
    def test_fl_initialization(self):
        """Test federated learning client initialization."""
        self.assertIn(
            AgentCapability.FEDERATED_LEARNING,
            self.client.get_capabilities()
        )
        self.assertIn(
            AgentCapability.PRIVACY_PRESERVING,
            self.client.get_capabilities()
        )
        self.assertIsNotNone(self.client.privacy)
    
    def test_local_training(self):
        """Test local model training."""
        training_data = [
            {"features": [1, 2, 3], "label": 0},
            {"features": [4, 5, 6], "label": 1},
        ]
        
        result = self.client.train_local_model(training_data, epochs=1)
        
        self.assertEqual(result["samples"], 2)
        self.assertEqual(result["epochs"], 1)
        self.assertIn("metrics", result)
        self.assertIsNotNone(self.client.local_model)
    
    def test_model_update_generation(self):
        """Test privacy-preserving model update generation."""
        # Train first
        training_data = [{"features": [1, 2], "label": 0}]
        self.client.train_local_model(training_data)
        
        # Generate update
        update = self.client.get_model_update(apply_privacy=True)
        
        self.assertIn("gradients", update)
        self.assertTrue(update["privacy_applied"])
        self.assertIn("privacy_params", update)
        self.assertEqual(update["privacy_params"]["epsilon"], 1.0)
    
    def test_global_model_application(self):
        """Test applying global model."""
        global_model = {
            "round": 5,
            "parameters": {"layer1": [0.1, 0.2], "layer2": [0.3, 0.4]},
        }
        
        result = self.client.apply_global_model(global_model)
        
        self.assertEqual(result["status"], "applied")
        self.assertEqual(result["global_round"], 5)
        self.assertIsNotNone(self.client.local_model)
    
    def test_differential_privacy(self):
        """Test differential privacy mechanisms."""
        gradients = [1.0, 2.0, 3.0, 4.0, 5.0]
        
        # Test gradient clipping
        clipped = self.client.privacy.clip_gradients(gradients, max_norm=1.0)
        self.assertIsNotNone(clipped)
        
        # Test noise addition
        noised = self.client.privacy.add_noise(gradients, sensitivity=1.0)
        self.assertEqual(len(noised), len(gradients))
        # Verify noise was added (values should differ)
        self.assertNotEqual(noised, gradients)
    
    def test_privacy_accounting(self):
        """Test privacy budget tracking."""
        # Train multiple rounds
        training_data = [{"features": [1], "label": 0}]
        
        for _ in range(3):
            self.client.train_local_model(training_data)
            self.client.get_model_update(apply_privacy=True)
        
        privacy_spent = self.client.compute_privacy_spent()
        
        self.assertEqual(privacy_spent["total_rounds"], 3)
        self.assertEqual(privacy_spent["total_epsilon_spent"], 3.0)
    
    def test_model_validation(self):
        """Test model validation."""
        # Train first
        training_data = [{"features": [1], "label": 0}]
        self.client.train_local_model(training_data)
        
        # Validate
        validation_data = [{"features": [2], "label": 1}]
        result = self.client.validate_model(validation_data)
        
        self.assertIn("metrics", result)
        self.assertIn("accuracy", result["metrics"])


class TestAgentRegistry(unittest.TestCase):
    """Tests for AgentRegistry."""
    
    def setUp(self):
        """Set up test registry and agents."""
        self.registry = AgentRegistry()
        
        self.agent1 = OfflineAgent(
            name="Agent 1",
            capabilities=[
                AgentCapability.OFFLINE_OPERATION,
                AgentCapability.AUTONOMOUS_INFERENCE,
            ],
            tags=["health", "surveillance"],
        )
        
        self.agent2 = FederatedLearningClient(
            name="Agent 2",
            tags=["health", "ml"],
        )
    
    def test_agent_registration(self):
        """Test agent registration."""
        success = self.registry.register(self.agent1)
        self.assertTrue(success)
        self.assertEqual(self.registry.get_agent_count(), 1)
        
        # Try duplicate registration
        success = self.registry.register(self.agent1)
        self.assertFalse(success)
        self.assertEqual(self.registry.get_agent_count(), 1)
    
    def test_search_by_capabilities(self):
        """Test capability-based search."""
        self.registry.register(self.agent1)
        self.registry.register(self.agent2)
        
        # Search for offline operation
        results = self.registry.search_by_capabilities([
            AgentCapability.OFFLINE_OPERATION
        ])
        self.assertEqual(len(results), 2)  # Both have offline capability
        
        # Search for federated learning
        results = self.registry.search_by_capabilities([
            AgentCapability.FEDERATED_LEARNING
        ])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].metadata.name, "Agent 2")
    
    def test_search_by_tags(self):
        """Test tag-based search."""
        self.registry.register(self.agent1)
        self.registry.register(self.agent2)
        
        # Search for health tag
        results = self.registry.search_by_tags(["health"])
        self.assertEqual(len(results), 2)
        
        # Search for surveillance tag
        results = self.registry.search_by_tags(["surveillance"])
        self.assertEqual(len(results), 1)
    
    def test_search_by_name(self):
        """Test name-based search."""
        self.registry.register(self.agent1)
        self.registry.register(self.agent2)
        
        results = self.registry.search_by_name("Agent 1")
        self.assertEqual(len(results), 1)
        
        # Case insensitive search
        results = self.registry.search_by_name("agent", case_sensitive=False)
        self.assertEqual(len(results), 2)
    
    def test_advanced_search(self):
        """Test advanced multi-criteria search."""
        self.registry.register(self.agent1)
        self.registry.register(self.agent2)
        
        # Search with multiple criteria
        results = self.registry.advanced_search(
            capabilities=[AgentCapability.OFFLINE_OPERATION],
            tags=["health"],
        )
        self.assertEqual(len(results), 2)
        
        # More specific search
        results = self.registry.advanced_search(
            capabilities=[AgentCapability.FEDERATED_LEARNING],
            tags=["ml"],
        )
        self.assertEqual(len(results), 1)
    
    def test_registry_summary(self):
        """Test registry summary generation."""
        self.registry.register(self.agent1)
        self.registry.register(self.agent2)
        
        summary = self.registry.get_registry_summary()
        
        self.assertEqual(summary["total_agents"], 2)
        self.assertIn("capability_distribution", summary)
        self.assertIn("status_distribution", summary)
        self.assertIn("agents", summary)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBaseAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestOfflineAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestFederatedLearningClient))
    suite.addTests(loader.loadTestsFromTestCase(TestAgentRegistry))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
