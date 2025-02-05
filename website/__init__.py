from flask import Flask
from dotenv import load_dotenv
import os
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["API_KEY"] = os.getenv("API_KEY")

    from .views import main_blueprint

    # Register blueprint for routes
    app.register_blueprint(main_blueprint)

    return app