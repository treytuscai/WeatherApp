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

@patch('website.views.get_lat_lon_from_city')
@patch('requests.get') 
def test_get_weather(mock_get, mock_get_lat_lon_from_city, client, mock_weather_response):
    """Test /weather endpoint with mocked API responses."""

    mock_get_lat_lon_from_city.return_value = (51.5074, -0.1278)
    mock_response = MagicMock()
    mock_response.json.return_value = mock_weather_response
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    response = client.get('/weather?city=London&country=GB')
    assert response.status_code == 200
    data = response.get_json()
    assert data["temperature"] == 22
    assert data["description"] == "Clear"
    assert data["humidity"] == 60

@patch('website.views.get_lat_lon_from_city')
@patch('requests.get') 
def test_get_weather_server_error(mock_get, mock_get_lat_lon_from_city, client, mock_weather_response):
    """Test /weather endpoint with mocked API responses."""

    mock_get_lat_lon_from_city.return_value = (51.5074, -0.1278)
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    response = client.get('/weather?city=London&country=GB')
    assert response.status_code == 500

@patch('website.views.get_lat_lon_from_city') 
def test_get_weather_city_not_found(mock_get_lat_lon_from_city, client):
    """Test /weather endpoint with mocked API responses."""
    
    mock_get_lat_lon_from_city.side_effect = ValueError("City not found")
    response = client.get('/weather?city=London&country=GB')
    assert response.status_code == 404
    assert response.json == {"error": "City not found or invalid API request."}

@patch('website.views.get_lat_lon_from_city')
@patch('requests.get') 
def test_get_weather_unknown_error(mock_get, mock_get_lat_lon_from_city, client, mock_weather_response):
    """Test /weather endpoint with mocked API responses."""

    mock_get_lat_lon_from_city.return_value = (51.5074, -0.1278)
    mock_response = MagicMock()
    mock_response.status_code = 405
    mock_get.return_value = mock_response

    response = client.get('/weather?city=London&country=GB')
    assert response.status_code == 418


@patch('website.views.get_lat_lon_from_city')
@patch('requests.get') 
def test_get_weather_forbidden(mock_get, mock_get_lat_lon_from_city, client, mock_weather_response):
    """Test /weather endpoint with mocked API responses."""

    mock_get_lat_lon_from_city.return_value = (51.5074, -0.1278)
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_get.return_value = mock_response

    response = client.get('/weather?city=London&country=GB')
    assert response.status_code == 403
