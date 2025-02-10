# conftest.py
import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Pytest Coverage Fix
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from website import create_app

@pytest.fixture(scope='module')
def client():
    """Create a test client for Flask app."""
    flask_app = create_app()
    with flask_app.test_client() as client:
        yield client

@pytest.fixture(scope='module')
def mock_weather_response():
    """Mock OpenWeather API response."""
    return { "current": {
            "temp": 22,
            "feels_like": 21,
            "pressure": 1012,
            "humidity": 60,
            "wind_speed": 5.2,
            "visibility": 10000,
            "clouds": 40,
            "sunrise": 1625034900,
            "sunset": 1625088900,
            "dew_point": 15,
            "weather": [{"main": "Clear", "icon": "01d"}],
            },
            "daily": [{"summary": "Sunny all day."}]
            }

@pytest.fixture
def mock_lat_lon_response():
    return {"lat": 51.5074, "lon": -0.1278}
