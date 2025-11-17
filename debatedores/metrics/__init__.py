"""
Sistema de métricas para o framework Debatedores.

Este módulo fornece métricas plugáveis para avaliação
de convergência e qualidade de debates.
"""
from debatedores.metrics.base import DebateMetric
from debatedores.metrics.agreement import AgreementScore
from debatedores.metrics.semantic import SemanticSimilarity
from debatedores.metrics.aggregator import MetricsAggregator

__all__ = [
    "DebateMetric",
    "AgreementScore",
    "SemanticSimilarity",
    "MetricsAggregator",
]
