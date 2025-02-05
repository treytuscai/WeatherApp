import pytest
from unittest.mock import patch
from flask import Flask
from weather import get_weather
from app import app

@pytest.fixture
def mock_weather_response():
    """Mock OpenWeather API response."""
    return {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 25.0, "humidity": 60},
        "name": "London"
    }

@pytest.fixture
def client():
    """Create a test client for Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("requests.get")
def test_get_weather_success(mock_get, mock_weather_response, client):
    """Test if get_weather returns correct data for a valid city."""
    # Mock the response from OpenWeather API
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_weather_response

    response = client.get("/weather/London")
    assert response.status_code == 200
    data = response.get_json()
    assert data["temperature"] == 25.0
    assert data["unit"] == "C"

@patch("requests.get")
def test_get_weather_api_error(mock_get, client):
    """Test API error handling (e.g., invalid city)."""
    # Mock the response for an invalid city
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = {"error": "City not found"}

    response = client.get("/weather/InvalidCity")
    assert response.status_code == 404
