"""
Métrica de similaridade semântica usando embeddings.
"""
from typing import Optional
import numpy as np
from debatedores.core.models import AgentPerspective
from debatedores.metrics.base import DebateMetric


class SemanticSimilarity(DebateMetric):
    """
    Calcula similaridade semântica entre perspectivas usando embeddings.

    Requer um modelo de embedding configurado.
    """

    def __init__(self, embed_model: Optional[any] = None):
        """
        Inicializa a métrica de similaridade semântica.

        Args:
            embed_model: Modelo de embedding LlamaIndex (opcional)
        """
        self.embed_model = embed_model

    def calculate(
        self,
        agent1: AgentPerspective,
        agent2: AgentPerspective
    ) -> float:
        """
        Calcula similaridade semântica entre dois agentes.

        Se embed_model não estiver disponível, retorna fallback
        baseado em overlap de palavras.

        Args:
            agent1: Perspectiva do primeiro agente
            agent2: Perspectiva do segundo agente

        Returns:
            Score de similaridade (0.0 a 1.0)
        """
        if self.embed_model is None:
            # Fallback: similaridade baseada em palavras
            return self._word_overlap_similarity(agent1, agent2)

        try:
            # Usar embeddings para similaridade semântica
            return self._embedding_similarity(agent1, agent2)
        except Exception:
            # Fallback em caso de erro
            return self._word_overlap_similarity(agent1, agent2)

    def _embedding_similarity(
        self,
        agent1: AgentPerspective,
        agent2: AgentPerspective
    ) -> float:
        """
        Calcula similaridade usando embeddings.

        Args:
            agent1: Perspectiva do agente 1
            agent2: Perspectiva do agente 2

        Returns:
            Similaridade de cosseno (0.0 a 1.0)
        """
        # Combinar posição e argumentos em um texto
        text1 = f"{agent1.position} " + " ".join(agent1.arguments)
        text2 = f"{agent2.position} " + " ".join(agent2.arguments)

        # Gerar embeddings
        embed1 = self.embed_model.get_text_embedding(text1)
        embed2 = self.embed_model.get_text_embedding(text2)

        # Calcular similaridade de cosseno
        similarity = self._cosine_similarity(embed1, embed2)

        # Normalizar para [0, 1]
        return (similarity + 1.0) / 2.0

    def _cosine_similarity(self, vec1: list, vec2: list) -> float:
        """
        Calcula similaridade de cosseno entre dois vetores.

        Args:
            vec1: Primeiro vetor
            vec2: Segundo vetor

        Returns:
            Similaridade de cosseno (-1.0 a 1.0)
        """
        vec1_np = np.array(vec1)
        vec2_np = np.array(vec2)

        dot_product = np.dot(vec1_np, vec2_np)
        norm1 = np.linalg.norm(vec1_np)
        norm2 = np.linalg.norm(vec2_np)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def _word_overlap_similarity(
        self,
        agent1: AgentPerspective,
        agent2: AgentPerspective
    ) -> float:
        """
        Fallback: similaridade baseada em overlap de palavras.

        Args:
            agent1: Perspectiva do agente 1
            agent2: Perspectiva do agente 2

        Returns:
            Score de similaridade (0.0 a 1.0)
        """
        # Combinar posição e argumentos
        text1 = f"{agent1.position} " + " ".join(agent1.arguments)
        text2 = f"{agent2.position} " + " ".join(agent2.arguments)

        # Tokenização simples
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        # Jaccard similarity
        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union) if union else 0.0

    def get_metric_name(self) -> str:
        """Retorna 'semantic_similarity'."""
        return "semantic_similarity"


__all__ = ["SemanticSimilarity"]
