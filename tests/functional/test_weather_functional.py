from unittest.mock import patch, MagicMock
from website.weather_utils import (
    validate_city_and_country,
    build_weather_api_url,
    fetch_weather_data,
    parse_weather_response,
    get_lat_lon_from_city
)

def test_home_page(client):
    """Tests empty home page"""
    response = client.get('/')
    assert response.status_code == 200

@patch("requests.get")
def test_weather_utils(mock_get, mock_weather_response):
    """Tests integrating all helper functions."""
    API_KEY = "test_api_key"
    CITY = "London"
    COUNTRY = "GB"

    # Validate city and country
    assert validate_city_and_country(CITY, COUNTRY) == True

    # Get lat and lon from city and country
    lat, lon = get_lat_lon_from_city(CITY, COUNTRY, API_KEY)

    # Build the weather API URL using lat and lon
    WEATHER_API_URL = build_weather_api_url(lat, lon, API_KEY)

    # Update the expected URL to use lat and lon (one call API)
    expected_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&appid={API_KEY}&units=metric"
    assert WEATHER_API_URL == expected_url

    # Mock the response from the API
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_weather_response
    
    # Fetch weather data using the API URL
    response_data, status_code = fetch_weather_data(WEATHER_API_URL)

    # Assert that the status code is 200 and response matches the mock data
    assert status_code == 200
    assert response_data == mock_weather_response

    # Parse the weather data
    parsed_data = parse_weather_response(response_data)

    # Test the parsed data
    assert parsed_data["temperature"] == None
    assert parsed_data["feels_like"] == None
    assert parsed_data["pressure"] == None
    assert parsed_data["humidity"] == None
    assert parsed_data["wind_speed"] == None
    assert parsed_data["visibility"] == None
    assert parsed_data["clouds"] == None
    assert parsed_data["description"] == None
    assert parsed_data["detailed_description"] == None
    assert parsed_data["icon"] == None
    assert parsed_data["sunrise"] == None
    assert parsed_data["sunset"] == None
    assert parsed_data["dew_point"] == None


def test_get_weather_missing_city(client):
    """Test if get_weather returns correct data for a missing city."""

    response = client.get("/weather?country=GB")
    data = response.get_json()
    assert response.status_code == 400
    assert data["error"] == "Invalid city or country format."

def test_get_weather_missing_country(client):
    """Test if get_weather returns correct data for a missing country."""

    response = client.get("/weather?city=London")
    data = response.get_json()
    assert response.status_code == 400
    assert data["error"] == "Invalid city or country format."

def test_get_weather_invalid_country_format(client):
    """Test if get_weather returns correct data for an invalid country format."""

    response = client.get("/weather?city=London&country=test")
    data = response.get_json()
    assert response.status_code == 400
    assert data["error"] == "Invalid city or country format."

def test_get_weather_invalid_city_format(client):
    """Test if get_weather returns correct data for an invalid city format."""

    response = client.get("/weather?city=123&country=GB")
    data = response.get_json()
    assert response.status_code == 400
    assert data["error"] == "Invalid city or country format."


@patch('requests.get')
def test_fetch_weather_data_failure(mock_get):
    """Test if fetch_weather_data handles 500 error correctly."""

    mock_response = MagicMock()
    mock_response.status_code = 405
    mock_response.json.return_value = {"error": "An unknown error occurred. Please try again later."}
    mock_get.return_value = mock_response
    
    response_data, status_code = fetch_weather_data("http://api.openweathermap.org/data/2.5/weather?q=London&appid=your_api_key")
    assert status_code == 418
    assert response_data["error"] == "An unknown error occurred. Please try again later."

@patch('website.weather_utils.get_lat_lon_from_city')
@patch('website.weather_utils.fetch_weather_data')
def test_get_weather(mock_fetch_weather_data, mock_get_lat_lon_from_city, client):
    mock_get_lat_lon_from_city.return_value = (51.5074, -0.1278)
    mock_fetch_weather_data.return_value = ({"name": "London", "temp": 22, "description": "Clear sky"}, 200)
    response = client.get('/weather?city=London&country=GB')
    assert response.status_code == 200
    data = response.get_json()
    assert data['clouds'] == 40

@patch('website.weather_utils.get_lat_lon_from_city')
def test_get_weather_value_error(mock_get_lat_lon_from_city, client):
    mock_get_lat_lon_from_city.side_effect = ValueError
    response = client.get('/weather?city=London&country=XX')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'City not found or invalid API request.'