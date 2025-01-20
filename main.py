from fastapi import FastAPI

from api.v1.router import api_router

app = FastAPI(
    title="Personal API",
    description="A FastAPI project for daily tools and services.",
    version="1.0.0",
)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
