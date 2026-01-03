"""
Acorn Protocol (IP-03): High-Fidelity Somatic Enrollment
Records 300s Resting + 300s Crisis biometric baseline (HRV, Gait, Micro-vibrations).
Uses simulated sensors (replace with real wearable/accelerometer data).
Generates non-custodial somatic key anchor.
"""

import time
import random
import json
import hashlib

def simulate_hrv(state: str):
    # Resting: High HRV, Crisis: Low HRV
    base = 80 if state == "resting" else 120
    variability = 15 if state == "resting" else 5
    return [base + random.uniform(-variability, variability) for _ in range(100)]

def simulate_gait_microvib(state: str):
    return [random.uniform(0.1, 0.5) if state == "resting" else random.uniform(0.8, 1.5) for _ in range(100)]

def enroll_state(state: str, duration: int = 300):
    print(f"Starting {duration}s {state.capitalize()} State enrollment... Stay {state}.")
    data = {"hrv": [], "gait_vib": []}
    for _ in range(duration // 3):
        data["hrv"].extend(simulate_hrv(state))
        data["gait_vib"].extend(simulate_gait_microvib(state))
        time.sleep(3)  # Simulate sensor batch
    return data

def generate_somatic_key(resting, crisis):
    combined = json.dumps({"resting": resting, "crisis": crisis})
    key_hash = hashlib.sha3_512(combined.encode()).hexdigest()
    print(f"Somatic Signature anchored. Non-custodial key: {key_hash[:64]}...")
    with open("biometric/acorn_protocol/somatic_anchor.json", "w") as f:
        json.dump({"anchor": key_hash}, f)
    print("Acorn Protocol activated - System exits Void-State.")

if __name__ == "__main__":
    print("=== Acorn Protocol Enrollment Session ===")
    resting = enroll_state("resting")
    crisis = enroll_state("crisis")
    generate_somatic_key(resting, crisis)
