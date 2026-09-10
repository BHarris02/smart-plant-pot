"""
src/output/laptop.py
"""
import pyttsx3

from src.output.api import OutputMethod


class LaptopSpeakerOutputMethod(OutputMethod):
    """
    Concrete `OutputMethod` that speaks text aloud via laptop speakers.
    Uses pyttsx3 (free, local, offline, FR-05)
    """
    def __init__(self, rate: int = 175):
        self._engine = pyttsx3.init()
        self._engine.setProperty("rate", rate)

    def answer_or_express(self, content: str) -> None:
        self._engine.say(content)
        self._engine.runAndWait()
