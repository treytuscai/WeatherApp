# conftest.py
import pytest
from app import app  # Import your app or necessary setup

@pytest.fixture
def client():
    """Create a test client for Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_weather_response():
    """Mock OpenWeather API response."""
    return {
        "name": "London",
        "sys": {"country": "GB"},
        "main": {"temp": 25.0, "humidity": 60},
        "weather": [{"description": "clear sky"}]
    }
