from flask import Blueprint, render_template, jsonify
from flask import request

# Create a blueprint
main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/', methods=['GET', 'POST'])
def weather():
    return render_template('index.html')

@main_blueprint.route("/weather", methods=["GET"])
def get_weather():
    return jsonify({"temperature": 25, "unit": "C"})