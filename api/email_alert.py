# email_alert.py
# Gmail alert sender (safe for automation)

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def send_gmail_alert(subject: str, body: str):
    """
    Sends an email via Gmail SMTP.

    Required env variables:
    - GMAIL_USER
    - GMAIL_APP_PASSWORD
    - ALERT_TO_EMAIL

    This function is SAFE for background automation:
    - Never crashes the app
    - Returns structured status
    """

    gmail_user = os.getenv("GMAIL_USER")
    gmail_pass = os.getenv("GMAIL_APP_PASSWORD")
    to_email = os.getenv("ALERT_TO_EMAIL")

    if not gmail_user or not gmail_pass or not to_email:
        print("[email_alert] Email not configured. Skipping alert.")
        return {"sent": False, "reason": "Email not configured"}

    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = gmail_user
        msg["To"] = to_email
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as smtp:
            smtp.login(gmail_user, gmail_pass)
            smtp.send_message(msg)

        print("[email_alert] Alert email sent successfully.")
        return {"sent": True}

    except Exception as e:
        print(f"[email_alert] Failed to send email: {e}")
        return {"sent": False, "reason": str(e)}
