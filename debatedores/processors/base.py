"""
Interface abstrata para processadores de documentos.

Este módulo define o contrato que todos os processadores
devem implementar para integração com o framework.
"""
from abc import ABC, abstractmethod
from typing import List
from pathlib import Path
from llama_index.core import Document


class DocumentProcessor(ABC):
    """
    Classe abstrata para processamento de documentos.

    Implementações concretas devem ser capazes de carregar
    documentos de diferentes fontes e formatos.
    """

    @abstractmethod
    async def process(self, source: str) -> List[Document]:
        """
        Processa um documento a partir de uma fonte.

        Args:
            source: Caminho do arquivo, URL ou identificador do documento

        Returns:
            Lista de documentos LlamaIndex processados

        Raises:
            FileNotFoundError: Se o documento não for encontrado
            ValueError: Se o formato não for suportado
        """
        pass

    @abstractmethod
    def supports(self, source: str) -> bool:
        """
        Verifica se este processador suporta a fonte fornecida.

        Args:
            source: Caminho do arquivo, URL ou identificador

        Returns:
            True se o processador pode processar esta fonte
        """
        pass

    def get_supported_extensions(self) -> List[str]:
        """
        Retorna as extensões de arquivo suportadas.

        Returns:
            Lista de extensões (ex: ['.pdf', '.txt'])
        """
        return []

    def validate_source(self, source: str) -> bool:
        """
        Valida se a fonte é acessível e válida.

        Args:
            source: Caminho ou URL da fonte

        Returns:
            True se a fonte é válida
        """
        return True


__all__ = ["DocumentProcessor"]
