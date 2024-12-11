from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any
from services.weather import fetch_weather_data

router = APIRouter()

@router.get("/weather", response_model=Dict[str, Any], status_code=200)
async def get_weather(city: str = Query(..., description="The city name to fetch weather for", example="London")):
    try:
        weather_data = fetch_weather_data(city)
    except HTTPException as e:
        raise e

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
