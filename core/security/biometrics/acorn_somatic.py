import numpy as np
import time

class AcornSomaticEngine:
    """
    Build-Rev 210: IP-03 Protocol.
    Behavioral biometrics based on posture and stillness.
    """
    def __init__(self):
        self.posture_baseline = "COMMAND_STANCE_ALPHA"
        self.stillness_threshold = 0.05 # Max allowable micro-tremor

    def analyze_stability(self, sensor_stream):
        """Analyzes tremor frequency to detect duress or unauthorized users."""
        # Simulate analyzing a 5-second window of movement data
        tremor_index = np.std(sensor_stream)
        
        if tremor_index > self.stillness_threshold:
            return False, f"ALERT: Somatic Duress Detected (Tremor: {tremor_index:.4f})"
        return True, "Somatic Identity Verified."

if __name__ == "__main__":
    acorn = AcornSomaticEngine()
    # Mock data: Stable clinician vs. Distressed/Unauthorized clinician
    stable_stream = np.random.normal(0, 0.02, 100)
    distressed_stream = np.random.normal(0, 0.1, 100)
    
    print(f"[*] Testing Stable Input: {acorn.analyze_stability(stable_stream)[1]}")
    print(f"[*] Testing Distressed Input: {acorn.analyze_stability(distressed_stream)[1]}")
