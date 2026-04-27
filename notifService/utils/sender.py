import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()
sender_email=os.getenv("MY_EMAIL")
app_password=os.getenv("APP_PASSWORD")

def send_email(bestRes, email):
    subject="Your resume has matched this Job"
    body= f"details: {bestRes}"
    msg = MIMEMultipart()
    msg["From"]=sender_email
    msg["To"]=email
    msg["Subject"]=subject
    msg.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("email sent ji..")
    except Exception as e:
        print(f"error: {str(e)}")
