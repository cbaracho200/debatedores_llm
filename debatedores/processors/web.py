"""
Processador para páginas web.
"""
from typing import List
from urllib.parse import urlparse
from llama_index.core import Document
from debatedores.processors.base import DocumentProcessor


class WebProcessor(DocumentProcessor):
    """
    Processador para páginas web via URL.

    Utiliza LlamaIndex readers para carregar conteúdo de URLs.
    Nota: Requer instalação de llama-index-readers-web.
    """

    SUPPORTED_SCHEMES = ['http', 'https']

    async def process(self, source: str) -> List[Document]:
        """
        Processa uma página web.

        Args:
            source: URL da página web

        Returns:
            Lista de documentos LlamaIndex

        Raises:
            ValueError: Se a URL não for válida
            ImportError: Se llama-index-readers-web não estiver instalado
        """
        if not self.supports(source):
            raise ValueError(f"URL inválida ou esquema não suportado: {source}")

        try:
            from llama_index.readers.web import SimpleWebPageReader
        except ImportError:
            raise ImportError(
                "llama-index-readers-web não está instalado. "
                "Execute: pip install llama-index-readers-web"
            )

        try:
            reader = SimpleWebPageReader()
            documents = reader.load_data([source])
            return documents
        except Exception as e:
            raise ValueError(f"Erro ao processar URL {source}: {str(e)}")

    def supports(self, source: str) -> bool:
        """
        Verifica se a fonte é uma URL válida.

        Args:
            source: URL a ser verificada

        Returns:
            True se for uma URL HTTP/HTTPS válida
        """
        try:
            parsed = urlparse(source)
            return parsed.scheme in self.SUPPORTED_SCHEMES
        except Exception:
            return False

    def get_supported_extensions(self) -> List[str]:
        """
        Retorna lista vazia (URLs não têm extensões fixas).

        Returns:
            Lista vazia
        """
        return []

    def validate_source(self, source: str) -> bool:
        """
        Valida se a URL está bem formada.

        Args:
            source: URL a ser validada

        Returns:
            True se a URL é válida
        """
        try:
            parsed = urlparse(source)
            return all([parsed.scheme, parsed.netloc])
        except Exception:
            return False


__all__ = ["WebProcessor"]
