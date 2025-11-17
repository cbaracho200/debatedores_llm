"""
Formatador Markdown para resultados de debate.
"""
from debatedores.core.models import FinalResult
from debatedores.formatters.base import OutputFormatter


class MarkdownFormatter(OutputFormatter):
    """
    Formata resultados em Markdown.

    Gera um documento markdown estruturado e legível.
    """

    def format(self, result: FinalResult) -> str:
        """
        Formata resultado como Markdown.

        Args:
            result: Resultado final do debate

        Returns:
            String Markdown formatada
        """
        sections = []

        # Cabeçalho
        sections.append("# 🎯 Resultado do Debate\n")

        # Status
        status_emoji = "✅" if result.success else "❌"
        sections.append(f"**Status**: {status_emoji} {'Sucesso' if result.success else 'Falha'}\n")

        # Métricas principais
        sections.append("## 📊 Métricas")
        sections.append(f"- **Rodadas executadas**: {result.total_rounds}")
        sections.append(f"- **Agreement score final**: {result.final_agreement_score:.2%}")
        sections.append(f"- **Tempo de processamento**: {result.processing_time:.2f}s\n")

        # Resposta final
        sections.append("## 💡 Resposta Final")
        sections.append(f"{result.final_answer}\n")

        # Key takeaways
        if result.key_takeaways:
            sections.append("## 🔑 Principais Conclusões")
            for i, takeaway in enumerate(result.key_takeaways, 1):
                sections.append(f"{i}. {takeaway}")
            sections.append("")

        # Resumo do debate
        sections.append("## 📝 Resumo do Debate")
        sections.append(f"{result.debate_summary}\n")

        return "\n".join(sections)


__all__ = ["MarkdownFormatter"]
