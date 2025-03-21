import json
import logging
import urllib.error
import urllib.request
from datetime import datetime
from typing import Literal
from services.coordinates import Coordinates, get_coordinates
from services.exceptions import ApiOpenWeatherException
from weather_models import Weather, WeatherType

Celsius = float
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)


def _parse_wether_response(answer):
    try:
        weather_as_dict = json.loads(answer)
    except json.JSONDecodeError:
        raise ApiOpenWeatherException
    if weather_as_dict["cod"] == 200:
        # pprint(answer.json())
        return Weather(
            temperature=_parse_temp(weather_as_dict) or 0,
            humidity=_parse_humidity(weather_as_dict) or 0,
            weather_type=_parse_weather_type(weather_as_dict),
            sunrise=_parse_sun_time(weather_as_dict, "sunrise"),
            sunset=_parse_sun_time(weather_as_dict, "sunset"),
            city=weather_as_dict["name"],
        )
    else:
        logger.error(weather_as_dict.get("message"))
        raise ApiOpenWeatherException


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


def _parse_temp(weather_as_dict: dict) -> Celsius | None:
    try:
        return weather_as_dict["main"]["temp"]
    except KeyError:
        logging.error("No correct 'temp' in weather data")


def _parse_humidity(weather_as_dict: dict) -> int | None:
    try:
        return weather_as_dict["main"]["humidity"]
    except KeyError:
        logging.error("No correct 'humidity' in weather data")


def _get_weather_service_response(url: str, coordinates: Coordinates) -> str:
    """Request direct ot Weather API"""

    try:
        with urllib.request.urlopen(
            url.format(
                latitude=coordinates.latitude,
                longtitude=coordinates.longitude,
            )
        ) as response:
            # response = request.get(url)
            data_from_api = response.read().decode()

    except urllib.error.URLError as e:
        logger.error(e)
        raise ApiOpenWeatherException

    if response.code == 200:
        return data_from_api
    else:
        raise ApiOpenWeatherException


def get_weather(url: str, coordinates: Coordinates | None) -> Weather | None:
    """get from weather service API and return data"""
    if coordinates:
        try:
            weather_service_response = _get_weather_service_response(
                url, coordinates=coordinates
            )
            # print(weather_service_response)
            weather = _parse_wether_response(weather_service_response)
            return weather
        except Exception as e:
            logging.error(f"{e}")
            raise ApiOpenWeatherException
    else:
        raise ApiOpenWeatherException


if __name__ == "__main__":
    from services.config import  OPEN_WEATHER_URL
    print(get_weather("", get_coordinates()))
    # print(WeatherType.CLEAR.name)
