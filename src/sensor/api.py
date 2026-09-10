"""
app/sensor/api.py
"""
from abc import ABC, abstractmethod

from src.sensor.models import SensorReading


class Sensor(ABC):
    """
    Abstract base class for sensors
    """
    name: str

    @abstractmethod
    def read(self) -> SensorReading:
        """
        Read the sensor's current value
        
        :return SensorReading: data read by sensor
        """
        raise NotImplementedError("Trying to use abstract `Sensor` as a concrete class")
