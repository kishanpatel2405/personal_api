import requests
from utils.enums import ErrorMessageCodes
from utils.errors import ApiException

OPENWEATHERMAP_API_KEY = "6f3076ebcaad58c12a8081eff50afc10"
OPENWEATHERMAP_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


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
