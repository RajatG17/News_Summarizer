# Send the summarized news articles to the user via email
import os
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = os.getenv("EMAIL_SMTP_HOST")
SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", 587))
SMTP_USER = os.getenv("EMAIL_SMTP_USER")
SMTP_PASSWORD = os.getenv("EMAIL_SMTP_PASS")
TO_EMAIL =  [addr.strip() for addr in os.getenv("TO_EMAIL").split(",")] if os.getenv("TO_EMAIL") else ""

def build_html_report(summaries: list[dict]) -> str:
    """
    Build an HTML report from the summaries.
    
    Args:
        summaries (list[dict]): List of summaries to include in the report.
        
    Returns:
        str: HTML formatted report.
    """
    html = "<html><body>"
    html += "<h1>News Summaries</h1>"
    for summary in summaries:
        html += f"<h2>{summary['title']}</h2>"
        html += f"<p>{summary['summary']}</p>"
        html += f"<a href='{summary['url']}'>Read more</a><br><br>"
    html += "</body></html>"
    return html

def send_report(items, subject: str="Daily News") -> None:
    html = build_html_report(items)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] =  ", ".join(TO_EMAIL)


    part = MIMEText(html, "html")
    msg.attach(part)

    try:
        with SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, TO_EMAIL, msg.as_string())
            server.quit()
        print(f"Email sent to {TO_EMAIL} with subject: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")

