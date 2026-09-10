"""
api/src/di.py
"""
from injector import Module, provider, singleton

from src.config import WHISPER_BASE_MODEL
from src.service import InputTranscriber


class AppModule(Module):
    """
    Application DI container
    """

    @provider
    @singleton
    def provide_input_transcriber(self) -> InputTranscriber:
        """
        Provide Whisper-backed `InputTranscriber`
        """
        return InputTranscriber(model_size=WHISPER_BASE_MODEL)
