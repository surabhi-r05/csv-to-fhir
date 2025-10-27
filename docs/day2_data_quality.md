# Day 2 — Data Quality & Loading Summary

This analysis loads NDJSON files into pandas and evaluates two key data quality metrics:
1. ✅ Dataset size (row counts)
2. ✅ Data completeness (missingness percentage)

All outputs are produced from:
- `src/analytics/01_load.py`
- `src/analytics/02_missingness.py`
- `src/analytics/03_row_counts.py`

Data analyzed from 15 Synthea resource files located in:

```
out/
```

Processed CSVs and results saved into:

```
out/analytics/
```

---

## 📊 Row Counts by Resource

The chart below shows the volume of data from each clinical domain:

🖼️ `out/analytics/row_counts.png`

> Helps identify **high-activity** clinical datasets (e.g., Observations) vs. smaller ones (e.g., Imaging Studies).

---

## ❗ Missingness by Resource

🖼️ `out/analytics/missingness_bar.png`

> This reveals variation in documentation completeness between resource types.

- Observations often show higher missingness due to many optional clinical fields
- Administrative tables like Providers and Payers show lower missingness

---

## ✅ Outputs Generated

| File | Description |
|------|-------------|
| `metrics_overview.csv` | Summary of rows + missing data %
| `*.csv` for each resource | Cleaned analytics-friendly versions
| `missingness_bar.png` | Visualization of missing data
| `row_counts.png` | Visualization of dataset volume

---

## 📌 Key Takeaways

- ✅ Observations and encounters are the **largest** datasets → important for downstream analytics
- ❗ Some clinical fields remain incomplete → needs handling in later transformations
- ✅ All datasets successfully loaded → foundation is ready for semantic mapping & analytics

---
