from fastapi import FastAPI, Request
from google.cloud import pubsub_v1
from dotenv import load_dotenv
load_dotenv()
import os, json, boto3, base64
import logging
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
credentials_path=os.getenv("cred")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credentials_path
publisher=pubsub_v1.PublisherClient()
JOB_TOPIC=os.getenv("JOB_TOPIC")
app=FastAPI()
