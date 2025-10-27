import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

analytics_root = "out/analytics"
patients_path = os.path.join(analytics_root, "patients_age.csv")

patients = pd.read_csv(patients_path)
patients.replace("", pd.NA, inplace=True)

# Remove rows without geolocation
patients = patients.dropna(subset=["LAT", "LON"])
patients["LAT"] = pd.to_numeric(patients["LAT"], errors="coerce")
patients["LON"] = pd.to_numeric(patients["LON"], errors="coerce")
patients = patients.dropna(subset=["LAT", "LON"])

# Count per city
city_counts = (
    patients.groupby(["CITY", "STATE", "LAT", "LON"])
    .size()
    .reset_index(name="COUNT")
)

# Bubble sizes (log scale for nice separation)
sizes = np.log1p(city_counts["COUNT"]) * 35  # adjust multiplier if needed

plt.figure(figsize=(14, 9))
scatter = plt.scatter(
    city_counts["LON"],
    city_counts["LAT"],
    s=sizes,
    c=city_counts["COUNT"],
    cmap="Reds",
    alpha=0.6,
    edgecolor="black"
)

plt.colorbar(scatter, label="Patient Count")
plt.title("Patient Density by City (Bubble Map)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()

output_path = os.path.join(analytics_root, "patients_city_bubbles.png")
plt.savefig(output_path, dpi=300)
plt.close()

print(f"✅ Bubble map saved → {output_path}")
