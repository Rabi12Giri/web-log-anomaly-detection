import pandas as pd
import numpy as np

IN_FILE = "./data/processed/features.csv"
OUT_FILE = "./data/processed/manual_anomaly_attack.csv"

df = pd.read_csv(IN_FILE)

# Keep ONLY the expected schema
cols = ["ip", "total_requests", "unique_urls", "avg_url_length", "error_rate"]
df = df[cols].copy()

# Shuffle rows
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

total = len(df)
attack_n = int(total * 0.7)

attack_idx = df.index < attack_n   # first 70% rows as "attack-like"
normal_idx = ~attack_idx

# --- Toned-down "attack-like" amplification (won’t explode file size) ---
# Requests + urls increase a bit, url length slightly, error rate increases but stays [0,1]
df.loc[attack_idx, "total_requests"] = (
    df.loc[attack_idx, "total_requests"] * np.random.uniform(1.3, 2.2)
).round()

df.loc[attack_idx, "unique_urls"] = (
    df.loc[attack_idx, "unique_urls"] * np.random.uniform(1.1, 1.8)
).round()

df.loc[attack_idx, "avg_url_length"] = (
    df.loc[attack_idx, "avg_url_length"] * np.random.uniform(1.05, 1.25)
)

df.loc[attack_idx, "error_rate"] = np.clip(
    df.loc[attack_idx, "error_rate"] + np.random.uniform(0.08, 0.25),
    0,
    1,
)

# --- Make sure values are logically consistent ---
# unique_urls should never exceed total_requests
df["total_requests"] = df["total_requests"].astype(int)
df["unique_urls"] = df["unique_urls"].astype(int)
df["unique_urls"] = np.minimum(df["unique_urls"], df["total_requests"])

# Reduce float precision to make CSV smaller
df["avg_url_length"] = df["avg_url_length"].round(2)
df["error_rate"] = df["error_rate"].round(3)

# Save with the SAME 5 columns
df.to_csv(OUT_FILE, index=False, columns=cols)

print("✔ Saved:", OUT_FILE)
print("Rows:", len(df))
print("Attack-like rows (first 70%):", attack_n)
print("Schema:", list(df.columns))
