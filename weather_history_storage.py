import datetime

from weather_api_service import Weather
from weather_formater import format_weather


class SaveWeatherStorage:
    def save(self, weather: Weather) -> None:
        raise NotImplementedError


class PlaneTextStorage(SaveWeatherStorage):
    def __init__(self, path: str) -> None:
        self.file = path

    def save(self, weather: Weather) -> None:
        if weather:
            with open(self.file, "a") as file:
                now = datetime.datetime.now()
                file.write(f"{now}\n{format_weather(weather)}\n")


def weather_save(weather: Weather | None, weather_storage: SaveWeatherStorage):
    if weather:
        weather_storage.save(weather)
