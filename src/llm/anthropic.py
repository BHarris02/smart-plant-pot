"""
src/llm/anthropic.py
"""
from anthropic import Anthropic

from src.llm.api import LLMClient
from src.llm.prompts import SYSTEM_PROMPT
from src.llm.schemas import PlantOutput


class AnthropicClient(LLMClient):
    """
    Concrete, Anthropic-backed `LLMClient`
    """
    def __init__(
            self,
            api_key: str,
            base_url: str,
            model: str,
            timeout: float,
            max_tokens: int
        ):
        self._client = Anthropic(api_key=api_key, base_url=base_url, timeout=timeout)
        self._model = model
        self._max_tokens = max_tokens

    def answer(self, question: str, sensor_summary: str) -> PlantOutput:
        return self._client.messages.parse(
            max_tokens=self._max_tokens,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"{question}\n\nCurrent sensor readings: \n{sensor_summary}"
                }
            ],
            model=self._model,
            output_format=PlantOutput
        ).parsed_output
