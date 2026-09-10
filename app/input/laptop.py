"""
app/input/laptop.py
"""
from io import BytesIO

from faster_whisper import WhisperModel
from speech_recognition import Microphone, Recognizer, WaitTimeoutError

from app.input.api import InputMethod


class LaptopMicrophoneInputMethod(InputMethod):
    """
    Concrete `InputMethod` capturing user input via laptop microphone.
    Input transcribed locally using faster-whisper (FR-06).
    """
    def __init__(
            self,
            model_size: str = "base",
            phrase_time_limit: float = 5.0,
            timeout: float = 5.0
        ):
        self._model = WhisperModel(model_size, device="cpu", compute_type="int8")
        self._phrase_time_limit = phrase_time_limit
        self._timeout = timeout
        self._recogniser = Recognizer()
        self._microphone = Microphone(device_index=0)

    def capture(self):
        input("Press Enter, then ask the plant something...")

        with self._microphone as source:
            self._recogniser.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self._recogniser.listen(source, phrase_time_limit=self._phrase_time_limit)
            except WaitTimeoutError:
                return ""

        return self._transcribe(BytesIO(audio.get_wav_data()))
