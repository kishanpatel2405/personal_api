from fastapi import APIRouter, HTTPException

from schemas.v1.health import HealthResult, IPAddressResponse
import socket
import requests

from utils.enums import Ip_Type

router = APIRouter()


@router.get("/health", response_model=HealthResult, name="health")
async def health():
    return HealthResult(is_alive=True)


def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    finally:
        s.close()
    return local_ip

def get_external_ip() -> str:
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        return response.json().get("ip")
    except requests.RequestException:
        raise HTTPException(status_code=500, detail="Unable to fetch external IP address.")

@router.get("/ip-address", response_model=IPAddressResponse)
async def get_ip_address(ip_type: Ip_Type = Ip_Type.LOCAL):
    if ip_type == Ip_Type.EXTERNAL:
        ip_address = get_external_ip()
        ip_type = "external"
    else:
        ip_address = get_local_ip()
        ip_type = "local"

    return IPAddressResponse(ip_address=ip_address, type=ip_type)
