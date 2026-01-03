import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()

def generate_sovereign_cohort(n_patients=1000, anomaly_rate=0.05):
    """
    Generates synthetic refugee health dataset with 'Patient Zero' outliers.
    """
    data = []
    for i in range(n_patients):
        is_anomaly = random.random() < anomaly_rate
        
        # Baseline: Malaria-like symptoms
        temp = np.random.normal(38.5, 0.5) 
        wbc = np.random.normal(12000, 2000)
        
        if is_anomaly:
            # Patient Zero: Marburg/VHF
            temp = np.random.normal(41.0, 0.2) # Spike
            wbc = np.random.normal(2500, 500)  # Leukopenia
        
        data.append({
            "id": fake.uuid4(),
            "temp_c": round(temp, 1),
            "wbc_count": int(wbc),
            "is_outlier": is_anomaly
        })
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_sovereign_cohort()
    df.to_csv("benchmarks/utils/synthetic_patient_zero.csv", index=False)
    print(f"[*] Generated {len(df)} synthetic records.")
