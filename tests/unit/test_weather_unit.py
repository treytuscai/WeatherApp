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

def test_parse_weather_response():
    """Test if weather data is correctly extracted from the OneCall API response."""
    mock_response = {
        "current": {
            "temp": 25.0,
            "feels_like": 23.0,
            "pressure": 1015,
            "humidity": 70,
            "wind_speed": 5.0,
            "visibility": 10000,
            "clouds": 40,
            "weather": [
                {
                    "main": "Clear",
                    "icon": "01d"
                }
            ],
            "sunrise": 1684926645,
            "sunset": 1684977332,
            "dew_point": 20.0
        },
        "daily": [
            {
                "summary": "Clear sky with no significant changes in the weather."
            }
        ]
    }

    expected_data = {
        "temperature": 25.0,
        "feels_like": 23.0,
        "pressure": 1015,
        "humidity": 70,
        "wind_speed": 5.0,
        "visibility": 10000,
        "clouds": 40,
        "description": "Clear",
        "detailed_description": "Clear sky with no significant changes in the weather.",
        "icon": "01d",
        "sunrise": 1684926645,
        "sunset": 1684977332,
        "dew_point": 20.0
    }

    parsed_data = parse_weather_response(mock_response)

    # Assert that the parsed data matches the expected data
    assert parsed_data["temperature"] == expected_data["temperature"]
    assert parsed_data["feels_like"] == expected_data["feels_like"]
    assert parsed_data["pressure"] == expected_data["pressure"]
    assert parsed_data["humidity"] == expected_data["humidity"]
    assert parsed_data["wind_speed"] == expected_data["wind_speed"]
    assert parsed_data["visibility"] == expected_data["visibility"]
    assert parsed_data["clouds"] == expected_data["clouds"]
    assert parsed_data["description"] == expected_data["description"]
    assert parsed_data["detailed_description"] == expected_data["detailed_description"]
    assert parsed_data["icon"] == expected_data["icon"]
    assert parsed_data["sunrise"] == expected_data["sunrise"]
    assert parsed_data["sunset"] == expected_data["sunset"]
    assert parsed_data["dew_point"] == expected_data["dew_point"]


def test_build_weather_api_url():
    """Tests constructing the OpenWeather API URL."""
    city, country, api_key = "0", "0", "test_key"
    expected_url = "https://api.openweathermap.org/data/3.0/onecall?lat=0&lon=0&exclude=minutely,hourly&appid=test_key&units=metric"
    assert build_weather_api_url(city, country, api_key) == expected_url


@patch("requests.get")
def test_fetch_weather_data_error(mock_get):
    """Tests making the API request and handling response errors."""
    mock_get.return_value.status_code = 404
    response, status_code = fetch_weather_data("fake_url")
    
    assert status_code == 404
    assert response["error"] == "City not found or invalid API request."
