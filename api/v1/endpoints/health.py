from fastapi import APIRouter

from schemas.v1.health import HealthResult, IPAddressResponse
from services.health import get_external_ip, get_local_ip

from utils.enums import Ip_Type

router = APIRouter()


@router.get("/health", response_model=HealthResult, name="health")
async def health():
    return HealthResult(is_alive=True)


@router.get("/ip-address", response_model=IPAddressResponse)
async def get_ip_address(ip_type: Ip_Type = Ip_Type.LOCAL):
    if ip_type == Ip_Type.EXTERNAL:
        ip_address = get_external_ip()
        ip_type = "external"
    else:
        ip_address = get_local_ip()
        ip_type = "local"

    return IPAddressResponse(ip_address=ip_address, type=ip_type)
