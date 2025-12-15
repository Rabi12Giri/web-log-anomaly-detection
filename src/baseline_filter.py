# baseline_filter.py
# Creates a clean baseline dataset by removing extreme traffic

import pandas as pd

INPUT_FILE = "data/processed/features.csv"
OUTPUT_FILE = "data/processed/features_baseline.csv"

print("Loading feature data...")

df = pd.read_csv(INPUT_FILE)

# Calculate threshold (top 1% traffic)
threshold = df["total_requests"].quantile(0.99)

print(f"Removing IPs with total_requests > {threshold}")

# Keep only baseline (mostly normal) data
baseline_df = df[df["total_requests"] <= threshold]

baseline_df.to_csv(OUTPUT_FILE, index=False)

print("Baseline filtering completed.")
print("Saved features_baseline.csv")
