from typing import Dict, List

from pydantic import BaseModel, condecimal

from utils.enums import Ip_Type


class HealthResult(BaseModel):
    is_alive: bool


class IPAddressResponse(BaseModel):
    ip_address: str
    type: Ip_Type


class SystemMetricsResponse(BaseModel):
    cpu_usage: float
    memory_usage: float


class DiskUsageResponse(BaseModel):
    total: int
    used: int
    free: int
    percent: condecimal(ge=0, le=100)


class NetworkStatsResponse(BaseModel):
    status: List[Dict[str, str]]


class CpuTemperatureResponse(BaseModel):
    core: str
    temperature: float
