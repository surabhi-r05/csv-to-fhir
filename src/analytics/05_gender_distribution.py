import pandas as pd
import matplotlib.pyplot as plt
import os

analytics_root = "out/analytics"

# Load patients with AGE already computed
patients_path = os.path.join(analytics_root, "patients_age.csv")
patients = pd.read_csv(patients_path)

# Clean: treat empty or weird values as NA
patients['GENDER'].replace(["", "U"], pd.NA, inplace=True)
patients.dropna(subset=['GENDER'], inplace=True)

gender_counts = patients['GENDER'].value_counts()

plt.figure(figsize=(6, 6))
gender_counts.plot(kind='pie', autopct='%1.1f%%')
plt.title("Gender Share")
plt.ylabel("")  # Removes the default ylabel
plt.tight_layout()

output_path = os.path.join(analytics_root, "gender_share.png")
plt.savefig(output_path)
plt.close()

print(f"✅ Gender share chart saved: {output_path}")
print("📌 File: gender_share.png")
