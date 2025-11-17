"""
Agregador de múltiplas métricas de debate.
"""
from typing import Dict, List
from debatedores.core.models import AgentPerspective
from debatedores.metrics.base import DebateMetric


class MetricsAggregator:
    """
    Agrega múltiplas métricas de debate em um score consolidado.

    Permite combinar diferentes métricas com pesos customizados.
    """

    def __init__(
        self,
        metrics: List[DebateMetric],
        weights: Optional[List[float]] = None
    ):
        """
        Inicializa o agregador de métricas.

        Args:
            metrics: Lista de métricas a serem agregadas
            weights: Pesos opcionais para cada métrica (soma deve ser 1.0)
                    Se None, usa pesos iguais

        Raises:
            ValueError: Se o número de pesos não corresponder ao número de métricas
        """
        if not metrics:
            raise ValueError("Lista de métricas não pode estar vazia")

        self.metrics = metrics

        # Configurar pesos
        if weights is None:
            # Pesos iguais
            self.weights = [1.0 / len(metrics)] * len(metrics)
        else:
            if len(weights) != len(metrics):
                raise ValueError(
                    f"Número de pesos ({len(weights)}) deve corresponder "
                    f"ao número de métricas ({len(metrics)})"
                )
            # Normalizar pesos para somar 1.0
            total = sum(weights)
            self.weights = [w / total for w in weights]

    def aggregate(
        self,
        agent1: AgentPerspective,
        agent2: AgentPerspective
    ) -> Dict[str, float]:
        """
        Calcula e agrega todas as métricas.

        Args:
            agent1: Perspectiva do primeiro agente
            agent2: Perspectiva do segundo agente

        Returns:
            Dicionário com scores individuais e agregado:
            {
                'agreement': 0.75,
                'semantic_similarity': 0.82,
                'aggregated': 0.785
            }
        """
        results = {}

        # Calcular cada métrica
        scores = []
        for metric in self.metrics:
            score = metric.calculate(agent1, agent2)
            metric_name = metric.get_metric_name()
            results[metric_name] = score
            scores.append(score)

        # Calcular score agregado (média ponderada)
        aggregated_score = sum(
            score * weight
            for score, weight in zip(scores, self.weights)
        )
        results['aggregated'] = aggregated_score

        return results

    def get_aggregated_score(
        self,
        agent1: AgentPerspective,
        agent2: AgentPerspective
    ) -> float:
        """
        Retorna apenas o score agregado.

        Args:
            agent1: Perspectiva do primeiro agente
            agent2: Perspectiva do segundo agente

        Returns:
            Score agregado (0.0 a 1.0)
        """
        return self.aggregate(agent1, agent2)['aggregated']

    def add_metric(self, metric: DebateMetric, weight: float = 1.0) -> None:
        """
        Adiciona uma nova métrica ao agregador.

        Args:
            metric: Métrica a ser adicionada
            weight: Peso da métrica
        """
        self.metrics.append(metric)
        self.weights.append(weight)

        # Renormalizar pesos
        total = sum(self.weights)
        self.weights = [w / total for w in self.weights]


from typing import Optional

__all__ = ["MetricsAggregator"]
