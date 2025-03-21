import pytest
from services.coordinates import Coordinates, get_coordinates
from services.weather_openwetherapi_service import Weather, WeatherType, get_weather
from services.exceptions import ApiOpenWeatherException


def test_coordinates():
    result = get_coordinates()
    assert isinstance(result.latitude, float)
    assert isinstance(result.longitude, float)
    assert result.latitude > 1
    assert result.longitude > 0


def test_get_weather():
    """Конечная точка модуля"""
    result = get_weather(Coordinates(55.7558,  37.6175)) #Москва

    assert isinstance(result, Weather), "вернул неправильный объект"
    assert result.city == "Москва", "неправильный город"
    assert -45 <= result.temperature <= 50.0, "Температура выходит за пределы"
    assert 0 <= result.humidity <= 100, "Влажность выходит за пределы"
    assert isinstance(result.weather_type, WeatherType), "вернул что-то не то"
    assert result.weather_type in WeatherType
    
    with pytest.raises(ApiOpenWeatherException):
        get_weather(None)
        get_weather("as")
