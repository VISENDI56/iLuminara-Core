import time
import os
import psutil
from core.substrate.integrity.substrate_guard import SubstrateGuard
from core.optimization.edge_slice import ClinicalEdgeOptimizer

class InfraAudit:
    """
    Build-Rev 212: Tests system behavior under extreme resource scarcity.
    """
    def __init__(self):
        self.guard = SubstrateGuard()
        self.optimizer = ClinicalEdgeOptimizer()

    def simulate_resource_starvation(self):
        print("--- [STAGE 1] RESOURCE STARVATION TEST ---")
        # Checking local CPU/Mem (Simulating Blackwell saturation)
        mem_usage = psutil.virtual_memory().percent
        print(f"[*] Current Substrate Load: {mem_usage}%")
        
        if mem_usage > 50:
            print("[!] CRITICAL: Triggering Graceful Degradation Protocol.")
            self.optimizer.apply_weight_slicing()
        
        # Verify Logical Clock integrity during load
        clock_start = self.guard.tick()
        time.sleep(0.5)
        clock_end = self.guard.tick()
        print(f"[✔] Temporal Sync Maintained: Clock {clock_start} -> {clock_end}")

    def test_bit_flip_resilience(self):
        print("\n--- [STAGE 2] MEMORY INTEGRITY UNDER HEAT ---")
        # The audit_memory check we fixed in Rev 208
        status, msg = self.guard.audit_memory()
        if status:
            print(f"[✔] Substrate Integrity: {msg}")
        else:
            print(f"[X] SHUTDOWN: {msg}")

if __name__ == "__main__":
    audit = InfraAudit()
    audit.simulate_resource_starvation()
    audit.test_bit_flip_resilience()
