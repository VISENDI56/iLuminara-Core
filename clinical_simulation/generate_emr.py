import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Parameters
population = 484000
months = 9
start_date = datetime(2025, 4, 1)
dates = [start_date + timedelta(days=x) for x in range(months * 30)]

# Common diagnoses (based on real camp data)
diagnoses = [
    "Malaria", "Acute Respiratory Infection", "Watery Diarrhea", 
    "Malnutrition", "Skin Infection", "Measles", "Cholera", "Tuberculosis",
    "Hypertension", "Diabetes", "Anemia", "Trauma"
]
weights = [0.25, 0.20, 0.15, 0.10, 0.08, 0.05, 0.04, 0.03, 0.03, 0.03, 0.02, 0.02]

# Generate ~50k consultations
np.random.seed(42)
data = {
    "date": np.random.choice(dates, 50000),
    "camp": np.random.choice(["Dadaab", "Kalobeyei"], 50000, p=[0.88, 0.12]),
    "age_group": np.random.choice(["<5", "5-14", "15-49", "50+"], 50000, p=[0.35, 0.20, 0.35, 0.10]),
    "gender": np.random.choice(["M", "F"], 50000),
    "diagnosis": np.random.choice(diagnoses, 50000, p=weights),
    "severity": np.random.choice(["Mild", "Moderate", "Severe"], 50000, p=[0.6, 0.3, 0.1])
}

df = pd.DataFrame(data)
df.to_csv("clinical_simulation/data/emr/emr_consultations_2025.csv", index=False)
print(f"EMR data generated: {len(df)} consultations")
print(df['diagnosis'].value_counts().head(10))
