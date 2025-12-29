# detector.py
# Uses predict logic with mitigation recommendations

import pandas as pd
import joblib
import hashlib
import json

from api.mitigation import assess_severity, suggest_mitigation

MODEL_FILE = "models/isolation_forest.pkl"


def _fingerprint_anomalies(anomalies_df: pd.DataFrame) -> str:
    """
    Creates a stable fingerprint for the current anomaly set.
    Used to detect whether anomalies are NEW or already seen.
    """
    if anomalies_df.empty:
        return "no-anomalies"

    payload = anomalies_df[["ip", "anomaly_score"]].round(5).to_dict(
        orient="records"
    )
    raw = json.dumps(payload, sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()


def run_detection(
    input_file: str = "data/processed/features.csv",
    top_n: int = 40
):
    """
    Loads features from CSV, runs anomaly detection,
    returns summary + top anomalies with mitigation guidance.
    """

    # Load features
    df = pd.read_csv(input_file)

    if "ip" not in df.columns:
        raise ValueError("CSV must contain an 'ip' column")

    X = df.drop(columns=["ip"])

    # Load model + scaler
    model, scaler = joblib.load(MODEL_FILE)

    # Scale features
    X_scaled = scaler.transform(X)

    # Predict anomalies
    df["anomaly_score"] = model.decision_function(X_scaled)
    df["anomaly_raw"] = model.predict(X_scaled)  # -1 anomaly, 1 normal
    df["anomaly"] = df["anomaly_raw"].apply(
        lambda x: "ANOMALY" if x == -1 else "NORMAL"
    )

    # Extract & sort anomalies
    anomalies = df[df["anomaly"] == "ANOMALY"].copy()
    anomalies_sorted = anomalies.sort_values(
        "anomaly_score"
    ).head(top_n)

    # Fingerprint anomalies (for automation)
    fingerprint = _fingerprint_anomalies(anomalies_sorted)

    # Build mitigation-aware response
    top_anomalies = []

    for _, row in anomalies_sorted.iterrows():
        anomaly_data = {
            "ip": row["ip"],
            "anomaly_score": row["anomaly_score"],
            "total_requests": row.get("total_requests", 0),
            "unique_urls": row.get("unique_urls", 0),
            "error_rate": row.get("error_rate", 0),
        }

        severity = assess_severity(anomaly_data)
        mitigation = suggest_mitigation(anomaly_data)

        top_anomalies.append({
            "ip": anomaly_data["ip"],
            "anomaly_score": anomaly_data["anomaly_score"],
            "severity": severity,
            "mitigation": mitigation
        })

    # Final result
    result = {
        "total_ips": int(len(df)),
        "anomalies_detected": int(len(anomalies)),
        "alert": bool(len(anomalies) > 0),
        "fingerprint": fingerprint,
        "top_anomalies": top_anomalies,
    }

    print ("result is, ", result)

    return result
