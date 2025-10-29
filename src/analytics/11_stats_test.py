import pandas as pd
import numpy as np
from scipy import stats
import os


# =============================
# CONFIG
# =============================
DATA_DIR = "out/analytics"
os.makedirs(DATA_DIR, exist_ok=True)

# --- Load data ---
los_df = pd.read_csv(os.path.join(DATA_DIR, "los_distribution.csv"))
patients = pd.read_csv("data/patients.csv", encoding="latin1")

# --- Clean + normalize columns ---
patients.columns = patients.columns.str.lower().str.strip()
los_df.columns = los_df.columns.str.lower().str.strip()

patients["birthdate"] = pd.to_datetime(patients["birthdate"], errors="coerce", dayfirst=True)

# =============================
# Derive age (approx, based on 2025)
# =============================
today = pd.Timestamp("2025-01-01")
patients["age"] = ((today - patients["birthdate"]).dt.days / 365.25).round(1)

# Merge LOS with patient info
los_df = los_df.merge(
    patients[["id", "gender", "age"]],
    left_on="patient",
    right_on="id",
    how="left"
)

# =============================
# 🧮 1️⃣ T-Test: LOS (Older Adults vs Others)
# =============================
older = los_df.loc[los_df["age"] >= 65, "los_days"].dropna()
others = los_df.loc[los_df["age"] < 65, "los_days"].dropna()

if len(older) > 2 and len(others) > 2:
    t_stat, p_val = stats.ttest_ind(older, others, equal_var=False, nan_policy="omit")
else:
    t_stat, p_val = np.nan, np.nan

t_interpret = "Significant difference" if (p_val < 0.05) else "No significant difference"

# =============================
# 🧮 2️⃣ Chi-Square: Hypertensive-like vs Gender
# =============================
# Hypertensive-like = systolic >=140 or diastolic >=90
obs = pd.read_csv("data/observations.csv")
obs = obs[obs["TYPE"].str.lower() == "numeric"]
obs["VALUE"] = pd.to_numeric(obs["VALUE"], errors="coerce")

bp = obs[obs["CODE"].isin(["8480-6", "8462-4"])].copy()  # systolic + diastolic
bp_summary = bp.pivot_table(index="PATIENT", columns="CODE", values="VALUE", aggfunc="mean").reset_index()
bp_summary["hypertensive_like"] = (bp_summary["8480-6"] >= 140) | (bp_summary["8462-4"] >= 90)

# Merge gender info
bp_summary = bp_summary.merge(
    patients[["id", "gender"]],
    left_on="PATIENT",
    right_on="id",
    how="left"
)
bp_summary["gender"] = bp_summary["gender"].str.upper().map({"M": "Male", "F": "Female"})

# Build contingency table
contingency = pd.crosstab(bp_summary["hypertensive_like"], bp_summary["gender"])
chi2, chi_p, dof, expected = stats.chi2_contingency(contingency)

chi_interpret = "Dependent" if (chi_p < 0.05) else "Independent"

# =============================
# 📊 Save results
# =============================
results = pd.DataFrame([
    {
        "Test": "T-test (LOS: Older vs Others)",
        "Statistic": round(t_stat, 4),
        "p_value": round(p_val, 6),
        "Interpretation": t_interpret
    },
    {
        "Test": "Chi-square (Hypertensive vs Gender)",
        "Statistic": round(chi2, 4),
        "p_value": round(chi_p, 6),
        "Interpretation": chi_interpret
    }
])

results.to_csv(os.path.join(DATA_DIR, "stats_tests.csv"), index=False)

print("✅ stats_tests.csv generated successfully!")
print(results)


