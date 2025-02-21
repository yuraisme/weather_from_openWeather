import json
import urllib.error
import urllib.request
from datetime import datetime
from enum import Enum
from logging import Logger
from typing import Dict, Literal, NamedTuple

from config import WEATHER_URL_ASTRONOMY, WEATHERAPI_URL_WEATHER
from coordinates import Coordinates, get_coordinates
from exceptions import ApiOpenWeatherException, ApiWeatherApiException

Celsius = float
WEATHER_CODES = {
    1000: "Ясно",
    1003: "Облачно",
    1006: "Облачно",
    1009: "Облачно",
    1030: "Туман",
    1063: "Облачно",
    1066: "Облачно",
    1069: "Облачно",
    1072: "Облачно",
    1087: "Гроза",
    1114: "Снег",
    1117: "Дожжь",
    1135: "Туман",
    1147: "Туман",
    1150: "Дожжь",
    1153: "Дожжь",
    1168: "Дожжь",
    1171: "Дожжь",
    1180: "Дожжь",
    1183: "Дожжь",
    1186: "Дожжь",
    1189: "Дожжь",
    1192: "Дожжь",
    1195: "Дожжь",
    1198: "Дожжь",
    1201: "Дожжь",
    1204: "Дожжь",
    1207: "Дожжь",
    1210: "Снег",
    1213: "Снег",
    1216: "Снег",
    1219: "Снег",
    1222: "Снег",
    1225: "Снег",
    1237: "Снег",
    1240: "Дожжь",
    1243: "Дожжь",
    1246: "Дожжь",
    1249: "Дожжь",
    1252: "Дожжь",
    1255: "Снег",
    1258: "Снег",
    1261: "Дожжь",
    1264: "Дожжь",
    1273: "Дожжь",
    1276: "Дожжь",
    1279: "Снег",
    1282: "Снег",
}


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
    """Like data class"""

    temperature: Celsius
    weather_type: WeatherType
    humidity: int
    sunrise: datetime
    sunset: datetime
    city: str


class Weather_response(NamedTuple):
    weather: str
    astronomy: str


def _parse_wether_response(answer_weather: str, answer_astronomy: str):

    try:
        weather_as_dict = json.loads(answer_weather)
        astro_as_dict = json.loads(answer_astronomy)
    except json.JSONDecodeError:
        raise ApiOpenWeatherException
    if weather_as_dict and astro_as_dict is not None:
        # pprint(answer.json())
        return Weather(
            temperature=_parse_temp(weather_as_dict),
            humidity=_parse_humidity(weather_as_dict),
            weather_type=_parse_weather_type(weather_as_dict),
            sunrise=_parse_sun_time(astro_as_dict, "sunrise"),
            sunset=_parse_sun_time(astro_as_dict, "sunset"),
            city=weather_as_dict.get("location", {}).get("name", ""),
        )
    else:
        raise ApiOpenWeatherException


def _parse_sun_time(
    weather_as_dict: dict,
    type_sun_time: Literal["sunrise"] | Literal["sunset"],
) -> datetime:
    today = datetime.today().date()

    match type_sun_time:
        case "sunrise":
            try:
                sunrise = datetime.strptime(
                    weather_as_dict.get("astronomy", {})
                    .get("astro", {})
                    .get("sunrise", ""),
                    "%I:%M %p",
                ).time()
                return datetime.combine(today, sunrise)
            except KeyError:
                raise ApiOpenWeatherException
        case "sunset":
            try:
                sunset = datetime.strptime(
                    weather_as_dict.get("astronomy", {})
                    .get("astro", {})
                    .get("sunset", ""),
                    "%I:%M %p",
                ).time()
                return datetime.combine(today, sunset)

            except KeyError:
                raise ApiOpenWeatherException


def _parse_weather_type(weather_as_dict: dict) -> WeatherType:
    weather_type_code = (
        weather_as_dict.get("current", {})
        .get("condition", {})
        .get("code", "")
    )
    # делаем более удобный варинт для поска по ключу
    weather_type = {w.value: w for w in WeatherType}

    return weather_type[WEATHER_CODES.get(weather_type_code, "")]


def _parse_temp(weather_as_dict) -> Celsius:
    return weather_as_dict["current"]["heatindex_c"]


def _parse_humidity(weather_as_dict) -> int:
    return weather_as_dict["current"]["humidity"]


def _get_weather_service_response(
    coordinates: Coordinates, data_type: Literal["weather", "sunset"]
) -> str:
    """Request direct ot Weather API"""
    match data_type:
        case "weather":
            url = WEATHERAPI_URL_WEATHER.format(
                latitude=coordinates.latitude,
                longtitude=coordinates.longitude,
            )
        case "sunset":
            url = WEATHER_URL_ASTRONOMY.format(
                latitude=coordinates.latitude,
                longtitude=coordinates.longitude,
                timestamp=datetime.now().strftime("%Y/%m/%d"),
            )

    try:
        with urllib.request.urlopen(url) as response:
            data_from_api = response.read().decode()
            # print(data_from_api)

    except urllib.error.URLError:
        raise ApiOpenWeatherException

    if response.code == 200:
        return data_from_api
    else:
        raise ApiOpenWeatherException


def get_weather(coordinates: Coordinates) -> Weather:
    """get from weather service API and return data"""
    if coordinates:
        try:
            weather_service_response = _get_weather_service_response(
                coordinates=coordinates, data_type="weather"
            )
            sunset_service_response = _get_weather_service_response(
                coordinates=coordinates, data_type="sunset"
            )
            # print(weather_service_response)
            weather = _parse_wether_response(
                weather_service_response,
                sunset_service_response,
            )
            return weather
        except:
            raise ApiWeatherApiException
    else:
        raise ApiWeatherApiException


if __name__ == "__main__":
    print(get_weather(get_coordinates()))
    # print(WeatherType.CLEAR.name)
