"""
src/__init__.py
"""
from flask import Flask
from flask_injector import FlaskInjector

from src.blueprint import api_spec, api_bp
from src.config import FLASK_SECRET_KEY
from src.module import LLMModule, OutputModule, SensorModule


def create_app() -> Flask:
    """
    Create and configure Flask app
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = FLASK_SECRET_KEY

    api_spec.register(app)
    app.register_blueprint(api_bp)

    FlaskInjector(app, modules=[LLMModule(), OutputModule(), SensorModule()])

    return app
