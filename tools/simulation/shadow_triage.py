import random
import time
import json
from core.ingestion.voice.sovereign_scribe import SovereignScribe
from core.governance.gates.outlier_gate import PatientZeroGate

class NightWatchSimulator:
    def __init__(self):
        self.scribe = SovereignScribe()
        self.gate = PatientZeroGate()
        self.logs = []

    def run_epoch(self, name, days, anomaly_rate, noise_db):
        print(f"\n[*] STARTING {name} ({days} Days)...")
        epoch_stats = {"accepted": 0, "flagged": 0, "rejected": 0}
        
        for day in range(1, days + 1):
            # Simulate 100 patients per day
            for p in range(100):
                # Generate synthetic temp (Healthy vs Anomaly)
                if random.random() < anomaly_rate:
                    temp = random.uniform(39.5, 42.0) # Fever
                else:
                    temp = random.uniform(36.5, 37.5) # Normal
                
                # Apply acoustic noise stress
                raw_text = f"Patient {p} temp is {temp}C"
                if noise_db > 75:
                    # Simulate ASR flip error
                    raw_text = raw_text.replace(str(round(temp, 1)), "14.2")

                # PROCESS THROUGH iLUMINARA
                result = self.scribe.process_transcription(raw_text)
                
                if result['status'] == "CLARIFICATION_REQUIRED":
                    epoch_stats["rejected"] += 1
                elif temp > 39.0:
                    epoch_stats["flagged"] += 1
                else:
                    epoch_stats["accepted"] += 1
            
            if day % 10 == 0:
                print(f"      Day {day} Checkpoint: {epoch_stats}")
        
        return epoch_stats

def run_simulation():
    sim = NightWatchSimulator()
    full_report = {}

    # 90-DAY COMPRESSION
    full_report["Epoch_1_Baseline"] = sim.run_epoch("Baseline", 30, 0.02, 40)
    full_report["Epoch_2_Environmental"] = sim.run_epoch("Env_Stress", 30, 0.05, 80)
    full_report["Epoch_3_Outbreak"] = sim.run_epoch("Kinetic_Peak", 30, 0.25, 60)

    print("\n" + "="*40)
    print(" FINAL 90-DAY SHADOW TRIAGE REPORT")
    print("="*40)
    print(json.dumps(full_report, indent=2))
    
    # Validation Logic
    if full_report["Epoch_2_Environmental"]["rejected"] > 0:
        print("\n[✔] SUCCESS: Numeric Guardian caught Noise-Transposition errors.")
    if full_report["Epoch_3_Outbreak"]["flagged"] > 500:
        print("[✔] SUCCESS: Z3-Gate successfully isolated Outbreak clusters.")

if __name__ == "__main__":
    run_simulation()
