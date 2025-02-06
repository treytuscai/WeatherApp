# conftest.py
import sys
import os
import pytest

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
    return {
        "name": "London",
        "sys": {"country": "GB"},
        "main": {"temp": 25.0, "humidity": 60},
        "weather": [{"description": "clear sky"}]
    }
