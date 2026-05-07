from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import os, json, base64
from dotenv import load_dotenv
from utils.sender import send_email
from google.cloud import pubsub_v1
import logging
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
load_dotenv()
#credentials_path=os.getenv("cred")
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credentials_path
publisher=pubsub_v1.PublisherClient()
RES_TOPIC=os.getenv("RES_TOPIC")
app=FastAPI()

def publish_data(payload):
    output=json.dumps(payload).encode("utf-8")
    pu=publisher.publish(RES_TOPIC, output)
    return pu.result()

@app.get("/health")
def chek():
    return {"status": "OK"}

@app.post("/notif")
async def noti(request: Request):
    try:
        body=await request.json()
        logger.info(f"RAW BODY: {body}")
        message=body.get("message", {})
        data=message.get("data")
        if not data:
            logger.error("DATA KEY MISSING! Pub/Sub is sending a different schema.")
            raise HTTPException(status_code=404, detail="no data found")
        logger.info(f"FULL RAW BODY: {data}")
        clean=data.replace("\n", "").replace("\r", "").strip()
        logger.info(f"CLEANED: {clean}")
        dcd=base64.b64decode(clean).decode("utf-8")
        logger.info(f"DECODE1: {dcd}")
        payload=json.loads(dcd)
        logger.info(f"PAYLOAD: {payload}")
        ranked, email=payload.get("ranked"), payload.get("email")
        logger.info(f"ranked: {ranked}")
        logger.info(f"email: {email}")
        bestRes=ranked[0]
        logger.info(f"bestRes: {bestRes}")
        send_email(bestRes, email)
        logger.info("EMAIL SENT JI.....")
        payload["taskStatus"]="notified"
        p=publish_data(payload)
        logger.info(f"Final payload: {payload}")
        return {"status": f"notified and published ID: {p}"}
    except Exception as e:
        logger.error(f"ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")


app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])



