import time
import psutil
from fastapi import APIRouter, HTTPException, BackgroundTasks
from schemas.v1.health import (DiskUsageResponse, HealthResult,
                               IPAddressResponse, NetworkStatsResponse,
                               SystemMetricsResponse, UptimeResponse)
from services.health import get_external_ip, get_local_ip
from utils.enums import Ip_Type

router = APIRouter()

# Helper function for handling potential issues
def handle_psutil_error(func):
    try:
        return func()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System error: {str(e)}")

@router.get("/health", response_model=HealthResult, name="health", status_code=200)
async def health():
    return HealthResult(is_alive=True)

@router.get("/ip-address", response_model=IPAddressResponse, status_code=200, name="ip-address")
async def get_ip_address(ip_type: Ip_Type = Ip_Type.LOCAL):
    try:
        if ip_type == Ip_Type.EXTERNAL:
            ip_address = await get_external_ip()
            ip_type = "external"
        else:
            ip_address = await get_local_ip()
            ip_type = "local"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not retrieve IP address: {str(e)}")

    return IPAddressResponse(ip_address=ip_address, type=ip_type)

@router.get("/metrics", response_model=SystemMetricsResponse, name="health-metrics", status_code=200)
async def get_system_metrics():
    try:
        # Using psutil asynchronously where possible (cpu_percent does not need async handling)
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not retrieve system metrics: {str(e)}")

    return SystemMetricsResponse(cpu_usage=cpu_usage, memory_usage=memory_usage)

@router.get("/uptime", response_model=UptimeResponse, name="system-uptime", status_code=200)
async def get_uptime():
    try:
        uptime_seconds = time.time() - psutil.boot_time()
        uptime = str(time.strftime("%H:%M:%S", time.gmtime(uptime_seconds)))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not retrieve uptime: {str(e)}")

    return UptimeResponse(uptime=uptime)

@router.get("/disk-usage", response_model=DiskUsageResponse, name="disk-usage", status_code=200)
async def get_disk_usage():
    try:
        disk_usage = psutil.disk_usage('/')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not retrieve disk usage: {str(e)}")

    return DiskUsageResponse(
        total=disk_usage.total,
        used=disk_usage.used,
        free=disk_usage.free,
        percent=disk_usage.percent
    )

@router.get("/network-status", response_model=NetworkStatsResponse, name="network-status", status_code=200)
async def get_network_stats():
    try:
        network_stats = psutil.net_io_counters(pernic=True)
        status = [
            {
                "interface": iface,
                "bytes_sent_total": io_stats.bytes_sent,
                "bytes_received_total": io_stats.bytes_recv,
                "packets_sent_total": io_stats.packets_sent,
                "packets_received_total": io_stats.packets_recv,
                "receive_errors": io_stats.errin,
                "transmit_errors": io_stats.errout
            }
            for iface, io_stats in network_stats.items()
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not retrieve network stats: {str(e)}")

    return NetworkStatsResponse(status=status)

