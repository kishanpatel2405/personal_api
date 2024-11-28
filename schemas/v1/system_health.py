from pydantic import BaseModel

class SystemHealthResponse(BaseModel):
    status: str
    uptime: str
    cpu_usage: float
    memory_usage: float
    disk_space: str
    #
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "status": "healthy",
    #             "uptime": "24 days, 3 hours",
    #             "cpu_usage": 35.5,
    #             "memory_usage": 70.3,
    #             "disk_space": "500GB"
    #         }
    #     }
