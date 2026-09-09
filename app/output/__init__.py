"""
app/output/__init__.py
"""
from .api import OutputMethod
from .laptop import LaptopSpeakerOutputMethod

__all__ = [
    "OutputMethod",
    "LaptopSpeakerOutputMethod"
]
