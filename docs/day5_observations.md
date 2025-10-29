# 📊 Day 5 – Observations Analysis

## Overview
This section analyzes key patient **vital signs** — including **Weight, BMI, Height, Heart Rate, Blood Pressure, Respiratory Rate,** and **Temperature** — based on the latest available measurements per patient.

We compute summary statistics such as **mean**, **median**, **standard deviation**, **percentiles (p10–p90)**, and **coverage (% of patients with recorded vitals)**.  
Additionally, we explore relationships between **BMI and Blood Pressure** and visualize inter-vital correlations.

---

## 🧮 Metrics Summary (`observation_summary.csv`)

| Vital Type | Mean | Median | Std | Min | Max | p10 | p90 | Patients | Coverage (%) |
|-------------|------|---------|------|------|------|------|-----------|---------------|
| BMI | 26.42 | 27.8 | 4.67 | 13.7 | 48.5 | 18.73 | 30.3 | 1134 | 96.84 |
| Body Temperature (°C) | 37.64 | 37.6 | 0.48 | 37.0 | 39.3 | 37.1 | 38.1 | 572 | 48.85 |
| Diastolic BP (mmHg) | 80.56 | 80.0 | 7.08 | 67.0 | 119.0 | 73.0 | 87.0 | 1171 | 100.0 |
| Heart Rate (/min) | 79.19 | 79.0 | 11.44 | 60.0 | 100.0 | 64.0 | 96.0 | 1171 | 100.0 |
| Height (cm) | 160.95 | 166.2 | 24.23 | 51.5 | 198.7 | 131.6 | 181.4 | 1171 | 100.0 |
| Respiratory Rate (/min) | 14.05 | 14.0 | 1.15 | 12.0 | 16.0 | 13.0 | 16.0 | 1171 | 100.0 |
| Systolic BP (mmHg) | 121.04 | 119.0 | 13.83 | 99.0 | 196.0 | 107.0 | 134.0 | 1171 | 100.0 |
| Weight (kg) | 71.25 | 76.8 | 23.65 | 3.1 | 130.2 | 32.2 | 95.0 | 1171 | 100.0 |

---

## 📈 Visuals Generated
- **`vitals_summary_bar.png`** – Mean ± SD for each vital type  
- **`bp_vs_bmi_scatter.png`** – Relationship between BMI and Systolic/Diastolic BP  
- **`vitals_correlation_heatmap.png`** – Annotated heatmap showing correlations among vitals  

---

## 💡 Insights
- **Coverage:** Nearly all patients have complete BP, HR, and Weight data (>95%), while Temperature is recorded for ~49% of the cohort.  
- **BMI Distribution:** Average BMI ~26.4 indicates a slightly overweight population.  
- **Blood Pressure:** Mean BP (121/81 mmHg) is within normal range, but tails (p90) suggest a subset with elevated BP.  
- **Heart Rate & Respiratory Rate:** Both fall within normal physiological limits, confirming data consistency.  
- **Correlations:** BMI shows a positive trend with both systolic and diastolic BP, aligning with clinical expectations.

---