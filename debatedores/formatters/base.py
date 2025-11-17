"""
Interface abstrata para formatadores de saída.
"""
from abc import ABC, abstractmethod
from typing import Any
from debatedores.core.models import FinalResult


class OutputFormatter(ABC):
    """
    Classe abstrata para formatação de resultados.

    Implementações concretas formatam FinalResult em
    diferentes representações (JSON, Markdown, HTML, etc.).
    """

    @abstractmethod
    def format(self, result: FinalResult) -> Any:
        """
        Formata o resultado final do debate.

        Args:
            result: Resultado final a ser formatado

        Returns:
            Resultado formatado (tipo depende da implementação)
        """
        pass

    def get_formatter_name(self) -> str:
        """
        Retorna o nome do formatador.

        Returns:
            Nome do formatador
        """
        return self.__class__.__name__.replace("Formatter", "").lower()


__all__ = ["OutputFormatter"]
