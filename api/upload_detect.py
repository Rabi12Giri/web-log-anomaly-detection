import os
import uuid
import json
import pandas as pd
import joblib
from fastapi import UploadFile, HTTPException

MODEL_FILE = "models/isolation_forest.pkl"
UPLOAD_DIR = "uploads"
PREDICTIONS_FILE = "logs/predictions.json"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)

def severity_label(score: float) -> str:
    if score < -0.15:
        return "Critical"
    elif score < -0.12:
        return "High"
    elif score < -0.08:
        return "Medium"
    else:
        return "Low"

def detect_from_uploaded_csv(file: UploadFile, top_n: int = 40):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    df = pd.read_csv(file_path)

    if "ip" not in df.columns:
        raise HTTPException(status_code=400, detail="CSV must contain 'ip' column")

    X = df.drop(columns=["ip"])

    model, scaler = joblib.load(MODEL_FILE)
    X_scaled = scaler.transform(X)

    # Isolation Forest outputs
    df["anomaly_score"] = model.decision_function(X_scaled)
    df["anomaly_raw"] = model.predict(X_scaled)
    df["anomaly"] = df["anomaly_raw"].apply(
        lambda x: "ANOMALY" if x == -1 else "NORMAL"
    )

    # Percentile (higher = more anomalous)
    df["anomaly_percentile"] = (
        df["anomaly_score"].rank(pct=True, ascending=False) * 100
    )

    df["severity"] = df["anomaly_score"].apply(severity_label)

    # Save predictions for charts
    with open(PREDICTIONS_FILE, "w") as f:
        json.dump(df.to_dict(orient="records"), f, indent=2)

    # Filter anomalies
    anomalies = df[df["anomaly"] == "ANOMALY"]

    # 🔥 SUMMARY METRICS
    summary = {
        "total_rows": int(len(df)),
        "anomalies_detected": int(len(anomalies)),
        "critical_count": int((anomalies["severity"] == "Critical").sum()),
        "high_count": int((anomalies["severity"] == "High").sum()),
        "medium_count": int((anomalies["severity"] == "Medium").sum()),
        "low_count": int((anomalies["severity"] == "Low").sum()),
        "anomaly_percentage": round((len(anomalies) / len(df)) * 100, 2) if len(df) > 0 else 0,
    }
    top_anomalies = anomalies.sort_values("anomaly_score").head(top_n)

    return {
        "uploaded_file": file.filename,

 
        "total_rows": int(len(df)),
        "anomalies_detected": int(len(anomalies)),
        "alert": bool(len(anomalies) > 0),

        # for summary cards)
        "summary": summary,

        "top_anomalies": top_anomalies[
            ["ip", "anomaly_score", "anomaly_percentile", "severity"]
        ].to_dict(orient="records"),
    }

