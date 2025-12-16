# fast API app


from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


from dotenv import load_dotenv
load_dotenv()

from api.detector import run_detection
from api.upload_detect import detect_from_uploaded_csv
from api.email_alert import send_gmail_alert
from api.charts import router as charts_router


app = FastAPI(title="Web Log Anomaly Detection API")

app.include_router(charts_router)

app.mount("/charts", StaticFiles(directory="charts"), name="charts")


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



@app.get("/")
def home():
    return {"status": "ok", "message": "API running"}

@app.post("/detect")
def detect():
    # Normal mode: always use real features.csv
    result = run_detection(input_file="data/processed/features.csv", top_n=10)

    # If anomalies exist, send Gmail alert
    if result["alert"]:
        subject = "Security Alert – Anomaly Detected"
        body = (
            f"Anomaly detected by the AI IDS.\n\n"
            f"Total IPs analyzed: {result['total_ips']}\n"
            f"Anomalies detected: {result['anomalies_detected']}\n\n"
            f"Top anomalies:\n" +
            "\n".join([f"{x['ip']} | score={x['anomaly_score']}" for x in result["top_anomalies"]])
        )
        email_status = send_gmail_alert(subject, body)
        result["email"] = email_status
    else:
        result["email"] = {"sent": False, "reason": "No anomalies detected"}

    return result


@app.post("/detect-upload")
def detect_upload(file: UploadFile = File(...)):
    result = detect_from_uploaded_csv(file)

    # Optional email alert
    if result["alert"]:
        subject = "Security Alert - Anomaly Detected (Uploaded Log)"
        body = (
            f"Uploaded file: {result['uploaded_file']}\n"
            f"Total rows analyzed: {result['total_rows']}\n"
            f"Anomalies detected: {result['anomalies_detected']}\n\n"
            "Top anomalies:\n" +
            "\n".join(
                [f"{x['ip']} | score={x['anomaly_score']}"
                 for x in result["top_anomalies"]]
            )
        )
        email_status = send_gmail_alert(subject, body)
        result["email"] = email_status
    else:
        result["email"] = {"sent": False, "reason": "No anomalies detected"}

    return result
