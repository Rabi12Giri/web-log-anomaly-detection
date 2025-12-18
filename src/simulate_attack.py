import pandas as pd
import numpy as np

IN_FILE = "./data/processed/features.csv"
OUT_FILE = "./data/processed/manual_anomaly_attack.csv"

TARGET_SIZE = 120_000        # choose 100k–150k
ATTACK_RATIO = 0.7           # 70% anomaly-like

# Load & keep schema
cols = ["ip", "total_requests", "unique_urls", "avg_url_length", "error_rate"]
df = pd.read_csv(IN_FILE, usecols=cols)

# Shuffle full dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Downsample to target size
df = df.iloc[:TARGET_SIZE].copy()

# Split counts
attack_n = int(TARGET_SIZE * ATTACK_RATIO)
normal_n = TARGET_SIZE - attack_n

attack_df = df.iloc[:attack_n].copy()
normal_df = df.iloc[attack_n:].copy()

# ---- Amplify ATTACK rows ----
attack_df["total_requests"] = (
    attack_df["total_requests"] * np.random.uniform(1.6, 2.5)
).round()

attack_df["unique_urls"] = (
    attack_df["unique_urls"] * np.random.uniform(1.3, 2.0)
).round()

attack_df["avg_url_length"] = (
    attack_df["avg_url_length"] * np.random.uniform(1.1, 1.4)
)

attack_df["error_rate"] = np.clip(
    attack_df["error_rate"] + np.random.uniform(0.15, 0.35),
    0,
    1,
)

# ---- Keep NORMAL rows clean (slightly dampened) ----
normal_df["error_rate"] = np.clip(
    normal_df["error_rate"] * np.random.uniform(0.5, 0.9),
    0,
    1,
)

# ---- Merge back ----
final_df = pd.concat([attack_df, normal_df], ignore_index=True)

# ---- Sanity checks ----
final_df["total_requests"] = final_df["total_requests"].astype(int)
final_df["unique_urls"] = final_df["unique_urls"].astype(int)
final_df["unique_urls"] = np.minimum(
    final_df["unique_urls"], final_df["total_requests"]
)

final_df["avg_url_length"] = final_df["avg_url_length"].round(2)
final_df["error_rate"] = final_df["error_rate"].round(3)

# Final shuffle (VERY IMPORTANT)
final_df = final_df.sample(frac=1, random_state=99).reset_index(drop=True)

# Save
final_df.to_csv(OUT_FILE, index=False, columns=cols)

print("✔ Dataset created")
print("Total rows:", len(final_df))
print("Attack-like rows:", attack_n)
print("Normal rows:", normal_n)
print("Schema:", list(final_df.columns))
