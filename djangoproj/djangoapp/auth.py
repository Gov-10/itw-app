from ninja.security import HttpBearer
from dotenv import load_dotenv
import os
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import CustomUser
load_dotenv()

GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID")
class CustomAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            idinfo=id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            email=idinfo["email"]
            sub=idinfo["sub"]
            user, _ = CustomUser.objects.get_or_create(
                email=email,
                defaults={"google_id": sub}
            )
            return user
        except Exception as e:
            print("error: ",str(e))
            return None
