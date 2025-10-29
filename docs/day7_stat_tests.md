# 🧮 Day 7 – Statistical Tests

## Overview
This step examines **differences between patient cohorts** using inferential statistics.  
Two key tests were performed:

1. **Independent t-test** – to compare Length of Stay (LOS) between **Older Adults (≥65 years)** and **Others**.  
2. **Chi-square test** – to assess the relationship between **Hypertensive-like status** (systolic ≥140 or diastolic ≥90) and **Gender**.

---

## 🧠 Test 1: T-test (LOS – Older vs Others)

**Goal:**  
Check if older adults (age ≥ 65) stay longer than younger patients.

**Method:**
- LOS in days was calculated as `STOP − START` from the encounters file.  
- Each encounter was linked to its patient’s birthdate to compute **age at encounter**.  
- Patients were grouped into:  
  - **Older Adults:** age ≥ 65 years  
  - **Others:** age < 65 years  
- Welch’s independent t-test (`equal_var = False`) was applied to compare the two LOS distributions.

| Metric | Value |
|--------|--------|
| **Test Statistic (t)** | -2.6014 |
| **p-value** | 0.009288 |
| **Interpretation** | ✅ **Significant difference** |

### 📊 Explanation:
- Since *p < 0.05*, the difference in **Length of Stay (LOS)** between **Older Adults** and **Younger Patients** is **statistically significant**.  
- The **negative t-statistic** indicates that **Older Adults tend to stay longer** in healthcare encounters compared to younger patients.  
- This aligns with real-world expectations — older populations often require **more extended observation and inpatient care** due to comorbidities and slower recovery.

---

## ⚖️ Test 2: Chi-square (Hypertensive vs Gender)

**Goal:**  
Examine whether hypertension prevalence differs between males and females.

**Method:**
- Counts of hypertensive males and females were taken from the Day 6 cohort summary.  
- A 2 × 2 contingency table was built comparing gender vs hypertension status.  
- Pearson’s Chi-Square test was used to test independence.

| Metric | Value |
|--------|--------|
| **Chi-square Statistic (χ²)** | 0.0000 |
| **p-value** | 1.0000 |
| **Interpretation** | ⚖️ **Independent** |

### 📊 Explanation:
- Since *p = 1.0*, there is **no significant relationship** between **Gender** and **Hypertensive-like status**.  
- Both males and females show similar likelihoods of having elevated blood pressure readings.  
- This suggests that hypertension prevalence in your dataset is **balanced across genders**, consistent with typical synthetic EHR data distributions.

---

## ✅ Final Output: `stats_tests.csv`

### 🧾 Summary
- **Older patients have significantly longer hospital stays.**  
- **Gender does not influence hypertension prevalence.**

These findings highlight how **statistical validation** supports trends observed during descriptive analysis and provide a foundation for **risk stratification** or **clinical resource planning** in subsequent analytics stages.
