"""
Sistema de templates de prompts.
"""
from typing import Dict, Any


class PromptTemplate:
    """
    Template de prompt com substituição de variáveis.

    Usa sintaxe simples {variable} para substituição.
    """

    def __init__(self, template: str):
        """
        Inicializa o template.

        Args:
            template: String template com placeholders {variable}
        """
        self.template = template

    def render(self, **kwargs: Any) -> str:
        """
        Renderiza o template com variáveis fornecidas.

        Args:
            **kwargs: Variáveis para substituição

        Returns:
            Template renderizado

        Raises:
            KeyError: Se variável obrigatória não for fornecida
        """
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            raise KeyError(
                f"Variável obrigatória não fornecida: {e}"
            )

    def get_variables(self) -> list[str]:
        """
        Extrai nomes de variáveis do template.

        Returns:
            Lista de nomes de variáveis
        """
        import re
        return re.findall(r'\{(\w+)\}', self.template)


__all__ = ["PromptTemplate"]
