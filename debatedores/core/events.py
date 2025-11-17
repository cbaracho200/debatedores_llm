"""
Eventos customizados para o workflow de debate.

Este módulo define os eventos que controlam o fluxo de execução
do workflow de debate utilizando o sistema de eventos do LlamaIndex.
"""
from typing import List, Literal, Optional
from llama_index.core.workflow import Event


class InitializeDebateEvent(Event):
    """
    Evento emitido para inicializar o debate.

    Attributes:
        question: Pergunta principal do debate
        pdf_paths: Lista de caminhos para documentos PDF
        context: Contexto adicional opcional
    """
    question: str
    pdf_paths: List[str]
    context: Optional[str] = None


class AgentDebateEvent(Event):
    """
    Evento emitido para iniciar uma rodada de debate entre agentes.

    Attributes:
        round_number: Número da rodada a ser executada
        previous_synthesis: Síntese da rodada anterior (para contexto)
    """
    round_number: int
    previous_synthesis: Optional[str] = None


class EvaluateDebateEvent(Event):
    """
    Evento emitido para avaliar o progresso do debate.

    Attributes:
        debate_round: Resultado da rodada que será avaliada
    """
    from debatedores.core.models import DebateRound
    debate_round: DebateRound


class FinalizeDebateEvent(Event):
    """
    Evento emitido para finalizar o debate.

    Attributes:
        reason: Razão da finalização (convergência, limite de rodadas ou erro)
    """
    reason: Literal["agreement", "max_rounds", "error"]


__all__ = [
    "InitializeDebateEvent",
    "AgentDebateEvent",
    "EvaluateDebateEvent",
    "FinalizeDebateEvent",
]
