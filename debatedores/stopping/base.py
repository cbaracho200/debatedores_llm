"""
Interface abstrata para critérios de parada de debate.
"""
from abc import ABC, abstractmethod
from typing import Tuple
from debatedores.core.models import DebateState


class StoppingCriterion(ABC):
    """
    Classe abstrata para critérios de parada.

    Implementações concretas definem condições específicas
    para encerrar um debate.
    """

    @abstractmethod
    def should_stop(self, state: DebateState) -> Tuple[bool, str]:
        """
        Avalia se o debate deve ser encerrado.

        Args:
            state: Estado atual do debate

        Returns:
            Tupla (should_stop, reason):
            - should_stop: True se deve parar
            - reason: Razão descritiva para a parada
        """
        pass

    def get_criterion_name(self) -> str:
        """
        Retorna o nome identificador do critério.

        Returns:
            Nome do critério
        """
        return self.__class__.__name__


__all__ = ["StoppingCriterion"]
