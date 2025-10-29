import pandas as pd
import os

# ============================
# CONFIG
# ============================

DATA_ROOT = "out"                     # Folder where .ndjson files are stored
ANALYTICS_ROOT = "out/analytics"      # Destination for cleaned CSVs
os.makedirs(ANALYTICS_ROOT, exist_ok=True)

# --- Choose which resources to load ---
LOAD_ALL = False  # 🔄 set to True if you want to process everything

# Minimal resources for analytics
CORE_RESOURCES = ["patients", "encounters", "observations"]

# Full FHIR dataset (for future expansion)
ALL_RESOURCES = [
    "patients", "encounters", "observations",
    "conditions", "allergies", "medications",
    "procedures", "immunizations", "devices",
    "careplans", "imaging_studies",
    "organizations", "providers",
    "payers", "payer_transitions"
]

resources = ALL_RESOURCES if LOAD_ALL else CORE_RESOURCES

summary = []

# ============================
# LOAD + CLEAN
# ============================

for r in resources:
    path = os.path.join(DATA_ROOT, f"{r}.ndjson")

    if not os.path.exists(path):
        print(f"⚠️ Missing file: {r}.ndjson — skipping.")
        continue

    try:
        df = pd.read_json(path, lines=True)
    except ValueError:
        print(f"❌ Error reading {r}.ndjson — check file format.")
        continue

    # Clean & type-convert
    df.replace("", pd.NA, inplace=True)
    df = df.convert_dtypes()

    # Basic metrics
    row_count = len(df)
    total_cells = df.shape[0] * df.shape[1]
    missing_pct = (df.isna().sum().sum() / total_cells * 100) if total_cells > 0 else 0

    summary.append({
        "resource": r,
        "rows": row_count,
        "missing_percent": round(missing_pct, 2)
    })

    # Export cleaned CSV
    out_csv = os.path.join(ANALYTICS_ROOT, f"{r}.csv")
    df.to_csv(out_csv, index=False)
    print(f"✅ Loaded {r}: {row_count:,} rows → {out_csv}")

# ============================
# SUMMARY REPORT
# ============================

summary_df = pd.DataFrame(summary)
summary_path = os.path.join(ANALYTICS_ROOT, "metrics_overview.csv")
summary_df.to_csv(summary_path, index=False)

print("\n📊 Summary saved to:", summary_path)
print(f"Loaded resources: {', '.join(resources)}")
