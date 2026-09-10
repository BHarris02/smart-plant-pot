"""
src/sensor/models.py
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SensorReading:
    """
    Models the data read by a sensor
    """
    value: float
    unit: str
    read_at: datetime
