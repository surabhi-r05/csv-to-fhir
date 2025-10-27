import pandas as pd
import matplotlib.pyplot as plt
import os

analytics_root = "out/analytics"

metrics = pd.read_csv(os.path.join(analytics_root, "metrics_overview.csv"))

plt.figure(figsize=(12, 6))
plt.bar(metrics['resource'], metrics['missing_percent'])
plt.xticks(rotation=75, ha='right')
plt.ylabel("Missing Data (%)")
plt.title("Average Missingness by Resource")

# ✅ Dynamic y-axis for visibility
plt.ylim(0, max(metrics['missing_percent']) + 5)

plt.tight_layout()
output_path = os.path.join(analytics_root, "missingness_bar.png")
plt.savefig(output_path)
plt.close()

print(f"✅ Saved chart: {output_path}")
