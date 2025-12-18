# GMAIL alert

import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv
load_dotenv()

def send_gmail_alert(subject: str, body: str):
    """
    Sends an email via Gmail SMTP.
    GMAIL_USER, GMAIL_APP_PASSWORD, ALERT_TO_EMAIL
    """
    gmail_user = os.getenv("GMAIL_USER")
    gmail_pass = os.getenv("GMAIL_APP_PASSWORD")
    to_email = os.getenv("ALERT_TO_EMAIL")

    # If not configured, skip sending (so API still works)
    if not gmail_user or not gmail_pass or not to_email:
        return {"sent": False, "reason": "Email not configured"}

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(gmail_user, gmail_pass)
        smtp.send_message(msg)

    return {"sent": True}

