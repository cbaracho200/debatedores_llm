"""
Provider para Google Gemini.
"""
import os
from typing import Any, Optional
from llama_index.core.llms import LLM
from llama_index.core.embeddings import BaseEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from debatedores.providers.base import LLMProvider


class GeminiProvider(LLMProvider):
    """
    Provider para modelos Google Gemini.

    Suporta:
    - Gemini Pro, Gemini 2.5 Pro
    - text-embedding-004
    """

    DEFAULT_LLM_MODEL = "gemini-2.5-pro"
    DEFAULT_EMBEDDING_MODEL = "text-embedding-004"

    def __init__(
        self,
        api_key: Optional[str] = None,
        default_llm_model: Optional[str] = None,
        default_embedding_model: Optional[str] = None
    ):
        """
        Inicializa o provider Gemini.

        Args:
            api_key: API key do Google (usa GEMINI_API_KEY do env se None)
            default_llm_model: Modelo LLM padrão
            default_embedding_model: Modelo de embedding padrão
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.default_llm_model = default_llm_model or self.DEFAULT_LLM_MODEL
        self.default_embedding_model = default_embedding_model or self.DEFAULT_EMBEDDING_MODEL

    def get_llm(
        self,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs: Any
    ) -> LLM:
        """
        Retorna instância do Gemini LLM.

        Args:
            model_name: Nome do modelo Gemini
            temperature: Temperatura de geração
            **kwargs: Argumentos adicionais

        Returns:
            Instância configurada do Gemini LLM
        """
        model = model_name or self.default_llm_model
        return GoogleGenAI(
            model=model,
            temperature=temperature,
            api_key=self.api_key,
            **kwargs
        )

    def get_embeddings(
        self,
        model_name: Optional[str] = None,
        **kwargs: Any
    ) -> BaseEmbedding:
        """
        Retorna instância do Gemini Embedding.

        Args:
            model_name: Nome do modelo de embedding
            **kwargs: Argumentos adicionais

        Returns:
            Instância configurada do Gemini Embedding
        """
        model = model_name or self.default_embedding_model
        return GoogleGenAIEmbedding(
            model=model,
            api_key=self.api_key,
            **kwargs
        )

    def get_provider_name(self) -> str:
        """Retorna 'gemini'."""
        return "gemini"

    def validate_config(self) -> bool:
        """
        Valida se a API key está configurada.

        Returns:
            True se a API key está disponível
        """
        return self.api_key is not None and len(self.api_key) > 0


__all__ = ["GeminiProvider"]
