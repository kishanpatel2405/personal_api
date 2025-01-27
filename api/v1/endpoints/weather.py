from typing import Any, Dict, Optional

from fastapi import APIRouter, Query

from services.weather import fetch_historical_weather_data, fetch_weather_data
from utils.enums import GujaratCities
from utils.errors import ApiException

router = APIRouter()


@router.get(
    "/weather", name="get live weather", response_model=Dict[str, Any], status_code=200
)
async def get_weather(
    city: Optional[GujaratCities] = Query(None),
    custom_city: Optional[str] = Query(None),
):
    if not city and not custom_city:
        return {
            "error": "No city parameter provided. Please select a city from the dropdown or enter a custom city.",
            "status_code": 400,
        }

    city_name = custom_city if city == "Other" else city.value if city else custom_city

    try:
        weather_data = fetch_weather_data(city_name)
    except ApiException as e:
        raise ApiException(
            msg=e.msg, error_code=e.error_code, status_code=e.status_code
        )

    return {
        "city": weather_data["city"],
        "temperature": weather_data["temperature"],
        "humidity": weather_data["humidity"],
        "pressure": weather_data["pressure"],
        "wind_speed": weather_data["wind_speed"],
        "weather_description": weather_data["weather_description"],
        "sunrise": weather_data["sunrise"],
        "sunset": weather_data["sunset"],
    }


@router.get(
    "/historical-weather",
    name="History of Weather",
    response_model=Dict[str, Any],
    status_code=200,
)
async def get_historical_weather(
    city: str = Query(
        ...,
        description="The city name to fetch historical weather data for",
        example="Ahmedabad",
    ),
    start_date: str = Query(
        ..., description="Start date in YYYY-MM-DD format", example="2023-01-01"
    ),
    end_date: str = Query(
        ..., description="End date in YYYY-MM-DD format", example="2023-01-05"
    ),
):
    try:
        historical_data = fetch_historical_weather_data(city, start_date, end_date)
    except ApiException as e:
        raise ApiException(
            msg=e.msg, error_code=e.error_code, status_code=e.status_code
        )

    return {
        "city": city,
        "start_date": start_date,
        "end_date": end_date,
        "historical_data": historical_data,
    }
