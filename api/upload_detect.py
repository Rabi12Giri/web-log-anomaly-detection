import os
import uuid
import pandas as pd
import joblib
from fastapi import UploadFile, File, HTTPException

MODEL_FILE = "models/isolation_forest.pkl"
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

def detect_from_uploaded_csv(file: UploadFile, top_n: int = 10):
    # Accept only CSV
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    # Save uploaded file
    file_id = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, file_id)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Load CSV
    df = pd.read_csv(file_path)

    if "ip" not in df.columns:
        raise HTTPException(status_code=400, detail="CSV must contain 'ip' column")

    # Prepare features
    X = df.drop(columns=["ip"])

    # Load model
    model, scaler = joblib.load(MODEL_FILE)
    X_scaled = scaler.transform(X)

    # Predict
    df["anomaly_score"] = model.decision_function(X_scaled)
    df["anomaly_raw"] = model.predict(X_scaled)
    df["anomaly"] = df["anomaly_raw"].apply(
        lambda x: "ANOMALY" if x == -1 else "NORMAL"
    )

    anomalies = df[df["anomaly"] == "ANOMALY"]
    top_anomalies = anomalies.sort_values("anomaly_score").head(top_n)

    return {
        "uploaded_file": file.filename,
        "total_rows": int(len(df)),
        "anomalies_detected": int(len(anomalies)),
        "alert": bool(len(anomalies) > 0),
        "top_anomalies": top_anomalies[
            ["ip", "anomaly_score"]
        ].to_dict(orient="records"),
    }
