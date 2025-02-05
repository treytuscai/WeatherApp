from flask import Blueprint, render_template, jsonify
from flask import request
import requests
import os

# Create a blueprint
main_blueprint = Blueprint('main', __name__)

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@main_blueprint.route('/', methods=['GET', 'POST'])
def weather():
    return render_template('index.html')

@main_blueprint.route("/weather/<city>", methods=["GET"])
def get_weather(city):

    params = {
        "q": city,  # City
        "appid": API_KEY,  # API Key
        "units": "metric"  # Celsius 
    }

    response = requests.get(BASE_URL, params=params)

    # If API call was successful
    if response.status_code == 200:
        data = response.json()
        # Extract weather data
        temperature = data["main"]["temp"]
        unit = "C"
        return jsonify({"temperature": temperature, "unit": unit})
    else:
        return jsonify({"error": "City not found"}), 404
