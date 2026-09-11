"""
src/sensor/bh1750.py
"""
from datetime import datetime

# pylint: disable=import-error
import adafruit_bh1750
import board

from src.sensor.api import Sensor
from src.sensor.models import SensorReading


class BH1750LightSensor(Sensor):
    """
    Concrete `Sensor` for reading ambient light from a BH1750 sensor over I2C
    """
    name = "bh1750_light_sensor"

    def __init__(self, i2c: board.I2C | None = None):
        self._sensor = adafruit_bh1750.BH1750(i2c or board.I2C())

    def read(self) -> SensorReading:
        return SensorReading(
            value=self._sensor.lux,
            unit="lux",
            read_at=datetime.now()
        )
