# 📊 Analytics — Methods & Outputs

This document summarizes **how each analysis was performed**, what files were generated, and where to find the results.  
All analyses were run on **already-cleaned CSVs** located in `out/analytics/`.

---

## ⚙️ Overview

**Primary inputs**
- `patients.csv`
- `encounters.csv`
- `observations.csv`

**Key summary outputs**
- `metrics_overview.csv`
- `demographics.csv`
- `los_summary.csv`
- `vitals_summary.csv`
- `cohort_summary.csv`
- `stats_tests.csv`

**Charts folder:** `out/analytics/*.png`

---

## 🧾 Metrics Overview (`01_load.py`, `02_missingness.py`, `03_row_counts.py`)

**Purpose:** Assess data completeness and record counts across resources.  
**Outputs:**
- `metrics_overview.csv` — rows & missingness per dataset
- `missingness_bar.png` — visual of null percentages
- `row_counts.png` — record counts per resource  

**Highlights**
- `patients.csv` has the highest missingness (~15.9%)  
- `observations.csv` well-covered (only 1.95% missing)

---

## 👤 Demographics (`04_age_distribution.py`, `05_gender_distribution.py`, `06_demographics_summary.py`)

**Methods**
- `AGE = floor((TODAY – BIRTHDATE)/365)`
- Age groups:  
  - Child (0–12) • Teen (13–18) • Young Adult (19–35)  
  - Adult (36–50) • Mid-Age (51–65) • Senior (65+)  

**Outputs**
- `demographics.csv`
- Charts: `age_distribution.png`, `age_boxplot.png`, `age_groups.png`, `gender_share.png`

**Findings**
- Avg age **49.7 yrs**, median **49.0**
- Seniors (65+) form **29%** of patients (341/1171)
- Gender near-balanced: **609 F / 562 M**

---

## 🗺️ Geography (`07_geo_citybubbles.py`)

**What:** City-level bubble map of patient residence.  
**Input:** CITY, LAT, LON from `patients.csv`  
**Output:** `patients_city_bubbles.png`  
**Use:** Identify geographic clusters for outreach or service allocation.

---

## 🏥 Encounters & LOS (`08_encounters_analysis.py`)

**Computed**
- `LOS_days = (STOP − START)/86400`, clipped ≥ 0  
- `LOS_hours = LOS_days × 24`
- Outlier removal rule: values > max(p95 per class, 14 days)

**Outputs**
- `los_distribution.csv` (cleaned with Id + Patient)
- `los_summary.csv` (count, mean, median, IQR, thresholds)
- `encounters_by_day.csv`
- Charts:  
  `encounters_trend.png` • `median_los_by_class.png`  
  `median_los_by_class_hours.png` • `los_box.png` • `avg_los_by_class.png`


### Outlier Thresholds (95th Percentile)

**Ambulatory:** 0.14 days | **Emergency:** 0.10 days | **Inpatient:** 1.17 days  
**Outpatient:** 0.04 days | **Urgent Care:** 0.01 days | **Wellness:** 0.02 days


---

## ❤️‍🩹 Observations / Vitals (`09_observations_analysis.py`)

**Steps**
- Filter numeric observations  
- Map standard LOINC codes → vital names  
- Keep *latest per patient per vital*  
- Compute mean, median, std, min, max, p10, p90, count, coverage %

**Outputs**
- `observation_summary.csv` — all vitals  
- `vitals_summary.csv` — key vitals (Weight, BMI, BP)
- Charts:  
  `vitals_summary_bar.png` • `bp_vs_bmi_scatter.png` • `vitals_correlation_heatmap.png`

## Highlights

| Vital          | Mean     | Median   | Coverage |
|----------------|----------|----------|----------:|
| BMI            | 26.4     | 27.8     | 96.8 %    |
| Systolic BP    | 121 mmHg | 119 mmHg | 100 %     |
| Diastolic BP   | 80.6 mmHg| 80 mmHg  | 100 %     |
| Heart Rate     | 79 bpm   | 79 bpm   | 100 %     |
| Temperature    | 37.6 °C  | 37.6 °C  | 48.9 %    |


**Charts**
- `bp_vs_bmi_scatter.png` → higher BMI linked to elevated BP  
- `vitals_correlation_heatmap.png` → strong BMI–Weight, moderate BP–BMI correlations

---

## 👥 Cohort Analysis (`10_cohort_analysis.py`)

**Cohorts**
1. **Older Adults:** Age ≥ 65  
2. **Multi-Encounter:** ≥ 3 encounters  
3. **Hypertensive-like:** Systolic ≥ 140 or Diastolic ≥ 90  

**Outputs**
- `cohort_summary.csv`
- `cohort_summary_detailed.csv`

**Summary**

| Cohort           | Patients | Avg Age | Avg Encounters |   % F  |   % M  |
|------------------|----------:|---------:|----------------:|-------:|-------:|
| Older Adults     | 349       | 82.4     | 77.0            | 47.3   | 52.7   |
| Multi-Encounter  | 1168      | 49.9     | 45.7            | 51.9   | 48.1   |
| Hypertensive-like| 157       | 48.8     | 74.1            | 51.6   | 48.4   |


---

## 📊 Statistical Tests (`11_stats_test.py`)

**Tests**
- **t-test:** LOS (Older vs Others) → *Welch’s unequal-variance*
- **χ² test:** Hypertensive-like × Gender independence

**Results**

| Test                         | Statistic | p value | Interpretation         |
|------------------------------|-----------:|---------:|------------------------|
| t-test (LOS Older vs Others) | −2.60      | 0.0093   | Significant difference |
| χ² (Hypertensive vs Gender)  | 0.00       | 1.000    | Independent            |


**Interpretation**
- Older adults **stay longer on average**, significant at p < 0.01.  
- Hypertension-like pattern shows **no gender bias**.

---

## 🖼️ Visual Highlights

| Chart | What it shows |
|-------|----------------|
| `age_distribution.png` | bell-shaped age spread centered near 50 |
| `gender_share.png` | balanced F/M ratio |
| `patients_city_bubbles.png` | dense patient clusters by city |
| `encounters_trend.png` | gradual growth + seasonal peaks |
| `median_los_by_class_hours.png` | short-stay durations clearly visible |
| `los_box.png` | inpatient long-tail contrast |
| `bp_vs_bmi_scatter.png` | upward BMI–BP trend |
| `vitals_correlation_heatmap.png` | strong BMI–Weight correlation |

---

## 🧩 Data Quality Notes

| File | Missing % |
|------|-----------:|
| patients.csv | 15.9 % |
| encounters.csv | 9.9 % |
| observations.csv | 1.9 % |

➡ Recommend focusing analyses on high-coverage columns (age, vitals, LOS).

---

## ⚡ How to Re-run the Pipeline

```bash
# (from project root)
python src/conversion.py
cd src/analytics

python 01_load.py
python 02_missingness.py
python 03_row_counts.py
python 04_age_distribution.py
python 05_gender_distribution.py
python 06_demographics_summary.py
python 07_geo_citybubbles.py
python 08_encounters_analysis.py
python 09_observations_analysis.py
python 10_cohort_analysis.py
python 11_stats_test.py
```
## 🔍 Quick Lookup

| Question | File / Chart |
|-----------|---------------|
| How many patients, avg age? | `demographics.csv` |
| Which cities dominate? | `patients_city_bubbles.png` |
| How long are typical stays? | `los_summary.csv`, `median_los_by_class.png` |
| How healthy are vitals? | `vitals_summary.csv`, `vitals_summary_bar.png` |
| Which groups are hypertensive or older? | `cohort_summary.csv` |
| Any significant group differences? | `stats_tests.csv` |

---