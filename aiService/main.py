from dotenv import load_dotenv
import os, json, base64
from google.cloud import pubsub_v1
import logging
from lang import lang_app
#credentials_path=os.getenv("cred")
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credentials_path
publisher=pubsub_v1.PublisherClient()
AI_TOPIC=os.getenv("AI_TOPIC")
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()

@app.get("/health")
def chek():
    return {"status": "OK"}
@app.post("/ai")
async def aiser(request: Request):
    try:
        body=await request.json()
        message=body.get("message", {})
        data=message.get("data")
        if not data:
            return {"status": "no idea"}
        dcd=base64.b64decode(data).decode("utf-8")
        payload=json.loads(dcd)
        skills,year = payload.get("skills"), payload.get("year")
        domain,text=payload.get("domain"), payload.get("text")
        text_hash, email=payload.get("text_hash"), payload.get("email")
        taskStatus, task_id=payload.get("taskStatus"), payload.get("task_id")
        op=lang_app.invoke({"skills": skills, "year": year, "domain": domain, "text": text })
        taskStatus="queryGenerated"
        output={"ai": op["queries"], "email": email, "skills": skills, "year": year, "domain": domain, "text": text, "task_id": task_id, "taskStatus": taskStatus}
        ot=json.dumps(output).encode("utf-8")
        pu=publisher.publish(AI_TOPIC, ot)
        return {"status": "processed"}
    except Exception as e:
        logger.error(f"error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
        
        
        


