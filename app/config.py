"""
app/config.py
"""
from os import getenv

from dotenv import load_dotenv


load_dotenv()

# plant config
PLANT_NAME = getenv("PLANT_NAME", "Planty McPlantface")
PLANT_SPECIES = getenv("PLANT_SPECIES", "unknown")
PLANT_PERSONALITY = getenv("PLANT_PERSONALITY", "warm and friendly")

LIGHT_MIN = float(getenv("LIGHT_MIN") or "50.0")
LIGHT_MAX = float(getenv("LIGHT_MAX") or "2000.0")

MOISTURE_MIN = float(getenv("MOISTURE_MIN") or "10.0")
MOISTURE_MAX = float(getenv("MOISTURE_MAX") or "90.0")


class MissingEnvironmentVariablesException(Exception):
    """
    Thrown when environment variables are missing
    """


# llm config
LLM_API_KEY = getenv("LLM_API_KEY")
LLM_MODEL = getenv("LLM_MODEL")
LLM_TIMEOUT = float(getenv("LLM_TIMEOUT") or "10.0")
LLM_MAX_TOKENS = int(getenv("LLM_MAX_TOKENS") or "1024")

if not all([LLM_API_KEY, LLM_MODEL]):
    raise MissingEnvironmentVariablesException("Some environment variables are not set")
