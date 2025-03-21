from unittest.mock import Mock, patch

import pytest

from services.weather_weatherapi_service import ApiOpenWeatherException, Coordinates, get_weather

CURRENT_ANSWER_JSON = """ {
                "current": {
                    "cloud": 0,
                    "condition": {
                        "code": 1000,
                        "icon": "//cdn.weatherapi.com/weather/64x64/day/113.png",
                        "text": "Sunny"
                    },
                    "dewpoint_c": -8.9,
                    "dewpoint_f": 15.9,
                    "feelslike_c": -5.5,
                    "feelslike_f": 22.1,
                    "gust_kph": 12.7,
                    "gust_mph": 7.9,
                    "heatindex_c": -6.4,
                    "heatindex_f": 20.4,
                    "humidity": 63,
                    "is_day": 1,
                    "last_updated": "2025-02-21 17:15",
                    "last_updated_epoch": 1740147300,
                    "precip_in": 0.0,
                    "precip_mm": 0.0,
                    "pressure_in": 30.62,
                    "pressure_mb": 1037.0,
                    "temp_c": -2.7,
                    "temp_f": 27.1,
                    "uv": 0.0,
                    "vis_km": 10.0,
                    "vis_miles": 6.0,
                    "wind_degree": 248,
                    "wind_dir": "WSW",
                    "wind_kph": 6.8,
                    "wind_mph": 4.3,
                    "windchill_c": -9.8,
                    "windchill_f": 14.3
                },
                "location": {
                    "country": "Russia",
                    "lat": 54.9008,
                    "localtime": "2025-02-21 17:26",
                    "localtime_epoch": 1740148015,
                    "lon": 38.0708,
                    "name": "Stupino",
                    "region": "Moskva",
                    "tz_id": "Europe/Moscow"
                }
            }
            """

ASTRONOMY_ANSWER_JSON ="""{
                        "astronomy": {
                            "astro": {
                                "is_moon_up": 0,
                                "is_sun_up": 0,
                                "moon_illumination": 58,
                                "moon_phase": "Last Quarter",
                                "moonrise": "02:13 AM",
                                "moonset": "09:22 AM",
                                "sunrise": "07:39 AM",
                                "sunset": "05:45 PM"
                            }
                        },
                        "location": {
                            "country": "Russia",
                            "lat": 54.9008,
                            "localtime": "2025-02-21 17:30",
                            "localtime_epoch": 1740148257,
                            "lon": 38.0708,
                            "name": "Stupino",
                            "region": "Moskva",
                            "tz_id": "Europe/Moscow"
                        }
                    } """

def test_get_weather_success():
    mock_coordinates = Coordinates(latitude=50.0, longitude=50.0)
    mock_weather_response = '{"main": {"temp": 20, "humidity": 50}, "weather": [{"main": "Clear"}], "name": "Test City", "astronomy": {"astronomy": {"sunrise": "06:00 AM", "sunset": "06:00 PM"}}}'
    mock_sunset_response = '{"sunrise": "06:00 AM", "sunset": "06:00 PM"}'
    with patch('weather._get_weather_service_response') as mock_get_weather_service_response:
        mock_get_weather_service_response.side_effect = [mock_weather_response, mock_sunset_response]
        weather = get_weather(mock_coordinates)
        assert weather.temperature == 20
        assert weather.humidity == 50
        assert weather.weather_type.name == 'CLEAR'
        assert weather.city == 'Test City'
        assert weather.sunrise == '06:00 AM'
        assert weather.sunset == '06:00 PM'

def test_get_weather_failure():
    mock_coordinates = Coordinates(latitude=50.0, longitude=50.0)
    with patch('weather._get_weather_service_response', side_effect=ApiOpenWeatherException):
        with pytest.raises(ApiOpenWeatherException):
            get_weather(mock_coordinates)    
        with patch('weather._get_weather_service_response', side_effect=ApiOpenWeatherException):
            with pytest.raises(ApiOpenWeatherException):
                get_weather(mock_coordinates)