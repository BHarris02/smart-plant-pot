"""
src/sensor/ada4026.py
"""
from __future__ import annotations
from datetime import datetime

# pylint: disable=import-error
import board
from adafruit_seesaw.seesaw import Seesaw

from src.sensor.api import Sensor
from src.sensor.models import SensorReading


class ADA4026SoilSensor(Sensor):
    """
    Concrete `Sensor` for reading raw soil moisture counts from an Adafruit
    STEMMA soil sensor (seesaw chip) over I2C
    """
    name = "ada4026_soil_sensor"

    def __init__(self, i2c: "board.I2C | None" = None, addr: int = 0x36):
        self._sensor = Seesaw(i2c or board.I2C(), addr=addr)

    def read(self) -> SensorReading:
        return SensorReading(
            value=float(self._sensor.moisture_read()),
            unit="raw_capacitive_count",
            read_at=datetime.now()
        )
