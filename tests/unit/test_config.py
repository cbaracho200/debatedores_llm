"""
Testes para sistema de configuração.
"""
import pytest
from pathlib import Path
from debatedores.config import (
    DebateSettings,
    LLMSettings,
    FrameworkConfig
)


def test_debate_settings_defaults():
    """Testa valores padrão de DebateSettings."""
    settings = DebateSettings()

    assert settings.max_rounds == 5
    assert settings.agreement_target == 0.8
    assert settings.chunk_size == 512
    assert settings.temperature == 0.7
    assert settings.verbose is True


def test_debate_settings_validation():
    """Testa validação de DebateSettings."""
    # Valores válidos
    DebateSettings(max_rounds=10, agreement_target=0.9)

    # max_rounds inválido
    with pytest.raises(ValueError):
        DebateSettings(max_rounds=0)

    # agreement_target inválido
    with pytest.raises(ValueError):
        DebateSettings(agreement_target=1.5)


def test_llm_settings():
    """Testa LLMSettings."""
    settings = LLMSettings(
        provider="openai",
        model_name="gpt-4"
    )

    assert settings.provider == "openai"
    assert settings.model_name == "gpt-4"


def test_framework_config_creation():
    """Testa criação de FrameworkConfig."""
    config = FrameworkConfig()

    assert isinstance(config.debate, DebateSettings)
    assert isinstance(config.llm, LLMSettings)
    assert config.llm.provider == "openai"


def test_framework_config_custom():
    """Testa config customizado."""
    config = FrameworkConfig(
        debate=DebateSettings(max_rounds=10),
        llm=LLMSettings(provider="gemini")
    )

    assert config.debate.max_rounds == 10
    assert config.llm.provider == "gemini"
