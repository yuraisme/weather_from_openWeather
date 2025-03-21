import datetime

from services.weather_openwetherapi_service import Weather, WeatherType


def format_weather(weather: Weather):
    """pretty format weather data"""
    return (
        f"       City: {weather.city} \n"
        f"{'-'*20}\n"
        f"Temperature: {weather.temperature:.1f}°С\n"
        f"   Humidity: {weather.humidity} %\n"
        f"    Weather: {weather.weather_type.value}\n"
        f"    Sunrise: {weather.sunrise:%H:%M}\n"
        f"     Sunset: {weather.sunset:%H:%M}\n"
    )


if __name__ == "__main__":
    print(
        format_weather(
            Weather(
                city="Stupino",
                temperature=-0.2,
                humidity=90,
                weather_type=WeatherType.SNOW,
                sunrise=datetime.datetime.now(),
                sunset=datetime.datetime.now(),
            )
        )
    )
