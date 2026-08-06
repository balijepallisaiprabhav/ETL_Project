import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email():
    if not EMAIL or not PASSWORD:
        raise ValueError("EMAIL_ADDRESS or EMAIL_PASSWORD is missing from the .env file")
    msg = EmailMessage()
    msg["Subject"] = "ETL Pipeline Completed Successfully"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    msg.set_content("""
Hello,

Your ETL Pipeline has completed successfully.

The transformed data has been loaded into Azure SQL Database.

Regards,
ETL Pipeline
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)

    print("Email sent successfully!")