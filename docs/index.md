# 🩺 Healthcare Analytics Project

Welcome to the **Healthcare Analytics Dashboard**, built using Synthea-generated healthcare data.  
This project automates the entire process — from raw FHIR-based CSVs to visualized insights.

---

## 📚 Overview

This repository demonstrates how to perform data analytics across multiple healthcare dimensions — demographics, encounters, vitals, cohorts, and statistical tests — using a reproducible Python pipeline.

### 🔍 Key Analyses

- **Data Quality:** Assess missingness and completeness  
- **Demographics:** Explore population distributions (age, gender, race, city)  
- **Encounters:** Analyze hospital visits, durations, and trends  
- **Vitals:** Study BMI, blood pressure, and other health indicators  
- **Cohorts:** Segment patients into custom health groups  
- **Statistical Tests:** Run group comparisons and significance checks  
- **Insights:** Visualized summaries for each analytical stage  

---

## ⚙️ Run Locally (Windows PowerShell)

To reproduce all analytics and view documentation locally, run the following commands **from your project root**:

```powershell
# 1️⃣ Execute all analytics scripts
Get-ChildItem src/analytics -Filter *.py | Sort-Object Name | ForEach-Object { python $_.FullName }

# 2️⃣ Copy all generated charts to docs/images
New-Item -ItemType Directory -Force -Path docs/images
Copy-Item -Path out/analytics\*.png -Destination docs/images -Force

# 3️⃣ Launch MkDocs preview
mkdocs serve
```