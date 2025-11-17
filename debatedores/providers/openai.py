"""
Provider para OpenAI (GPT models).
"""
import os
from typing import Any, Optional
from llama_index.core.llms import LLM
from llama_index.core.embeddings import BaseEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from debatedores.providers.base import LLMProvider


class OpenAIProvider(LLMProvider):
    """
    Provider para modelos OpenAI GPT e embeddings.

    Suporta:
    - GPT-4, GPT-3.5, GPT-5
    - text-embedding-3-small, text-embedding-3-large
    """

    DEFAULT_LLM_MODEL = "gpt-5.1-2025-11-13"
    DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"

    def __init__(
        self,
        api_key: Optional[str] = None,
        default_llm_model: Optional[str] = None,
        default_embedding_model: Optional[str] = None
    ):
        """
        Inicializa o provider OpenAI.

        Args:
            api_key: API key da OpenAI (usa OPENAI_API_KEY do env se None)
            default_llm_model: Modelo LLM padrão
            default_embedding_model: Modelo de embedding padrão
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.default_llm_model = default_llm_model or self.DEFAULT_LLM_MODEL
        self.default_embedding_model = default_embedding_model or self.DEFAULT_EMBEDDING_MODEL

    def get_llm(
        self,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs: Any
    ) -> LLM:
        """
        Retorna instância do OpenAI LLM.

        Args:
            model_name: Nome do modelo GPT
            temperature: Temperatura de geração
            **kwargs: Argumentos adicionais (max_tokens, timeout, etc.)

        Returns:
            Instância configurada do OpenAI LLM
        """
        model = model_name or self.default_llm_model
        return OpenAI(
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
        Retorna instância do OpenAI Embedding.

        Args:
            model_name: Nome do modelo de embedding
            **kwargs: Argumentos adicionais

        Returns:
            Instância configurada do OpenAI Embedding
        """
        model = model_name or self.default_embedding_model
        return OpenAIEmbedding(
            model=model,
            api_key=self.api_key,
            **kwargs
        )

    def get_provider_name(self) -> str:
        """Retorna 'openai'."""
        return "openai"

    def validate_config(self) -> bool:
        """
        Valida se a API key está configurada.

        Returns:
            True se a API key está disponível
        """
        return self.api_key is not None and len(self.api_key) > 0


__all__ = ["OpenAIProvider"]
