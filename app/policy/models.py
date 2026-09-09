"""
app/policy/models.py
"""
from dataclasses import dataclass

from app.sensor import SensorReading


@dataclass(frozen=True)
class Need:
    """
    Models a plant's need
    """
    metric: str
    reading: SensorReading
    min_value: float
    max_value: float
