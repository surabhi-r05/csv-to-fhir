import pandas as pd
import matplotlib.pyplot as plt
import os

analytics_root = "out/analytics"

patients_path = os.path.join(analytics_root, "patients.csv")
patients = pd.read_csv(patients_path)

# Fix missing values
patients.replace("", pd.NA, inplace=True)

# Convert BIRTHDATE to datetime
patients['BIRTHDATE'] = pd.to_datetime(patients['BIRTHDATE'], errors='coerce')

# Calculate Age
today = pd.Timestamp.today()
patients['AGE'] = (today - patients['BIRTHDATE']).dt.days // 365

# Filter realistic ages
patients = patients[patients['AGE'].between(0, 120)]

# ✅ Age group bins + readable labels
age_bins = [0, 12, 18, 35, 50, 65, 120]
age_labels = [
    "Child (0–12)",
    "Teen (13–18)",
    "Young Adult (19–35)",
    "Adult (36–50)",
    "Mid-Age (51–65)",
    "Senior (65+)"
]

patients['AGE_GROUP'] = pd.cut(
    patients['AGE'],
    bins=age_bins,
    labels=age_labels,
    include_lowest=True
)

age_group_counts = patients['AGE_GROUP'].value_counts().reindex(age_labels)

# ✅ Age Group Bar Chart
plt.figure(figsize=(12,6))
age_group_counts.plot(kind='bar')
plt.title("Age Groups with Ranges")
plt.ylabel("Number of Patients")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(analytics_root, "age_groups.png"))
plt.close()

# ✅ Age Box Plot
plt.figure(figsize=(6,5))
patients['AGE'].plot(kind='box')
plt.title("Age Distribution (Box Plot)")
plt.tight_layout()
plt.savefig(os.path.join(analytics_root, "age_boxplot.png"))
plt.close()

# ✅ Save updated CSV for future steps
patients.to_csv(os.path.join(analytics_root, "patients_age.csv"), index=False)

print("✅ Age distribution visualizations saved:")
print("- age_groups.png")
print("- age_boxplot.png")
print("✅ Updated patients CSV with AGE saved → patients_age.csv")
