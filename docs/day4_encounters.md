# 🩺 Day 4 – Encounter & LOS Analysis

**Script:** `08_encounters_analysis.py`  
**Outputs:**  
- `encounters_by_day.csv`  
- `los_distribution.csv`  
- `los_summary.csv`  
- `encounters_trend.png`  
- `median_los_by_class.png`  
- `median_los_by_class_hours.png`  
- `los_box.png`

---

## 📘 Overview

This analysis focuses on **encounter activity and duration (Length of Stay – LOS)** across different encounter classes.  
Key steps included:

- Calculating **LOS in both days and hours**  
- Removing **outliers dynamically** per class using the 95th percentile (or >14 days)  
- Summarizing **encounter patterns and medians**  
- Visualizing **trends and duration distributions**

---

## 📅 Encounters per Day

A time-series line chart (`encounters_trend.png`) visualizes encounter volume trends.  
Short spikes often correspond to **wellness or ambulatory visits**, while inpatient events are rarer but longer.

---

## 📊 LOS Summary by Encounter Class

| Encounter Class | Count | Mean (days) | Median (days) | IQR | Max | P95 Threshold (days) | Median (hours) |
|------------------|-------|--------------|----------------|------|------|-----------------------|----------------|
| **inpatient** | 1,834 | 1.09 | 1.02 | 0.08 | 6.0 | 1.17 | — |
| **emergency** | 2,089 | 0.06 | 0.05 | 0.02 | 0.37 | 0.10 | 1.25 |
| **ambulatory** | 18,851 | 0.12 | 0.03 | 0.04 | 14.0 | 0.14 | 0.75 |
| **outpatient** | 8,890 | 0.02 | 0.01 | 0.01 | 7.0 | 0.04 | 0.25 |
| **urgentcare** | 2,373 | 0.01 | 0.01 | 0.00 | 0.01 | 0.01 | 0.25 |
| **wellness** | 19,106 | 0.02 | 0.01 | 0.01 | 0.05 | 0.02 | 0.25 |

---

## 📈 Visual Highlights

### 🩹 1. **Encounter Trend**
- Shows overall encounter activity per day.
- Helps identify **service utilization peaks**.

### 🕒 2. **Median LOS (Days)**
- `median_los_by_class.png`
- Inpatients have the longest median LOS (~1 day).
- Other classes show sub-day durations.

### ⏱️ 3. **Median LOS (Hours)**
- `median_los_by_class_hours.png`
- Useful for **short-stay** classes like *ambulatory*, *outpatient*, and *wellness*.

### 📦 4. **LOS Boxplot**
- `los_box.png`
- Displays LOS distribution spread and skew per class.
- **Inpatient** stays show modest variation around the 1-day median, while **ambulatory** visits have a long right tail (occasional extended stays).

---

## 💡 Key Insights

- **Inpatient stays** are short (median ~1 day) but tightly distributed, showing good discharge efficiency.  
- **Ambulatory and outpatient** visits dominate in volume and represent the majority of same-day encounters.  
- **Emergency** encounters have a slightly longer spread, averaging ~1.25 hours.  
- **Wellness and urgent care** are consistently brief, indicating preventive or minor consultation-type visits.  
- Outlier filtering (>95th percentile or >14 days) ensures that only realistic encounter durations contribute to LOS statistics.

---

## 📁 Output Summary

| File | Description |
|------|--------------|
| `encounters_by_day.csv` | Number of encounters per day |
| `los_distribution.csv` | Detailed LOS data per encounter (in days & hours) |
| `los_summary.csv` | Aggregated LOS stats, thresholds & median hours |
| `encounters_trend.png` | Line chart of daily encounters |
| `median_los_by_class.png` | Median LOS by encounter class (days) |
| `median_los_by_class_hours.png` | Median LOS by encounter class (hours) |
| `los_box.png` | Boxplot showing LOS distribution per class |

---

✅ **Conclusion:**  
Encounter data reveals a strong predominance of ambulatory and wellness visits, with inpatient stays averaging around one day.  
The inclusion of both **days and hours metrics** enhances interpretability across short- and long-duration encounter classes.
