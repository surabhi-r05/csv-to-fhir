# ============================================================
# 🩺 FHIR Analytics Project - Windows Makefile
# ============================================================

# --- Variables ---
PYTHON = python
SRC_DIR = src/analytics
OUT_DIR = out/analytics
DOC_IMG_DIR = docs/images

# ============================================================
# 1️⃣ Run All Analytics Scripts (01–11)
# ============================================================
analytics:
	@echo Running analytics pipeline...
	$(PYTHON) $(SRC_DIR)/01_load.py
	$(PYTHON) $(SRC_DIR)/02_missingness.py
	$(PYTHON) $(SRC_DIR)/03_row_counts.py
	$(PYTHON) $(SRC_DIR)/04_age_distribution.py
	$(PYTHON) $(SRC_DIR)/05_gender_distribution.py
	$(PYTHON) $(SRC_DIR)/06_demographics_summary.py
	$(PYTHON) $(SRC_DIR)/07_geo_citybubbles.py
	$(PYTHON) $(SRC_DIR)/08_encounters_analysis.py
	$(PYTHON) $(SRC_DIR)/09_observations_analysis.py
	$(PYTHON) $(SRC_DIR)/10_cohort_analysis.py
	$(PYTHON) $(SRC_DIR)/11_stats_test.py
	@echo ✅ Analytics completed successfully!

# ============================================================
# 2️⃣ Copy Output Charts → docs/images for MkDocs
# ============================================================
copy-to-docs:
	@echo Copying analytics charts to docs/images...
	if not exist $(DOC_IMG_DIR) mkdir $(DOC_IMG_DIR)
	xcopy $(OUT_DIR)\* $(DOC_IMG_DIR)\ /E /I /Y >nul
	@echo ✅ Charts copied successfully!

# ============================================================
# 3️⃣ Build and Preview MkDocs Site Locally
# ============================================================
serve:
	@echo Starting MkDocs local server...
	mkdocs serve

# ============================================================
# 4️⃣ Full Workflow: Run Analytics → Copy Images → Serve Docs
# ============================================================
site:
	@echo Running full site workflow...
	make analytics
	make copy-to-docs
	mkdocs serve

# ============================================================
# 5️⃣ Cleanup (optional)
# ============================================================
clean:
	@echo Cleaning output folders...
	if exist $(OUT_DIR) rmdir /s /q $(OUT_DIR)
	if exist $(DOC_IMG_DIR) rmdir /s /q $(DOC_IMG_DIR)
	@echo 🧹 Cleanup complete!
