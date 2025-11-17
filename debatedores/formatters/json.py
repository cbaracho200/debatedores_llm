"""
Formatador JSON para resultados de debate.
"""
import json
from typing import Any, Dict
from debatedores.core.models import FinalResult
from debatedores.formatters.base import OutputFormatter


class JSONFormatter(OutputFormatter):
    """
    Formata resultados em JSON.

    Suporta opções de indentação e ordenação de chaves.
    """

    def __init__(self, indent: int = 2, sort_keys: bool = True):
        """
        Inicializa o formatador JSON.

        Args:
            indent: Número de espaços para indentação
            sort_keys: Se deve ordenar as chaves alfabeticamente
        """
        self.indent = indent
        self.sort_keys = sort_keys

    def format(self, result: FinalResult) -> str:
        """
        Formata resultado como JSON string.

        Args:
            result: Resultado final do debate

        Returns:
            String JSON formatada
        """
        result_dict = result.model_dump()

        return json.dumps(
            result_dict,
            indent=self.indent,
            sort_keys=self.sort_keys,
            ensure_ascii=False
        )

    def format_to_dict(self, result: FinalResult) -> Dict[str, Any]:
        """
        Converte resultado para dicionário Python.

        Args:
            result: Resultado final do debate

        Returns:
            Dicionário Python
        """
        return result.model_dump()


__all__ = ["JSONFormatter"]
