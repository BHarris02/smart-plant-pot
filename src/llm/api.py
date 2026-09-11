"""
app/llm/api.py
"""
from abc import ABC, abstractmethod

from src.llm.schemas import PlantOutput


class LLMClient(ABC):
    """
    Abstract base class for generating a plant's output grounded in sensor data.
    E.g. plant answering a question or expressing a need
    """
    @abstractmethod
    def answer(
        self,
        question: str,
        sensor_summary: str,
        image: str | None = None
    ) -> PlantOutput:
        """
        Generate a sensor-grounded answer to a given question

        :param str question: question asked by user
        :param str sensor_summary: latest readings per sensor name, formatted as text
        :param str | None image: optional base64-encoded photo of the plant
        :return PlantOutput: the plant's answer
        """
        raise NotImplementedError("Trying to use abstract `LLMClient` as a concrete class")
