from unittest.mock import patch
from website.weather_utils import (
    validate_city_and_country,
    build_weather_api_url,
    fetch_weather_data,
    parse_weather_response,
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

    WEATHER_API_URL = build_weather_api_url(CITY, COUNTRY, API_KEY)
    assert validate_city_and_country(CITY, COUNTRY) == True
    
    expected_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY},{COUNTRY}&appid={API_KEY}&units=metric"
    assert WEATHER_API_URL == expected_url

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_weather_response
    response_data, status_code = fetch_weather_data(WEATHER_API_URL)
    assert status_code == 200
    assert response_data == mock_weather_response

    parsed_data = parse_weather_response(response_data)
    assert parsed_data["city"] == CITY
    assert parsed_data["country"] == COUNTRY
    assert parsed_data["temperature"] == 25.0
    assert parsed_data["description"] == "clear sky"
    assert parsed_data["humidity"] == 60

@patch("requests.get")
def test_get_weather_success(mock_get, mock_weather_response, client):
    """Test if get_weather returns correct data for a valid city and country."""
    
    # Mock the response from OpenWeather API
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_weather_response

    response = client.get("/weather?city=London&country=GB")
    assert response.status_code == 200
    
    data = response.get_json()
    assert data["city"] == "London"
    assert data["country"] == "GB"
    assert data["temperature"] == 25.0
    assert data["description"] == "clear sky"
    assert data["humidity"] == 60

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

@patch("requests.get")
def test_get_weather_invalid_country(mock_get, client):
    """Test if get_weather returns correct data for an invalid country code."""
    
    # Mock the response from OpenWeather API
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = {"error": "City not found or invalid API request."}

    response = client.get("/weather?city=London&country=XX")
    data = response.get_json()
    assert response.status_code == 404
    assert data["error"] == "City not found or invalid API request."

@patch("requests.get")
def test_get_weather_invalid_city(mock_get, client):
    """Test if get_weather returns correct data for an invalid city."""
    
    # Mock the response from OpenWeather API
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = {"error": "City not found or invalid API request."}

    response = client.get("/weather?city=Testtest&country=GB")
    data = response.get_json()
    assert response.status_code == 404
    assert data["error"] == "City not found or invalid API request."

@patch("requests.get")
def test_get_weather_bad_request(mock_get, client):
    """Test if get_weather returns correct data for a bad request (400)."""
    
    # Mock the response from OpenWeather API
    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = {"error": "Bad request, check parameters or API key."}

    response = client.get("/weather?city=London&country=GB")
    data = response.get_json()
    assert response.status_code == 400
    assert data["error"] == "Bad request, check parameters or API key."

@patch("requests.get")
def test_get_weather_unauthorized(mock_get, client):
    """Test if get_weather returns correct data for unauthorized (401)."""
    
    # Mock the response from OpenWeather API
    mock_get.return_value.status_code = 401
    mock_get.return_value.json.return_value = {"error": "Unauthorized, check your API key."}

    response = client.get("/weather?city=London&country=GB")
    data = response.get_json()
    assert response.status_code == 401
    assert data["error"] == "Unauthorized, check your API key."

@patch("requests.get")
def test_get_weather_forbidden(mock_get, client):
    """Test if get_weather returns correct data for forbidden access (403)."""
    
    # Mock the response from OpenWeather API
    mock_get.return_value.status_code = 403
    mock_get.return_value.json.return_value = {"error": "Forbidden, access denied."}

    response = client.get("/weather?city=London&country=GB")
    data = response.get_json()
    assert response.status_code == 403
    assert data["error"] == "Forbidden, access denied."


@patch("requests.get")
def test_get_weather_internal_server_error(mock_get, client):
    """Test if get_weather returns correct data for internal server error (500)."""
    
    # Mock the response from OpenWeather API
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {"error": "Internal server error, try again later."}

    response = client.get("/weather?city=London&country=GB")
    data = response.get_json()
    assert response.status_code == 500
    assert data["error"] == "Internal server error, try again later."

@patch("requests.get")
def test_get_weather_service_unavailable(mock_get, client):
    """Test if get_weather returns correct data for service unavailable (503)."""
    
    # Mock the response from OpenWeather API
    mock_get.return_value.status_code = 503
    mock_get.return_value.json.return_value = {"error": "Service unavailable, try again later."}

    response = client.get("/weather?city=London&country=GB")
    data = response.get_json()
    assert response.status_code == 503
    assert data["error"] == "Service unavailable, try again later."

@patch("requests.get")
def test_get_weather_unknown_error(mock_get, client):
    """Test if get_weather returns correct data for an unknown error."""
    
    # Mock the response from OpenWeather API for an unknown error
    mock_get.return_value.status_code = 418
    mock_get.return_value.json.return_value = {"error": "An unknown error occurred. Please try again later."}

    response = client.get("/weather?city=London&country=GB")
    data = response.get_json()
    assert response.status_code == 418
    assert data["error"] == "An unknown error occurred. Please try again later."