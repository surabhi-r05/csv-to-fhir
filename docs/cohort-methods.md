# 🧩 Cohort Definition Methods

This document describes how patient cohorts were created for comparative analysis.

---

## 👵 Older Adults (65+)
**Rule:**  
Patients aged **65 years or older** at the time of analysis.

**Logic:**
- Age calculated from `BIRTHDATE` in `patients.csv`.
- Included if `AGE ≥ 65`.
- Joined with encounters to compute average number of visits and LOS metrics.

**Purpose:**  
To study care patterns and hospitalization duration among elderly patients.

---

## 🔁 Multi-Encounter Patients (≥3)
**Rule:**  
Patients with **three or more encounters** recorded in `encounters.csv`.

**Logic:**
- Grouped by `PATIENT` ID.
- Counted number of encounters per patient.
- Included if `COUNT ≥ 3`.

**Purpose:**  
To identify frequent users of healthcare services and analyze engagement patterns.

---

## ❤️ Hypertensive-like Cohort
**Rule:**  
Patients with at least one **blood pressure reading** indicating possible hypertension.

**Logic:**
- Used `observations.csv` for systolic (`8480-6`) and diastolic (`8462-4`) codes.
- Classified as hypertensive-like if:
  - `Systolic ≥ 130 mmHg` **or**  
  - `Diastolic ≥ 80 mmHg`
- Latest valid observation per patient was used.

**Purpose:**  
To study prevalence and patterns among patients with high blood pressure indicators.

---

## 🧮 Summary Outputs
| File | Description |
|------|--------------|
| `cohort_summary.csv` | Overview of main cohorts with size, age, gender mix, and avg encounters. |
| `cohort_summary_detailed.csv` | Extended version with more computed metrics. |
| `stats_tests.csv` | T-test (LOS difference) and Chi-square (hypertension vs gender). |

---

## 📊 Interpretation of Cohort Summary

| Cohort | Key Insights |
|---------|---------------|
| **Older Adults (65+)** | 349 patients, avg. age ~82 years. They had the **highest average encounters (≈77)**, showing high utilization of inpatient and long-term care. Gender split is roughly balanced (47% F, 53% M). |
| **Multi-Encounter (≥3)** | 1,168 patients with an avg. of **~46 encounters each**, average age around 50. This indicates a broad active population using care services regularly. |
| **Hypertensive-like** | 157 patients with **avg. 74 encounters** and mean age near 49. Slight female predominance (52%). Indicates chronic management and frequent monitoring. |

**Overall Trends:**
- Older adults contribute disproportionately to total encounters.  
- Hypertension overlaps heavily with multi-encounter patients.  
- Gender distribution remains balanced across cohorts, suggesting no strong bias in care access.

---

## 🧠 Notes
- Each cohort is non-exclusive (patients may appear in multiple groups).  
- Cohort membership was derived directly from the analytics outputs.  
- Results were later used in `docs/insights.md` for comparative interpretation.
