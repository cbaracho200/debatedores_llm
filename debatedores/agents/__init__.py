"""
Sistema de agentes para o framework Debatedores.

Este módulo fornece classes para configuração e execução
de agentes de debate.
"""
from debatedores.agents.config import (
    AgentConfig,
    ADVOCATUS_CONFIG,
    DIABOLI_CONFIG,
)
from debatedores.agents.agent import Agent

__all__ = [
    "AgentConfig",
    "ADVOCATUS_CONFIG",
    "DIABOLI_CONFIG",
    "Agent",
]
