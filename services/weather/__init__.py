from datetime import datetime

import requests

from utils.enums import ErrorMessageCodes
from utils.errors import ApiException

OPENWEATHERMAP_API_KEY = "6f3076ebcaad58c12a8081eff50afc10"
OPENWEATHERMAP_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHERMAP_HISTORICAL_BASE_URL = "https://api.openweathermap.org/data/2.5/onecall/timemachine"


def fetch_weather_data(city: str):
    try:
        response = requests.get(
            OPENWEATHERMAP_BASE_URL,
            params={
                "q": city,
                "appid": OPENWEATHERMAP_API_KEY,
                "units": "metric"
            }
        )
        if response.status_code == 404:
            raise ApiException(
                msg=f"City '{city}' not found.",
                error_code=ErrorMessageCodes.NOT_FOUND,
                status_code=404
            )
        elif response.status_code != 200:
            raise ApiException(
                msg="Failed to fetch weather data. Please try again later.",
                error_code=ErrorMessageCodes.BAD_REQUEST,
                status_code=response.status_code
            )

        data = response.json()

        if "main" not in data:
            raise ApiException(
                msg=f"Invalid weather data received for city '{city}'.",
                error_code=ErrorMessageCodes.BAD_REQUEST,
                status_code=500
            )

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

    except requests.RequestException as e:
        raise ApiException(
            msg="An error occurred while connecting to the weather service.",
            error_code=ErrorMessageCodes.BAD_REQUEST,
            status_code=500
        )


def fetch_city_coordinates(city: str):
    geocode_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHERMAP_API_KEY
    }
    response = requests.get(geocode_url, params=params)

    if response.status_code != 200:
        raise ApiException(
            msg="City not found or API error.",
            error_code=ErrorMessageCodes.NOT_FOUND,
            status_code=response.status_code
        )

    data = response.json()

    if "coord" not in data:
        raise ApiException(
            msg=f"City '{city}' not found.",
            error_code=ErrorMessageCodes.NOT_FOUND,
            status_code=404
        )

    return data["coord"]


def get_weather_for_date(coords, timestamp):
    url = OPENWEATHERMAP_HISTORICAL_BASE_URL
    params = {
        "lat": coords["lat"],
        "lon": coords["lon"],
        "dt": timestamp,
        "appid": OPENWEATHERMAP_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise ApiException(
            msg="Failed to fetch historical weather data.",
            error_code=ErrorMessageCodes.BAD_REQUEST,
            status_code=response.status_code
        )

    data = response.json()

    if "current" not in data:
        raise ApiException(
            msg="Historical data not available.",
            error_code=ErrorMessageCodes.NOT_FOUND,
            status_code=404
        )

    weather_info = {
        "date": datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d'),
        "temperature": data["current"]["temp"],
        "humidity": data["current"]["humidity"],
        "pressure": data["current"]["pressure"],
        "weather_description": data["current"]["weather"][0]["description"],
        "wind_speed": data["current"]["wind_speed"]
    }

    return weather_info
