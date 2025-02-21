from unittest.mock import Mock, patch

import pytest

from weather_weatherapi_service import ApiOpenWeatherException, Coordinates, get_weather


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
            get_weather(mock_coordinates)    with patch('weather._get_weather_service_response', side_effect=ApiOpenWeatherException):
        with pytest.raises(ApiOpenWeatherException):
            get_weather(mock_coordinates)