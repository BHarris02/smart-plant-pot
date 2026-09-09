"""
app/sensor/moisture.py
"""
from datetime import datetime
from random import uniform

from app.sensor.api import Sensor
from app.sensor.models import SensorReading


class MoistureSensor(Sensor):
    """
    Concrete `Sensor` for providing mock soil moisture readings
    """
    name = "mock_moisture_sensor"

    def read(self) -> SensorReading:
        return SensorReading(
            value=round(uniform(10, 90), 1),
            unit="pct",
            read_at=datetime.now()
        )
