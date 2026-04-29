from fastapi import FastAPI, Request
from dotenv import load_dotenv
from utils.extractor import extra
import os, json
from google.cloud import pubsub_v1
from google.cloud import storage
credentials_path=os.getenv("cred")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/govind/Ember-link/bright-raceway-468304-e1-d7622ad6eb37.json"
publisher=pubsub_v1.PublisherClient()
EXTRACT_TOPIC=os.getenv("EXTRACT_TOPIC")
storage_client = storage.Client()
bucket = storage_client.bucket(os.getenv("GCS_BUCKET_NAME"))
load_dotenv()
app=FastAPI()

@app.post("/extract")
async def extr(request: Request):
    try:
        body=await request.json()
        message=body.get("message", {})
        data=message.get("data")
        if not data:
            return {"status": "no idea"}
        dcd=base64.b64decode(data).decode("utf-8")
        payload=json.loads(dcd)
        file_key, email=payload.get("file_key"), payload.get("email")
        task_id, taskStatus=payload.get("task_id"), payload.get("taskStatus")
        taskStatus="textExtracted"
        blob = bucket.blob(file_key)
        file_bytes = blob.download_as_bytes()
        skills, year, domain, text_hash, text=extra(file_bytes)
        ou={"email": email, "skills": skills, "domain": domain, "text": text, "text_hash": text_hash, "year": year, "task_id": task_id, "taskStatus": taskStatus}
        ot=json.dumps(ou).encode("utf-8")
        pu=publisher.publish(EXTRACT_TOPIC, ot)
        logging.info(f"pub: {pu.result()}")
        return {"status": "processed"}
    except Exception as e:
        logger.error(f"error: {str(e)}")
        return {"status" : "failed"}

        


