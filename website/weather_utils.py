import requests
import re

def validate_city_and_country(city: str, country: str) -> bool:
    """Validates the city and country format."""
    if not city or not country:
        return False
    if not city.isalnum() or not re.match("^[a-zA-Z\\s]*$", city):
        return False
    if not re.match("^[A-Z]{2}$", country):
        return False
    return True

def build_weather_api_url(city: str, country: str, api_key: str) -> str:
    """Constructs the OpenWeather API URL."""
    return f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric"

def fetch_weather_data(url: str):
    """Makes the API request and handles response errors."""
    response = requests.get(url)

    if response.status_code == 400:
        return {"error": "Bad request, check parameters or API key."}, 400
    elif response.status_code == 401:
        return {"error": "Unauthorized, check your API key."}, 401
    elif response.status_code == 403:
        return {"error": "Forbidden, access denied."}, 403
    elif response.status_code == 404:
        return {"error": "City not found or invalid API request."}, 404
    elif response.status_code == 500:
        return {"error": "Internal server error, try again later."}, 500
    elif response.status_code == 503:
        return {"error": "Service unavailable, try again later."}, 503
    elif response.status_code != 200:
        return {"error": "An unknown error occurred. Please try again later."}, 418

    return response.json(), 200

def parse_weather_response(response_json):
    """Extracts relevant weather data from API response."""
    return {
        "city": response_json.get("name"),
        "country": response_json.get("sys", {}).get("country"),
        "temperature": response_json.get("main", {}).get("temp"),
        "description": response_json.get("weather", [{}])[0].get("description"),
        "humidity": response_json.get("main", {}).get("humidity"),
    }
