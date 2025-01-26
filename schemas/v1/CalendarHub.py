from datetime import datetime

from pydantic import BaseModel


class Event(BaseModel):
    id: str
    summary: str
    start: datetime
    end: datetime
