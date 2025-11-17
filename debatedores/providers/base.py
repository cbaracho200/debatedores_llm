"""
Interface abstrata para providers de LLM e embeddings.

Este módulo define o contrato que todos os providers devem
implementar para integração com o framework.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from llama_index.core.llms import LLM
from llama_index.core.embeddings import BaseEmbedding


class LLMProvider(ABC):
    """
    Classe abstrata para providers de LLM.

    Implementações concretas devem fornecer métodos para
    obter instâncias de LLM e modelos de embedding.
    """

    @abstractmethod
    def get_llm(
        self,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs: Any
    ) -> LLM:
        """
        Retorna uma instância configurada do LLM.

        Args:
            model_name: Nome do modelo (usa padrão se None)
            temperature: Temperatura para geração (0.0 a 1.0)
            **kwargs: Argumentos adicionais específicos do provider

        Returns:
            Instância configurada do LLM
        """
        pass

    @abstractmethod
    def get_embeddings(
        self,
        model_name: Optional[str] = None,
        **kwargs: Any
    ) -> BaseEmbedding:
        """
        Retorna uma instância configurada do modelo de embeddings.

        Args:
            model_name: Nome do modelo (usa padrão se None)
            **kwargs: Argumentos adicionais específicos do provider

        Returns:
            Instância configurada do modelo de embeddings
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Retorna o nome identificador do provider.

        Returns:
            Nome do provider (ex: "openai", "gemini", "anthropic")
        """
        pass

    def validate_config(self) -> bool:
        """
        Valida a configuração do provider.

        Returns:
            True se a configuração é válida, False caso contrário
        """
        return True


__all__ = ["LLMProvider"]
