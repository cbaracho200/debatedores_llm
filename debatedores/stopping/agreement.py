"""
Critério de parada baseado em threshold de convergência.
"""
from typing import Tuple
from debatedores.core.models import DebateState
from debatedores.stopping.base import StoppingCriterion


class AgreementThreshold(StoppingCriterion):
    """
    Para o debate quando o agreement score atinge o threshold.
    """

    def __init__(self, threshold: float = 0.8):
        """
        Inicializa o critério.

        Args:
            threshold: Valor mínimo de agreement (0.0 a 1.0)

        Raises:
            ValueError: Se threshold não estiver entre 0.0 e 1.0
        """
        if not 0.0 <= threshold <= 1.0:
            raise ValueError(
                f"Threshold deve estar entre 0.0 e 1.0, recebido: {threshold}"
            )
        self.threshold = threshold

    def should_stop(self, state: DebateState) -> Tuple[bool, str]:
        """
        Verifica se o agreement score atingiu o threshold.

        Args:
            state: Estado do debate

        Returns:
            (True, razão) se atingiu threshold, (False, "") caso contrário
        """
        if state.agreement_score >= self.threshold:
            return (
                True,
                f"Agreement score ({state.agreement_score:.2f}) "
                f"atingiu threshold ({self.threshold:.2f})"
            )
        return (False, "")


__all__ = ["AgreementThreshold"]
