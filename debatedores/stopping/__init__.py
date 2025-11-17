"""
Critérios de parada para debates.

Este módulo fornece critérios extensíveis para determinar
quando um debate deve ser encerrado.
"""
from debatedores.stopping.base import StoppingCriterion
from debatedores.stopping.agreement import AgreementThreshold
from debatedores.stopping.max_rounds import MaxRounds
from debatedores.stopping.manager import StoppingManager

__all__ = [
    "StoppingCriterion",
    "AgreementThreshold",
    "MaxRounds",
    "StoppingManager",
]
