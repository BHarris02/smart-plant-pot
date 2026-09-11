"""
src/module/sensor.py
"""
# pylint: disable=import-error
import board
from injector import Module, multiprovider, singleton

from src.sensor import Sensor, ADA4026SoilSensor, BH1750LightSensor


class SensorModule(Module):
    """
    DI module for `Sensor`s
    """
    @multiprovider
    @singleton
    def provide_all_sensors(self) -> list[Sensor]:
        """
        Provide concrete `Sensor`s for all metrics
        """
        i2c = board.I2C()  # shared bus: both sensors sit on the same SDA/SCL pair
        return [
            BH1750LightSensor(i2c=i2c),
            ADA4026SoilSensor(i2c=i2c)
        ]
