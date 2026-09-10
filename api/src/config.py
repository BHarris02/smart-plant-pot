"""
api/src/config.py
"""
from os import getenv

from dotenv import load_dotenv


load_dotenv()


class MissingEnvironmentVariablesException(Exception):
    """
    Thrown when environment variables are not set
    """


# flask config
FLASK_ENV = getenv("FLASK_ENV", "prod").lower()
FLASK_SECRET_KEY = getenv("FLASK_SECRET_KEY")

if not FLASK_SECRET_KEY:
    raise MissingEnvironmentVariablesException("Flask secret key is not set in environment")

# whisper config
WHISPER_BASE_MODEL = getenv("WHISPER_BASE_MODEL", "base").lower()
