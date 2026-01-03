import os
import argparse

print("=== iLuminara Sovereign Benchmark Suite ===")
os.system("python3 benchmarks/outlier_detection/run_outlier_bench.py")
os.system("python3 benchmarks/efficiency/run_power_bench.py")
print("=== Certification Complete ===")
