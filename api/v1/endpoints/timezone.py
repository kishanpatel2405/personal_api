from datetime import datetime
from typing import Dict, List

import pytz
from fastapi import APIRouter, Query

from schemas.v1.timezone import TimezoneSuggestionsSchema
from utils.enums import ErrorMessageCodes, Timezone
from utils.errors import ApiException

router = APIRouter()

timezone_favorites = []


@router.get(
    "/convert", response_model=Dict[str, str], summary="Convert time between time zones"
)
def convert_time(
    from_zone: Timezone,
    to_zones: List[Timezone] = Query(...),
    time: str = Query(datetime.now().strftime("%H:%M:%S")),
):
    try:
        from_tz = pytz.timezone(from_zone.value)
        converted_times = {}

        naive_time = datetime.strptime(time, "%H:%M:%S")
        localized_time = from_tz.localize(naive_time)

        for to_zone in to_zones:
            to_tz = pytz.timezone(to_zone.value)
            converted_time = localized_time.astimezone(to_tz)
            converted_times[to_zone.value] = converted_time.strftime("%H:%M:%S")

        return converted_times
    except Exception:
        raise ApiException(
            msg="Error converting time.",
            error_code=ErrorMessageCodes.BAD_REQUEST,
            status_code=400,
        )


@router.post(
    "/favorites",
    response_model=List[str],
    summary="Save frequently used time zones to favorites",
)
def save_timezone_to_favorites(zone: Timezone):
    if zone not in pytz.all_timezones:
        raise ApiException(
            msg="Invalid time zone.",
            error_code=ErrorMessageCodes.BAD_REQUEST,
            status_code=400,
        )
    if zone not in timezone_favorites:
        timezone_favorites.append(zone)
    return timezone_favorites


@router.get(
    "/suggestions",
    response_model=TimezoneSuggestionsSchema,
    summary="Suggest optimal meeting times for saved time zones",
)
def get_meeting_suggestions(base_time: str):
    try:
        base_time_dt = datetime.strptime(base_time, "%Y-%m-%d %H:%M:%S")
        suggestions = {}
        for zone in timezone_favorites:
            tz = pytz.timezone(zone)
            localized_time = base_time_dt.astimezone(tz)
            suggestions[zone] = localized_time.strftime("%Y-%m-%d %H:%M:%S")
        return TimezoneSuggestionsSchema(base_time=base_time, suggestions=suggestions)
    except Exception:
        raise ApiException(
            msg="Error suggesting meeting times.",
            error_code=ErrorMessageCodes.BAD_REQUEST,
            status_code=400,
        )
