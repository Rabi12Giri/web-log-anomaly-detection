import pandas as pd
import numpy as np
import requests

# =============================
# CONFIG
# =============================
IN_FILE = "./data/processed/features.csv"
OUT_FILE = "./data/processed/manual_anomaly_attack.csv"

API_URL = "http://127.0.0.1:8000/detect-ingest"


TARGET_SIZE = 120_000        # 100k–150k is ideal
ATTACK_RATIO = 0.7           # 70% anomaly-like

RANDOM_SEED_1 = 42
RANDOM_SEED_2 = 99

# =============================
# LOAD BASE DATA
# =============================
cols = [
    "ip",
    "total_requests",
    "unique_urls",
    "avg_url_length",
    "error_rate",
]

df = pd.read_csv(IN_FILE, usecols=cols)

# Shuffle original dataset
df = df.sample(frac=1, random_state=RANDOM_SEED_1).reset_index(drop=True)

# Downsample
df = df.iloc[:TARGET_SIZE].copy()

# =============================
# SPLIT NORMAL / ATTACK
# =============================
attack_n = int(TARGET_SIZE * ATTACK_RATIO)
normal_n = TARGET_SIZE - attack_n

attack_df = df.iloc[:attack_n].copy()
normal_df = df.iloc[attack_n:].copy()

# =============================
# AMPLIFY ATTACK BEHAVIOUR
# =============================
attack_df["total_requests"] = (
    attack_df["total_requests"] *
    np.random.uniform(1.6, 2.5)
).round()

attack_df["unique_urls"] = (
    attack_df["unique_urls"] *
    np.random.uniform(1.3, 2.0)
).round()

attack_df["avg_url_length"] = (
    attack_df["avg_url_length"] *
    np.random.uniform(1.1, 1.4)
)

attack_df["error_rate"] = np.clip(
    attack_df["error_rate"] +
    np.random.uniform(0.15, 0.35),
    0,
    1,
)

# =============================
# KEEP NORMAL BEHAVIOUR CLEAN
# =============================
normal_df["error_rate"] = np.clip(
    normal_df["error_rate"] *
    np.random.uniform(0.5, 0.9),
    0,
    1,
)

# =============================
# MERGE & FINAL SANITY CHECKS
# =============================
final_df = pd.concat(
    [attack_df, normal_df],
    ignore_index=True
)

final_df["total_requests"] = final_df["total_requests"].astype(int)
final_df["unique_urls"] = final_df["unique_urls"].astype(int)

final_df["unique_urls"] = np.minimum(
    final_df["unique_urls"],
    final_df["total_requests"]
)

final_df["avg_url_length"] = final_df["avg_url_length"].round(2)
final_df["error_rate"] = final_df["error_rate"].round(3)

# Final shuffle (VERY IMPORTANT)
final_df = final_df.sample(
    frac=1,
    random_state=RANDOM_SEED_2
).reset_index(drop=True)

# =============================
# SAVE CSV (OPTIONAL / DEMO)
# =============================
final_df.to_csv(OUT_FILE, index=False, columns=cols)

print("Synthetic dataset created")
print("Total rows:", len(final_df))
print("Attack-like rows:", attack_n)
print("Normal rows:", normal_n)
print("Schema:", list(final_df.columns))

# =============================
# AUTOMATIC API INGESTION
# =============================
print("\n Sending data to FastAPI for automated ingestion...")

response = requests.post(
    API_URL,
    json=final_df.to_dict(orient="records"),
    timeout=120
)

print("API status:", response.status_code)
print("Raw API response:")
print(response.text)
