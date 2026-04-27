from fastapi import FastAPI, Request, HTTPException
from google.cloud import pubsub_v1
from dotenv import load_dotenv
load_dotenv()
import os, json, boto3, base64
import logging
from utils.ranker import rank_jobs
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
credentials_path=os.getenv("cred")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credentials_path
publisher=pubsub_v1.PublisherClient()
RANK_TOPIC=os.getenv("RANK_TOPIC")
app=FastAPI()

@app.post("/rank")
async def ran(request: Request):
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
        ranked=rank_jobs(text, jobs, skills)
        output={"ranked": ranked, "email": email, "ai": ai, "domain": domain, "skills": skills}
        ot=json.dumps(output).encode("utf-8")
        pu=publisher.publish(RANK_TOPIC, ot)
        return {"status": f"published to rank topic: {pu.result()}"}
    except Exception as e:
        logger.error(f"error: {str(e)} ")
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")

        

        



