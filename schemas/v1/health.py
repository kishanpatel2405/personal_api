from pydantic import BaseModel

from utils.enums import Ip_Type


class HealthResult(BaseModel):
    is_alive: bool


class IPAddressResponse(BaseModel):
    ip_address: str
    type: Ip_Type
