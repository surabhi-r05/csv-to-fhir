import pandas as pd
import matplotlib.pyplot as plt
import os

analytics_root = "out/analytics"

# Load metrics generated earlier
metrics = pd.read_csv(os.path.join(analytics_root, "metrics_overview.csv"))

plt.figure(figsize=(12, 6))
plt.bar(metrics['resource'], metrics['rows'])
plt.xticks(rotation=75, ha='right')
plt.ylabel("Number of Rows")
plt.title("Row Count by Resource")
plt.tight_layout()

output_path = os.path.join(analytics_root, "row_counts.png")
plt.savefig(output_path)
plt.close()

print(f"✅ Saved chart: {output_path}")
