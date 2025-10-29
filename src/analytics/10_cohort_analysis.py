import pandas as pd
from pathlib import Path

# === Setup ===
base = Path("data")
out = Path("out/analytics")
out.mkdir(parents=True, exist_ok=True)

# === Load Patients ===
patients = pd.read_csv(base / "patients.csv", encoding="latin1")
patients["BIRTHDATE"] = pd.to_datetime(patients["BIRTHDATE"], errors="coerce", dayfirst=True)
patients["AGE"] = (pd.Timestamp.now() - patients["BIRTHDATE"]).dt.days // 365

# === Load Encounters & Observations ===
encounters = pd.read_csv(base / "encounters.csv")
obs = pd.read_csv(base / "observations.csv")
obs["VALUE"] = pd.to_numeric(obs["VALUE"], errors="coerce")

# === Cohort 1: Older Adults (age >= 65) ===
older_adults = patients.loc[patients["AGE"] >= 65, "Id"].unique()

# === Cohort 2: Multi-Encounter (>= 3 encounters) ===
multi_encounter = encounters["PATIENT"].value_counts().loc[lambda x: x >= 3].index.tolist()

# === Cohort 3: Hypertensive-like (systolic ≥140 or diastolic ≥90) ===
bp = obs[obs["DESCRIPTION"].isin(["Systolic Blood Pressure", "Diastolic Blood Pressure"])]
bp_pivot = bp.pivot_table(index="PATIENT", columns="DESCRIPTION", values="VALUE", aggfunc="max").fillna(0)
hypertensive_like = bp_pivot.loc[
    (bp_pivot["Systolic Blood Pressure"] >= 140) | (bp_pivot["Diastolic Blood Pressure"] >= 90)
].index.tolist()

# === Base Summary ===
summary = pd.DataFrame({
    "Cohort": ["Older Adults (65+)", "Multi-Encounter (≥3)", "Hypertensive-like"],
    "Count": [len(older_adults), len(multi_encounter), len(hypertensive_like)],
    "Percent of Population": [
        len(older_adults) / len(patients) * 100,
        len(multi_encounter) / len(patients) * 100,
        len(hypertensive_like) / len(patients) * 100,
    ],
}).round(2)
summary.to_csv(out / "cohort_summary.csv", index=False)

# === Detailed Metrics ===
detailed = []

for name, ids in [
    ("Older Adults (65+)", older_adults),
    ("Multi-Encounter (≥3)", multi_encounter),
    ("Hypertensive-like", hypertensive_like),
]:
    cohort_patients = patients[patients["Id"].isin(ids)]
    cohort_encounters = encounters[encounters["PATIENT"].isin(ids)]
    avg_age = cohort_patients["AGE"].mean()
    avg_encounters = cohort_encounters.groupby("PATIENT").size().mean() if not cohort_encounters.empty else 0
    gender_counts = cohort_patients["GENDER"].value_counts(normalize=True) * 100
    pct_female = gender_counts.get("F", 0)
    pct_male = gender_counts.get("M", 0)
    detailed.append({
        "Cohort": name,
        "Patients": len(cohort_patients),
        "Avg Age": round(avg_age, 1),
        "Avg Encounters/Patient": round(avg_encounters, 2),
        "% Female": round(pct_female, 1),
        "% Male": round(pct_male, 1),
    })

detailed_df = pd.DataFrame(detailed)
detailed_df.to_csv(out / "cohort_summary_detailed.csv", index=False)

print("✅ Generated:")
print(" - cohort_summary.csv")
print(" - cohort_summary_detailed.csv")
print("\nDetailed cohort metrics:")
print(detailed_df)
