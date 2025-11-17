"""
Testes para sistema de métricas.
"""
import pytest
from debatedores.core.models import AgentPerspective
from debatedores.metrics import AgreementScore, MetricsAggregator


def test_agreement_score_identical_positions():
    """Testa score de concordância para posições idênticas."""
    metric = AgreementScore()

    agent1 = AgentPerspective(
        agent_name="Agent 1",
        position="Machine learning é importante",
        arguments=["Argumento A", "Argumento B"],
        confidence=0.8,
        citations=[]
    )

    agent2 = AgentPerspective(
        agent_name="Agent 2",
        position="Machine learning é importante",
        arguments=["Argumento A", "Argumento B"],
        confidence=0.8,
        citations=[]
    )

    score = metric.calculate(agent1, agent2)

    # Score deve ser alto (próximo de 1.0)
    assert score > 0.7


def test_agreement_score_opposite_positions():
    """Testa score para posições opostas."""
    metric = AgreementScore()

    agent1 = AgentPerspective(
        agent_name="Agent 1",
        position="IA deve ser regulada",
        arguments=["Segurança", "Ética"],
        confidence=0.9,
        citations=[]
    )

    agent2 = AgentPerspective(
        agent_name="Agent 2",
        position="Completamente diferente xyz",
        arguments=["Outro A", "Outro B"],
        confidence=0.5,
        citations=[]
    )

    score = metric.calculate(agent1, agent2)

    # Score deve ser baixo
    assert score < 0.5


def test_metrics_aggregator():
    """Testa agregador de métricas."""
    metric1 = AgreementScore()
    aggregator = MetricsAggregator(metrics=[metric1])

    agent1 = AgentPerspective(
        agent_name="A1",
        position="test",
        arguments=[],
        confidence=0.7,
        citations=[]
    )

    agent2 = AgentPerspective(
        agent_name="A2",
        position="test",
        arguments=[],
        confidence=0.7,
        citations=[]
    )

    results = aggregator.aggregate(agent1, agent2)

    assert 'agreement' in results
    assert 'aggregated' in results
    assert 0.0 <= results['aggregated'] <= 1.0


def test_metrics_aggregator_empty_list():
    """Testa que lista vazia de métricas levanta erro."""
    with pytest.raises(ValueError):
        MetricsAggregator(metrics=[])
