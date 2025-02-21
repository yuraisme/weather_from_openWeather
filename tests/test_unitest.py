import json
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from weather_openwetherapi_service import (
    ApiOpenWeatherException,
    Coordinates,
    Weather,
    WeatherType,
    _parse_humidity,
    _parse_sun_time,
    _parse_temp,
    _parse_weather_type,
    _parse_wether_response,
    get_weather,
)


class TestWeatherModule(unittest.TestCase):
    """real json from the server openweather"""

    def setUp(self):
        self.sample_response = {
            "base": "stations",
            "clouds": {"all": 99},
            "cod": 200,
            "coord": {"lat": 55.7558, "lon": 37.6175},
            "dt": 1739886340,
            "id": 524901,
            "main": {
                "feels_like": -6.5,
                "grnd_level": 1000,
                "humidity": 52,
                "pressure": 1020,
                "sea_level": 1020,
                "temp": -4.13,
                "temp_max": -3.68,
                "temp_min": -5.76,
            },
            "name": "Москва",
            "sys": {
                "country": "RU",
                "id": 2094500,
                "sunrise": 1739854052,
                "sunset": 1739889581,
                "type": 2,
            },
            "timezone": 10800,
            "visibility": 10000,
            "weather": [
                {
                    "description": "пасмурно",
                    "icon": "04d",
                    "id": 804,
                    "main": "Clouds",
                }
            ],
            "wind": {"deg": 204, "gust": 2.86, "speed": 1.52},
        }

    def test_parse_temp(self):
        temp = _parse_temp(self.sample_response)
        self.assertEqual(temp, -4.13)

    def test_parse_humidity(self):
        humidity = _parse_humidity(self.sample_response)
        self.assertEqual(humidity, 52)

    def test_parse_weather_type(self):
        weather_type = _parse_weather_type(self.sample_response)
        self.assertEqual(weather_type, WeatherType.CLOUDS)

    def test_parse_sun_time(self):
        sun_time = _parse_sun_time(self.sample_response, "sunrise")
        self.assertEqual(sun_time, datetime.fromtimestamp(1739854052))

    def test_parse_weather_response(self):
        weather = _parse_wether_response(json.dumps(self.sample_response))
        self.assertIsInstance(weather, Weather)
        self.assertEqual(weather.temperature, -4.13)
        self.assertEqual(weather.humidity, 52)
        self.assertEqual(weather.weather_type, WeatherType.CLOUDS)
        self.assertEqual(weather.sunrise, datetime.fromtimestamp(1739854052))
        self.assertEqual(weather.sunset, datetime.fromtimestamp(1739889581))
        self.assertEqual(weather.city, "Москва")

    @patch("weather_openwetherapi_service._get_weather_service_response")
    def test_get_weather(self, mock_get_weather_service_response):
        mock_get_weather_service_response.return_value = json.dumps(
            self.sample_response
        )
        weather = get_weather(
            Coordinates(latitude=55.7504461, longitude=37.6176)
        )
        if weather:
            self.assertIsInstance(weather, Weather)
            self.assertEqual(weather.temperature, -4.13)
            self.assertEqual(weather.humidity, 52)
            self.assertEqual(weather.weather_type, WeatherType.CLOUDS)
            self.assertEqual(weather.sunrise, datetime.fromtimestamp(1739854052))
            self.assertEqual(weather.sunset, datetime.fromtimestamp(1739889581))
            self.assertEqual(weather.city, "Москва")

    @patch("weather_openwetherapi_service._get_weather_service_response")
    def test_get_weather_api_error(self, mock_get_weather_service_response):
        mock_get_weather_service_response.side_effect = (
            ApiOpenWeatherException()
        )
        coordinates = Coordinates(latitude=55.7558, longitude=37.6174943)
        with self.assertRaises(ApiOpenWeatherException):
            get_weather(coordinates)

    def test_parse_weather_response_invalid_json(self):
        with self.assertRaises(ApiOpenWeatherException):
            _parse_wether_response("invalid json")

    def test_parse_weather_response_error_code(self):
        error_response = {"cod": 401, "message": "key not found"}
        with self.assertRaises(ApiOpenWeatherException):
            _parse_wether_response(json.dumps(error_response))


if __name__ == "__main__":
    unittest.main()
