"""
Módulo core do framework Debatedores.

Este módulo contém as classes e estruturas fundamentais
para execução de debates multi-agente.
"""
from debatedores.core.models import (
    AgentPerspective,
    DebateRound,
    DebateState,
    FinalResult,
)
from debatedores.core.events import (
    InitializeDebateEvent,
    AgentDebateEvent,
    EvaluateDebateEvent,
    FinalizeDebateEvent,
)

__all__ = [
    # Models
    "AgentPerspective",
    "DebateRound",
    "DebateState",
    "FinalResult",
    # Events
    "InitializeDebateEvent",
    "AgentDebateEvent",
    "EvaluateDebateEvent",
    "FinalizeDebateEvent",
]
