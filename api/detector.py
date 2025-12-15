# Uses predict logic

import pandas as pd
import joblib

MODEL_FILE = "models/isolation_forest.pkl"

def run_detection(input_file: str = "data/processed/features.csv", top_n: int = 10):
    """
    Loads features from CSV, runs anomaly detection, returns summary + top anomalies.
    """
    df = pd.read_csv(input_file)

    if "ip" not in df.columns:
        raise ValueError("CSV must contain an 'ip' column")

    ips = df["ip"]
    X = df.drop(columns=["ip"])

    # Load model + scaler
    model, scaler = joblib.load(MODEL_FILE)

    # Scale features
    X_scaled = scaler.transform(X)

    # Predict
    df["anomaly_score"] = model.decision_function(X_scaled)
    df["anomaly_raw"] = model.predict(X_scaled)  # -1 anomaly, 1 normal
    df["anomaly"] = df["anomaly_raw"].apply(lambda x: "ANOMALY" if x == -1 else "NORMAL")

    anomalies = df[df["anomaly"] == "ANOMALY"].copy()
    anomalies_sorted = anomalies.sort_values("anomaly_score").head(top_n)

    result = {
        "total_ips": int(len(df)),
        "anomalies_detected": int(len(anomalies)),
        "alert": bool(len(anomalies) > 0),
        "top_anomalies": anomalies_sorted[["ip", "anomaly_score"]].to_dict(orient="records"),
    }

    return result



