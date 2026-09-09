"""
app/sensor/utils.py
"""
from app.sensor.api import Sensor


def build_sensor_summary(sensors: list[Sensor]) -> str:
    """
    Read all sensors and format their current values as one line per sensor
    """
    lines = (
        f"{sensor.name}: {sensor.read().value} {sensor.read().unit}"
        for sensor in sensors
    )
    return "\n".join(lines)
