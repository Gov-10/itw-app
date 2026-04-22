from ninja import NinjaAPI
api=NinjaAPI()

@api.get("/health")
def chek(request):
    return {"status": "OK"}