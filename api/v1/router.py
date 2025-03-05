from fastapi import APIRouter

from api.v1.endpoints import (CalendarHub, DailyEnglish, MotivatorPlay,
                              affirmations, crypto, health, stock, timezone,
                              translation, weather)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])

api_router.include_router(stock.router, prefix="/stock", tags=["Stock Insights"])

api_router.include_router(weather.router, tags=["Weather"])

api_router.include_router(affirmations.router, tags=["Affirmations"])

api_router.include_router(timezone.router, tags=["Timezones"])

api_router.include_router(crypto.router, prefix="/crypto", tags=["Crypto"])

api_router.include_router(CalendarHub.router, tags=["Calendar Hub"])

api_router.include_router(MotivatorPlay.router, tags=["Motivator Play"])

api_router.include_router(DailyEnglish.router, tags=["Daily English"])

api_router.include_router(translation.router, prefix="/translate", tags=["Translation"])
