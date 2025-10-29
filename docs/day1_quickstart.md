# Quickstart

This project converts Synthea-based healthcare CSV files into NDJSON format for analytics.

---

## ✅ Setup

Install Python requirements:

```bash
pip install pandas
```

Place all input CSV files in:

```
data/
```

Example:
- patients.csv
- encounters.csv
- observations.csv
- conditions.csv
- medications.csv
- allergies.csv
- ... (up to 15 CSVs)

---

## 🔄 Convert CSV → NDJSON

Run the conversion script:

```bash
python src/convert_all.py
```

This will generate NDJSON files in:

```
out/
```

Example output:
- patients.ndjson
- encounters.ndjson
- observations.ndjson
- ... (15 NDJSON files)

---

## 🔍 Verify Output

Check a few rows:

```bash
head -3 out/patients.ndjson
```

Each line should show one JSON object.

Next, clean the data and prepare it for analytics.

python src/analytics/01_load.py

## Folder Structure

project/
├── data/
│   ├── patients.csv
│   ├── encounters.csv
│   └── observations.csv
│
├── src/
│   ├── conversion.py
│   └── analytics/
│       └── 01_load.py
│
├── out/
│   ├── *.ndjson
│   └── analytics/
│       ├── *.csv
│       └── metrics_overview.csv
│
└── docs/
    └── quickstart.md
