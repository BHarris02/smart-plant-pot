"""
src/module/sensor.py
"""
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
        return [
            BH1750LightSensor(),
            ADA4026SoilSensor()
        ]
