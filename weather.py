#!/home/yuraisme/.pyenv/shims/python
import os
from pathlib import Path

from services.coordinates import get_coordinates
from services.exceptions import ApiOpenWeatherException
from services.print import print_weather
from weather_history_storage import PlaneTextStorage, weather_save
from services.weather_openwetherapi_service import get_weather as open_get_weather
from services.weather_weatherapi_service import get_weather as weatherapi_get_weather
from services.config import OPEN_WEATHER_URL

def main_open():
    coordinates = get_coordinates()
    try:
        weather = open_get_weather( OPEN_WEATHER_URL, coordinates=coordinates)
        print_weather(weather)
        # for history
        weather_save(
            weather,
            PlaneTextStorage(os.path.join(Path.cwd(), "weather_history.txt")),
        )

    except ApiOpenWeatherException:
        print("Что-то с сервисом погоды, неудача")
        exit(1)


def main_weather_api():
    coordinates = get_coordinates()
    try:
        weather = weatherapi_get_weather(coordinates=coordinates)
        print_weather(weather)
        # for history
        weather_save(
            weather,
            PlaneTextStorage(os.path.join(Path.cwd(), "weather_history.txt")),
        )

    except ApiOpenWeatherException:
        print("Что-то с сервисом погоды, неудача")
        exit(1)


if __name__ == "__main__":
    main_open()
    main_weather_api()

    input("Press Enter")
