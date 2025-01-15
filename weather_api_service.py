import json
import urllib.error
import urllib.request
from datetime import datetime
from enum import Enum
from typing import Literal, NamedTuple

from config import OPEN_WEATHER_URL
from coordinates import Coordinates, get_coordinates
from exceptions import ApiWeatherException

Celsius = float


class WeatherType(Enum):
    """Enumirate of weather type from service"""

    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморозь"
    RAIN = "Дожжь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    CLOUDS = "Облачно"
    FOG = "Туман"


class Weather(NamedTuple):
    temperature: Celsius
    weather_type: WeatherType
    humidity: int
    sunrise: datetime
    sunset: datetime
    city: str


def _parse_wether_response(answer):
    try:
        weather_as_dict = json.loads(answer)
    except json.JSONDecodeError:
        raise ApiWeatherException
    if weather_as_dict["cod"] == 200:
        # pprint(answer.json())
        return Weather(
            temperature=_parse_temp(weather_as_dict),
            humidity=_parse_humidity(weather_as_dict),
            weather_type=_parse_weather_type(weather_as_dict),
            sunrise=_parse_sun_time(weather_as_dict, "sunrise"),
            sunset=_parse_sun_time(weather_as_dict, "sunset"),
            city=weather_as_dict["name"],
        )
    else:
        raise ApiWeatherException


def _parse_sun_time(
    weather_as_dict: dict,
    type_sun_time: Literal["sunrise"] | Literal["sunset"],
) -> datetime:
    return datetime.fromtimestamp(weather_as_dict["sys"][type_sun_time])


def _parse_weather_type(weather_as_dict: dict):
    weather_type = weather_as_dict["weather"][0]["main"].upper()
    tp = list(
        filter(
            lambda x: x.name == weather_type,
            WeatherType,
        )
    )
    return tp[0]


def _parse_temp(weather_as_dict) -> Celsius:
    return weather_as_dict["main"]["temp"]


def _parse_humidity(weather_as_dict) -> int:
    return weather_as_dict["main"]["humidity"]


def _get_weather_service_response(coordinates: Coordinates) -> str:
    """Request direct ot Weather API"""
    url = OPEN_WEATHER_URL.format(
        latitude=coordinates.latitude, longtitude=coordinates.longitude
    )

    try:
        with urllib.request.urlopen(url) as response:
            # response = request.get(url)
            data_from_api = response.read().decode()

    except urllib.error.URLError:
        raise ApiWeatherException

    if response.code == 200:
        return data_from_api
    else:
        raise ApiWeatherException


def get_weather(coordinates: Coordinates) -> Weather | None:
    """get from weather service API and return this one"""
    weather_service_response = _get_weather_service_response(
        coordinates=coordinates
    )
    print(weather_service_response)
    weather = _parse_wether_response(weather_service_response)
    return weather


if __name__ == "__main__":
    print(get_weather(get_coordinates()))
    # print(WeatherType.CLEAR.name)
