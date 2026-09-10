"""
app/output/__init__.py
"""
from .api import OutputMethod
# temp: remove before packaging for production
from .laptop import LaptopSpeakerOutputMethod

__all__ = [
    "OutputMethod",
    # temp: remove before packaging for production
    "LaptopSpeakerOutputMethod"
]
