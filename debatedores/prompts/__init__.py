"""
Sistema de prompts para o framework Debatedores.

Este módulo fornece templates e bibliotecas de prompts
reutilizáveis para debates.
"""
from debatedores.prompts.templates import PromptTemplate
from debatedores.prompts.library import PromptLibrary

__all__ = [
    "PromptTemplate",
    "PromptLibrary",
]
