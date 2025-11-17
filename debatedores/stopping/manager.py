"""
Gerenciador de múltiplos critérios de parada.
"""
from typing import List, Tuple
from debatedores.core.models import DebateState
from debatedores.stopping.base import StoppingCriterion


class StoppingManager:
    """
    Gerencia múltiplos critérios de parada.

    Avalia todos os critérios e para se qualquer um deles for satisfeito.
    """

    def __init__(self, criteria: List[StoppingCriterion]):
        """
        Inicializa o gerenciador.

        Args:
            criteria: Lista de critérios de parada

        Raises:
            ValueError: Se a lista estiver vazia
        """
        if not criteria:
            raise ValueError("Lista de critérios não pode estar vazia")
        self.criteria = criteria

    def evaluate(self, state: DebateState) -> Tuple[bool, str]:
        """
        Avalia todos os critérios.

        Args:
            state: Estado atual do debate

        Returns:
            (should_stop, reason):
            - should_stop: True se qualquer critério for satisfeito
            - reason: Razão da parada (do primeiro critério satisfeito)
        """
        for criterion in self.criteria:
            should_stop, reason = criterion.should_stop(state)
            if should_stop:
                return (True, reason)

        return (False, "")

    def add_criterion(self, criterion: StoppingCriterion) -> None:
        """
        Adiciona um novo critério.

        Args:
            criterion: Critério a ser adicionado
        """
        self.criteria.append(criterion)

    def remove_criterion(self, criterion_name: str) -> bool:
        """
        Remove um critério pelo nome.

        Args:
            criterion_name: Nome do critério a remover

        Returns:
            True se removido com sucesso, False se não encontrado
        """
        for i, criterion in enumerate(self.criteria):
            if criterion.get_criterion_name() == criterion_name:
                self.criteria.pop(i)
                return True
        return False


__all__ = ["StoppingManager"]
