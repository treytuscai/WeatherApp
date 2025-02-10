import pytest
from unittest.mock import patch, MagicMock

from website.weather_utils import (
    validate_city_and_country,
    build_weather_api_url,
    fetch_weather_data,
    parse_weather_response,
    get_lat_lon_from_city
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

def test_parse_weather_response(mock_weather_response):
    """Test if weather data is correctly extracted from the OneCall API response."""
    parsed_data = parse_weather_response(mock_weather_response, 0, 0)
    assert parsed_data["temperature"] == 22

def test_build_weather_api_url():
    """Tests constructing the OpenWeather API URL."""
    city, country, api_key = "0", "0", "test_key"
    expected_url = "https://api.openweathermap.org/data/3.0/onecall?lat=0&lon=0&exclude=minutely,hourly&appid=test_key&units=metric"
    assert build_weather_api_url(city, country, api_key) == expected_url

@patch('requests.get')
def test_get_lat_lon_from_city(mock_get):
    """Test get_lat_lon_from_city without calling the API."""
    
    mock_response = MagicMock()
    mock_response.json.return_value = [{"lat": 51.5074, "lon": -0.1278}]
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    lat, lon = get_lat_lon_from_city("London", "GB", "fake_api_key")

    assert lat == 51.5074
    assert lon == -0.1278

@patch("requests.get")
def test_fetch_weather_data_error(mock_get):
    """Tests making the API request and handling response errors."""
    mock_get.return_value.status_code = 404
    response, status_code = fetch_weather_data("fake_url")
    
    assert status_code == 404
    assert response["error"] == "City not found or invalid API request."

@patch('requests.get')
def test_get_lat_lon_from_city_value_error(mock_get):
    """Test if ValueError is raised when no data is returned from the API."""
    
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_get.return_value = mock_response
    
    with pytest.raises(ValueError, match="Unable to fetch latitude and longitude"):
        get_lat_lon_from_city("London", "GB", "your_api_key")

@patch('requests.get')
def test_fetch_weather_data_500_error(mock_get):
    """Test if fetch_weather_data handles 500 error correctly."""

    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"error": "Internal server error, try again later."}
    mock_get.return_value = mock_response
    
    response_data, status_code = fetch_weather_data("http://api.openweathermap.org/data/2.5/weather?q=London&appid=your_api_key")
    assert status_code == 500
    assert response_data["error"] == "Internal server error, try again later."