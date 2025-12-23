# fast API app

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from threading import Thread

import json
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from api.detector import run_detection
from api.upload_detect import detect_from_uploaded_csv
from api.email_alert import send_gmail_alert
from api.charts import router as charts_router
from api.live_monitor import automated_monitor  
from api.live_monitor import MONITOR_STATUS

app = FastAPI(title="Web Log Anomaly Detection API")

app.include_router(charts_router)

app.mount("/charts", StaticFiles(directory="charts"), name="charts")

LATEST_RESULT_FILE = Path("logs/latest_detection.json")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# AUTOMATION STARTS HERE
# -------------------------------

@app.on_event("startup")
def start_automation():
    """
    Starts automated live log monitoring in background.
    Does NOT block the API.
    """
    thread = Thread(target=automated_monitor, daemon=True)
    thread.start()
    print("[main] Automated log monitor started.")

# -------------------------------


@app.get("/")
def home():
    return {"status": "ok", "message": "API running with automation enabled"}


@app.post("/detect")
def detect():
    result = run_detection(input_file="data/processed/features.csv", top_n=40)

    # Save latest detection (for frontend & monitoring)
    LATEST_RESULT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LATEST_RESULT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    # Email logic
    if result["alert"]:
        subject = "Security Alert – Anomaly Detected"
        body = (
            f"Anomaly detected by the AI IDS.\n\n"
            f"Total IPs analyzed: {result['total_ips']}\n"
            f"Anomalies detected: {result['anomalies_detected']}"
        )
        send_gmail_alert(subject, body)

    return result


@app.post("/detect-upload")
def detect_upload(file: UploadFile = File(...)):
    result = detect_from_uploaded_csv(file)

    if result["alert"]:
        subject = "Security Alert - Anomaly Detected (Uploaded Log)"
        body = (
            f"Uploaded file: {result['uploaded_file']}\n"
            f"Total rows analyzed: {result['total_rows']}\n"
            f"Anomalies detected: {result['anomalies_detected']}\n\n"
            "Top anomalies:\n" +
            "\n".join(
                f"{x['ip']} | score={x['anomaly_score']}"
                for x in result["top_anomalies"]
            )
        )
        email_status = send_gmail_alert(subject, body)
        result["email"] = email_status
    else:
        result["email"] = {"sent": False, "reason": "No anomalies detected"}

    return result


@app.get("/monitor/status")
def monitor_status():
    """
    Returns current status of automated log monitoring.
    """
    return MONITOR_STATUS

@app.get("/detect/latest")
def get_latest_detection():
    if not LATEST_RESULT_FILE.exists():
        return {
            "message": "No detection run yet",
            "top_anomalies": []
        }

    try:
        with open(LATEST_RESULT_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        # File may be mid-write by automation
        return {
            "message": "Detection in progress, try again",
            "error": str(e),
            "top_anomalies": []
        }
