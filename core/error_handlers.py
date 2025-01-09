from fastapi import FastAPI
from fastapi.responses import JSONResponse

from utils.errors import ApiException

app = FastAPI()


@app.exception_handler(ApiException)
async def api_exception_handler(request, exc: ApiException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.msg, "error_code": exc.error_code.value},
    )
