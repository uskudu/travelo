from fastapi import FastAPI
from app.api_v1 import routers

app = FastAPI()


for router in routers:
    app.include_router(router)
