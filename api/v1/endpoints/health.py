import time

import psutil
from fastapi import APIRouter

from schemas.v1.health import (DiskUsageResponse, HealthResult,
                               IPAddressResponse, NetworkStatsResponse,
                               SystemMetricsResponse, UptimeResponse)
from services.health import get_external_ip, get_local_ip
from utils.enums import Ip_Type

router = APIRouter()


@router.get("/health", response_model=HealthResult, name="health", status_code=200)
async def health():
    return HealthResult(is_alive=True)


@router.get("/ip-address", response_model=IPAddressResponse, status_code=200, name="ip-address")
async def get_ip_address(ip_type: Ip_Type = Ip_Type.LOCAL):
    if ip_type == Ip_Type.EXTERNAL:
        ip_address = get_external_ip()
        ip_type = "external"
    else:
        ip_address = get_local_ip()
        ip_type = "local"

    return IPAddressResponse(ip_address=ip_address, type=ip_type)


@router.get("/metrics", response_model=SystemMetricsResponse, name="health-metrics", status_code=200)
async def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent

    return SystemMetricsResponse(cpu_usage=cpu_usage, memory_usage=memory_usage)


@router.get("/uptime", response_model=UptimeResponse, name="system-uptime", status_code=200)
async def get_uptime():
    uptime_seconds = time.time() - psutil.boot_time()
    uptime = str(time.strftime("%H:%M:%S", time.gmtime(uptime_seconds)))
    return UptimeResponse(uptime=uptime)


@router.get("/disk-usage", response_model=DiskUsageResponse, name="disk-usage", status_code=200)
async def get_disk_usage():
    disk_usage = psutil.disk_usage('/')
    return DiskUsageResponse(
        total=disk_usage.total,
        used=disk_usage.used,
        free=disk_usage.free,
        percent=disk_usage.percent
    )


@router.get("/network-status", response_model=NetworkStatsResponse, name="network-status", status_code=200)
async def get_network_stats():
    network_stats = psutil.net_io_counters(pernic=True)
    status = []
    for iface, io_stats in network_stats.items():
        status.append({
            "interface": iface,
            "bytes_sent_total": io_stats.bytes_sent,
            "bytes_received_total": io_stats.bytes_recv,
            "packets_sent_total": io_stats.packets_sent,
            "packets_received_total": io_stats.packets_recv,
            "receive_errors": io_stats.errin,
            "transmit_errors": io_stats.errout
        })
    return NetworkStatsResponse(status=status)
