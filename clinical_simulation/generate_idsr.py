import pandas as pd
import numpy as np

idsr_diseases = ["Malaria", "Measles", "Cholera", "Acute Flaccid Paralysis", "Meningitis", "Dysentery"]
weeks = pd.date_range("2025-04-01", periods=39, freq='W-MON')  # 9 months ≈ 39 weeks

reports = []
for week in weeks:
    for camp in ["Dadaab", "Kalobeyei"]:
        row = {"week": week, "camp": camp}
        for disease in idsr_diseases:
            if disease == "Malaria":
                cases = random.randint(800, 2000) if camp == "Dadaab" else random.randint(150, 400)
            elif disease in ["Measles", "Cholera"]:
                cases = random.randint(0, 50)
            else:
                cases = random.randint(0, 20)
            row[f"{disease}_cases"] = cases
            row[f"{disease}_deaths"] = random.randint(0, max(1, cases//50))
        reports.append(row)

df = pd.DataFrame(reports)
df.to_csv("clinical_simulation/data/idsr/idsr_weekly_2025.csv", index=False)
print(f"IDSR weekly reports generated: {len(df)} entries")
print("Top malaria week:", df['Malaria_cases'].max())
