"""
app/input/api.py
"""
from abc import ABC, abstractmethod


class InputMethod(ABC):
    """
    Abstract base class for input, i.e asking the plant a question
    """
    @abstractmethod
    def capture(self) -> str:
        """
        Get user input. Blocks until a question is asked

        :return str: user's question as text
        """
        raise NotImplementedError("Trying to use abstract `InputMethod` as a concrete class")
