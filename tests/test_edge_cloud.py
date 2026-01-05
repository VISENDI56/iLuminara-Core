import unittest
from core.edge.inference import infer

class TestEdgeCloudParity(unittest.TestCase):
    def test_infer_local(self):
        inputs={"a":10}
        result = infer(inputs)
        self.assertIn("result", result)
if __name__ == "__main__":
    unittest.main()
