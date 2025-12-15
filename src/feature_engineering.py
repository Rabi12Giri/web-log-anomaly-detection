# feature_engineering.py
# Converts parsed logs into ML-ready features

import pandas as pd

INPUT_FILE = "data/processed/parsed_logs.csv"
OUTPUT_FILE = "data/processed/features.csv"

print("Starting feature engineering...")

# Load data in chunks (safe for large files)
chunks = pd.read_csv(INPUT_FILE, chunksize=500_000, parse_dates=["time"])

aggregated = []

for chunk in chunks:
    # Group by IP
    group = chunk.groupby("ip").agg(
        total_requests=("url", "count"),
        unique_urls=("url", "nunique"),
        avg_url_length=("url", lambda x: x.str.len().mean()),
        error_rate=("status", lambda x: (x.astype(int) >= 400).mean()),
    )
    aggregated.append(group)

# Combine all chunks
features = pd.concat(aggregated).groupby("ip").mean().reset_index()

# Save features
features.to_csv(OUTPUT_FILE, index=False)

print("Feature engineering completed.")
print("Saved features.csv")
