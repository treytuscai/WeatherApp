import pytest
from unittest.mock import patch

from website.weather_utils import (
    validate_city_and_country,
    build_weather_api_url,
    fetch_weather_data,
    parse_weather_response
)

@pytest.mark.parametrize("city, country, expected", [
    ("London", "GB", True),
    ("NewYork", "US", True),
    ("123", "GB", False),
    ("London", "gbr", False),
    ("Paris", "FRA", False),
])
def test_validate_city_and_country(city, country, expected):
    """Test if valid country or city format."""
    assert validate_city_and_country(city, country) == expected

def test_parse_weather_response():
    """Test if weather data is correctly extracted from API response."""
    mock_response = {
        "name": "London",
        "sys": {"country": "GB"},
        "main": {"temp": 25.0, "humidity": 60},
        "weather": [{"description": "clear sky"}],
    }
    
    expected_data = {
        "city": "London",
        "country": "GB",
        "temperature": 25.0,
        "description": "clear sky",
        "humidity": 60,
    }
    
    assert parse_weather_response(mock_response) == expected_data

def test_build_weather_api_url():
    """Tests constructing the OpenWeather API URL."""
    city, country, api_key = "London", "GB", "test_key"
    expected_url = "http://api.openweathermap.org/data/2.5/weather?q=London,GB&appid=test_key&units=metric"
    assert build_weather_api_url(city, country, api_key) == expected_url


@patch("requests.get")
def test_fetch_weather_data_error(mock_get):
    """Tests making the API request and handling response errors."""
    mock_get.return_value.status_code = 404
    response, status_code = fetch_weather_data("fake_url")
    
    assert status_code == 404
    assert response["error"] == "City not found or invalid API request."
