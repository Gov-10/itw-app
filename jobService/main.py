from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os, json, boto3, base64
from google.cloud import pubsub_v1
import logging
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
credentials_path=os.getenv("cred")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credentials_path
publisher=pubsub_v1.PublisherClient()
JOB_TOPIC=os.getenv("JOB_TOPIC")
load_dotenv()
app=FastAPI()

@app.post("/jobs")
def jobser(request:Request):
    try:
        body=await request.json()
        message=body.get("message", {})
        data=message.get("data")
        if not data:
            return {"status": "no idea"}
        dcd=base64.b64decode(data).decode("utf-8")
        payload=json.loads(dcd)


