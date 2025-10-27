import pandas as pd
import os

analytics_root = "out/analytics"
patients_path = os.path.join(analytics_root, "patients_age.csv")

patients = pd.read_csv(patients_path)

# Clean empty values
patients.replace("", pd.NA, inplace=True)

# === Age Summary ===
age_mean = round(patients['AGE'].mean(), 1)
age_median = round(patients['AGE'].median(), 1)
age_min = int(patients['AGE'].min())
age_max = int(patients['AGE'].max())

age_bins = [0, 12, 18, 35, 50, 65, 120]
age_labels = [
    "Child (0–12)",
    "Teen (13–18)",
    "Young Adult (19–35)",
    "Adult (36–50)",
    "Mid-Age (51–65)",
    "Senior (65+)"
]

patients["AGE_GROUP"] = pd.cut(
    patients["AGE"], bins=age_bins,
    labels=age_labels, include_lowest=True
)

age_group_counts = patients["AGE_GROUP"].value_counts().reindex(age_labels)

# === Gender, Race, Ethnicity, Marital, State ===
gender_counts = patients["GENDER"].value_counts(dropna=True)
race_counts = patients["RACE"].value_counts(dropna=True)
ethnicity_counts = patients["ETHNICITY"].value_counts(dropna=True)
marital_counts = patients["MARITAL"].value_counts(dropna=True)
state_counts = patients["STATE"].value_counts(dropna=True)

# === Build summary table ===
summary_rows = [
    {"metric": "Total Patients", "value": len(patients)},
    {"metric": "Average Age", "value": age_mean},
    {"metric": "Median Age", "value": age_median},
    {"metric": "Age Range", "value": f"{age_min}–{age_max}"}
]

# Add age groups
for label in age_labels:
    summary_rows.append({"metric": f"Age Group - {label}", "value": int(age_group_counts[label])})

# Add gender breakdown
for g, count in gender_counts.items():
    summary_rows.append({"metric": f"Gender - {g}", "value": int(count)})

# Add race
for r, count in race_counts.items():
    summary_rows.append({"metric": f"Race - {r}", "value": int(count)})

# Add ethnicity
for e, count in ethnicity_counts.items():
    summary_rows.append({"metric": f"Ethnicity - {e}", "value": int(count)})

# Add marital status
for m, count in marital_counts.items():
    summary_rows.append({"metric": f"Marital Status - {m}", "value": int(count)})

# Add states
for s, count in state_counts.items():
    summary_rows.append({"metric": f"State - {s}", "value": int(count)})

# Save to CSV
summary_df = pd.DataFrame(summary_rows)
output_path = os.path.join(analytics_root, "demographics.csv")
summary_df.to_csv(output_path, index=False)

print(f"✅ Demographics summary saved → {output_path}")
