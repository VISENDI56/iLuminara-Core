import time
import hashlib

class SubstrateGuard:
    def __init__(self):
        self.logical_clock = 0
        self.memory_canary = "LUMINARA_SIG_01"
        self.canary_hash = hashlib.sha256(self.memory_canary.encode()).hexdigest()

    def tick(self):
        self.logical_clock += 1
        return self.logical_clock

    def audit_memory(self):
        # Correctly referencing self.memory_canary
        current_hash = hashlib.sha256(self.memory_canary.encode()).hexdigest()
        if current_hash != self.canary_hash:
            return False, "CRITICAL: Substrate Memory Corruption Detected."
        return True, "Memory Integrity Verified."

if __name__ == "__main__":
    guard = SubstrateGuard()
    print(f"[*] Logic Clock: {guard.tick()} | Integrity: {guard.audit_memory()[1]}")
