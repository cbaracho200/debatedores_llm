"""
Testes para modelos Pydantic.
"""
import pytest
from debatedores.core.models import (
    AgentPerspective,
    DebateRound,
    DebateState,
    FinalResult
)


def test_agent_perspective_creation():
    """Testa criação de AgentPerspective."""
    perspective = AgentPerspective(
        agent_name="Test",
        position="Test position",
        arguments=["Arg 1", "Arg 2"],
        confidence=0.75,
        citations=[]
    )

    assert perspective.agent_name == "Test"
    assert perspective.confidence == 0.75
    assert len(perspective.arguments) == 2


def test_agent_perspective_confidence_validation():
    """Testa validação de confiança."""
    # Deve aceitar valores válidos
    AgentPerspective(
        agent_name="Test",
        position="Pos",
        arguments=[],
        confidence=0.0
    )

    AgentPerspective(
        agent_name="Test",
        position="Pos",
        arguments=[],
        confidence=1.0
    )

    # Deve rejeitar valores inválidos
    with pytest.raises(ValueError):
        AgentPerspective(
            agent_name="Test",
            position="Pos",
            arguments=[],
            confidence=1.5
        )


def test_debate_state_defaults():
    """Testa valores padrão do DebateState."""
    state = DebateState()

    assert state.current_round == 0
    assert state.max_rounds == 5
    assert state.agreement_target == 0.8
    assert state.agreement_score == 0.0
    assert len(state.debate_history) == 0
    assert state.final_answer is None


def test_final_result_creation():
    """Testa criação de FinalResult."""
    result = FinalResult(
        success=True,
        final_answer="Test answer",
        total_rounds=3,
        final_agreement_score=0.85,
        key_takeaways=["Point 1", "Point 2"],
        debate_summary="Test summary",
        processing_time=10.5
    )

    assert result.success is True
    assert result.total_rounds == 3
    assert result.processing_time == 10.5
