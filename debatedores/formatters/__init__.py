"""
Formatadores de saída para o framework Debatedores.

Este módulo fornece formatadores para diferentes
representações de resultados de debate.
"""
from debatedores.formatters.base import OutputFormatter
from debatedores.formatters.json import JSONFormatter
from debatedores.formatters.markdown import MarkdownFormatter
from debatedores.formatters.html import HTMLFormatter

__all__ = [
    "OutputFormatter",
    "JSONFormatter",
    "MarkdownFormatter",
    "HTMLFormatter",
]
