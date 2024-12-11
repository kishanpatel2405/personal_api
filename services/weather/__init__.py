import requests
from fastapi import HTTPException

# Define OpenWeatherMap API key and base URL
OPENWEATHERMAP_API_KEY = "6f3076ebcaad58c12a8081eff50afc10"
OPENWEATHERMAP_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather_data(city: str):
    response = requests.get(
        OPENWEATHERMAP_BASE_URL,
        params={
            "q": city,
            "appid": OPENWEATHERMAP_API_KEY,
            "units": "metric"
        }
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch weather data.")

    data = response.json()

    if "main" not in data:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found.")

    weather = {
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "weather_description": data["weather"][0]["description"],
        "sunrise": data["sys"]["sunrise"],
        "sunset": data["sys"]["sunset"],
    }

    return weather
