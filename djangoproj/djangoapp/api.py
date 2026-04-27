from ninja import NinjaAPI
from google.cloud import pubsub_v1
import os, json, base64
from dotenv import load_dotenv
load_dotenv()
from .schema import UploadSchema, UpSc
import boto3
from ninja.erros import HttpError
import uuid
from .auth import CustomAuth
import pusher
pusher_client=pusher.Pusher(app_id=os.getenv("PUSHER_APP_ID"), key=os.getenv("PUSHER_KEY"), secret=os.getenv("PUSHER_SECRET"), cluster=os.getenv("PUSHER_CLUSTER"), ssl=True)
credentials_path = os.getenv("cred")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
publisher = pubsub_v1.PublisherClient()
topic_path = os.getenv("INPUT_TOPIC")
api=NinjaAPI()
s3 = boto3.client('s3', 
    region_name= os.getenv("COGNITO_REGION"),
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),)

bucket_name= os.getenv("S3_BUCKET_NAME")
@api.get("/health")
def chek(request):
    return {"status": "OK"}

@api.get("/auth-check", auth=CustomAuth())
def che(request):
    user=request.auth
    email=user["email"]
    return {"email": email}

@api.post("/upload", auth=CustomAuth())
def upl(request, payload:UploadSchema):
    user=request.auth
    google_id=user["google_id"]
    file_id=str(uuid.uuid4())
    key=f"resume/{google_id}/{file_id}-{payload.file_name}"
    presigned_url = s3.generate_presigned_url(
        ClientMethod = 'put_object', 
        Params = {
            'Bucket': bucket_name, 
            "Key" : key, 
            "ContentType": payload.content_type
        }, 
        ExpiresIn = 600
    )
    return {"upload_url": presigned_url, "file_key": key}

@api.post("/upload-fin", auth=CustomAuth())
def uplc(request, payload:UpSc):
    task_id=str(uuid.uuid4())
    taskStatus="fileUploaded"
    email=user["email"]
    dt={"file_key": payload.file_key, "email": email, "task_id": task_id, "taskStatus": taskStatus}
    data=json.dumps(dt).encode("utf-8")
    pu=publisher.publish(topic_path, data)
    return {"status": f"Published: {pu.result()} "}

@api.post("/receiveres")
async def rec(request):
    try:
        body = await request.json()
        message=body.get("message", {})
        data=message.get("data")
        if not data:
            raise HttpError(404, "Data not found")
        dcd=base64.b64decode(data).decode("utf-8")
        payload=json.loads(dcd)
        ranked=payload.get("ranked")
        ai, domain=payload.get("ai"), payload.get("domain")
        skills=payload.get("skills")
        task_id=payload.get("task_id")
        taskStatus=payload.get("taskStatus")
        taskStatus="completed and notified"
        pal = {"taskStatus": taskStatus, "task_id": task_id, "ai": ai, "ranked": ranked, "domain": domain, "email": payload.get("email"), "domain":domain, "skills": skills }
        pusher_client.trigger(f"task_id- {task_id}", "jobs-ready", pal)
        return {"status": "pushed"}
    except Exception as e:
        raise HttpError(500, f"error: {str(e)}")

        








