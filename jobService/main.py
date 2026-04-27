from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os, json, boto3, base64
from google.cloud import pubsub_v1
import logging
from utils.jobScrape import scrapeJobs
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
        ai,email=payload.get("ai"), payload.get("email")
        skills, year=payload.get("skills"), payload.get("year")
        domain, text=payload.get("domain"), payload.get("text")
        taskStatus, task_id=payload.get("taskStatus"), payload.get("task_id")
        jobList=scrapeJobs(ai)
        taskStatus="jobsFound"
        output={"jobs": jobList, "ai": ai, "email": email, "domain": domain, "skills": skills, "year": year, "text": text, "taskStatus": taskStatus, "task_id": task_id}
        ot=json.dumps(output).encode("utf-8")
        pu=publisher.publish(JOB_TOPIC, ot)
        return {"status": "processed"}
    except Exception as e:
        logger.error(f"error: {str(e)}")
        return {"status" : "failed"}




