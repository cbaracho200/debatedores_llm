"""
Processador para documentos Markdown.
"""
from typing import List
from pathlib import Path
from llama_index.core import Document, SimpleDirectoryReader
from debatedores.processors.base import DocumentProcessor


class MarkdownProcessor(DocumentProcessor):
    """
    Processador para arquivos Markdown.

    Processa arquivos .md e .markdown utilizando
    LlamaIndex SimpleDirectoryReader.
    """

    SUPPORTED_EXTENSIONS = ['.md', '.markdown']

    async def process(self, source: str) -> List[Document]:
        """
        Processa um arquivo Markdown.

        Args:
            source: Caminho para o arquivo Markdown

        Returns:
            Lista de documentos LlamaIndex

        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValueError: Se não for um arquivo Markdown válido
        """
        path = Path(source)

        if not path.exists():
            raise FileNotFoundError(f"Arquivo Markdown não encontrado: {source}")

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Extensão inválida: {path.suffix}. "
                f"Esperado: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )

        try:
            documents = SimpleDirectoryReader(
                input_files=[str(path)]
            ).load_data()

            return documents
        except Exception as e:
            raise ValueError(f"Erro ao processar Markdown {source}: {str(e)}")

    def supports(self, source: str) -> bool:
        """
        Verifica se a fonte é um arquivo Markdown.

        Args:
            source: Caminho do arquivo

        Returns:
            True se for um arquivo Markdown
        """
        path = Path(source)
        return path.suffix.lower() in self.SUPPORTED_EXTENSIONS

    def get_supported_extensions(self) -> List[str]:
        """Retorna ['.md', '.markdown']."""
        return self.SUPPORTED_EXTENSIONS

    def validate_source(self, source: str) -> bool:
        """
        Valida se o arquivo Markdown existe.

        Args:
            source: Caminho do arquivo

        Returns:
            True se o arquivo existe
        """
        path = Path(source)
        return path.exists() and path.is_file()


__all__ = ["MarkdownProcessor"]
