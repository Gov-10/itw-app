from fastapi import FastAPI, HTTPException, Request
import os, redis
from dotenv import load_dotenv
load_dotenv()
app=FastAPI()

@app.get("/health")
def chek():
    return {"status": "OK"}

@app.post("/notif")
async def noti(request: Request):
    try:
        body=await request.json()
        message=body.get("message", {})
        data=message.get("data")
        if not data:
            raise HTTPException(status_code=404, detail="no data found")
        dcd=base64.b64decode(data).decode("utf-8")
        payload=json.loads(dcd)
        ranked, email=payload.get("ranked"), payload.get("email")
        #TODO: Baaki code
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")

