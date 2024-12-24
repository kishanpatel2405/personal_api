from fastapi import FastAPI

from api.v1.router import api_router as api_v1_router

app = FastAPI()
app.include_router(api_v1_router, prefix="/api/v1")
