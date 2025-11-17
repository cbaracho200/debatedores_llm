"""
Processador para documentos PDF.
"""
from typing import List
from pathlib import Path
from llama_index.core import Document, SimpleDirectoryReader
from debatedores.processors.base import DocumentProcessor


class PDFProcessor(DocumentProcessor):
    """
    Processador para arquivos PDF.

    Utiliza LlamaIndex SimpleDirectoryReader para carregar
    e processar documentos PDF.
    """

    SUPPORTED_EXTENSIONS = ['.pdf']

    async def process(self, source: str) -> List[Document]:
        """
        Processa um arquivo PDF.

        Args:
            source: Caminho para o arquivo PDF

        Returns:
            Lista de documentos LlamaIndex

        Raises:
            FileNotFoundError: Se o arquivo PDF não existir
            ValueError: Se não for um arquivo PDF válido
        """
        path = Path(source)

        if not path.exists():
            raise FileNotFoundError(f"Arquivo PDF não encontrado: {source}")

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Extensão inválida: {path.suffix}. "
                f"Esperado: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )

        try:
            # Usar SimpleDirectoryReader para carregar o PDF
            documents = SimpleDirectoryReader(
                input_files=[str(path)]
            ).load_data()

            return documents
        except Exception as e:
            raise ValueError(f"Erro ao processar PDF {source}: {str(e)}")

    def supports(self, source: str) -> bool:
        """
        Verifica se a fonte é um arquivo PDF.

        Args:
            source: Caminho do arquivo

        Returns:
            True se for um arquivo PDF
        """
        path = Path(source)
        return path.suffix.lower() in self.SUPPORTED_EXTENSIONS

    def get_supported_extensions(self) -> List[str]:
        """Retorna ['.pdf']."""
        return self.SUPPORTED_EXTENSIONS

    def validate_source(self, source: str) -> bool:
        """
        Valida se o arquivo PDF existe e é acessível.

        Args:
            source: Caminho do arquivo PDF

        Returns:
            True se o arquivo existe
        """
        path = Path(source)
        return path.exists() and path.is_file()


__all__ = ["PDFProcessor"]
