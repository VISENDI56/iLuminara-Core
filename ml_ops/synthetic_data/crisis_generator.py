import random
import json

class RareEventGenerator:
    """
    Generates 'Sampling Zeros' - plausible but unseen crisis scenarios.
    Used to pre-train the JEPA World Model on edge cases.
    """
    def generate_scenario(self, event_type="PANDEMIC_SPILLOVER"):
        """
        Creates a synthetic outbreak trajectory.
        """
        print(f"   [Synthetic] Hallucinating {event_type} scenario...")
        
        # Simulating a viral spread vector
        scenario = {
            "id": f"SYNTH_{random.randint(1000,9999)}",
            "patient_zero_location": [0.4, 0.9],
            "R0_trajectory": [2.5, 3.1, 4.2, 5.0], # Exponential spread
            "resource_depletion_rate": 0.15
        }
        return scenario

    def batch_generate(self, n=100):
        # Generates a dataset for 'Ghost-Nexus' training
        return [self.generate_scenario() for _ in range(n)]