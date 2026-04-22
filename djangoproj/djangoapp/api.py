from ninja import NinjaAPI
import os
from dotenv import load_dotenv
load_dotenv()
from schema import UploadSchema
import boto3
import uuid
api=NinjaAPI()
s3 = boto3.client('s3', 
    region_name= os.getenv("COGNITO_REGION"),
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),)

bucket_name= os.getenv("S3_BUCKET_NAME")
@api.get("/health")
def chek(request):
    return {"status": "OK"}


@api.post("/upload")
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




