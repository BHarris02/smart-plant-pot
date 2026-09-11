"""
app/output/__init__.py
"""
from .api import OutputMethod
from .pi import PiSpeakerOutputMethod

__all__ = [
    "OutputMethod",
    "PiSpeakerOutputMethod"
]
