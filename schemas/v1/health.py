from pydantic import BaseModel


class HealthResult(BaseModel):
    is_alive: bool
