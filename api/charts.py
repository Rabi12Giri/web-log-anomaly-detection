import os
import json
import threading
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fastapi import APIRouter

router = APIRouter()

CHART_DIR = "charts"
os.makedirs(CHART_DIR, exist_ok=True)

PREDICTIONS_FILE = "logs/predictions.json"

# Global lock for matplotlib & file access
CHART_LOCK = threading.Lock()


def load_predictions_safe():
    if not os.path.exists(PREDICTIONS_FILE):
        return pd.DataFrame()

    try:
        with open(PREDICTIONS_FILE, "r") as f:
            data = json.load(f)
    except Exception:
        return pd.DataFrame()

    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)

    if "anomaly" not in df.columns and "anomaly_raw" in df.columns:
        df["anomaly"] = df["anomaly_raw"].apply(
            lambda x: "ANOMALY" if x == -1 else "NORMAL"
        )

    return df.copy() 

@router.get("/charts/anomaly-score-distribution")
def anomaly_score_distribution():
    with CHART_LOCK:
        df = load_predictions_safe()

        if df.empty or "anomaly_score" not in df.columns:
            return {"message": "No prediction data available"}

        normal = df[df["anomaly"] == "NORMAL"]["anomaly_score"]
        anomaly = df[df["anomaly"] == "ANOMALY"]["anomaly_score"]

        if normal.empty and anomaly.empty:
            return {"message": "No anomaly score data"}

        plt.figure(figsize=(8, 5))

        if not normal.empty:
            plt.hist(normal, bins=40, alpha=0.6, label="Normal")

        if not anomaly.empty:
            plt.hist(anomaly, bins=40, alpha=0.9, label="Anomalous")

        plt.title("Anomaly Score Distribution")
        plt.xlabel("Anomaly Score")
        plt.ylabel("Frequency")
        plt.legend()

        file_path = os.path.join(CHART_DIR, "anomaly_score_distribution.png")
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close("all")

        return {"chart": file_path}


@router.get("/charts/anomaly-count")
def anomaly_count():
    with CHART_LOCK:
        df = load_predictions_safe()

        if df.empty or "anomaly" not in df.columns:
            return {"message": "No prediction data available"}

        counts = df["anomaly"].value_counts()

        if counts.empty:
            return {"message": "No anomaly count data"}

        plt.figure(figsize=(6, 4))
        counts.plot(kind="bar")

        plt.title("Normal vs Anomalous Traffic")
        plt.xlabel("Traffic Type")
        plt.ylabel("Count")

        file_path = os.path.join(CHART_DIR, "anomaly_count.png")
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close("all")

        return {"chart": file_path}


@router.get("/charts/top-anomalies")
def top_anomalies():
    with CHART_LOCK:
        df = load_predictions_safe()

        if df.empty:
            return {"message": "No prediction data available"}

        top = df[df["anomaly"] == "ANOMALY"].sort_values(
            "anomaly_score"
        ).head(10)

        if top.empty:
            return {"message": "No anomalies detected"}

        plt.figure(figsize=(10, 5))
        plt.bar(top["ip"], top["anomaly_score"])
        plt.xticks(rotation=45, ha="right")

        plt.title("Top 10 Anomalous IPs")
        plt.xlabel("IP Address")
        plt.ylabel("Anomaly Score")

        file_path = os.path.join(CHART_DIR, "top_anomalies.png")
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close("all")

        return {"chart": file_path}
