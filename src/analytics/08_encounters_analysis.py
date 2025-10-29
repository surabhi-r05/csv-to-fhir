import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

analytics_root = "out/analytics"
os.makedirs(analytics_root, exist_ok=True)

# --- Load encounters ---
enc = pd.read_csv("data/encounters.csv")
enc["START"] = pd.to_datetime(enc["START"], errors="coerce")
enc["STOP"] = pd.to_datetime(enc["STOP"], errors="coerce")

# ==============================================================
# 🧮 Compute Length of Stay (LOS) in days (float)
# ==============================================================

enc["LOS_days"] = (enc["STOP"] - enc["START"]).dt.total_seconds() / (24 * 3600)
enc["LOS_days"] = enc["LOS_days"].clip(lower=0)

# Drop invalid rows
enc = enc.dropna(subset=["LOS_days", "ENCOUNTERCLASS"])

# --- Identify outliers ---
p95 = enc["LOS_days"].quantile(0.95)
enc["is_outlier"] = (enc["LOS_days"] > p95) | (enc["LOS_days"] > 14)

# --- Remove outliers ---
enc_clean = enc[~enc["is_outlier"]].copy()

# ==============================================================
# 📁 Save detailed LOS data
# ==============================================================

los_full = enc_clean[["ENCOUNTERCLASS", "LOS_days"]]
los_full.to_csv(os.path.join(analytics_root, "los_distribution.csv"), index=False)

# --- Summary (count, mean, median, IQR) ---
def iqr(s): return s.quantile(0.75) - s.quantile(0.25)

los_summary = (
    los_full.groupby("ENCOUNTERCLASS")["LOS_days"]
    .agg(
        count="count",
        mean="mean",
        median="median",
        q25=lambda x: x.quantile(0.25),
        q75=lambda x: x.quantile(0.75),
        iqr=iqr,
        max="max"
    )
    .reset_index()
    .sort_values("median", ascending=False)
)
los_summary.to_csv(os.path.join(analytics_root, "los_summary.csv"), index=False)

# ==============================================================
# 📅 Encounters per Day
# ==============================================================

encounters_by_day = (
    enc_clean.groupby(enc_clean["START"].dt.date)
    .size()
    .reset_index(name="COUNT")
)
encounters_by_day.to_csv(os.path.join(analytics_root, "encounters_by_day.csv"), index=False)

# ==============================================================
# 📈 Chart 1 – Encounter Trend
# ==============================================================

plt.figure(figsize=(10, 5))
plt.plot(
    encounters_by_day["START"],
    encounters_by_day["COUNT"],
    color="#5B8FF9",
    linewidth=2.5,
    marker="o"
)
plt.fill_between(
    encounters_by_day["START"],
    encounters_by_day["COUNT"],
    color="#5B8FF9",
    alpha=0.15
)
plt.title("Encounters per Day", fontsize=13)
plt.xlabel("Date")
plt.ylabel("Number of Encounters")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(analytics_root, "encounters_trend.png"), dpi=300)
plt.close()

# ==============================================================
# 📊 Chart 2 – Median LOS (days) by Encounter Class
# ==============================================================

plt.figure(figsize=(8, 5))
plt.bar(
    los_summary["ENCOUNTERCLASS"],
    los_summary["median"],
    color="#F66D44",
    edgecolor="black",
    alpha=0.85
)
plt.title("Median Encounter Duration by Class (days)", fontsize=13)
plt.ylabel("Median LOS (days)")
plt.xlabel("Encounter Class")
plt.xticks(rotation=30, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig(os.path.join(analytics_root, "median_los_by_class.png"), dpi=300)
plt.close()

# ==============================================================
# 📦 Chart 3 – LOS Boxplot by Class
# ==============================================================

plt.figure(figsize=(9, 6))
los_full.boxplot(by="ENCOUNTERCLASS", column="LOS_days", grid=False)
plt.title("Length of Stay (LOS) by Encounter Class (days)", fontsize=13)
plt.suptitle("")  # remove default pandas title
plt.xlabel("Encounter Class")
plt.ylabel("LOS (days)")
plt.tight_layout()
plt.savefig(os.path.join(analytics_root, "los_box.png"), dpi=300)
plt.close()

print("✅ Generated outputs:")
print(" - encounters_by_day.csv")
print(" - los_distribution.csv (cleaned, no outliers)")
print(" - los_summary.csv (aggregated stats)")
print(" - encounters_trend.png")
print(" - median_los_by_class.png")
print(" - los_box.png")
print(f"ℹ️ Outlier threshold: >{round(p95,2)} days or >14 days removed.")
