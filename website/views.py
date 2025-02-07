"""This module contains endpoints for the weather app."""
import os
from flask import Blueprint, render_template, jsonify
from flask import request
from website.weather_utils import (
    validate_city_and_country,
    build_weather_api_url,
    fetch_weather_data,
    parse_weather_response,
    get_lat_lon_from_city
)

# Create a blueprint
main_blueprint = Blueprint('main', __name__)

API_KEY = os.getenv("API_KEY")

@main_blueprint.route('/', methods=['GET', 'POST'])
def weather():
    """Endpoint to get main page."""
    return render_template('index.html')

@main_blueprint.route('/weather', methods=['GET'])
def get_weather():
    """Endpoint to get weather data based on city and country."""
    city = request.args.get('city')
    country = request.args.get('country')

    if not validate_city_and_country(city, country):
        return jsonify({"error": "Invalid city or country format."}), 400

    try:
        lat, lon = get_lat_lon_from_city(city, country, API_KEY)
    except ValueError:
        return jsonify({"error": "City not found or invalid API request."}), 404

    url = build_weather_api_url(lat, lon, API_KEY)
    response_data, status_code = fetch_weather_data(url)

    if status_code != 200:
        return jsonify(response_data), status_code
    weather_info = parse_weather_response(response_data, lat, lon)
    return jsonify(weather_info)
