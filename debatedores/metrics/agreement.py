"""
Métrica de acordo/convergência entre agentes.
"""
from debatedores.core.models import AgentPerspective
from debatedores.metrics.base import DebateMetric


class AgreementScore(DebateMetric):
    """
    Calcula score de concordância entre duas perspectivas.

    Considera múltiplos fatores:
    - Similaridade de posições
    - Sobreposição de argumentos
    - Proximidade de níveis de confiança
    """

    def calculate(
        self,
        agent1: AgentPerspective,
        agent2: AgentPerspective
    ) -> float:
        """
        Calcula agreement score entre dois agentes.

        A métrica combina:
        1. Similaridade textual das posições (40%)
        2. Sobreposição de argumentos (40%)
        3. Proximidade de confiança (20%)

        Args:
            agent1: Perspectiva do primeiro agente
            agent2: Perspectiva do segundo agente

        Returns:
            Score de 0.0 (total desacordo) a 1.0 (total acordo)
        """
        # 1. Similaridade de posições (simples comparação de palavras-chave)
        position_score = self._calculate_position_similarity(
            agent1.position,
            agent2.position
        )

        # 2. Sobreposição de argumentos
        argument_score = self._calculate_argument_overlap(
            agent1.arguments,
            agent2.arguments
        )

        # 3. Proximidade de confiança
        confidence_score = 1.0 - abs(agent1.confidence - agent2.confidence)

        # Média ponderada
        final_score = (
            0.4 * position_score +
            0.4 * argument_score +
            0.2 * confidence_score
        )

        return self.normalize(final_score)

    def _calculate_position_similarity(self, pos1: str, pos2: str) -> float:
        """
        Calcula similaridade entre duas posições.

        Usa uma abordagem simples baseada em palavras comuns.
        Para implementação mais robusta, use embeddings.

        Args:
            pos1: Posição do agente 1
            pos2: Posição do agente 2

        Returns:
            Score de similaridade (0.0 a 1.0)
        """
        # Tokenização simples
        words1 = set(pos1.lower().split())
        words2 = set(pos2.lower().split())

        if not words1 or not words2:
            return 0.0

        # Jaccard similarity
        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union) if union else 0.0

    def _calculate_argument_overlap(
        self,
        args1: list[str],
        args2: list[str]
    ) -> float:
        """
        Calcula sobreposição entre listas de argumentos.

        Args:
            args1: Argumentos do agente 1
            args2: Argumentos do agente 2

        Returns:
            Score de sobreposição (0.0 a 1.0)
        """
        if not args1 or not args2:
            return 0.0

        # Contar argumentos similares
        similar_count = 0
        for arg1 in args1:
            for arg2 in args2:
                similarity = self._calculate_position_similarity(arg1, arg2)
                if similarity > 0.5:  # Threshold de similaridade
                    similar_count += 1
                    break

        # Normalizar pelo número total de argumentos
        total_args = max(len(args1), len(args2))
        return similar_count / total_args if total_args > 0 else 0.0

    def get_metric_name(self) -> str:
        """Retorna 'agreement'."""
        return "agreement"


__all__ = ["AgreementScore"]
