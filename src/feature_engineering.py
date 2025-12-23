# feature_engineering.py
# Converts parsed logs into ML-ready features

import pandas as pd
from pathlib import Path

# Default paths (used by manual mode)
DEFAULT_INPUT_FILE = "data/processed/parsed_logs.csv"
DEFAULT_OUTPUT_FILE = "data/processed/features.csv"


def build_features(
    input_file: str = DEFAULT_INPUT_FILE,
    output_file: str = DEFAULT_OUTPUT_FILE,
    chunksize: int = 500_000
):
    """
    Builds aggregated IP-level features from parsed logs.

    Safe for:
    - repeated automated execution
    - large log files (chunked)
    - live log growth scenarios
    """

    input_path = Path(input_file)
    if not input_path.exists():
        print(f"[feature_engineering] Input file not found: {input_file}")
        return

    print("[feature_engineering] Starting feature engineering...")

    chunks = pd.read_csv(
        input_file,
        chunksize=chunksize,
        parse_dates=["time"]
    )

    aggregated = []

    for chunk in chunks:
        group = chunk.groupby("ip").agg(
            total_requests=("url", "count"),
            unique_urls=("url", "nunique"),
            avg_url_length=("url", lambda x: x.str.len().mean()),
            error_rate=("status", lambda x: (x.astype(int) >= 400).mean()),
        )
        aggregated.append(group)

    if not aggregated:
        print("[feature_engineering] No data to process.")
        return

    # Combine chunk-level aggregations
    features = (
        pd.concat(aggregated)
        .groupby("ip")
        .mean()
        .reset_index()
    )

    features.to_csv(output_file, index=False)

    print("[feature_engineering] Feature engineering completed.")
    print(f"[feature_engineering] Saved to {output_file}")


def main():
    build_features()


if __name__ == "__main__":
    main()
