import pytest
from app import app  # Import Flask app

@pytest.fixture
def client():
    """Create a test client for Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_weather_endpoint(client):
    """Test Flask API endpoint for fetching weather."""
    response = client.get("/weather/London")
    assert response.status_code == 200
    assert "temperature" in response.get_json()

def test_weather_endpoint_invalid_city(client):
    """Test endpoint with an invalid city."""
    response = client.get("/weather/InvalidCity")
    assert response.status_code == 404