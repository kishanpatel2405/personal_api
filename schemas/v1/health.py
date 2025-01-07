from typing import Dict, List

from pydantic import BaseModel, Field, condecimal

from utils.enums import Ip_Type


class HealthResult(BaseModel):
    """
    Response model indicating the health status of the system.
    """
    is_alive: bool = Field(..., description="Indicates whether the system is alive or not.")


class IPAddressResponse(BaseModel):
    """
    Response model for returning the IP address of the system.
    """
    ip_address: str = Field(..., description="The IP address of the system.")
    type: Ip_Type = Field(..., description="The type of IP address: LOCAL or EXTERNAL.")


class SystemMetricsResponse(BaseModel):
    """
    Response model for returning system resource usage metrics.
    """
    cpu_usage: float = Field(..., ge=0, le=100, description="The CPU usage percentage of the system.")
    memory_usage: float = Field(..., ge=0, le=100, description="The memory usage percentage of the system.")


class DiskUsageResponse(BaseModel):
    """
    Response model for returning disk usage statistics.
    """
    total: int = Field(..., description="Total disk space in bytes.")
    used: int = Field(..., description="Used disk space in bytes.")
    free: int = Field(..., description="Free disk space in bytes.")
    percent: condecimal(ge=0, le=100) = Field(..., description="Disk usage percentage (0 to 100%).")


class UptimeResponse(BaseModel):
    """
    Response model for returning the system uptime.
    """
    uptime: str = Field(..., description="System uptime in HH:MM:SS format.")


class NetworkStatsResponse(BaseModel):
    """
    Response model for returning network statistics.
    """
    status: List[Dict[str, str]] = Field(..., description="List of network interfaces with their statistics.")


class CpuTemperatureResponse(BaseModel):
    core: str = Field(..., description="The core temperature label.")
    temperature: float = Field(..., description="The temperature of the CPU in Celsius.")
