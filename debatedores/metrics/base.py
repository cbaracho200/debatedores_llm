"""
Interface abstrata para métricas de debate.

Este módulo define o contrato que todas as métricas devem
implementar para integração com o framework.
"""
from abc import ABC, abstractmethod
from debatedores.core.models import AgentPerspective


class DebateMetric(ABC):
    """
    Classe abstrata para métricas de debate.

    Implementações concretas devem calcular uma métrica específica
    comparando as perspectivas de diferentes agentes.
    """

    @abstractmethod
    def calculate(
        self,
        agent1: AgentPerspective,
        agent2: AgentPerspective
    ) -> float:
        """
        Calcula a métrica entre duas perspectivas de agentes.

        Args:
            agent1: Perspectiva do primeiro agente
            agent2: Perspectiva do segundo agente

        Returns:
            Valor da métrica (tipicamente entre 0.0 e 1.0)
        """
        pass

    def get_metric_name(self) -> str:
        """
        Retorna o nome identificador da métrica.

        Returns:
            Nome da métrica (ex: "agreement", "semantic_similarity")
        """
        return self.__class__.__name__.lower().replace("metric", "")

    def normalize(self, value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """
        Normaliza um valor para o intervalo [min_val, max_val].

        Args:
            value: Valor a ser normalizado
            min_val: Valor mínimo do intervalo
            max_val: Valor máximo do intervalo

        Returns:
            Valor normalizado
        """
        if value < min_val:
            return min_val
        if value > max_val:
            return max_val
        return value


__all__ = ["DebateMetric"]
