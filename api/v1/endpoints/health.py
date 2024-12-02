import psutil
from fastapi import APIRouter
from schemas.v1.health import (
    HealthResult,
    IPAddressResponse,
    SystemMetricsResponse,
    DiskUsageResponse,
    UptimeResponse,
    NetworkStatsResponse
)
from services.health import get_external_ip, get_local_ip

import time
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


@router.get("/health/metrics", response_model=SystemMetricsResponse, name="health-metrics")
async def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)  # CPU usage in percentage
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent  # Memory usage in percentage

    return SystemMetricsResponse(cpu_usage=cpu_usage, memory_usage=memory_usage)


@router.get("/health/uptime", response_model=UptimeResponse, name="system-uptime")
async def get_uptime():
    # Get system uptime in seconds
    uptime_seconds = time.time() - psutil.boot_time()
    uptime = str(time.strftime("%H:%M:%S", time.gmtime(uptime_seconds)))
    return UptimeResponse(uptime=uptime)


@router.get("/health/disk-usage", response_model=DiskUsageResponse, name="disk-usage")
async def get_disk_usage():
    disk_usage = psutil.disk_usage('/')
    return DiskUsageResponse(
        total=disk_usage.total,
        used=disk_usage.used,
        free=disk_usage.free,
        percent=disk_usage.percent
    )


@router.get("/health/network-stats", response_model=NetworkStatsResponse, name="network-stats")
async def get_network_stats():
    network_stats = psutil.net_io_counters(pernic=True)
    status = []
    for iface, io_stats in network_stats.items():
        status.append({
            "interface": iface,
            "bytes_sent": io_stats.bytes_sent,
            "bytes_recv": io_stats.bytes_recv,
            "packets_sent": io_stats.packets_sent,
            "packets_recv": io_stats.packets_recv,
            "errin": io_stats.errin,
            "errout": io_stats.errout
        })
    return NetworkStatsResponse(status=status)
