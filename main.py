from fastapi import FastAPI
import uvicorn

from api.v1.router import api_router

app = FastAPI(
    title="Personal API",
    description="A FastAPI project for daily tools and services.",
    version="1.0.0",
)
from api.v1.router import api_router as api_v1_router

app.include_router(api_router)
app = FastAPI()
app.include_router(api_v1_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
