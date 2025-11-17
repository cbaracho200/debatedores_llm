"""
Modelos de dados Pydantic para o framework Debatedores.

Este módulo define as estruturas de dados principais utilizadas
durante todo o processo de debate multi-agente.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentPerspective(BaseModel):
    """
    Perspectiva de um agente individual no debate.

    Attributes:
        agent_name: Nome identificador do agente
        position: Posição ou tese defendida pelo agente
        arguments: Lista de argumentos principais que suportam a posição
        confidence: Nível de confiança do agente (0.0 a 1.0)
        citations: Citações ou referências extraídas dos documentos
    """
    agent_name: str = Field(description="Nome do agente")
    position: str = Field(description="Posição defendida")
    arguments: List[str] = Field(description="Lista de argumentos principais")
    confidence: float = Field(ge=0.0, le=1.0, description="Confiança na posição")
    citations: List[str] = Field(default_factory=list, description="Citações do documento")


class DebateRound(BaseModel):
    """
    Resultado consolidado de uma rodada de debate.

    Attributes:
        round_number: Número sequencial da rodada
        agent1_response: Resposta do primeiro agente
        agent2_response: Resposta do segundo agente
        synthesis: Síntese das perspectivas de ambos os agentes
        agreement_score: Métrica de convergência entre os agentes (0.0 a 1.0)
        key_insights: Principais insights extraídos da rodada
    """
    round_number: int
    agent1_response: AgentPerspective
    agent2_response: AgentPerspective
    synthesis: str
    agreement_score: float = Field(ge=0.0, le=1.0)
    key_insights: List[str]


class DebateState(BaseModel):
    """
    Estado global do debate.

    Mantém todas as informações necessárias para gerenciar
    o progresso e a evolução do debate ao longo das rodadas.

    Attributes:
        current_round: Rodada atual do debate
        max_rounds: Número máximo de rodadas permitidas
        agreement_target: Meta de convergência para finalização antecipada
        agreement_score: Score de convergência atual
        debate_history: Histórico de todas as rodadas executadas
        final_answer: Resposta final consolidada (após finalização)
        metadata: Metadados adicionais do debate
    """
    current_round: int = Field(default=0)
    max_rounds: int = Field(default=5)
    agreement_target: float = Field(default=0.8)
    agreement_score: float = Field(default=0.0)
    debate_history: List[DebateRound] = Field(default_factory=list)
    final_answer: Optional[str] = Field(default=None)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FinalResult(BaseModel):
    """
    Resultado final do debate após conclusão.

    Attributes:
        success: Indica se o debate foi concluído com sucesso
        final_answer: Resposta final consolidada
        total_rounds: Total de rodadas executadas
        final_agreement_score: Score de convergência final
        key_takeaways: Principais conclusões do debate
        debate_summary: Resumo executivo do debate
        processing_time: Tempo total de processamento em segundos
    """
    success: bool
    final_answer: str
    total_rounds: int
    final_agreement_score: float
    key_takeaways: List[str]
    debate_summary: str
    processing_time: float


__all__ = [
    "AgentPerspective",
    "DebateRound",
    "DebateState",
    "FinalResult",
]
