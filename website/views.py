from flask import Blueprint, render_template, jsonify
from flask import request
import os
from website.weather_utils import (
    validate_city_and_country,
    build_weather_api_url,
    fetch_weather_data,
    parse_weather_response
)

# Create a blueprint
main_blueprint = Blueprint('main', __name__)

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@main_blueprint.route('/', methods=['GET', 'POST'])
def weather():
    return render_template('index.html')

@main_blueprint.route('/weather', methods=['GET'])
def get_weather():
    """Endpoint to get weather data based on city and country."""
    city = request.args.get('city')
    country = request.args.get('country')

    if not validate_city_and_country(city, country):
        return jsonify({"error": "Invalid city or country format."}), 400

    url = build_weather_api_url(city, country, API_KEY)
    response_data, status_code = fetch_weather_data(url)

    if status_code != 200:
        return jsonify(response_data), status_code

    weather_info = parse_weather_response(response_data)
    return jsonify(weather_info)

