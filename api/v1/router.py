from fastapi import APIRouter

from api.v1.endpoints import health, stock, system_health, crypto

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])

api_router.include_router(system_health.router, tags=["System Health"])

api_router.include_router(stock.router, prefix="/stock", tags=["Stock Insights"])

api_router.include_router(crypto.router, prefix="/crypto", tags=["Crypto"])

