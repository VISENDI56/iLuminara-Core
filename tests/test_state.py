import unittest
from core.state.sovereign_bus import bus

class TestState(unittest.TestCase):
    def test_state_mutation(self):
        bus.set("test_key","test_val")
        self.assertEqual(bus.get("test_key"),"test_val")

if __name__=="__main__": unittest.main()
