import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

sender_email = os.getenv("MY_EMAIL")
app_password = os.getenv("APP_PASSWORD")

def send_email(bestRes, email):
    if not sender_email or not app_password:
        raise ValueError("Email credentials missing in environment variables.")
    if not email:
        raise ValueError("Recipient email address is missing.")
    subject = "Your resume has matched this Job!"
    title = bestRes.get("title", "Job Match")
    company = bestRes.get("company", "Unknown Company")
    location = bestRes.get("location", "Not Specified")
    apply_link = bestRes.get("apply_link", "#")
    description = bestRes.get("description", "No description available.")
    body = f"""
    Hello,

    We found a high-matching job for your profile!

    Position: {title}
    Company: {company}
    Location: {location}
    
    Description:
    {description}

    Apply here: {apply_link}

    Best of luck,
    JobScan AI Team
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = None
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, email, msg.as_string())
        logger.info(f"Email successfully sent to {email}")
        return True
    except Exception as e:
        logger.error(f"SMTP failed to send email: {str(e)}")
        raise e
    finally:
        if server:
            try:
                server.quit()
            except Exception:
                pass
