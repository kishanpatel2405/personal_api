import psutil
from fastapi import APIRouter

from schemas.v1.health import (CpuTemperatureResponse, DiskUsageResponse,
                               HealthResult, IPAddressResponse,
                               NetworkStatsResponse, SystemMetricsResponse)
from services.health import get_external_ip, get_local_ip
from utils.enums import Ip_Type
from utils.errors import ApiException, ErrorMessageCodes

router = APIRouter()


@router.get("/health", response_model=HealthResult, name="health", status_code=200)
async def health():
    return HealthResult(is_alive=True)


@router.get(
    "/ip-address", response_model=IPAddressResponse, status_code=200, name="ip-address"
)
async def get_ip_address(ip_type: Ip_Type = Ip_Type.LOCAL):
    try:
        if ip_type == Ip_Type.EXTERNAL:
            ip_address = get_external_ip()
            ip_type = "external"
        else:
            ip_address = get_local_ip()
            ip_type = "local"
    except Exception as e:
        raise ApiException(
            msg=f"Could not retrieve IP address: {str(e)}",
            error_code=ErrorMessageCodes.IP_RETRIEVAL_FAILED,
            status_code=500,
        )

    return IPAddressResponse(ip_address=ip_address, type=ip_type)


@router.get(
    "/metrics",
    response_model=SystemMetricsResponse,
    name="health-metrics",
    status_code=200,
)
async def get_system_metrics():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
    except Exception as e:
        raise ApiException(
            msg=f"Could not retrieve system metrics: {str(e)}",
            error_code=ErrorMessageCodes.SYSTEM_METRICS_FAILED,
            status_code=500,
        )

    return SystemMetricsResponse(cpu_usage=cpu_usage, memory_usage=memory_usage)


@router.get(
    "/disk-usage", response_model=DiskUsageResponse, name="disk-usage", status_code=200
)
async def get_disk_usage():
    try:
        disk_usage = psutil.disk_usage("/")
    except Exception as e:
        raise ApiException(
            msg=f"Could not retrieve disk usage: {str(e)}",
            error_code=ErrorMessageCodes.DISK_USAGE_FAILED,
            status_code=500,
        )

    return DiskUsageResponse(
        total=disk_usage.total,
        used=disk_usage.used,
        free=disk_usage.free,
    )


@router.get(
    "/network-status",
    response_model=NetworkStatsResponse,
    name="network-status",
    status_code=200,
)
async def get_network_stats():
    try:
        network_stats = psutil.net_io_counters(pernic=True)
        status = [
            {
                "interface": iface,
                "bytes_sent_total": str(io_stats.bytes_sent),
                "bytes_received_total": str(io_stats.bytes_recv),
                "packets_sent_total": str(io_stats.packets_sent),
                "packets_received_total": str(io_stats.packets_recv),
                "receive_errors": str(io_stats.errin),
                "transmit_errors": str(io_stats.errout),
            }
            for iface, io_stats in network_stats.items()
        ]
    except Exception as e:
        raise ApiException(
            msg=f"Could not retrieve network stats: {str(e)}",
            error_code=ErrorMessageCodes.NETWORK_STATS_FAILED,
            status_code=500,
        )

    return NetworkStatsResponse(status=status)


@router.get(
    "/cpu-temperature",
    response_model=CpuTemperatureResponse,
    name="cpu-temperature",
    status_code=200,
)
async def get_cpu_temperature():
    temperatures = psutil.sensors_temperatures()

    if "coretemp" in temperatures:
        core_temperatures = temperatures["coretemp"]
        if core_temperatures:
            return CpuTemperatureResponse(
                core=core_temperatures[0].label,
                temperature=core_temperatures[0].current,
            )

    return CpuTemperatureResponse(core="N/A", temperature=-1.0)
