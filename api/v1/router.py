from fastapi import APIRouter

from api.v1.endpoints import (health,
                              stock,
                              crypto,
                              clean_temp,
                              weather,
                              typing_test)

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])

api_router.include_router(stock.router, prefix="/stock", tags=["Stock Insights"])

api_router.include_router(crypto.router, prefix="/crypto", tags=["Crypto"])
api_router.include_router(clean_temp.router, prefix="/clean-temp", tags=["System Maintenance"])

api_router.include_router(weather.router, prefix="/weather", tags=["Weather"])
api_router.include_router(typing_test.router, prefix="/typing-test", tags=["Typing Test"])
