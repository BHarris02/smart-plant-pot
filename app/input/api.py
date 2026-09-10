"""
app/input/api.py
"""
from abc import ABC, abstractmethod

from requests import post, RequestException

from app.config import BACKEND_API_URL, BACKEND_API_TIMEOUT


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

    def _transcribe(self, wav_bytes: bytes) -> str:
        try:
            response = post(
                f"{BACKEND_API_URL}/transcribe",
                files={"file": ("audio.wav", wav_bytes, "audio/wav")},
                timeout=BACKEND_API_TIMEOUT,
            )
            response.raise_for_status()
        except RequestException:
            return ""

        return response.json().get("text", "")
