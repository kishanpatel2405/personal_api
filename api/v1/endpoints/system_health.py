import psutil
from fastapi import APIRouter
from datetime import datetime
from schemas.v1.system_health import SystemHealthResponse

router = APIRouter()


def get_system_uptime() -> str:
    boot_time = psutil.boot_time()
    uptime = datetime.now() - datetime.fromtimestamp(boot_time)
    return str(uptime).split('.')[0]


def get_cpu_usage() -> float:
    return psutil.cpu_percent(interval=1)


def get_memory_usage() -> float:
    memory_info = psutil.virtual_memory()
    return memory_info.percent


def get_disk_space() -> str:
    disk_info = psutil.disk_usage('/')
    return f"{disk_info.total / (1024 ** 3):.2f} GB"


@router.get("/system/health", response_model=SystemHealthResponse)
async def get_system_health():
    return SystemHealthResponse(
        status="healthy",
        uptime=get_system_uptime(),
        cpu_usage=get_cpu_usage(),
        memory_usage=get_memory_usage(),
        disk_space=get_disk_space()
    )
