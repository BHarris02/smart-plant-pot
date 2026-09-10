"""
api/src/__init__.py
"""
from flask import Flask
from flask_injector import FlaskInjector

from src.blueprint import api_bp, api_spec
from src.config import FLASK_SECRET_KEY
from src.di import AppModule


def create_app() -> Flask:
    """
    Build and configure Flask application
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = FLASK_SECRET_KEY

    api_spec.register(app)
    app.register_blueprint(api_bp)

    FlaskInjector(app=app, modules=[AppModule])

    return app
