import pandas as pd
import os

data_root = "data"

for file in os.listdir(data_root):
    if file.endswith(".csv"):
        path = os.path.join(data_root, file)
        try:
            df = pd.read_csv(path, nrows=1)
            print(f"\n📄 {file}")
            print(list(df.columns))
        except Exception as e:
            print(f"⚠️ Could not read {file}: {e}")

pd.read_csv("data/patients.csv", encoding="latin1", nrows=1).columns
