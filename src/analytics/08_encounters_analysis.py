import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# =========================
# ⚙️ Config & Setup
# =========================
analytics_root = "out/analytics"
os.makedirs(analytics_root, exist_ok=True)

# --- Load Encounters ---
enc = pd.read_csv("data/encounters.csv")
enc["START"] = pd.to_datetime(enc["START"], errors="coerce")
enc["STOP"] = pd.to_datetime(enc["STOP"], errors="coerce")

# ==============================================================
# 🧮 Compute Length of Stay (LOS)
# ==============================================================
enc["LOS_days"] = (enc["STOP"] - enc["START"]).dt.total_seconds() / (24 * 3600)
enc["LOS_days"] = enc["LOS_days"].clip(lower=0)
enc["LOS_hours"] = enc["LOS_days"] * 24  # readability

enc = enc.dropna(subset=["LOS_days", "ENCOUNTERCLASS"])

# ==============================================================
# 🚫 Outlier Detection (per encounter class)
# ==============================================================
p95_per_class = enc.groupby("ENCOUNTERCLASS")["LOS_days"].quantile(0.95).to_dict()

enc["is_outlier"] = enc.apply(
    lambda x: x["LOS_days"] > max(p95_per_class.get(x["ENCOUNTERCLASS"], 0), 14),
    axis=1
)
enc_clean = enc[~enc["is_outlier"]].copy()

# ==============================================================
# 📁 Save Detailed LOS Data
# ==============================================================
los_full = enc_clean[["Id", "ENCOUNTERCLASS", "LOS_days", "LOS_hours", "PATIENT"]]
los_full.to_csv(os.path.join(analytics_root, "los_distribution.csv"), index=False)

# ==============================================================
# 📊 LOS Summary Stats (with thresholds + hours)
# ==============================================================
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
)

# Add threshold per class
los_summary["p95_threshold_days"] = los_summary["ENCOUNTERCLASS"].map(p95_per_class)

# Add median LOS in hours for better readability (except inpatient)
los_summary["median_hours"] = np.where(
    los_summary["ENCOUNTERCLASS"] != "inpatient",
    los_summary["median"] * 24,
    np.nan
)

# Sort nicely
los_summary = los_summary.sort_values("median", ascending=False)

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
# 🕒 Chart 3 – Median LOS (hours) for Short-Stay Classes
# ==============================================================
short_stay = los_summary[los_summary["ENCOUNTERCLASS"] != "inpatient"].copy()

plt.figure(figsize=(8, 5))
plt.bar(
    short_stay["ENCOUNTERCLASS"],
    short_stay["median_hours"],
    color="#36CFC9",
    edgecolor="black",
    alpha=0.85
)
plt.title("Median Encounter Duration by Class (hours)", fontsize=13)
plt.ylabel("Median LOS (hours)")
plt.xlabel("Encounter Class")
plt.xticks(rotation=30, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig(os.path.join(analytics_root, "median_los_by_class_hours.png"), dpi=300)
plt.close()

# ==============================================================
# 📦 Chart 4 – LOS Boxplot by Class
# ==============================================================
plt.figure(figsize=(9, 6))
los_full.boxplot(
    column="LOS_days",
    by="ENCOUNTERCLASS",
    grid=False,
    patch_artist=True,
    boxprops=dict(facecolor="#AEDFF7", color="#2980B9"),
    medianprops=dict(color="#D35400", linewidth=2),
)
plt.title("Length of Stay (LOS) by Encounter Class (days)", fontsize=13)
plt.suptitle("")  # remove default pandas title
plt.xlabel("Encounter Class")
plt.ylabel("LOS (days)")
plt.tight_layout()
plt.savefig(os.path.join(analytics_root, "los_box.png"), dpi=300)
plt.close()

# ==============================================================
# ✅ Summary Log
# ==============================================================
print("\n✅ Generated outputs:")
print(" - encounters_by_day.csv")
print(" - los_distribution.csv (cleaned, with Id & hours)")
print(" - los_summary.csv (aggregated stats + thresholds)")
print(" - encounters_trend.png")
print(" - median_los_by_class.png")
print(" - median_los_by_class_hours.png")
print(" - los_box.png")

print("\nℹ️ Outlier thresholds by encounter class (95th percentile, days):")
for k, v in p95_per_class.items():
    print(f"   {k:<12} : {round(v, 2)} days (values > max(p95, 14) removed)")
