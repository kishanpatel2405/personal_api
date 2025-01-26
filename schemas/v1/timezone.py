from typing import Dict, List

from pydantic import BaseModel

from utils.enums import Timezone


class TimezoneFavoriteSchema(BaseModel):
    zone: str


class TimezoneSuggestionsSchema(BaseModel):
    base_time: str
    suggestions: Dict[str, str]


class TimezoneConvertSchema(BaseModel):
    from_zone: Timezone
    to_zones: List[Timezone]
    time: str
