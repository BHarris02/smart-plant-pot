"""
app/input/__init__.py
"""
from .api import InputMethod
from .laptop import LaptopMicrophoneInputMethod

__all__ = [
    "InputMethod",
    "LaptopMicrophoneInputMethod"
]
