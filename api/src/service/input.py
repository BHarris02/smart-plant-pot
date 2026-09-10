"""
api/src/service/input.py
"""
from io import BytesIO

from faster_whisper import WhisperModel


class InputTranscriber:
    """
    Whisper-backed input transcriber
    """
    def __init__(self, model_size: str):
        self._model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def transcribe(self, audio_bytes: bytes) -> tuple:
        """
        Transcribe audio from raw audio bytes
        """
        if not audio_bytes:
            return ""

        try:
            segments, _ = self._model.transcribe(BytesIO(audio_bytes))
        # pylint: disable=broad-exception-caught
        except Exception:
            return ""

        return "".join(segment.text for segment in segments).strip()
