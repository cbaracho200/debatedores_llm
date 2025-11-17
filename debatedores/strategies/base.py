"""
Interface abstrata para estratégias de debate.
"""
from abc import ABC, abstractmethod
from typing import List
from llama_index.core.query_engine import BaseQueryEngine
from debatedores.core.models import DebateRound
from debatedores.agents.agent import Agent


class DebateStrategy(ABC):
    """
    Classe abstrata para estratégias de debate.

    Implementações concretas definem diferentes abordagens
    para conduzir debates entre agentes.
    """

    @abstractmethod
    async def execute_round(
        self,
        round_number: int,
        agents: List[Agent],
        context: str,
        query_engine: BaseQueryEngine = None
    ) -> DebateRound:
        """
        Executa uma rodada de debate.

        Args:
            round_number: Número da rodada atual
            agents: Lista de agentes participantes
            context: Contexto do debate (pergunta, histórico, etc.)
            query_engine: Engine opcional para consultar documentos

        Returns:
            Resultado da rodada de debate
        """
        pass

    def get_strategy_name(self) -> str:
        """
        Retorna o nome da estratégia.

        Returns:
            Nome da estratégia
        """
        return self.__class__.__name__.replace("Strategy", "").lower()


__all__ = ["DebateStrategy"]
