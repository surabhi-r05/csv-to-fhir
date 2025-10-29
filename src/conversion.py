import pandas as pd
import json
import os

data_root = "../data"
out_root = "../out"


def write_ndjson(records, filename):
    if not records:
        print(f"⚠️ Skipped empty: {filename}")
        return
    path = os.path.join(out_root, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(json.dumps(r, ensure_ascii=False) for r in records))
    print(f"✅ Wrote {len(records):>5} → {path}")

def safe_read(csvname):
    path = os.path.join(data_root, csvname)
    if not os.path.exists(path):
        print(f"❌ Missing {csvname}")
        return None
    try:
        return pd.read_csv(path, encoding="latin1")
    except Exception as e:
        print(f"⚠️ Error reading {csvname}: {e}")
        return None

def convert(csvname, outname):
    df = safe_read(csvname)
    if df is not None:
        records = df.fillna("").to_dict(orient="records")
        write_ndjson(records, outname)

# ======================================================
# Lossless conversion for ALL 15 key Synthea CSV files
# ======================================================

convert("patients.csv", "patients.ndjson")
convert("encounters.csv", "encounters.ndjson")
convert("observations.csv", "observations.ndjson")
convert("conditions.csv", "conditions.ndjson")
convert("allergies.csv", "allergies.ndjson")
convert("medications.csv", "medications.ndjson")
convert("procedures.csv", "procedures.ndjson")
convert("immunizations.csv", "immunizations.ndjson")
convert("devices.csv", "devices.ndjson")
convert("careplans.csv", "careplans.ndjson")
convert("imaging_studies.csv", "imaging_studies.ndjson")
convert("organizations.csv", "organizations.ndjson")
convert("providers.csv", "providers.ndjson")
convert("payers.csv", "payers.ndjson")
convert("payer_transitions.csv", "payer_transitions.ndjson")

print("\n🎯 All conversions complete! NDJSON files are ready in /out/")
