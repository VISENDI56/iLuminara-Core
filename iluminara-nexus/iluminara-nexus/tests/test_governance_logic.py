import unittest
from modules.validator import validate_input
from modules.governance import GovernanceKernel
from modules.state_manager import StateManager
import os

class TestILuminaraCore(unittest.TestCase):
    
    def setUp(self):
        """Setup a clean test environment."""
        self.gov = GovernanceKernel()
        # Use a temporary state file for testing
        self.sm = StateManager(file_path="iluminara-nexus/audit/test_state.json")

    def test_data_integrity_regex(self):
        """Phase 4.1: Verify location whitelist enforcement (Nairobi should fail)."""
        bad_data = {
            "source_id": "TEST-OP",
            "location": "Nairobi", # Invalid camp zone
            "symptom_code": "COLD-01",
            "severity_score": 2
        }
        is_valid, errors = validate_input(bad_data)
        self.assertFalse(is_valid, "System should reject non-camp locations.")

    def test_governance_certification(self):
        """Phase 2.1: Verify every decision generates a Policy Anchor."""
        cert = self.gov.certify_decision("Drone_Launch", 0.9, ["REFUGEE_PROTECTION"])
        self.assertIn("policy_anchor", cert)
        self.assertTrue(cert["policy_anchor"].startswith("1951 Refugee"), "Policy must anchor to international law.")

    def test_state_persistence(self):
        """Phase 0.1: Verify state survives a reboot cycle."""
        self.sm.update_mode("ACTIVE")
        # Simulate reboot by creating a new manager pointed at the same file
        new_sm = StateManager(file_path="iluminara-nexus/audit/test_state.json")
        self.assertEqual(new_sm.state["system_mode"], "ACTIVE", "State must persist across reboots.")

    def tearDown(self):
        """Clean up test artifacts."""
        if os.path.exists("iluminara-nexus/audit/test_state.json"):
            os.remove("iluminara-nexus/audit/test_state.json")

if __name__ == "__main__":
    unittest.main()
