import pytest
import requests
from unittest.mock import patch
from weather import get_weather  # Import the function to test

@pytest.fixture
def mock_weather_response():
    """Mock OpenWeather API response."""
    return {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 25.0, "humidity": 60},
        "name": "London"
    }

@patch("requests.get")
def test_get_weather_success(mock_get, mock_weather_response):
    """Test if get_weather returns correct data for a valid city."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_weather_response

    result = get_weather("London")
    assert result["name"] == "London"
    assert result["main"]["temp"] == 25.0
    assert result["weather"][0]["description"] == "clear sky"

@patch("requests.get")
def test_get_weather_api_error(mock_get):
    """Test API error handling (e.g., invalid API key)."""
    mock_get.return_value.status_code = 401
    mock_get.return_value.json.return_value = {"cod": 401, "message": "Invalid API key"}

    result = get_weather("London")
    assert "error" in result
    assert "401" in result["error"]
