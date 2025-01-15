#!/home/yuraisme/.pyenv/shims/python
import os
from pathlib import Path

from coordinates import get_coordinates
from exceptions import ApiWeatherException
from print import print_weather
from weather_api_service import get_weather
from weather_history_storage import PlaneTextStorage, weather_save


def main():
    coordinates = get_coordinates()
    try:
        weather = get_weather(coordinates=coordinates)
        print_weather(weather)
        # for history
        weather_save(
            weather,
            PlaneTextStorage(os.path.join(Path.cwd(), "weather_history.txt")),
        )

    except ApiWeatherException:
        print("Что-то с сервисом погоды, неудача")
        exit(1)


if __name__ == "__main__":
    main()
    input("Press Enter")
