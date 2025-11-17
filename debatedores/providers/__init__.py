"""
Providers de LLM para o framework Debatedores.

Este módulo fornece abstrações para diferentes providers de LLM,
permitindo fácil integração e troca entre providers.
"""
from debatedores.providers.base import LLMProvider
from debatedores.providers.openai import OpenAIProvider
from debatedores.providers.gemini import GeminiProvider

__all__ = [
    "LLMProvider",
    "OpenAIProvider",
    "GeminiProvider",
]
