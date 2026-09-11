"""
src/__init__.py
"""
from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector

from src.blueprint import api_spec, api_bp
from src.config import CORS_ORIGIN, FLASK_SECRET_KEY, MAX_CONTENT_LENGTH
from src.module import LLMModule, OutputModule, SensorModule


def create_app() -> Flask:
    """
    Create and configure Flask app
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = FLASK_SECRET_KEY
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

    CORS(app, origins=CORS_ORIGIN)  # phone-browser SPA is a cross-origin client

    api_spec.register(app)
    app.register_blueprint(api_bp)

    FlaskInjector(app, modules=[LLMModule(), OutputModule(), SensorModule()])

    return app
