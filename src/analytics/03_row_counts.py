import pandas as pd
import matplotlib.pyplot as plt
import os

analytics_root = "out/analytics"
os.makedirs(analytics_root, exist_ok=True)

# --- Load metrics file ---
metrics_path = os.path.join(analytics_root, "metrics_overview.csv")

if not os.path.exists(metrics_path):
    raise FileNotFoundError(f"❌ {metrics_path} not found. Run 01_load.py first.")

metrics = pd.read_csv(metrics_path)

# --- Clean and ensure numeric ---
metrics.columns = metrics.columns.str.strip().str.lower()
metrics['rows'] = pd.to_numeric(metrics['rows'], errors='coerce').fillna(0).astype(int)

# --- Sort by row count for clarity ---
metrics = metrics.sort_values('rows', ascending=False)

# --- Plot ---
plt.figure(figsize=(10, 6))
bars = plt.bar(metrics['resource'], metrics['rows'])
plt.xticks(rotation=45, ha='right')
plt.ylabel("Number of Rows")
plt.title("Row Count by Resource")
plt.tight_layout()

# --- Annotate values on top of bars ---
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f"{height:,}", 
             ha='center', va='bottom', fontsize=9)

# --- Save ---
output_path = os.path.join(analytics_root, "row_counts.png")
plt.savefig(output_path, dpi=300)
plt.close()

print(f"✅ Saved chart: {output_path}")
