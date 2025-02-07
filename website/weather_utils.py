import requests
import re

def validate_city_and_country(city: str, country: str) -> bool:
    """Validates the city and country format, allowing spaces in city names."""
    if not city or not country:
        return False
    # Allow only letters and spaces in the city name.
    if not re.fullmatch(r"[A-Za-z\s]+", city):
        return False
    # Country must be exactly two uppercase letters.
    if not re.fullmatch(r"[A-Z]{2}", country):
        return False
    return True

def get_lat_lon_from_city(city: str, country: str, api_key: str) -> tuple:
    """Fetches latitude and longitude for a city and country."""
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&limit=1&appid={api_key}"
    response = requests.get(geo_url)
    data = response.json()
    if data:
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        return lat, lon
    else:
        raise ValueError("Unable to fetch latitude and longitude")

def build_weather_api_url(lat: float, lon: float, api_key: str, exclude: str = "minutely,hourly") -> str:
    """Constructs the OpenWeather OneCall API URL using latitude and longitude."""
    return f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={api_key}&units=metric"

def fetch_weather_data(url: str):
    """Makes the API request and handles response errors."""
    response = requests.get(url)

    if response.status_code == 404:
        return {"error": "City not found or invalid API request."}, 404
    elif response.status_code == 403:
        return {"error": "Forbidden API request."}, 403
    elif response.status_code == 500:
        return {"error": "Internal server error, try again later."}, 500
    elif response.status_code != 200:
        return {"error": "An unknown error occurred. Please try again later."}, 418

    return response.json(), 200

def parse_weather_response(response_json):
    """Extracts relevant weather data from the OneCall API response."""
    current_weather = response_json.get("current", {})
    daily = response_json.get("daily", [{}])[0]
    weather = current_weather.get("weather", [{}])[0]

    return {
        "temperature": current_weather.get("temp"),
        "feels_like": current_weather.get("feels_like"),
        "pressure": current_weather.get("pressure"),
        "humidity": current_weather.get("humidity"),
        "wind_speed": current_weather.get("wind_speed"),
        "visibility": current_weather.get("visibility"),
        "clouds": current_weather.get("clouds"),
        "description": weather.get("main"),
        "detailed_description": daily.get("summary"),
        "icon": weather.get("icon"),
        "sunrise": current_weather.get("sunrise"),
        "sunset": current_weather.get("sunset"),
        "dew_point": current_weather.get("dew_point"),
    }


