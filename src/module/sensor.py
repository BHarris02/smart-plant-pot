"""
src/module/sensor.py
"""
from injector import Module, multiprovider, singleton

from src.sensor import Sensor
# temp: remove before packaging for production
from src.sensor import MockMoistureSensor, MockLightSensor


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
            MockLightSensor(),
            MockMoistureSensor()
        ]
