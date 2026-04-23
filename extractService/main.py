from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os, json, boto3
from utils.extractor import extra
from google.cloud import pubsub_v1
credentials_path=os.getenv("cred")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credentials_path
publisher=pubsub_v1.PublisherClient()
EXTRACT_TOPIC=os.getenv("EXTRACT_TOPIC")
s3=boto3.client('s3', region_name=os.getenv("COGNITO_REGION"), aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
bucket_name=os.getenv("S3_BUCKET_NAME")
load_dotenv()
app=FastAPI()

@api.post("/extract")
def extr(request: Request):
    try:
        body=await request.json()
        message=body.get("message", {})
        data=message.get("data")
        if not data:
            return {"status": "no idea"}
        dcd=base64.b64decode(data).decode("utf-8")
        payload=json.loads(dcd)
        file_key, email=payload.get("file_key"), payload.get("email")
        skills, year, domain, text_hash, tex=extra(file_key)
        output={"email": email, "file_key": file_key, "skills": skills, "year": year, "domain":domain, "text_hash": text_hash, "tex": tex}
        dt= json.dumps(output).encode("utf-8")
        pu=publisher.publish(EXTRACT_TOPIC, dt)
        return {"status": "ok"}
    except Exception as e:
        print(f"error: {e}")
        return {"status": "failed"}

        


