import pandas as pd
import numpy as np
from datetime import datetime, timedelta

alert_types = ["Suspected Measles", "Suspected Cholera", "Acute Malnutrition", "Fever Cluster", "Diarrhea Outbreak"]
dates = pd.date_range("2025-04-01", periods=270, freq='D')

alerts = []
for _ in range(800):  # ~3 alerts/day average
    alerts.append({
        "date": np.random.choice(dates),
        "camp": np.random.choice(["Dadaab", "Kalobeyei"], p=[0.88, 0.12]),
        "alert_type": np.random.choice(alert_types, p=[0.3, 0.25, 0.2, 0.15, 0.1]),
        "cases_reported": np.random.randint(1, 15),
        "source": "Community Health Volunteer"
    })

df = pd.DataFrame(alerts)
df.to_csv("clinical_simulation/data/cbs/cbs_alerts_2025.csv", index=False)
print(f"CBS alerts generated: {len(df)} events")
print(df['alert_type'].value_counts())
