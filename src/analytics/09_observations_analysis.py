import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ========== CONFIG ==========
DATA_PATH = "data/observations.csv"
OUT_DIR = "out/analytics"
os.makedirs(OUT_DIR, exist_ok=True)

# --- Load & Clean ---
df = pd.read_csv(DATA_PATH)
df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
df = df[df["TYPE"] == "numeric"].copy()

# Convert VALUE to numeric
df["VALUE"] = pd.to_numeric(df["VALUE"], errors="coerce")

# --- Vital Codes (Synthea standard LOINC) ---
vitals = {
    "29463-7": "Weight (kg)",
    "39156-5": "BMI",
    "8302-2": "Height (cm)",
    "8867-4": "Heart Rate (/min)",
    "9279-1": "Respiratory Rate (/min)",
    "8310-5": "Body Temperature (°C)",
    "8480-6": "Systolic BP (mmHg)",
    "8462-4": "Diastolic BP (mmHg)"
}
df = df[df["CODE"].isin(vitals.keys())]
df["VITAL"] = df["CODE"].map(vitals)

# ========== Latest per patient ==========
latest = (
    df.sort_values("DATE")
      .groupby(["PATIENT", "VITAL"])
      .tail(1)
)

# ========== Coverage ==========
total_patients = df["PATIENT"].nunique()
coverage = latest.groupby("VITAL")["PATIENT"].nunique() / total_patients * 100

# ========== Summary Stats (All Vitals) ==========
summary = latest.groupby("VITAL")["VALUE"].agg(
    mean="mean",
    median="median",
    std="std",
    min="min",
    max="max",
    p10=lambda x: x.quantile(0.1),
    p90=lambda x: x.quantile(0.9),
    patient_count="count"
).reset_index()

summary["coverage_pct"] = summary["VITAL"].map(coverage)
summary = summary.rename(columns={"VITAL": "vital_type"})
summary = summary.round(2)

# Save complete summary
summary.to_csv(os.path.join(OUT_DIR, "observation_summary.csv"), index=False)
print("✅ observation_summary.csv generated successfully")

# ========== Extract Vitals Only ==========
core_vitals = ["Weight (kg)", "BMI", "Systolic BP (mmHg)", "Diastolic BP (mmHg)"]
vitals_summary = summary[summary["vital_type"].isin(core_vitals)].copy()
vitals_summary.to_csv(os.path.join(OUT_DIR, "vitals_summary.csv"), index=False)
print("✅ vitals_summary.csv generated successfully")

# ========== Visualization 1: Bar chart (Mean ± SD) ==========
plt.figure(figsize=(10, 5))
plt.bar(summary["vital_type"], summary["mean"], yerr=summary["std"], capsize=5, color="#c084f5")
plt.title("Vital Signs Summary (Mean ± SD)")
plt.ylabel("Value")
plt.xticks(rotation=25, ha='right')
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "vitals_summary_bar.png"))
plt.close()

# ========== Visualization 2: BP vs BMI Scatter ==========
bp_bmi = latest.pivot(index="PATIENT", columns="VITAL", values="VALUE").reset_index()
plt.figure(figsize=(6, 5))
plt.scatter(bp_bmi["BMI"], bp_bmi["Systolic BP (mmHg)"], alpha=0.7, label="Systolic", color="#f5426f")
plt.scatter(bp_bmi["BMI"], bp_bmi["Diastolic BP (mmHg)"], alpha=0.7, label="Diastolic", color="#4682b4")
plt.xlabel("BMI (kg/m²)")
plt.ylabel("Blood Pressure (mmHg)")
plt.title("Blood Pressure vs BMI")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "bp_vs_bmi_scatter.png"))
plt.close()

# ========== Visualization 3: Enhanced Correlation Heatmap ==========
corr = bp_bmi.drop(columns=["PATIENT"]).corr()

fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(corr, cmap="RdPu", interpolation="nearest")

# Add values on heatmap
for i in range(len(corr.columns)):
    for j in range(len(corr.columns)):
        ax.text(j, i, f"{corr.iloc[i, j]:.2f}",
                ha="center", va="center", color="black", fontsize=8)

plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns, rotation=35, ha="right")
ax.set_yticklabels(corr.columns)
plt.title("Vitals Correlation Heatmap", pad=10)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "vitals_correlation_heatmap.png"))
plt.close()

print(f"""
✅ Generated outputs:
 - {OUT_DIR}/observation_summary.csv
 - {OUT_DIR}/vitals_summary.csv
 - {OUT_DIR}/vitals_summary_bar.png
 - {OUT_DIR}/bp_vs_bmi_scatter.png
 - {OUT_DIR}/vitals_correlation_heatmap.png
""")
