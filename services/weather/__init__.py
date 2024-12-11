import requests
from fastapi import HTTPException

# Define OpenWeatherMap API key and base URL
OPENWEATHERMAP_API_KEY = "6f3076ebcaad58c12a8081eff50afc10"
OPENWEATHERMAP_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather_data(city: str):
    """
    Fetch current weather data for a given city using OpenWeatherMap API.
    """
    # Send GET request to OpenWeatherMap API
    response = requests.get(
        OPENWEATHERMAP_BASE_URL,
        params={
            "q": city,
            "appid": OPENWEATHERMAP_API_KEY,
            "units": "metric"  # Temperature in Celsius
        }
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch weather data.")

    data = response.json()

    # Check if the city is valid
    if "main" not in data:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found.")

    # Extract relevant data
    weather = {
        "city": city,
        "temperature": data["main"]["temp"],  # Temperature in Celsius
        "humidity": data["main"]["humidity"],  # Humidity in percentage
        "pressure": data["main"]["pressure"],  # Atmospheric pressure in hPa
        "wind_speed": data["wind"]["speed"],  # Wind speed in m/s
        "weather_description": data["weather"][0]["description"],  # Weather description
        "sunrise": data["sys"]["sunrise"],  # Sunrise time (UNIX timestamp)
        "sunset": data["sys"]["sunset"],  # Sunset time (UNIX timestamp)
    }

    return weather
