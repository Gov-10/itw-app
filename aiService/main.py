from dotenv import load_dotenv
import os, json, base64
from google.cloud import pubsub_v1
import logging
from lang import lang_app
credentials_path=os.getenv("cred")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credentials_path
publisher=pubsub_v1.PublisherClient()
AI_TOPIC=os.getenv("AI_TOPIC")
load_dotenv()

from fastapi import FastAPI, Request
app=FastAPI()

@app.post("/ai")
def aiser(request: Request):
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
        op=lang_graph.invoke({"skills": skills, "year": year, "domain": domain, "text": text })
        output={"ai": op["queries"], "email": email, "skills": skills, "year": year, "domain": domain, "text": text}
        ot=json.dumps(output).encode("utf-8")
        pu=publisher.publish(AI_TOPIC, ot)
        return {"status": "processed"}
    except Exception as e:
        logger.error(f"error: {str(e)}")
        return {"status": "failed"}

        
        
        

