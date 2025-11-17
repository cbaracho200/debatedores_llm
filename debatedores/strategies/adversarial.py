"""
Estratégia de debate adversarial (posições opostas).
"""
import asyncio
from typing import List, Optional
from llama_index.core.query_engine import BaseQueryEngine
from debatedores.core.models import DebateRound
from debatedores.agents.agent import Agent
from debatedores.strategies.base import DebateStrategy


class AdversarialDebate(DebateStrategy):
    """
    Estratégia adversarial: agentes defendem posições opostas.

    Executa agentes em paralelo e sintetiza as perspectivas.
    """

    async def execute_round(
        self,
        round_number: int,
        agents: List[Agent],
        context: str,
        query_engine: Optional[BaseQueryEngine] = None
    ) -> DebateRound:
        """
        Executa rodada adversarial.

        Args:
            round_number: Número da rodada
            agents: Lista de agentes (requer exatamente 2)
            context: Contexto do debate
            query_engine: Engine opcional para documentos

        Returns:
            Resultado da rodada

        Raises:
            ValueError: Se não houver exatamente 2 agentes
        """
        if len(agents) != 2:
            raise ValueError(
                f"AdversarialDebate requer exatamente 2 agentes, "
                f"recebido: {len(agents)}"
            )

        # Executar agentes em paralelo
        responses = await asyncio.gather(
            agents[0].respond(context, query_engine),
            agents[1].respond(context, query_engine)
        )

        # Sintetizar respostas
        synthesis = await self._synthesize(
            responses[0],
            responses[1],
            context
        )

        # Calcular agreement score
        from debatedores.metrics import AgreementScore
        metric = AgreementScore()
        agreement_score = metric.calculate(responses[0], responses[1])

        # Extrair insights
        key_insights = self._extract_insights(synthesis)

        return DebateRound(
            round_number=round_number,
            agent1_response=responses[0],
            agent2_response=responses[1],
            synthesis=synthesis,
            agreement_score=agreement_score,
            key_insights=key_insights
        )

    async def _synthesize(self, resp1, resp2, context: str) -> str:
        """
        Sintetiza duas perspectivas.

        Implementação simplificada - idealmente usar LLM para síntese.

        Args:
            resp1: Resposta do agente 1
            resp2: Resposta do agente 2
            context: Contexto do debate

        Returns:
            Síntese textual
        """
        # Implementação simplificada
        return f"""Síntese da Rodada:

{resp1.agent_name} defende: {resp1.position}
Confiança: {resp1.confidence:.0%}

{resp2.agent_name} argumenta: {resp2.position}
Confiança: {resp2.confidence:.0%}

Pontos de convergência e divergência necessitam ser explorados nas próximas rodadas."""

    def _extract_insights(self, synthesis: str) -> List[str]:
        """
        Extrai insights da síntese.

        Implementação simplificada.

        Args:
            synthesis: Texto da síntese

        Returns:
            Lista de insights
        """
        # Implementação básica
        return [
            "Perspectivas identificadas e documentadas",
            "Argumentos principais mapeados",
            "Convergências e divergências registradas"
        ]

    def get_strategy_name(self) -> str:
        """Retorna 'adversarial'."""
        return "adversarial"


__all__ = ["AdversarialDebate"]
