# 📊 Day 3 – Demographics Analytics

This step focused on understanding the characteristics of the synthetic patient population using our consolidated **demographics.csv** dataset.

We analyzed key attributes such as age, gender, race, ethnicity, marital status, and geographic spread.

Total Patients Analyzed: **1,171**

---

## 👶 Age Distribution

Two complementary visualizations were generated:

🖼️ `out/analytics/age_groups_with_ranges.png`  
🖼️ `out/analytics/age_distribution_histogram.png`

**Summary of Age Statistics**
- **Average Age:** 49.7 years  
- **Median Age:** 49.0 years  
- **Age Range:** 5 to 115 years

**Population Spread by Age Group**
| Age Group | Patients |
|----------|----------:|
| Child (0–12) | 86 |
| Teen (13–18) | 74 |
| Young Adult (19–35) | 246 |
| Adult (36–50) | 200 |
| Mid-Age (51–65) | 224 |
| **Senior (65+)** | **341** |

➡️ Seniors make up the largest group → important for chronic disease analytics.

---

## 🚻 Gender Distribution

🖼️ `out/analytics/gender_share.png`

| Gender | Count |
|--------|------:|
| Female | 609 |
| Male | 562 |

Nearly equal distribution — valuable for bias-free model evaluation.

---

## 🌎 Race & Ethnicity Composition

Race and ethnicity align with Synthea’s real-world diversity assumptions.

| Category | Count |
|---------|------:|
| White | 965 |
| Black | 101 |
| Asian | 90 |
| Native | 13 |
| Other | 2 |

| Ethnicity | Count |
|----------|------:|
| Non-Hispanic | 1,058 |
| Hispanic | 113 |

➡️ Majority Non-Hispanic White but with meaningful representation of minority groups.

---

## 💍 Marital Status

| Status | Count |
|-------|------:|
| Married | 638 |
| Single | 153 |
| Other / Unknown | Remaining population |

Married segment aligns with the strong adult/senior population presence.

---

## 📍 Geographic Distribution (City-Level Population)

🖼️ `out/analytics/patients_city_bubbles.png`

Cities were derived from location fields and plotted based on latitude/longitude.

➡️ A few cities show clear population clusters — guiding future regional healthcare analysis.

---

## ✅ Insights Summary

| Key Demographic Finding | Why it matters |
|------------------------|----------------|
| Seniors form the largest age group | Higher chronic condition load expected |
| Balanced gender mix | No gender imbalance in clinical outcomes |
| Diverse race/ethnicity | Enables fairness analysis in future models |
| Distinct geographic clusters | Supports localized health burden comparisons |

