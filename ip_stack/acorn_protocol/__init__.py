import numpy as np
class AcornProtocol:
    """IP-03: Biometric stillness and somatic stance verification."""
    def verify_presence(self, somatic_stream):
        stability = np.std(somatic_stream)
        return (True, "LEVEL_5_VERIFIED") if stability < 0.05 else (False, "DURESS_DETECTED")
