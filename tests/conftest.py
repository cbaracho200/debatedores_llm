"""
Configuração de fixtures para testes.
"""
import pytest
from debatedores.core.models import AgentPerspective, DebateState
from debatedores.agents import AgentConfig


@pytest.fixture
def sample_agent_perspective():
    """Perspectiva de agente de exemplo."""
    return AgentPerspective(
        agent_name="Test Agent",
        position="Posição de teste",
        arguments=["Argumento 1", "Argumento 2", "Argumento 3"],
        confidence=0.8,
        citations=["Citação 1", "Citação 2"]
    )


@pytest.fixture
def sample_debate_state():
    """Estado de debate de exemplo."""
    return DebateState(
        current_round=1,
        max_rounds=5,
        agreement_target=0.8,
        agreement_score=0.5,
        debate_history=[],
        metadata={"test": True}
    )


@pytest.fixture
def sample_agent_config():
    """Configuração de agente de exemplo."""
    return AgentConfig(
        name="Test Agent",
        role="tester",
        system_prompt="Test prompt",
        temperature=0.7
    )
