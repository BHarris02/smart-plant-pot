"""
app/polling/events.py
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class QuestionEvent:
    question: str


@dataclass(frozen=True)
class SensorCheckEvent:
    pass
