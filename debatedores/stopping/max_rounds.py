"""
Critério de parada baseado em número máximo de rodadas.
"""
from typing import Tuple
from debatedores.core.models import DebateState
from debatedores.stopping.base import StoppingCriterion


class MaxRounds(StoppingCriterion):
    """
    Para o debate após atingir número máximo de rodadas.
    """

    def __init__(self, max_rounds: int = 5):
        """
        Inicializa o critério.

        Args:
            max_rounds: Número máximo de rodadas

        Raises:
            ValueError: Se max_rounds não for positivo
        """
        if max_rounds <= 0:
            raise ValueError(
                f"max_rounds deve ser positivo, recebido: {max_rounds}"
            )
        self.max_rounds = max_rounds

    def should_stop(self, state: DebateState) -> Tuple[bool, str]:
        """
        Verifica se atingiu o número máximo de rodadas.

        Args:
            state: Estado do debate

        Returns:
            (True, razão) se atingiu máximo, (False, "") caso contrário
        """
        if state.current_round >= self.max_rounds:
            return (
                True,
                f"Número máximo de rodadas ({self.max_rounds}) atingido"
            )
        return (False, "")


__all__ = ["MaxRounds"]
