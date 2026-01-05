import unittest
from core.governance.kernel import govern

class TestGovernance(unittest.TestCase):
    def test_decision_provenance(self):
        record = govern(
            inputs={"x":1},
            constraints={"human_safety": True},
            outcome={"y":1},
            policy_refs={"law":"1.0"}
        )
        self.assertIn("decision_id", record)
        self.assertTrue(record["constraints_applied"]["human_safety"])

if __name__ == "__main__":
    unittest.main()
