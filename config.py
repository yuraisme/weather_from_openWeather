from tokens import WEATHER_API_KEY, OPENWEATHER_API_KEY

OPEN_WEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather?"
    "lat={latitude}&"
    "lon={longtitude}&"
    "lang=ru&"
    "units=metric&appid=" + OPENWEATHER_API_KEY
)

WEATHERAPI_URL_WEATHER = (
    f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}"
    "&q={latitude},{longtitude}&aqi=no"
)
WEATHER_URL_ASTRONOMY = (
    f"http://api.weatherapi.com/v1/astronomy.json?key={WEATHER_API_KEY}"
    "&q={latitude},{longtitude}"
    "&dt={timestamp}"
)
