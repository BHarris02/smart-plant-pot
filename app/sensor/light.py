"""
app/sensor/light.py
"""
from datetime import datetime
from random import uniform

from app.sensor.api import Sensor
from app.sensor.models import SensorReading


class LightSensor(Sensor):
    """
    Concrete `Sensor` for providing mock light readings
    """
    name = "mock_light_sensor"

    def read(self) -> SensorReading:
        return SensorReading(
            value=round(uniform(50, 2000), 1),
            unit="lux",
            read_at=datetime.now()
        )
