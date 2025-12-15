# simulate_attack.py
# Injects multiple artificial attack patterns

import pandas as pd

INPUT_FILE = "data/processed/features_baseline.csv"
OUTPUT_FILE = "data/processed/features_with_attack.csv"

print("Loading feature data...")
df = pd.read_csv(INPUT_FILE)

print("Injecting multiple artificial attack patterns...")

max_requests = df["total_requests"].max()
max_urls = df["unique_urls"].max()
avg_url_len = df["avg_url_length"].mean()

attack_rows = [
    # Attack 1: Extreme brute-force / bot
    {
        "ip": "999.999.999.1",
        "total_requests": max_requests * 50,
        "unique_urls": max_urls * 50,
        "avg_url_length": avg_url_len,
        "error_rate": 0.95
    },

    # Attack 2: URL scanning attack
    {
        "ip": "999.999.999.2",
        "total_requests": max_requests * 10,
        "unique_urls": max_urls * 40,
        "avg_url_length": avg_url_len * 2,
        "error_rate": 0.60
    },

    # Attack 3: Low-and-slow suspicious behaviour
    {
        "ip": "999.999.999.3",
        "total_requests": max_requests * 5,
        "unique_urls": max_urls * 5,
        "avg_url_length": avg_url_len,
        "error_rate": 0.20
    },

    # Attack 4: Error-heavy probing
    {
        "ip": "999.999.999.4",
        "total_requests": max_requests * 8,
        "unique_urls": max_urls * 8,
        "avg_url_length": avg_url_len,
        "error_rate": 0.99
    }
]

attack_df = pd.DataFrame(attack_rows)

df = pd.concat([df, attack_df], ignore_index=True)

df.to_csv(OUTPUT_FILE, index=False)

print("Multiple attack simulation completed.")
print("Saved features_with_attack.csv")
