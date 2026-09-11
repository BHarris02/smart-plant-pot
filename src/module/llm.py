"""
src/module/llm.py
"""
from injector import Module, provider, singleton

from src.config import (
    LLM_API_KEY,
    LLM_BASE_URL,
    LLM_MODEL,
    LLM_TIMEOUT,
    LLM_MAX_TOKENS
)
from src.llm import LLMClient, AnthropicClient

class LLMModule(Module):
    """
    DI module for `LLMClient`s
    """
    @provider
    @singleton
    def provide_llm_client(self) -> LLMClient:
        """
        Provide a concrete `LLMClient`
        """
        return AnthropicClient(
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL,
            model=LLM_MODEL,
            timeout=LLM_TIMEOUT,
            max_tokens=LLM_MAX_TOKENS
        )
