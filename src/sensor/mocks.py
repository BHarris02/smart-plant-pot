"""
src/sensor/mocks.py
"""
from datetime import datetime
from random import uniform

from src.sensor.api import Sensor
from src.sensor.models import SensorReading


class MockLightSensor(Sensor):
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


class MockMoistureSensor(Sensor):
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
