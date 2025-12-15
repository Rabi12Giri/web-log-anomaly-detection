# plot_attack_comparison.py
# Compares anomaly scores before and after attack injection

import pandas as pd
import joblib
import matplotlib.pyplot as plt

MODEL_FILE = "models/isolation_forest.pkl"

# Load model
model, scaler = joblib.load(MODEL_FILE)

# Load normal data
df_normal = pd.read_csv("data/processed/features.csv")
X_normal = df_normal.drop(columns=["ip"])
X_normal_scaled = scaler.transform(X_normal)
df_normal["anomaly_score"] = model.decision_function(X_normal_scaled)

# Load attack data
df_attack = pd.read_csv("data/processed/features_with_attack.csv")
X_attack = df_attack.drop(columns=["ip"])
X_attack_scaled = scaler.transform(X_attack)
df_attack["anomaly_score"] = model.decision_function(X_attack_scaled)

# Plot
plt.figure()
plt.hist(df_normal["anomaly_score"], bins=50, alpha=0.6, label="Normal Data")
plt.hist(df_attack["anomaly_score"], bins=50, alpha=0.6, label="With Attack Data")
plt.xlabel("Anomaly Score (lower = more suspicious)")
plt.ylabel("Frequency")
plt.title("Anomaly Score Comparison")
plt.legend()
plt.show()
