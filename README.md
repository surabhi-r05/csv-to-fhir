# 🩺 Healthcare Analytics Project

An **end-to-end healthcare data analytics pipeline** that transforms raw **Synthea-generated FHIR-like CSVs** into rich, visualized insights — using Python and MkDocs Material.

Explore the live analytics site here:  
👉 **[https://surabhi-r05.github.io/csv-to-fhir/](https://surabhi-r05.github.io/csv-to-fhir/)**

---

## 🚀 Features

- **Automated Analytics Pipeline:** Sequentially runs all Python scripts in `src/analytics/`
- **Data Quality Checks:** Missingness, coverage, and completeness analysis  
- **Demographic Profiling:** Age, gender, race, and location distributions  
- **Encounter & Vitals Trends:** Length of stay, BMI, BP, heart rate  
- **Cohort-Based Insights:** Older adults, hypertensive-like, multi-encounter patients  
- **Interactive Documentation:** Built and deployed via MkDocs Material  

---

## ⚙️ Run Locally

```powershell
# 1️⃣ Run all analytics scripts
Get-ChildItem src/analytics -Filter *.py | Sort-Object Name | ForEach-Object { python $_.FullName }

# 2️⃣ Copy generated charts to docs/images
New-Item -ItemType Directory -Force -Path docs/images; Copy-Item -Path out/analytics\*.png -Destination docs/images -Force

# 3️⃣ Serve documentation locally
mkdocs serve
```
---

##  Folder Structure
```text

csv-to-fhir/
│
├── src/
│   └── analytics/             # All daily Python analytics scripts (Day 1–Day 8)
│
├── data/                      # Raw CSVs (patients, encounters, observations, etc.)
│
├── out/
│   └── analytics/             # Generated charts and processed data outputs
│
├── docs/
│   ├── images/                # Visualization images copied here for MkDocs
│   ├── index.md               # Homepage
│   ├── dayX_*.md              # Day-wise reports
│   └── insights.md            # Final integrated insights
│
├── styles/
│   └── extra.css              # Custom theme overrides
│
├── mkdocs.yml                 # MkDocs configuration file
└── README.md                  # Project overview (this file)
```
---

## 🧩 Tech Stack

- **Python 3.12+** — Data cleaning, aggregation, and visualization  
- **MkDocs Material** — Documentation and interactive dashboard  
- **GitHub Pages** — Hosting for live deployment  

