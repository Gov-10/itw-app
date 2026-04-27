from fastapi import FastAPI, Request, HTTPException
from google.cloud import pubsub_v1
from dotenv import load_dotenv
load_dotenv()
import os, json, boto3, base64
import logging
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
credentials_path=os.getenv("cred")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credentials_path
publisher=pubsub_v1.PublisherClient()
JOB_TOPIC=os.getenv("JOB_TOPIC")
app=FastAPI()

@app.post(request: Request):
    try:
        body=await request.json()
        message=body.get("message", {})
        data=message.get("data")
        if not data:
            raise HTTPException(status_code=404, detail="No data found")
        dcd=base64.b64decode(data).decode("utf-8")
        payload=json.loads(dcd)
        jobs, ai=payload.get("jobList"), payload.get("email")
        email, domain=payload.get("email"), payload.get("domain")
        skills, year=payload.get("skills"), payload.get("year")
        text=payload.get("text")
        
        



