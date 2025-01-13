from fastapi import APIRouter

from api.v1.endpoints import (affirmations, clean_temp, health, timezone,
                              weather)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])

api_router.include_router(
    clean_temp.router, prefix="/clean-temp", tags=["System Maintenance"]
)

api_router.include_router(weather.router, prefix="/weather", tags=["Weather"])

api_router.include_router(
    affirmations.router, prefix="/affirmations", tags=["Affirmations"]
)

api_router.include_router(timezone.router, prefix="/timezones", tags=["Timezones"])
