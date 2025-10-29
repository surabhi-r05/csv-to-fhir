# 🏥 Day 4 – Encounters Analytics

This step focuses on analyzing patient encounters to understand care activity patterns, encounter mix, and visit durations.

The analysis was performed on the `encounters.csv` dataset, producing daily encounter metrics and length-of-stay (LOS) statistics across different encounter classes.

---

## 📈 Encounter Volume Trend

🖼️ `out/analytics/encounters_trend.png`

Encounters were grouped by their `START` date to measure patient flow over time.

- Each point represents the number of encounters recorded per day.
- A smoothed line and shaded area highlight fluctuations in daily activity.

📁 Output: `encounters_by_day.csv`

> **Insight:** Encounter volume fluctuates modestly over time, with clear patterns of peak activity on certain days, reflecting typical synthetic dataset scheduling behavior.

---

## ⏱️ Encounter Duration (LOS – Length of Stay)

To better reflect real-world durations, Length of Stay (LOS) was calculated in **hours** using the difference between encounter `STOP` and `START` timestamps.

Two complementary perspectives were produced:

### 1️⃣ LOS by Encounter Class (Box Plot)

🖼️ `out/analytics/los_box.png`  
📁 Raw Data: `los_distribution.csv`

- Each box represents the LOS spread for a given encounter class.
- Most outpatient and wellness encounters occur within an hour.
- Ambulatory visits show similar short durations.

> **Observation:** The dataset primarily contains same-day visits (e.g., ambulatory and wellness), with minimal inpatient representation — typical for Synthea’s synthetic data.

---

### 2️⃣ Average LOS by Encounter Class

🖼️ `out/analytics/avg_los_by_class.png`  
📁 Summary Table: `los_summary.csv`

| Metric | Description |
|---------|--------------|
| **count** | Number of encounters in each class |
| **mean** | Average duration (hours) |
| **median** | Median duration |
| **max** | Longest observed stay |

> **Insight:** Average durations are short (typically under one hour), consistent with preventive or outpatient care patterns.

---

## ✅ Summary

| Key Metric | Description |
|-------------|--------------|
| **Encounters/day** | Daily volume of patient visits |
| **Encounter Class Mix** | Proportion of Ambulatory, Wellness, Outpatient, etc. |
| **LOS (hours)** | Length of Stay – duration between START and STOP times |

**Generated Outputs**

| Type | File |
|------|------|
| Encounter Trend | `encounters_trend.png` |
| LOS Boxplot | `los_box.png` |
| Avg LOS by Class | `avg_los_by_class.png` |
| Daily Metrics | `encounters_by_day.csv` |
| LOS Distribution (all rows) | `los_distribution.csv` |
| LOS Summary (aggregated) | `los_summary.csv` |

---

## 🧭 Insights Summary


| Encounter Class | Count | Avg LOS (hours) | Median | Max LOS (hours) | Interpretation |
|-----------------|-------:|----------------:|--------:|----------------:|----------------|
| **Outpatient** | 9,003 | 2,993.45 | 0.25 | 766,080.25 | Data irregularities detected — likely timestamp errors for some encounters. Most outpatient visits should be under a day, but a few extreme outliers inflated the mean. |
| **Inpatient** | 1,838 | 432.97 | 24.4 | 485,164.67 | True multi-day hospitalizations visible (median ≈ 1 day). Outliers again inflate the mean but trend matches expected inpatient behavior. |
| **Emergency** | 2,090 | 27.18 | 1.25 | 53,952.00 | Short emergency visits dominate; occasional long records likely reflect mis-coded or extended stays. |
| **Ambulatory** | 18,936 | 9.86 | 0.75 | 61,608.00 | Mostly short same-day consultations (median < 1 hr). A few incorrect timestamps cause outliers. |
| **Wellness** | 19,106 | 0.37 | 0.25 | 1.28 | Consistent with check-up visits — typically under an hour, low variance. |
| **Urgent Care** | 2,373 | 0.25 | 0.25 | 0.25 | All visits recorded as short-duration same-day episodes, perfectly aligned with expected clinic workflow. |

---

### 📊 Overall Interpretation

- **Wellness** and **Urgent Care** visits dominate in count and show realistic durations (~15–30 minutes).  
- **Ambulatory** and **Outpatient** classes include timestamp outliers — some with unrealistic durations extending to months.  
- **Inpatient** encounters display reasonable medians (≈24 hours), aligning with overnight or short-stay hospitalizations.  
- **Emergency** shows mixed durations, reflecting both brief ER consultations and a few longer emergency-to-admission transitions.  
- Overall, **median values** provide a more reliable insight than the inflated means due to outlier timestamps.  




