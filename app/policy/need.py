"""
app/policy/need.py
"""
from datetime import datetime, timedelta

from app.policy.models import Need
from app.sensor import SensorReading


class NeedPolicy:
    """
    Flags when a sensor drifts outside its ideal range.
    Suppresses repeat alerts during cooldown.
    """
    def __init__(
            self,
            metric: str,
            min_value: float,
            max_value: float,
            cooldown: timedelta
        ):
        self._metric = metric
        self._min = min_value
        self._max = max_value
        self._cooldown = cooldown
        self._last_alerted: datetime | None = None

    def evaluate(self, reading: SensorReading) -> Need | None:
        """
        Evaluates if the reading is out of range and cooldown has elapsed
        
        :param SensorReading reading: sensors reading to evaluate
        :return Need | None: what the plant needs if anything
        """
        if self._in_range(reading.value):
            self._clear_cooldown()
            return None

        if self._is_cooling_down():
            return None

        self._start_cooldown()
        return Need(
            metric=self._metric,
            reading=reading,
            min_value=self._min,
            max_value=self._max
        )

    def _in_range(self, value: float) -> bool:
        return self._min <= value <= self._max

    def _is_cooling_down(self) -> bool:
        return (self._last_alerted is not None) and (datetime.now() - self._last_alerted < self._cooldown)

    def _start_cooldown(self) -> None:
        self._last_alerted = datetime.now()

    def _clear_cooldown(self) -> None:
        self._last_alerted = None
