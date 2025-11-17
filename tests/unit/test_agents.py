"""
Testes para sistema de agentes.
"""
import pytest
from debatedores.agents import AgentConfig, ADVOCATUS_CONFIG, DIABOLI_CONFIG


def test_agent_config_creation():
    """Testa criação de AgentConfig."""
    config = AgentConfig(
        name="Test Agent",
        role="tester",
        system_prompt="Test prompt",
        temperature=0.5
    )

    assert config.name == "Test Agent"
    assert config.role == "tester"
    assert config.temperature == 0.5


def test_agent_config_temperature_validation():
    """Testa validação de temperatura."""
    # Valores válidos
    AgentConfig(
        name="Test",
        role="test",
        system_prompt="prompt",
        temperature=0.0
    )

    AgentConfig(
        name="Test",
        role="test",
        system_prompt="prompt",
        temperature=1.0
    )

    # Valores inválidos
    with pytest.raises(ValueError):
        AgentConfig(
            name="Test",
            role="test",
            system_prompt="prompt",
            temperature=1.5
        )


def test_predefined_configs():
    """Testa configurações pré-definidas."""
    assert ADVOCATUS_CONFIG.name == "Agent Advocatus"
    assert ADVOCATUS_CONFIG.role == "defender"
    assert DIABOLI_CONFIG.name == "Agent Diaboli"
    assert DIABOLI_CONFIG.role == "challenger"
