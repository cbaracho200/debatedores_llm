"""
Testes para critérios de parada.
"""
import pytest
from debatedores.core.models import DebateState
from debatedores.stopping import (
    AgreementThreshold,
    MaxRounds,
    StoppingManager
)


def test_agreement_threshold():
    """Testa critério de agreement threshold."""
    criterion = AgreementThreshold(threshold=0.8)

    # Estado abaixo do threshold
    state1 = DebateState(agreement_score=0.7)
    should_stop, _ = criterion.should_stop(state1)
    assert should_stop is False

    # Estado acima do threshold
    state2 = DebateState(agreement_score=0.9)
    should_stop, reason = criterion.should_stop(state2)
    assert should_stop is True
    assert "0.90" in reason or "0.9" in reason


def test_max_rounds():
    """Testa critério de máximo de rodadas."""
    criterion = MaxRounds(max_rounds=5)

    # Rodada abaixo do máximo
    state1 = DebateState(current_round=3, max_rounds=5)
    should_stop, _ = criterion.should_stop(state1)
    assert should_stop is False

    # Rodada no máximo
    state2 = DebateState(current_round=5, max_rounds=5)
    should_stop, reason = criterion.should_stop(state2)
    assert should_stop is True
    assert "5" in reason


def test_stopping_manager():
    """Testa gerenciador de critérios."""
    criteria = [
        AgreementThreshold(0.8),
        MaxRounds(5)
    ]
    manager = StoppingManager(criteria)

    # Nenhum critério satisfeito
    state1 = DebateState(current_round=2, agreement_score=0.5)
    should_stop, _ = manager.evaluate(state1)
    assert should_stop is False

    # Agreement satisfeito
    state2 = DebateState(current_round=2, agreement_score=0.9)
    should_stop, reason = manager.evaluate(state2)
    assert should_stop is True
    assert "agreement" in reason.lower()

    # Max rounds satisfeito
    state3 = DebateState(current_round=5, agreement_score=0.5)
    should_stop, reason = manager.evaluate(state3)
    assert should_stop is True


def test_stopping_manager_empty_criteria():
    """Testa que lista vazia de critérios levanta erro."""
    with pytest.raises(ValueError):
        StoppingManager(criteria=[])
