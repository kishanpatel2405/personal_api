from fastapi import APIRouter

from schemas.v1.health import HealthResult

router = APIRouter()


@router.get("/health", response_model=HealthResult, name="health")
async def health():
    return HealthResult(is_alive=True)
