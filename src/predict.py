# predict.py
# Runs anomaly detection using trained model

import pandas as pd
import joblib
import json

INPUT_FILE = "data/processed/features.csv"
MODEL_FILE = "models/isolation_forest.pkl"
OUTPUT_LOG = "logs/predictions.json"

print("Loading data and model...")

# Load data
df = pd.read_csv(INPUT_FILE)
ips = df["ip"]
X = df.drop(columns=["ip"])

# Load model and scaler
model, scaler = joblib.load(MODEL_FILE)

# Scale input
X_scaled = scaler.transform(X)

print("Generating anomaly predictions...")

# Predict anomalies
df["anomaly_score"] = model.decision_function(X_scaled)
df["anomaly"] = model.predict(X_scaled)

# Convert output (-1 = anomaly, 1 = normal)
df["anomaly"] = df["anomaly"].apply(lambda x: "ANOMALY" if x == -1 else "NORMAL")

# Save predictions
results = df[["ip", "anomaly_score", "anomaly"]].to_dict(orient="records")

with open(OUTPUT_LOG, "w") as f:
    json.dump(results, f, indent=2)

print("Prediction completed.")
print("Results saved to logs/predictions.json")

# Show top anomalies
print("\nTop suspicious IPs:")
print(df.sort_values("anomaly_score").head(5))
