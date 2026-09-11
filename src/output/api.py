"""
src/output/api.py
"""
from abc import ABC, abstractmethod


class OutputMethod(ABC):
    """
    Abstract base class for output, i.e.:
    - the plant responding to a question
    - the plant expressing a need
    """
    @abstractmethod
    def answer_or_express(self, content: str) -> None:
        """
        Answer a question or express a need
        """
        raise NotImplementedError("Trying to use abstract `OutputMethod` as a concrete class")
