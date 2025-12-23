# live_monitor.py
# Automated backend monitor for simulated live web logs

import time
import json
from pathlib import Path
from datetime import datetime

from src.prepare import parse_logs
from src.feature_engineering import build_features
from api.detector import run_detection
from api.email_alert import send_gmail_alert

# -------- CONFIG --------

CHUNK_DIR = Path("data/raw/chunks")
LIVE_LOG = Path("data/raw/live_access.log")
STATE_FILE = Path("logs/monitor_state.json")
CHECK_INTERVAL = 120  # seconds
LATEST_RESULT_FILE = Path("logs/latest_detection.json")

# -------- STATUS (NEW) --------

MONITOR_STATUS = {
    "running": False,
    "interval_seconds": CHECK_INTERVAL,
    "processed_chunks": 0,
    "last_chunk": None,
    "last_run": None,
    "last_anomaly_detected": False,
}


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {
        "processed_chunks": [],
        "last_fingerprint": None
    }


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def append_next_chunk(state: dict) -> bool:
    for chunk in sorted(CHUNK_DIR.iterdir()):
        if chunk.name not in state["processed_chunks"]:
            with open(chunk, "r", encoding="utf-8") as src, \
                 open(LIVE_LOG, "a", encoding="utf-8") as dst:
                dst.writelines(src.readlines())

            state["processed_chunks"].append(chunk.name)
            save_state(state)

            MONITOR_STATUS["processed_chunks"] = len(state["processed_chunks"])
            MONITOR_STATUS["last_chunk"] = chunk.name

            print(f"[monitor] Appended log chunk: {chunk.name}")
            return True
    return False


def automated_monitor():
    print("[monitor] Automated live log monitor started.")
    MONITOR_STATUS["running"] = True

    LIVE_LOG.parent.mkdir(parents=True, exist_ok=True)
    LIVE_LOG.touch(exist_ok=True)

    state = load_state()

    while True:
        try:
            MONITOR_STATUS["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            new_data = append_next_chunk(state)

            if new_data:
                parse_logs(
                    log_file=str(LIVE_LOG),
                    output_file="data/processed/parsed_logs.csv",
                    show_progress=False
                )

                build_features(
                    input_file="data/processed/parsed_logs.csv",
                    output_file="data/processed/features.csv"
                )

                result = run_detection()
                LATEST_RESULT_FILE.parent.mkdir(parents=True, exist_ok=True)
                with open(LATEST_RESULT_FILE, "w") as f:
                    json.dump(result, f, indent=2)
                if result["alert"] and result["fingerprint"] != state["last_fingerprint"]:
                    MONITOR_STATUS["last_anomaly_detected"] = True

                    send_gmail_alert(
                        subject="Automated Web IDS Alert",
                        body=(
                            "New anomalous traffic detected.\n\n"
                            f"Total IPs analyzed: {result['total_ips']}\n"
                            f"Anomalies detected: {result['anomalies_detected']}"
                        )
                    )

                    state["last_fingerprint"] = result["fingerprint"]
                    save_state(state)
                else:
                    MONITOR_STATUS["last_anomaly_detected"] = False

            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print(f"[monitor] Error: {e}")
            time.sleep(CHECK_INTERVAL)
