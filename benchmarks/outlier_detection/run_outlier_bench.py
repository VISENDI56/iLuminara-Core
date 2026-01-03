import time
import z3
import pandas as pd
import numpy as np
from benchmarks.utils.data_gen import generate_sovereign_cohort

class MockZ3Gate:
    def verify_vital_sign(self, val):
        s = z3.Solver()
        s.set("timeout", 50) # 50ms guillotine
        v = z3.Real('v')
        s.add(v == val)
        s.add(v > 40.0) 
        return s.check()

def run_z3_performance_test():
    print(f"[*] Running Z3-Gate Latency Test (1000 samples)...")
    df = generate_sovereign_cohort(1000, anomaly_rate=0.1)
    gate = MockZ3Gate()
    
    latencies = []
    for _, row in df.iterrows():
        start = time.perf_counter_ns()
        gate.verify_vital_sign(row['temp_c'])
        latencies.append((time.perf_counter_ns() - start) / 1e6)

    print(f"    Avg Latency: {np.mean(latencies):.2f}ms")
    print(f"    P99 Latency: {np.percentile(latencies, 99):.2f}ms")

if __name__ == "__main__":
    run_z3_performance_test()
