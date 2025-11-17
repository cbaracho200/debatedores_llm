"""
Biblioteca de prompts pré-definidos.
"""
from debatedores.prompts.templates import PromptTemplate


class PromptLibrary:
    """
    Biblioteca de templates de prompts comumente usados.
    """

    # Prompt para síntese de rodada
    SYNTHESIS = PromptTemplate("""Analise as duas perspectivas a seguir e crie uma síntese que:
1. Identifique os principais pontos de cada perspectiva
2. Destaque áreas de acordo e desacordo
3. Sugira direções para exploração futura

PERGUNTA ORIGINAL: {question}

PERSPECTIVA 1 ({agent1_name}):
Posição: {agent1_position}
Argumentos:
{agent1_arguments}

PERSPECTIVA 2 ({agent2_name}):
Posição: {agent2_position}
Argumentos:
{agent2_arguments}

Crie uma síntese estruturada e objetiva.""")

    # Prompt para resposta final
    FINAL_ANSWER = PromptTemplate("""Baseado no debate completo entre múltiplas perspectivas,
gere uma resposta final consolidada para a pergunta original.

PERGUNTA: {question}

HISTÓRICO DO DEBATE:
{debate_history}

AGREEMENT SCORE FINAL: {agreement_score:.0%}

Crie uma resposta que:
1. Responda diretamente à pergunta original
2. Integre as melhores evidências e argumentos de ambas as perspectivas
3. Reconheça nuances e limitações
4. Seja clara, objetiva e fundamentada

RESPOSTA FINAL:""")

    # Prompt para extração de insights
    EXTRACT_INSIGHTS = PromptTemplate("""Analise a seguinte síntese de debate e extraia 3-5 insights principais:

SÍNTESE:
{synthesis}

Liste os insights mais importantes no formato:
- Insight 1
- Insight 2
- Insight 3
...""")

    # Prompt para resumo executivo
    EXECUTIVE_SUMMARY = PromptTemplate("""Crie um resumo executivo do debate completo:

PERGUNTA: {question}
RODADAS: {total_rounds}
AGREEMENT SCORE: {agreement_score:.0%}

HISTÓRICO:
{debate_history}

Crie um resumo de 2-3 parágrafos que destaque:
1. O objetivo do debate
2. Principais perspectivas exploradas
3. Convergências alcançadas
4. Conclusão principal

RESUMO:""")

    @classmethod
    def get_template(cls, name: str) -> PromptTemplate:
        """
        Recupera um template pelo nome.

        Args:
            name: Nome do template (SYNTHESIS, FINAL_ANSWER, etc.)

        Returns:
            PromptTemplate correspondente

        Raises:
            AttributeError: Se template não existir
        """
        return getattr(cls, name.upper())


__all__ = ["PromptLibrary"]
