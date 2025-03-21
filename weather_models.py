
from datetime import datetime
from enum import Enum
from typing import NamedTuple


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
    """Like data class"""

    temperature: Celsius
    weather_type: WeatherType
    humidity: int
    sunrise: datetime
    sunset: datetime
    city: str

