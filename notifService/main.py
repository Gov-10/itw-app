from fastapi import FastAPI, HTTPException, Request
import os, json, base64
from dotenv import load_dotenv
from utils.sender import send_email
from google.cloud import pubsub_v1
load_dotenv()
credentials_path=os.getenv("cred")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credentials_path
publisher=pubsub_v1.PublisherClient()
RES_TOPIC=os.getenv("RES_TOPIC")
app=FastAPI()
redis_client=redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), password=os.getenv("REDIS_PASSWORD"), decode_responses=True)

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
        message=body.get("message", {})
        data=message.get("data")
        if not data:
            raise HTTPException(status_code=404, detail="no data found")
        dcd=base64.b64decode(data).decode("utf-8")
        payload=json.loads(dcd)
        ranked, email=payload.get("ranked"), payload.get("email")
        bestRes=ranked[0]
        send_email(bestRes, email)
        payload["taskStatus"]="notified"
        p=publish_data(payload)
        return {"status": f"notified and published ID: {p}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")

