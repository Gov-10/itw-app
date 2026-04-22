from ninja import NinjaAPI
from google.cloud import pubsub_v1
import os, json
from dotenv import load_dotenv
load_dotenv()
from .schema import UploadSchema, UpSc
import boto3
import uuid
from .auth import CustomAuth
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
    email=user["email"]
    dt={"file_key": payload.file_key, "email": email}
    data=json.dumps(dt).encode("utf-8")
    pu=publisher.publish(topic_path, data)
    return {"status": f"Published: {pu.result()} "}






