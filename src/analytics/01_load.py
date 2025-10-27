import pandas as pd
import os

data_root = "out"
analytics_root = "out/analytics"
os.makedirs(analytics_root, exist_ok=True)

resources = [
    "patients",
    "encounters",
    "observations",
    "conditions",
    "allergies",
    "medications",
    "procedures",
    "immunizations",
    "devices",
    "careplans",
    "imaging_studies",
    "organizations",
    "providers",
    "payers",
    "payer_transitions"
]

summary = []

for r in resources:
    path = os.path.join(data_root, f"{r}.ndjson")

    if not os.path.exists(path):
        print(f"❌ Missing: {r}")
        continue

    df = pd.read_json(path, lines=True)

    # ✅ Correct handling of missing values
    df.replace("", pd.NA, inplace=True)
    df = df.convert_dtypes()

    row_count = len(df)
    total_cells = df.shape[0] * df.shape[1]
    if total_cells > 0:
        missing_pct = (df.isna().sum().sum() / total_cells) * 100
    else:
        missing_pct = 0

    summary.append({
        "resource": r,
        "rows": row_count,
        "missing_percent": round(missing_pct, 2)
    })

    # Export cleaned CSV (for analysis)
    df.to_csv(os.path.join(analytics_root, f"{r}.csv"), index=False)

    print(f"✅ Loaded {r}: {row_count} rows")

# Export report
summary_df = pd.DataFrame(summary)
summary_df.to_csv(os.path.join(analytics_root, "metrics_overview.csv"), index=False)

print("\n🎯 Done! Metrics saved to out/analytics/metrics_overview.csv")
