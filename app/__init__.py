"""
app/__init__.py
"""
from app.config import (
    LLM_API_KEY,
    LLM_BASE_URL,
    LLM_MODEL,
    LLM_TIMEOUT,
    LLM_MAX_TOKENS
)
from app.input import LaptopMicrophoneInputMethod
from app.llm import AnthropicClient
from app.output import LaptopSpeakerOutputMethod
from app.sensor import LightSensor, MoistureSensor, build_sensor_summary


class SmartPlantPotApplication:
    """
    Application orchestrator
    """
    def __init__(self):
        self._input = LaptopMicrophoneInputMethod()
        self._sensors = [LightSensor(), MoistureSensor()]
        self._llm = AnthropicClient(
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL,
            model=LLM_MODEL,
            timeout=LLM_TIMEOUT,
            max_tokens=LLM_MAX_TOKENS
        )
        self._output = LaptopSpeakerOutputMethod()

        self._llm.answer("Hello, how are you?", "No summary")

    def run(self) -> None:
        """
        Run the smart plant pot application
        """
        print("Plant pot ready. Press Ctrl+C to quit\n")
        while True:
            try:
                self._handle_question()
            except KeyboardInterrupt:
                print("Goodbye!")
                break

    def _handle_question(self) -> None:
        user_question = self._input.capture()
        if not user_question.strip():
            self._output.answer_or_express("Sorry, I didn't catch that.")
            return

        sensor_summary = build_sensor_summary(self._sensors)
        plant_output = self._llm.answer(user_question, sensor_summary)
        self._output.answer_or_express(plant_output.content)
