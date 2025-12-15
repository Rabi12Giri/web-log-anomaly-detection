# train.py
# Trains an Isolation Forest model on engineered features

import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

INPUT_FILE = "data/processed/features.csv"
MODEL_FILE = "models/isolation_forest.pkl"

print("Loading feature data...")

# Load features
df = pd.read_csv(INPUT_FILE)

# Separate IP column (not used for training)
ips = df["ip"] #--> removing IP coz its a identifier and not a pattern.
X = df.drop(columns=["ip"])

print("Scaling features...")

# Scale features (important for ML)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("Training Isolation Forest model...")

# Create Isolation Forest model
model = IsolationForest(
    n_estimators=100,
    contamination=0.02,  # assuming 2% anomalies
    random_state=42
)

# Train model
model.fit(X_scaled)

# Save model and scaler
joblib.dump((model, scaler), MODEL_FILE)

print("Model training completed.")
print("Model saved to models/isolation_forest.pkl")
