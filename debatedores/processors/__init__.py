"""
Processadores de documentos para o framework Debatedores.

Este módulo fornece processadores para diferentes tipos de documentos
(PDF, Markdown, Web, etc.), permitindo fácil extensão.
"""
from debatedores.processors.base import DocumentProcessor
from debatedores.processors.pdf import PDFProcessor
from debatedores.processors.markdown import MarkdownProcessor
from debatedores.processors.web import WebProcessor

__all__ = [
    "DocumentProcessor",
    "PDFProcessor",
    "MarkdownProcessor",
    "WebProcessor",
]
