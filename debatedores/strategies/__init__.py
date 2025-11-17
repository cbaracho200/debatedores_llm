"""
Estratégias de debate para o framework Debatedores.

Este módulo fornece diferentes estratégias para
condução de debates multi-agente.
"""
from debatedores.strategies.base import DebateStrategy
from debatedores.strategies.adversarial import AdversarialDebate

__all__ = [
    "DebateStrategy",
    "AdversarialDebate",
]
