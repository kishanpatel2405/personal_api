from typing import List

from pydantic import BaseModel

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
    percent: float


class UptimeResponse(BaseModel):
    uptime: str


class NetworkStatsResponse(BaseModel):
    status: List[dict]


class CpuTemperatureResponse(BaseModel):
    core: int
    temperature: float
